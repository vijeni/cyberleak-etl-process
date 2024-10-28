import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
