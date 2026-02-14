import os
from dotenv import load_dotenv

load_dotenv()

SQL_CONN_STR = os.getenv("SQL_CONN_STR", "")
