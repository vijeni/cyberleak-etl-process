import os
import re
import logging
from datetime import datetime
from urllib.parse import urlparse
from db.database import connect_db
from db.operacoes import (
    inserir_dim_tempo,
    inserir_dim_dominio,
    inserir_dim_email,
    inserir_dim_senha,
    inserir_dim_fonte_vazamento,
    inserir_fato_vazamentos_email,
    inserir_fato_vazamentos_senha
)

def configure_logging(plataforma_origem):
    log_filename = f'{plataforma_origem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        filename="./log/"+log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def extrair_dominio(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc 
        if dominio.startswith("www."):
            dominio = dominio[4:]        
        return dominio
    except Exception as e:
        logger.error(f"Erro ao extrair domínio da URL: {url}. Erro: {e}")
        return url

def email_valido(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def extrair_dados_arquivo(nome_arquivo):
    pattern = r'(\d{4}-\d{2}-\d{2})_(.+)\.(txt|csv)'
    match = re.match(pattern, nome_arquivo)
    if match:
        data = match.group(1)
        plataforma_origem = match.group(2)
        return data, plataforma_origem
    else:
        temp_logger = logging.getLogger("temp_logger")
        temp_logger.warning("O nome do arquivo não segue o padrão esperado.")
        return None, None

def processar_arquivo(db, caminho_arquivo, separador):
    data, plataforma_origem = extrair_dados_arquivo(os.path.basename(caminho_arquivo))
    if not data or not plataforma_origem:
        return

    global logger
    logger = configure_logging(plataforma_origem)
    
    id_tempo = inserir_dim_tempo(db, data)
    
    id_fonte_vazamento = inserir_dim_fonte_vazamento(db, plataforma_origem)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        if caminho_arquivo.lower().endswith('.csv'):
            next(arquivo)
        
        for linha in arquivo:
            linha = linha.replace('\x00', '').strip()
            
            if not linha:
                continue

            if separador == ':':
                if "|" in linha:
                    partes = linha.split("|")
                
                    if len(partes) != 3:
                        logger.warning(f"Erro ao processar linha (formato inesperado): {linha}")
                        continue
                    url, usuario, senha = partes
                else:
                    partes = linha.rsplit(separador, 2)
                    
                    if len(partes) == 3:
                        url, usuario, senha = partes
                        
                        # Regex para capturar URLs (http, https, android) e lidar com portas
                        match = re.match(r'^(https?):\/\/[^:]+(?::\d+)?@?[^:]*', url)
                        if match:
                            url = match.group(0)
                        else:
                            logger.warning(f"Formato inválido (URL): {linha}")
                            continue
                    else:
                        logger.warning(f"Formato inválido (componentes insuficientes): {linha}")
                        continue
            else:
                partes = linha.split(separador)
                
                if len(partes) != 3:
                    logger.warning(f"Erro ao processar linha (formato inesperado): {linha}")
                    continue
                
                url, usuario, senha = partes

            if not senha:
                logger.warning(f"Usuário ou senha vazios: {linha}")
                continue
            if len(senha) > 40 or len(senha) < 4:
                logger.warning(f"Senha não possui entre 4 e 40 caracteres: {senha} - {len(senha)}")
                continue

            id_dominio = inserir_dim_dominio(db, extrair_dominio(url))
            id_senha = inserir_dim_senha(db, senha)
            inserir_fato_vazamentos_senha(db, id_dominio, id_senha, id_fonte_vazamento)

            if email_valido(usuario):
              id_email = inserir_dim_email(db, usuario)
              inserir_fato_vazamentos_email(db, id_tempo, id_dominio, id_email, id_fonte_vazamento)
            
