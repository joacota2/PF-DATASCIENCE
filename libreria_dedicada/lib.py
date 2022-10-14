from typing import Union
from google.cloud import bigquery
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

bq = bigquery.Client()

table_lay = "pf-henry-365404.SR.{}"

tables = [
    "AmazonInstantVideo",
    "AndroidApps",
    "Automotive",
    "Baby",
    "Beauty",
    "Books",
    "CDandVinyl",
    "CellphonesAndAccessories",
    "ClothingAndShoesAndJewerly",
    "Digital_Music",
    "Electronics",
    "GroceryAndGourmetFood",
    "HealthAndPersonalCare",
    "Home_and_Kitchen",
    "KindleStore",
    "MoviesAndTV",
    "MusicalInstruments",
    "Office_Products",
    "PatioLawnGarden",
    "PetSupplies",
    "SportsAndOutdoors",
    "ToolsAndHomeImprovement",
    "ToysAndGames",
    "VideoGames",
]


def get_table_data(
    table_id: Union[int, str], limit: int = 10, return_mode: Union[str, int] = "df"
):

    """
    `Ejemplo completo de la función:`

        - get_table_data(table_id = 15, limit = 10, return_mode = 'dict')

    `1. table_id:`

    Nombre de la tabla o identificador numérico.

    `2. limit:`

    Cantidad de registros.

    `3. return_mode:`

    Tipo de valor que retorna la función.

        0. 'df': Pandas Dataframe
        1. 'dict': Diccionario de Python
    """

    if type(table_id) == int:
        table = table_lay.format(tables[table_id])
    else:
        table = table_lay.format(table_id)

    result = (
        bq.query(f"SELECT * FROM `{table}` LIMIT {limit}").to_dataframe().fillna("N/A")
    )

    if return_mode == 0 or return_mode == "df":
        return result
    elif return_mode == 1 or return_mode == "dict":
        return result.to_dict("records")


def get_data_where(
    table_id: Union[int, str],
    where: dict,
    comparison: str = "=",
    where_mode: str = "&",
    limit: int = 10,
    return_mode: Union[str, int] = "df",
):

    """
    `Ejemplo completo de la función:`

        - get_data_where(table_id=15, where=dict(asin='B000BKY8CU'))

    `1. table_id:`

    Nombre de la tabla o identificador numérico.

    `2. where:`

    Cadena de filtros.

    Ej:

        1. dict(asin='B000BKY8CU', reviewTime = '01 1, 2009')

        2. {'asin': 'B000BKY8CU', 'reviewTime' = '01 1, 2009'}

    `3. comparison:`

    Símbolo para comparar keys/values de `where`.

    `4. where_mode:`

    Modo de condiciones.

        '&'

        '|'

    `5. limit:`

    Cantidad de registros.

    `6. return_mode:`

    Tipo de valor que retorna la función.

        0. 'df': Pandas Dataframe
        1. 'dict': Diccionario de Python
    """

    if not " " in where_mode:
        FILTER = f" {where_mode} ".join(
            [f"{key} {comparison} '{value}'" for key, value in where.items()]
        )
    else:
        FILTER = where_mode.join(
            [f"{key} {comparison} '{value}'" for key, value in where.items()]
        )

    if type(table_id) == int:
        table = table_lay.format(tables[table_id])
    else:
        table = table_lay.format(table_id)

    result = (
        bq.query(f"SELECT * FROM `{table}` WHERE {FILTER} LIMIT {limit}")
        .to_dataframe()
        .fillna("N/A")
    )

    if return_mode == 0 or return_mode == "df":
        return result
    elif return_mode == 1 or return_mode == "dict":
        return result.to_dict("records")


def get_custom_query(query, return_mode: Union[str, int] = "df"):

    """
    `Ejemplo completo de la función:`

        - get_custom_query("SELECT * FROM 'pf-henry-365404.SR.MusicalInstruments' LIMIT 10")

    `1. query:`

    Query para ejecutar.

    `Ex:`

    "SELECT * FROM 'pf-henry-365404.SR.MusicalInstruments' LIMIT 10"

    `2. return_mode:`

    Tipo de valor que retorna la función.

        0. 'df': Pandas Dataframe
        1. 'dict': Diccionario de Python
    """

    result = bq.query(query).to_dataframe().fillna("N/A")

    if return_mode == 0 or return_mode == "df":
        return result
    elif return_mode == 1 or return_mode == "dict":
        return result.to_dict("records")


def get_tables():
    """
    Retorna las tablas en formato de lista.
    """
    return tables
