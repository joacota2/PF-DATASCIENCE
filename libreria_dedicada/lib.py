from typing import Union
from google.cloud import bigquery

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
    "metaLORD",
]


def get_table_data(
    table_id: Union[int, str],
    columns: list[str] = "*",
    limit: int = 10,
    return_mode: Union[str, int] = "df",
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
        bq.query(f"SELECT {', '.join(columns)} FROM `{table}` LIMIT {limit}")
        .to_dataframe()
        .fillna("N/A")
    )

    try:
        if return_mode == 0 or return_mode == "df":
            return result
        elif return_mode == 1 or return_mode == "dict":
            return result.to_dict("records")
    except:
        return None


def get_data_where(
    table_id: Union[int, str],
    where: dict,
    first: bool = False,
    columns: Union[str, list[str]] = "*",
    comparison: str = "=",
    where_mode: str = "AND",
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
            [
                f"{key} {comparison} {value}"
                if type(value) == int or type(value) == float
                else f"{key} {comparison} '{value}'"
                for key, value in where.items()
            ]
        )
    else:
        FILTER = where_mode.join(
            [
                f"{key} {comparison} {value}"
                if type(value) == int or type(value) == float
                else f"{key} {comparison} '{value}'"
                for key, value in where.items()
            ]
        )

    if type(table_id) == int:
        table = table_lay.format(tables[table_id])
    else:
        table = table_lay.format(table_id)

    query = f"SELECT {', '.join(columns)} FROM `{table}` WHERE {FILTER} LIMIT {limit}"

    print("Sending query:", query)

    result = bq.query(query).to_dataframe().fillna("N/A")

    print("Query sent, returning answer...")

    try:
        if return_mode == 0 or return_mode == "df":
            if first:
                return result.head(1)
            return result
        elif return_mode == 1 or return_mode == "dict":
            if first:
                return result.to_dict("records")[0]
            return result.to_dict("records")
    except:
        return None


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

    try:
        if return_mode == 0 or return_mode == "df":
            return result
        elif return_mode == 1 or return_mode == "dict":
            return result.to_dict("records")
    except:
        return None


def insert_data(table_id: Union[int, str], data: Union[dict, list[dict]]):
    if type(table_id) == int:
        table = table_lay.format(tables[table_id])
    else:
        table = table_lay.format(table_id)

    try:
        if bq.insert_rows_json(table, data) == []:

            return True

        return False
    except:
        return None


def get_tables():
    """
    Retorna las tablas en formato de lista.

    0. AmazonInstantVideo
    1. AndroidApps
    2. Automotive
    3. Baby
    4. Beauty
    5. Books
    6. CDandVinyl
    7. CellphonesAndAccessories
    8. ClothingAndShoesAndJewerly
    9. Digital_Music
    10. Electronics
    11. GroceryAndGourmetFood
    12. HealthAndPersonalCare
    13. Home_and_Kitchen
    14. KindleStore
    16. MoviesAndTV
    17. MusicalInstruments
    18. Office_Products
    19. PatioLawnGarden
    20. PetSupplies
    21. SportsAndOutdoors
    22. ToolsAndHomeImprovement
    23. ToysAndGames
    24. VideoGames
    25. metaLORD
    """
    return tables
