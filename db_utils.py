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
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

def insert_dim_email(cursor, email):
    cursor.execute("SELECT id_email FROM dim_email WHERE endereco = %s", (email,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO dim_email (endereco, validado) VALUES (%s, %s) RETURNING id_email", (email, True))
        return cursor.fetchone()[0]

def insert_dim_senha(cursor, senha_hash, complexidade, tipo_criptografia):
    cursor.execute("SELECT id_senha FROM dim_senha WHERE senha_hash = %s", (senha_hash,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO dim_senha (senha_hash, complexidade, tipo_criptografia) VALUES (%s, %s, %s) RETURNING id_senha",
            (senha_hash, complexidade, tipo_criptografia)
        )
        return cursor.fetchone()[0]

def insert_dim_dominio(cursor, dominio):
    cursor.execute("SELECT id_dominio FROM dim_dominio WHERE dominio = %s", (dominio,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO dim_dominio (dominio) VALUES (%s) RETURNING id_dominio", (dominio,))
        return cursor.fetchone()[0]

def insert_dim_plataforma(cursor, nome_plataforma, descricao):
    cursor.execute("SELECT id_plataforma FROM dim_plataforma WHERE nome_plataforma = %s", (nome_plataforma,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO dim_plataforma (nome_plataforma, descricao) VALUES (%s, %s) RETURNING id_plataforma",
            (nome_plataforma, descricao)
        )
        return cursor.fetchone()[0]

def insert_fato_vazamento_email(cursor, id_tempo, id_plataforma, id_dominio, id_email, id_fonte_vazamento):
    cursor.execute("""
        INSERT INTO fato_vazamentos_email (id_tempo, id_plataforma, id_dominio, id_email, id_fonte_vazamento)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_tempo, id_plataforma, id_dominio, id_email, id_fonte_vazamento))

def insert_fato_vazamento_senha(cursor, id_tempo, id_plataforma, id_dominio, id_senha, id_fonte_vazamento):
    cursor.execute("""
        INSERT INTO fato_vazamentos_senha (id_tempo, id_plataforma, id_dominio, id_senha, id_fonte_vazamento)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_tempo, id_plataforma, id_dominio, id_senha, id_fonte_vazamento))
