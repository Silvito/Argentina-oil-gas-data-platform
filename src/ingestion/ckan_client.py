import requests


API_URL = "https://datos.gob.ar/api/3/action/package_show"
DATASET_ID = "produccion-de-petroleo-y-gas-por-pozo"


def get_dataset(dataset_id: str) -> dict:
    """
    Obtiene los metadatos de un dataset desde CKAN.
    """
    params = {
        "id": dataset_id
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data["result"]


def get_resources(dataset: dict) -> list:
    """
    Obtiene los recursos disponibles dentro de un dataset CKAN.
    """
    return dataset["resources"]


def find_resources_by_year(resources: list, year: int) -> list:
    """
    Busca recursos cuyo nombre contenga el año indicado.
    """
    return [
        resource
        for resource in resources
        if str(year) in resource.get("name", "")
    ]


if __name__ == "__main__":

    try:
        dataset = get_dataset(DATASET_ID)

        resources = get_resources(dataset)

        print(f"Cantidad de recursos: {len(resources)}")

        resources_2026 = find_resources_by_year(
            resources,
            2026
        )

        print(f"\nRecursos encontrados para 2026: {len(resources_2026)}\n")

        for resource in resources_2026:
            print(f"Nombre: {resource.get('name')}")
            print(f"Formato: {resource.get('format')}")
            print(f"URL: {resource.get('url')}")
            print("-" * 80)

    except requests.exceptions.HTTPError as error:
        print(f"HTTP error: {error}")

    except requests.exceptions.JSONDecodeError:
        print("La respuesta del servidor no contiene JSON válido.")

    except requests.exceptions.Timeout:
        print("La solicitud superó el tiempo de espera.")

    except requests.exceptions.RequestException as error:
        print(f"Error de conexión: {error}")