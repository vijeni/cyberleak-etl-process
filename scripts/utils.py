# scripts/utils.py
import logging
import re
from urllib.parse import urlparse
from datetime import datetime


def configure_logging(plataforma_origem):
    log_filename = f'./log/{plataforma_origem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        filename=log_filename,
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
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao extrair domínio: {url}. Erro: {e}")
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
        logger = logging.getLogger(__name__)
        logger.warning("Nome do arquivo não segue o padrão esperado.")
        return None, None
