
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import unicodedata
import plotly.graph_objects as go

# --------------------------------------------------
# Configuración
# --------------------------------------------------

st.set_page_config(
    page_title="Argentina Oil & Gas Analytics",
    page_icon="🛢️",
    layout="wide",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOLD_PATH = PROJECT_ROOT / "data" / "gold" / "production_monthly"

st.title("🛢️ Argentina Oil & Gas Analytics")
st.caption(
    "Explorador de producción de petróleo y gas | "
    "Fuente: capa Gold del pipeline de Data Engineering"
)


# --------------------------------------------------
# Lectura de Gold
# --------------------------------------------------

@st.cache_data
def load_gold(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    required_columns = [
        "anio",
        "mes",
        "provincia",
        "cuenca",
        "produccion_petroleo",
        "produccion_gas",
        "produccion_agua",
        "cantidad_pozos",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(
            f"Faltan columnas requeridas: {missing}. "
            f"Columnas disponibles: {df.columns.tolist()}"
        )

    numeric_columns = [
        "anio",
        "mes",
        "produccion_petroleo",
        "produccion_gas",
        "produccion_agua",
        "cantidad_pozos",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["provincia"] = df["provincia"].fillna("Sin provincia").astype(str)
    df["cuenca"] = df["cuenca"].fillna("Sin cuenca").astype(str)

    return df


if not GOLD_PATH.exists():
    st.error(f"No se encontró la capa Gold: {GOLD_PATH}")
    st.info("Ejecutá primero el pipeline para generar los datos Gold.")
    st.stop()

try:
    gold = load_gold(str(GOLD_PATH))
except Exception as exc:
    st.error(f"No se pudieron cargar los datos Gold: {exc}")
    st.stop()

if gold.empty:
    st.warning("La capa Gold no contiene registros.")
    st.stop()


# --------------------------------------------------
# Filtros
# --------------------------------------------------

st.sidebar.header("Filtros")

years = sorted(gold["anio"].dropna().astype(int).unique().tolist())

selected_years = st.sidebar.multiselect(
    "Año",
    options=years,
    default=years,
)

year_data = gold[gold["anio"].isin(selected_years)]

months = sorted(year_data["mes"].dropna().astype(int).unique().tolist())

selected_months = st.sidebar.multiselect(
    "Mes",
    options=months,
    default=months,
)

province_options = sorted(year_data["provincia"].unique().tolist())

selected_provinces = st.sidebar.multiselect(
    "Provincia",
    options=province_options,
    default=province_options,
)

basin_data = year_data[
    year_data["provincia"].isin(selected_provinces)
]

basin_options = sorted(basin_data["cuenca"].unique().tolist())

selected_basins = st.sidebar.multiselect(
    "Cuenca",
    options=basin_options,
    default=basin_options,
)

filtered = gold[
    gold["anio"].isin(selected_years)
    & gold["mes"].isin(selected_months)
    & gold["provincia"].isin(selected_provinces)
    & gold["cuenca"].isin(selected_basins)
].copy()

if filtered.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()


# --------------------------------------------------
# Indicadores principales
# --------------------------------------------------

total_oil = filtered["produccion_petroleo"].sum()
total_gas = filtered["produccion_gas"].sum()
total_water = filtered["produccion_agua"].sum()

# Cantidad de pozos correspondiente al último mes seleccionado.
# No sumamos los conteos de distintos meses, porque un pozo
# puede aparecer en varios períodos.
latest_year = filtered["anio"].max()
latest_month = filtered.loc[
    filtered["anio"] == latest_year, "mes"
].max()

latest_data = filtered[
    (filtered["anio"] == latest_year)
    & (filtered["mes"] == latest_month)
]

reported_wells = latest_data["cantidad_pozos"].sum()


st.subheader("Resumen de producción")

col1, col2, col3, col4 = st.columns(4)

# Convertir a millones según la unidad original de cada indicador.
oil_millions = total_oil / 1_000_000
gas_millions = total_gas / 1_000
water_millions = total_water / 1_000_000

col1.metric(
    "Petróleo",
    f"{oil_millions:,.2f} M m³",
    help="Producción acumulada en millones de metros cúbicos.",
)

col2.metric(
    "Gas",
    f"{gas_millions:,.2f} M m³",
    help=(
        "Producción acumulada en millones de metros cúbicos. "
        "El dato original está expresado en miles de m³."
    ),
)

col3.metric(
    "Agua",
    f"{water_millions:,.2f} M m³",
    help="Producción acumulada en millones de metros cúbicos.",
)

col4.metric(
    "Pozos reportados",
    f"{reported_wells:,.0f}",
    help=(
        f"Suma de pozos reportados para "
        f"{int(latest_month):02d}/{int(latest_year)} "
        "en los grupos seleccionados. "
        "No necesariamente representa pozos únicos "
        "en todo el período seleccionado."
    ),
)

st.caption(
    "Unidades: petróleo y agua en m³; gas en miles de m³ "
    "en la fuente original. Las tarjetas de producción se "
    "muestran en millones de m³. Los pozos corresponden "
    "al período indicado en su descripción."
)



# --------------------------------------------------
# Mapa interactivo de Argentina
# --------------------------------------------------

st.divider()
st.subheader("Mapa de producción por provincia")

st.caption(
    "Las provincias con producción aparecen en colores vibrantes. "
    "Las provincias sin datos se muestran en gris."
)


def normalize_name(value):
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(
        char
        for char in value
        if not unicodedata.combining(char)
    )
    return value.strip().casefold()



@st.cache_data(ttl=86400)
def load_provinces_geojson():
    url = "https://apis.datos.gob.ar/georef/api/v2.0/provincias.geojson"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    geojson = response.json()

    for feature in geojson["features"]:
        feature["properties"]["map_key"] = normalize_name(
            feature["properties"]["nombre"]
        )

        geometry = feature.get("geometry")

        # Excluir polígonos antárticos que alejan demasiado el mapa.
        if geometry and geometry["type"] == "MultiPolygon":
            filtered_polygons = []

            for polygon in geometry["coordinates"]:
                if not polygon or not polygon[0]:
                    continue

                outer_ring = polygon[0]
                latitudes = [point[1] for point in outer_ring]

                # Conservar las áreas al norte de la Antártida.
                if max(latitudes) > -60:
                    filtered_polygons.append(polygon)

            geometry["coordinates"] = filtered_polygons

    return geojson



map_metric = st.selectbox(
    "Indicador del mapa",
    options=["Petróleo", "Gas", "Agua"],
)

map_columns = {
    "Petróleo": "produccion_petroleo",
    "Gas": "produccion_gas",
    "Agua": "produccion_agua",
}

map_labels = {
    "Petróleo": "Producción de petróleo",
    "Gas": "Producción de gas",
    "Agua": "Producción de agua",
}

try:
    # Cargar los límites geográficos de todas las provincias.
    geojson = load_provinces_geojson()

    # Calcular producción según los filtros seleccionados.
    # Estado Nacional no es una provincia geográfica.
    province_totals = (
        filtered[
            filtered["provincia"].str.casefold() != "estado nacional"
        ]
        .groupby("provincia", as_index=False)
        .agg(valor=(map_columns[map_metric], "sum"))
    )

    province_totals["map_key"] = province_totals[
        "provincia"
    ].map(normalize_name)

    # Obtener todas las provincias del GeoJSON.
    all_provinces = pd.DataFrame({
        "map_key": [
            feature["properties"]["map_key"]
            for feature in geojson["features"]
        ]
    })

    fig_map = go.Figure()

    # --------------------------------------------------
    # CAPA 1: todas las provincias en gris.
    # --------------------------------------------------
    fig_map.add_trace(
        go.Choropleth(
            geojson=geojson,
            locations=all_provinces["map_key"],
            featureidkey="properties.map_key",
            z=[1] * len(all_provinces),
            colorscale=[
                [0, "#D1D5DB"],
                [1, "#D1D5DB"],
            ],
            showscale=False,
            marker_line_color="#FFFFFF",
            marker_line_width=1.2,
            hovertemplate=(
                "Provincia: %{location}"
                "<extra></extra>"
            ),
            name="Provincias",
        )
    )

    # --------------------------------------------------
    # CAPA 2: provincias con producción.
    # --------------------------------------------------
    if not province_totals.empty:
        fig_map.add_trace(
            go.Choropleth(
                geojson=geojson,
                locations=province_totals["map_key"],
                z=province_totals["valor"],
                featureidkey="properties.map_key",
                colorscale=[
                    [0, "#22D3EE"],
                    [0.5, "#0891B2"],
                    [1, "#7C3AED"],
                ],
                colorbar={
                    "title": map_labels[map_metric],
                    "thickness": 18,
                    "len": 0.75,
                },
                marker_line_color="#FFFFFF",
                marker_line_width=1.2,
                text=province_totals["provincia"],
                hovertemplate=(
                    "%{text}<br>"
                    + map_labels[map_metric]
                    + ": %{z:,.2f}"
                    + "<extra></extra>"
                ),
                name="Producción",
            )
        )

    # --------------------------------------------------
    # ENCUADRE Y TAMAÑO DEL MAPA.
    # --------------------------------------------------
    fig_map.update_geos(
    visible=False,
    projection_type="mercator",
    center={
        "lat": -38,
        "lon": -64,
    },
    projection_scale= 7.5,
    bgcolor="white",
    showland=False,)



    fig_map.update_layout(
        title={
            "text": f"{map_labels[map_metric]} por provincia",
            "x": 0.5,
            "xanchor": "center",
        },
        height=1000,
        autosize=True,
        margin={
            "r": 20,
            "t": 70,
            "l": 20,
            "b": 20,
        },
        showlegend=False,
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True,
        config={
            "responsive": True,
            "scrollZoom": True,
        },
    )

except Exception as exc:
    st.error("No se pudo construir el mapa geográfico.")
    st.exception(exc)



# --------------------------------------------------
# Evolución mensual
# --------------------------------------------------

st.divider()
st.subheader("Evolución mensual de la producción")

monthly = (
    filtered.groupby(["anio", "mes"], as_index=False)
    .agg(
        petroleo=("produccion_petroleo", "sum"),
        gas=("produccion_gas", "sum"),
        agua=("produccion_agua", "sum"),
    )
    .sort_values(["anio", "mes"])
)

monthly["periodo"] = (
    monthly["anio"].astype(int).astype(str)
    + "-"
    + monthly["mes"].astype(int).astype(str).str.zfill(2)
)

metric = st.selectbox(
    "Métrica para visualizar",
    options=["Petróleo", "Gas", "Agua"],
)

metric_columns = {
    "Petróleo": "petroleo",
    "Gas": "gas",
    "Agua": "agua",
}

fig_monthly = px.line(
    monthly,
    x="periodo",
    y=metric_columns[metric],
    markers=True,
    title=f"{metric}: evolución mensual",
    labels={
        "periodo": "Período",
        metric_columns[metric]: "Producción",
    },
)

fig_monthly.update_layout(hovermode="x unified")
st.plotly_chart(fig_monthly, use_container_width=True)


# --------------------------------------------------
# Comparación por provincia y cuenca
# --------------------------------------------------

left, right = st.columns(2)

with left:
    st.subheader("Producción por provincia")

    province_chart = (
        filtered.groupby("provincia", as_index=False)
        .agg(
            petroleo=("produccion_petroleo", "sum"),
            gas=("produccion_gas", "sum"),
        )
        .sort_values("petroleo", ascending=False)
    )

    fig_province = px.bar(
        province_chart,
        x="provincia",
        y="petroleo",
        title="Producción de petróleo",
        labels={
            "provincia": "Provincia",
            "petroleo": "Producción",
        },
    )

    fig_province.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig_province, use_container_width=True)

with right:
    st.subheader("Producción por cuenca")

    basin_chart = (
        filtered.groupby("cuenca", as_index=False)
        .agg(
            petroleo=("produccion_petroleo", "sum"),
            gas=("produccion_gas", "sum"),
        )
        .sort_values("gas", ascending=False)
    )

    fig_basin = px.bar(
        basin_chart,
        x="cuenca",
        y="gas",
        title="Producción de gas",
        labels={
            "cuenca": "Cuenca",
            "gas": "Producción",
        },
    )

    fig_basin.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig_basin, use_container_width=True)


# --------------------------------------------------
# Tabla de datos
# --------------------------------------------------

st.divider()
st.subheader("Datos de la capa Gold")

st.caption(
    "Esta tabla muestra las agregaciones originales de Gold "
    "que cumplen con los filtros seleccionados."
)

st.dataframe(
    filtered.sort_values(["anio", "mes", "provincia", "cuenca"]),
    use_container_width=True,
    hide_index=True,
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Descargar datos filtrados (CSV)",
    data=csv,
    file_name="argentina_oil_gas_gold.csv",
    mime="text/csv",
)

st.caption(
    "Proyecto de Data Engineering con datos públicos de producción "
    "de petróleo y gas de Argentina."
)
