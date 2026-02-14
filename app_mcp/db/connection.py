import pyodbc
from app_mcp.deps import SQL_CONN_STR


def get_conn():
    return pyodbc.connect(SQL_CONN_STR)
