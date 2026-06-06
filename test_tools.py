#

import sqlite3
from pprint import pprint
from langchain_anthropic import ChatAnthropic
from docstring_parser import rest


def get_database_schema() -> str:
    """
    Da acceso al eschema de la base de datos.
    :return Schema: Retorna un string con el schema de la base de datos.
    """

    conn = sqlite3.connect("Chinook_Sqlite.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sqlite_schema")
    schema = cursor.fetchall()

    conn.close()

    return f"El esquema es el siguiente: {schema}"


def ejecutar_sql(query: str) -> str:
    """
    Ejecuta querys sobre la base de datos.
    :param query: Query de SQL Lite a ejecutar.
    :return: Retorna un str de los datos cosultados.
    """

    conn = sqlite3.connect("Chinook_Sqlite.sqlite")
    cursor = conn.cursor()
    cursor.execute(query)
    resultado = cursor.fetchall()

    return pprint(f"Resultado de la consulta: {resultado}")


if __name__ == "__main__":
    get_database_schema()
    ejecutar_sql("SELECT COUNT(*) FROM Track")