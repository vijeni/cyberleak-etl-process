import os
import re
from tqdm import tqdm
from db.operacoes import (
    inserir_dim_tempo,
    inserir_dim_dominio,
    inserir_dim_email,
    inserir_dim_senha,
    inserir_dim_fonte_vazamento,
    inserir_fato_vazamentos_email,
    inserir_fato_vazamentos_senha
)
from scripts.utils import configure_logging, extrair_dominio, email_valido, extrair_dados_arquivo
from colorama import Fore, Style, init

# Barra de progresso
init(autoreset=True)
barra_progresso_custom = (
    "{l_bar}" + Fore.YELLOW + "{bar}" + Style.RESET_ALL +
    "| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
)


def processar_arquivo(db, caminho_arquivo, separador):
    data, plataforma_origem = extrair_dados_arquivo(
        os.path.basename(caminho_arquivo))
    if not data or not plataforma_origem:
        return

    logger = configure_logging(plataforma_origem)
    id_tempo = inserir_dim_tempo(db, data)
    id_fonte_vazamento = inserir_dim_fonte_vazamento(db, plataforma_origem)

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        quantidade_linhas = sum(1 for _ in arquivo)
        arquivo.seek(0)

        contador_linhas = 0

        with tqdm(total=quantidade_linhas, desc=Fore.BLUE + "Processando" + Style.RESET_ALL, bar_format=barra_progresso_custom,
                ascii=False, unit=" linha") as barra:
            if caminho_arquivo.lower().endswith('.csv'):
                next(arquivo)

            for linha in arquivo:
                contador_linhas += 1
                barra.update(1)

                linha = linha.replace('\x00', '').strip()

                if not linha:
                    continue

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

                        if len(partes) == 3:
                            url, usuario, senha = partes

                            # Regex para capturar URLs (http, https, android) e lidar com portas
                            match = re.match(
                                r'^(https?):\/\/[^:]+(?::\d+)?@?[^:]*', url)
                            if match:
                                url = match.group(0)
                            else:
                                logger.warning(f"Formato inválido (URL): {linha}")
                                continue
                        else:
                            logger.warning(
                                f"Formato inválido (componentes insuficientes): {linha}")
                            continue
                else:
                    partes = linha.split(separador)

                    if len(partes) != 3:
                        logger.warning(
                            f"Erro ao processar linha (formato inesperado): {linha}")
                        continue

                    url, usuario, senha = partes

                if not senha:
                    logger.warning(f"Usuário ou senha vazios: {linha}")
                    continue
                if len(senha) > 40 or len(senha) < 4:
                    logger.warning(
                        f"Senha não possui entre 4 e 40 caracteres: {senha} - {len(senha)}")
                    continue

                id_dominio = inserir_dim_dominio(db, extrair_dominio(url))
                id_senha = inserir_dim_senha(db, senha)
                inserir_fato_vazamentos_senha(
                    db, id_dominio, id_senha, id_fonte_vazamento)

                if email_valido(usuario):
                    id_email = inserir_dim_email(db, usuario)
                    inserir_fato_vazamentos_email(
                        db, id_tempo, id_dominio, id_email, id_fonte_vazamento)
    return contador_linhas
