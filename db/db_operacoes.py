from datetime import datetime
from scripts.tratamento_senhas import contabilizar_caracteres, avaliar_senha, criptografar_senha


def inserir_dim_tempo(db, data):
    cursor = db.cursor()
    data_formatada = datetime.strptime(data, '%Y-%m-%d').date()
    ano = data_formatada.year
    mes = data_formatada.month
    dia = data_formatada.day

    cursor.execute("""
        INSERT INTO dim_tempo (data, ano, mes, dia)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (data, ano, mes, dia) DO NOTHING
        RETURNING id_tempo;
    """, (data_formatada, ano, mes, dia))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            SELECT id_tempo FROM dim_tempo WHERE data = %s AND ano = %s AND mes = %s AND dia = %s;
        """, (data_formatada, ano, mes, dia,))
        result = cursor.fetchone()

    id_tempo = result[0]
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
    qntd_caract, qntd_caract_text, qntd_caract_especiais, qntd_numeros, qntd_caract_text_upper, qntd_caract_text_lower = contabilizar_caracteres(
        senha)
    complexidade, avisos, tempo_adivinhacao = avaliar_senha(senha)
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO dim_senha (senha, qntd_caract, qntd_caract_text, qntd_caract_especiais, qntd_numeros, qntd_caract_text_upper, qntd_caract_text_lower, complexidade, avisos, tempo_adivinhacao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_senha;
    """, (criptografar_senha(senha), qntd_caract, qntd_caract_text, qntd_caract_especiais, qntd_numeros, qntd_caract_text_upper, qntd_caract_text_lower, complexidade, avisos, tempo_adivinhacao,))

    id_senha = cursor.fetchone()[0]
    db.commit()
    return id_senha


def inserir_fato_fonte_vazamento(db, plataforma_origem):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO fato_fonte_vazamento (nome_fonte)
        VALUES (%s)
        ON CONFLICT (nome_fonte) DO NOTHING
        RETURNING id_fonte_vazamento;
    """, (plataforma_origem,))

    result = cursor.fetchone()

    if result is None:
        cursor.execute("""
            SELECT id_fonte_vazamento FROM fato_fonte_vazamento WHERE nome_fonte = %s;
        """, (plataforma_origem,))
        result = cursor.fetchone()

    id_fonte_vazamento = result[0]

    db.commit()
    return id_fonte_vazamento


def inserir_fato_vazamentos_email(db, id_tempo, id_dominio, id_email):
    cursor = db.cursor()
    result = cursor.execute("""
        INSERT INTO fato_vazamentos_email (id_tempo, id_dominio, id_email)
        VALUES (%s, %s, %s)
        RETURNING id_vazamento_email;
    """, (id_tempo, id_dominio, id_email,))

    id_vazamento_email = cursor.fetchone()[0]

    db.commit()
    return id_vazamento_email


def inserir_fato_vazamentos_senha(db, id_tempo, id_dominio, id_senha):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO fato_vazamentos_senha (id_tempo, id_dominio, id_senha)
        VALUES (%s, %s, %s)
        RETURNING id_vazamento_senha;
    """, (id_tempo, id_dominio, id_senha,))

    id_vazamento_senha = cursor.fetchone()[0]
    db.commit()
    return id_vazamento_senha
