import os
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from db.db_operacoes import (
    inserir_dim_tempo,
    inserir_dim_dominio,
    inserir_dim_email,
    inserir_dim_senha,
    inserir_fato_vazamentos_email,
    inserir_fato_vazamentos_senha
)
from scripts.utils import configure_logging, extrair_dominio, email_valido, extrair_dados_arquivo
from colorama import Fore, Style, init

init(autoreset=True)
barra_progresso_custom = (
    "{l_bar}" + Fore.YELLOW + "{bar}" + Style.RESET_ALL +
    "| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
)


def processar_chunk(chunk, db, id_tempo, separador, logger, barra):
    contador_linhas = 0
    for linha in chunk:
        linha = linha.replace('\x00', '').strip()
        if not linha:
            continue

        contador_linhas += 1
        if separador == ':':
            if "|" in linha:
                partes = linha.split("|")
                if len(partes) != 3:
                    logger.warning(
                        f"Erro ao processar linha (formato inesperado): {linha}")
                    continue
                url, usuario, senha = partes
            else:
                partes = linha.rsplit(separador, 2)
                if len(partes) != 3:
                    logger.warning(
                        f"Formato inválido (componentes insuficientes): {linha}")
                    continue
                url, usuario, senha = partes
        else:
            partes = linha.split(separador)
            if len(partes) != 3:
                logger.warning(
                    f"Erro ao processar linha (formato inesperado): {linha}")
                continue
            url, usuario, senha = partes

        match = re.match(r'^(https?):\/\/[^:]+(?::\d+)?@?[^:]*', url)
        if not match:
            logger.warning(f"Formato inválido (URL): {linha}")
            continue
        url = match.group(0)

        if not senha or len(senha) > 40 or len(senha) < 4:
            logger.warning(f"Senha inválida: {senha}")
            continue

        id_dominio = inserir_dim_dominio(db, extrair_dominio(url))
        id_senha = inserir_dim_senha(db, senha)
        inserir_fato_vazamentos_senha(db, id_tempo, id_dominio, id_senha)

        if email_valido(usuario):
            id_email = inserir_dim_email(db, usuario)
            inserir_fato_vazamentos_email(db, id_tempo, id_dominio, id_email)

        barra.update(1)

    return contador_linhas


def processar_arquivo(db, caminho_arquivo, separador, max_workers=1):
    data, plataforma_origem = extrair_dados_arquivo(
        os.path.basename(caminho_arquivo))
    if not data or not plataforma_origem:
        return

    logger = configure_logging(plataforma_origem)
    id_tempo = inserir_dim_tempo(db, data)

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        quantidade_linhas = sum(1 for _ in arquivo)
        arquivo.seek(0)
        print(max_workers)
        chunk_size = int((quantidade_linhas / max_workers)+1) 
        print(chunk_size)
        if caminho_arquivo.lower().endswith('.csv'):
            next(arquivo)

        with tqdm(total=quantidade_linhas, desc=Fore.BLUE + "Processando" + Style.RESET_ALL,
                  bar_format=barra_progresso_custom, ascii=False, unit=" linha") as barra:

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                chunk = []

                for linha in arquivo:
                    chunk.append(linha)
                    if len(chunk) >= chunk_size:
                        futures.append(executor.submit(
                            processar_chunk, chunk, db, id_tempo, separador, logger, barra))
                        chunk = []

                if chunk:
                    futures.append(executor.submit(
                        processar_chunk, chunk, db, id_tempo, separador, logger, barra))

                total_linhas = sum(f.result() for f in futures)
                print(f"Total de linhas processadas: {total_linhas}")

    return total_linhas
