from datetime import datetime

def inserir_dim_tempo(db, data):
    cursor = db.cursor()
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
    db.commit()
    return id_tempo

def inserir_dim_dominio(db, dominio):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dim_dominio (dominio)
        VALUES (%s)
        ON CONFLICT (dominio) DO NOTHING
        RETURNING id_dominio;
    """, (dominio,))

    result = cursor.fetchone()
    if result is None:
        cursor.execute("""
            SELECT id_dominio FROM dim_dominio WHERE dominio = %s;
        """, (dominio,))
        result = cursor.fetchone()

    id_dominio = result[0]    
    db.commit()
    return id_dominio

def inserir_dim_email(db, email):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dim_email (endereco)
        VALUES (%s)
        ON CONFLICT (endereco) DO NOTHING
        RETURNING id_email;
    """, (email,))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            SELECT id_email FROM dim_email WHERE endereco = %s;
        """, (email,))
        result = cursor.fetchone()

    id_email = result[0]
    db.commit()
    return id_email

def inserir_dim_senha(db, senha):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dim_senha (senha)
        VALUES (%s)
        RETURNING id_senha;
    """, (senha,))

    id_senha = cursor.fetchone()[0]
    db.commit()
    return id_senha

def inserir_dim_fonte_vazamento(db, plataforma_origem):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dim_fonte_vazamento (nome_fonte)
        VALUES (%s)
        ON CONFLICT (nome_fonte) DO NOTHING
        RETURNING id_fonte_vazamento;
    """, (plataforma_origem,))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            SELECT id_fonte_vazamento FROM dim_fonte_vazamento WHERE nome_fonte = %s;
        """, (plataforma_origem,))
        result = cursor.fetchone()

    id_fonte_vazamento = result[0]
    
    db.commit()
    return id_fonte_vazamento
  
def inserir_fato_vazamentos_email(db, id_tempo, id_dominio, id_email, id_fonte_vazamento):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO fato_vazamentos_email (id_tempo, id_dominio, id_email, id_fonte_vazamento)
        VALUES (%s, %s, %s, %s)
        RETURNING id_vazamento_email;
    """, (id_tempo, id_dominio, id_email, id_fonte_vazamento))
    
    id_vazamento_email = cursor.fetchone()[0]
   
    db.commit()
    return id_vazamento_email

def inserir_fato_vazamentos_senha(db, id_dominio, id_senha, id_fonte_vazamento):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO fato_vazamentos_senha (id_dominio, id_senha, id_fonte_vazamento)
        VALUES (%s, %s, %s)
        RETURNING id_vazamento_senha;
    """, (id_dominio, id_senha, id_fonte_vazamento))
    
    id_vazamento_senha = cursor.fetchone()[0]
    db.commit()
    return id_vazamento_senha
