
import csv
import os
import tempfile
from pathlib import Path

import requests


API_URL = "https://datos.gob.ar/api/3/action/package_show"
DATASET_ID = "produccion-de-petroleo-y-gas-por-pozo"

RESOURCE_NAME = "Producción de Pozos de Gas y Petróleo – 2026"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "production_2026.csv"


def get_dataset(dataset_id: str) -> dict:
    """Obtiene los metadatos del dataset desde CKAN."""
    response = requests.get(
        API_URL,
        params={"id": dataset_id},
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise RuntimeError(f"CKAN no pudo consultar el dataset: {dataset_id}")

    return data["result"]


def get_resources(dataset: dict) -> list:
    """Devuelve los recursos publicados por el dataset."""
    return dataset.get("resources", [])


def find_resource_by_name(resources: list, name: str) -> dict:
    """Selecciona el recurso por su nombre exacto."""
    matches = [
        resource
        for resource in resources
        if resource.get("name", "").strip() == name
    ]

    if len(matches) != 1:
        available = [
            resource.get("name", "(sin nombre)")
            for resource in resources
            if "2026" in resource.get("name", "")
        ]
        raise ValueError(
            f"Se esperaba exactamente un recurso llamado {name!r}. "
            f"Recursos de 2026 disponibles: {available}"
        )

    resource = matches[0]

    if resource.get("format", "").upper() != "CSV":
        raise ValueError(
            f"El recurso seleccionado no es CSV: {resource.get('format')}"
        )

    if not resource.get("url"):
        raise ValueError("El recurso seleccionado no tiene URL de descarga.")

    return resource


def download_resource(url: str, output_path: Path) -> int:
    """
    Descarga y valida el CSV antes de reemplazar el archivo de destino.
    Devuelve el número de bytes descargados.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with requests.get(
            url,
            timeout=(15, 180),
            stream=True,
            headers={"User-Agent": "ArgentinaOilGasDataPlatform/1.0"},
        ) as response:
            response.raise_for_status()

            total_bytes = 0
            header_sample = bytearray()

            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=output_path.parent,
                prefix="production_2026_",
                suffix=".tmp",
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)

                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue

                    if len(header_sample) < 65536:
                        remaining = 65536 - len(header_sample)
                        header_sample.extend(chunk[:remaining])

                    temp_file.write(chunk)
                    total_bytes += len(chunk)

        if total_bytes == 0:
            raise ValueError("CKAN devolvió un archivo vacío.")

        sample_text = header_sample.decode("utf-8-sig", errors="replace")

        if sample_text.lstrip().lower().startswith(
            ("<!doctype html", "<html")
        ):
            raise ValueError(
                "La URL devolvió HTML en lugar de un archivo CSV."
            )

        first_line = sample_text.splitlines()[0] if sample_text.splitlines() else ""
        try:
            dialect = csv.Sniffer().sniff(first_line, delimiters=",;\t|")
            delimiter = dialect.delimiter
        except csv.Error:
            delimiter = ","

        headers = next(csv.reader([first_line], delimiter=delimiter), [])
        normalized_headers = {
            header.strip().lstrip("\ufeff").lower()
            for header in headers
        }

        required_columns = {"idpozo", "anio", "mes"}
        missing_columns = required_columns - normalized_headers

        if missing_columns:
            raise ValueError(
                "El archivo descargado no tiene las columnas esperadas. "
                f"Faltan: {sorted(missing_columns)}. "
                f"Columnas encontradas: {headers}"
            )

        # Reemplazo atómico: el archivo anterior queda intacto
        # si la descarga o las validaciones fallan.
        os.replace(temp_path, output_path)
        temp_path = None

        return total_bytes

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def ingest_resource(resource: dict, output_path: Path) -> None:
    """Descarga el recurso seleccionado y registra el resultado."""
    print(f"Recurso: {resource['name']}", flush=True)
    print(f"URL: {resource['url']}", flush=True)

    size_bytes = download_resource(resource["url"], output_path)

    print(f"Archivo guardado: {output_path}", flush=True)
    print(f"Tamaño: {size_bytes:,} bytes", flush=True)


def main() -> None:
    print("Consultando el catálogo de CKAN...", flush=True)

    dataset = get_dataset(DATASET_ID)
    resources = get_resources(dataset)

    print(f"Recursos publicados: {len(resources)}", flush=True)

    resource = find_resource_by_name(resources, RESOURCE_NAME)
    ingest_resource(resource, OUTPUT_PATH)

    print("Ingesta completada correctamente.", flush=True)


if __name__ == "__main__":
    main()


  