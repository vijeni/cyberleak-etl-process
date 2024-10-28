import psycopg2
from datetime import datetime


# Insere a data na tabela dim_tempo e retorna o id_tempo
def inserir_dim_tempo(conn, data):
    cursor = conn.cursor()
    data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
    ano = data_formatada.year
    mes = data_formatada.month
    dia = data_formatada.day

    cursor.execute("""
        INSERT INTO dim_tempo (data, ano, mes, dia)
        VALUES (%s, %s, %s, %s)
        RETURNING id_tempo;
    """, (data_formatada, ano, mes, dia))

    id_tempo = cursor.fetchone()[0]
    conn.commit()
    return id_tempo

# Insere a URL na tabela dim_dominio e retorna o id_dominio
def inserir_dim_dominio(conn, dominio):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dim_dominio (dominio)
        VALUES (%s)
        ON CONFLICT (dominio) DO NOTHING
        RETURNING id_dominio;
    """, (dominio,))

    result = cursor.fetchone()
    if result is None:
        # If no row was inserted (due to conflict), query for the existing ID
        cursor.execute("""
            SELECT id_dominio FROM dim_dominio WHERE dominio = %s;
        """, (dominio,))
        result = cursor.fetchone()
        print(dominio)

    id_dominio = result[0]    
    conn.commit()
    return id_dominio

# Insere o email na tabela dim_email e retorna o id_email
def inserir_dim_email(conn, email):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dim_email (endereco)
        VALUES (%s)
        ON CONFLICT (endereco) DO NOTHING
        RETURNING id_email;
    """, (email,))

    result = cursor.fetchone()

    if result is None:
        # If no row was inserted (due to conflict), query for the existing ID
        cursor.execute("""
            SELECT id_email FROM dim_email WHERE endereco = %s;
        """, (email,))
        result = cursor.fetchone()

    id_email = result[0]
    conn.commit()
    return id_email

# Insere a senha na tabela dim_senha e retorna o id_senha
def inserir_dim_senha(conn, senha):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dim_senha (senha)
        VALUES (%s)
        RETURNING id_senha;
    """, (senha,))

    id_senha = cursor.fetchone()[0]
    conn.commit()
    return id_senha

# Insere a plataforma de origem na tabela dim_fonte_vazamento e retorna o id_fonte_vazamento
def inserir_dim_fonte_vazamento(conn, plataforma_origem):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO dim_fonte_vazamento (nome_fonte)
        VALUES (%s)
        ON CONFLICT (nome_fonte) DO NOTHING
        RETURNING id_fonte_vazamento;
    """, (plataforma_origem,))

    result = cursor.fetchone()

    if result is None:
        # If no row was inserted (due to conflict), query for the existing ID
        cursor.execute("""
            SELECT id_fonte_vazamento FROM dim_fonte_vazamento WHERE nome_fonte = %s;
        """, (plataforma_origem,))
        result = cursor.fetchone()

    id_fonte_vazamento = result[0]
    
    conn.commit()
    return id_fonte_vazamento
  
# Insere um registro na tabela fato_vazamentos_email
def inserir_fato_vazamentos_email(conn, id_tempo, id_dominio, id_email, id_fonte_vazamento):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fato_vazamentos_email (id_tempo, id_dominio, id_email, id_fonte_vazamento)
        VALUES (%s, %s, %s, %s)
        RETURNING id_vazamento_email;
    """, (id_tempo, id_dominio, id_email, id_fonte_vazamento))
    
    id_vazamento_email = cursor.fetchone()[0]
   
    conn.commit()
    return id_vazamento_email

# Insere um registro na tabela fato_vazamentos_senha
def inserir_fato_vazamentos_senha(conn, id_dominio, id_senha, id_fonte_vazamento):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fato_vazamentos_senha (id_dominio, id_senha, id_fonte_vazamento)
        VALUES (%s, %s, %s)
        RETURNING id_vazamento_senha;
    """, (id_dominio, id_senha, id_fonte_vazamento))
    
    id_vazamento_senha = cursor.fetchone()[0]
    conn.commit()
    return id_vazamento_senha
