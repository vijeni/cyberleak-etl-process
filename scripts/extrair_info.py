import os
import re
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

def extrair_dominio(url):
    try:
        parsed_url = urlparse(url)
        dominio = parsed_url.netloc 
        if dominio.startswith("www."):
            dominio = dominio[4:]        
        return dominio
    except Exception as e:
        print(f"Erro ao extrair domínio da URL: {url}. Erro: {e}")
        return None


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
        print("O nome do arquivo não segue o padrão esperado.")
        return None, None

def processar_arquivo(db, caminho_arquivo, separador):
    data, plataforma_origem = extrair_dados_arquivo(os.path.basename(caminho_arquivo))
    if not data or not plataforma_origem:
        return
    
    id_tempo = inserir_dim_tempo(db, data)
    
    id_fonte_vazamento = inserir_dim_fonte_vazamento(db, plataforma_origem)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        if caminho_arquivo.lower().endswith('.csv'):
          next(arquivo) 
        for linha in arquivo:
            linha = linha.strip()  
            
            if not linha:
                continue  

            if separador == ':':
                partes = linha.rsplit(':', 2)
                
                if len(partes) == 3:
                    url, usuario, senha = partes
                    
                    # Regex para capturar URLs (http, https, android) e lidar com portas
                    match = re.match(r'^(https?|android):\/\/[^:]+(?::\d+)?@?[^:]*', url)
                    if match:
                        url = match.group(0) 
                    else:
                        print(f"Formato inválido (URL): {linha}")
                        continue
                else:
                    print(f"Formato inválido (componentes insuficientes): {linha}")
                    continue

            else:
                partes = linha.split(separador)
                
                if len(partes) != 3:
                    print(f"Erro ao processar linha (formato inesperado): {linha}")
                    continue
                
                url, usuario, senha = partes

            if not senha:
                print(f"Usuário ou senha vazios: {linha}")
                continue
          

            id_dominio = inserir_dim_dominio(db, extrair_dominio(url))
            id_senha = inserir_dim_senha(db, senha)
            inserir_fato_vazamentos_senha(db, id_dominio, id_senha, id_fonte_vazamento)

            if email_valido(usuario):
              id_email = inserir_dim_email(db, usuario)
              inserir_fato_vazamentos_email(db, id_tempo, id_dominio, id_email, id_fonte_vazamento)
            
