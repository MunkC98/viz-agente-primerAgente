import sqlite3
from langchain.agents import create_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect("Chinook_Sqlite.sqlite", check_same_thread=False)

cursor = conn.cursor()


# Creamos la herramienta para que el agente pueda explorar la base de datos.
@tool
def get_database_schema() -> str:
    """
    Da acceso al eschema de la base de datos.
    :param cursor: Conexión a SQLite para ejecutar las consutlas.
    :return Schema: Retorna un string con el schema de la base de datos.
    """
    try:
        cursor.execute("SELECT * FROM sqlite_schema")
        schema = cursor.fetchall()
    except sqlite3.Error as e:
        return f"No se logro ejecutar la consulta: {e}"

    return f"El esquema es el siguiente: {schema}"

@tool
def ejecutar_sql(query: str) -> str:
    """
    Ejecuta querys sobre la base de datos.
    :param query: Query de SQL Lite a ejecutar.
    :return: Retorna un str de los datos cosultados.
    """
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
    except sqlite3.Error as e:
        return  f"No se logro ejecutar la consulta: {e}"

    return f"Resultado de la consulta: {resultado}"

agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=[ejecutar_sql, get_database_schema],
    system_prompt="Eres un analista experto en SQLite"
)
inputs = {"messages": [{"role": "user", "content": "Cuantos artistas hay?"}]}
for chunk in agent.stream(inputs, stream_mode="updates"):
    print(chunk)