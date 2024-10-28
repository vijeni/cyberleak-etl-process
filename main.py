# main.py
import os
import re
from db.db_connection import connect_db
from db.db_operations import (
    inserir_dim_tempo,
    inserir_dim_dominio,
    inserir_dim_email,
    inserir_dim_senha,
    inserir_dim_fonte_vazamento,
    inserir_fato_vazamentos_email,
    inserir_fato_vazamentos_senha
)

def email_valido(email):
    # Expressão regular para validar um e-mail simples
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Extrai a data e a plataforma do nome do arquivo
def extrair_dados_arquivo(nome_arquivo):
    pattern = r'(\d{4}-\d{2}-\d{2})_(.+)\.(txt|csv)'
    match = re.match(pattern, nome_arquivo)
    if match:
        data = match.group(1)
        plataforma_origem = match.group(2) + '-' + match.group(3)
        return data, plataforma_origem
    else:
        print("O nome do arquivo não segue o padrão esperado.")
        return None, None

# Processa o arquivo e faz os inserts necessários
def processar_arquivo(conn, caminho_arquivo, separador):
    data, plataforma_origem = extrair_dados_arquivo(os.path.basename(caminho_arquivo))
    if not data or not plataforma_origem:
        return
    
    # Inserir a data na tabela dim_tempo
    id_tempo = inserir_dim_tempo(conn, data)
    
    # Inserir a plataforma na tabela dim_fonte_vazamento
    id_fonte_vazamento = inserir_dim_fonte_vazamento(conn, plataforma_origem)
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        if caminho_arquivo.lower().endswith('.csv'):
          next(arquivo)  # Skip the header line
        for linha in arquivo:
            linha = linha.strip()  # Remove espaços e quebras de linha ao redor
            
            if not linha:
                continue  # Ignora linhas vazias

            # Verifica o tipo de separador e realiza o tratamento adequado
            if separador == ':':
                # Separar a linha em no máximo 3 partes da direita para a esquerda
                partes = linha.rsplit(':', 2)
                
                # Verifica se conseguimos dividir em exatamente 3 partes (URL, usuário e senha)
                if len(partes) == 3:
                    url_usuario, usuario, senha = partes
                    
                    # Regex para capturar URLs (http, https, android) e lidar com portas
                    match = re.match(r'^(https?|android):\/\/[^:]+(?::\d+)?@?[^:]*', url_usuario)
                    if match:
                        url = match.group(0)  # Captura a URL completa
                    else:
                        print(f"Formato inválido (URL): {linha}")
                        continue
                else:
                    print(f"Formato inválido (componentes insuficientes): {linha}")
                    continue

            else:
                # Separação padrão para delimitadores como ',' ou '|'
                partes = linha.split(separador)
                
                if len(partes) != 3:
                    print(f"Erro ao processar linha (formato inesperado): {linha}")
                    continue
                
                # Atribui diretamente se o split com delimitador padrão for bem-sucedido
                url, usuario, senha = partes

            # Verificação de campos vazios e tamanho do usuário
            if not senha:
                print(f"Usuário ou senha vazios: {linha}")
                continue
          

            # Inserir a URL (domínio)
            id_dominio = inserir_dim_dominio(conn, url)
            
            # Inserir a senha
            id_senha = inserir_dim_senha(conn, senha)

            # Inserir na tabela de fatos (vazamento senha)
            inserir_fato_vazamentos_senha(conn, id_dominio, id_senha, id_fonte_vazamento)

            if email_valido(usuario):
              # Inserir o email
              id_email = inserir_dim_email(conn, usuario)
              # Inserir na tabela de fatos (vazamento email)
              inserir_fato_vazamentos_email(conn, id_tempo, id_dominio, id_email, id_fonte_vazamento)
            

# Função principal
def main():
    diretorio = './input'
    arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    print("Arquivos disponíveis:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}. {arquivo}")

    escolha = int(input("Escolha um arquivo para processar: ")) - 1
    separador = input("Escolha o separador do arquivo (| , :): ")

    caminho_arquivo = os.path.join(diretorio, arquivos[escolha])

    # Conectar ao banco e processar o arquivo
    conn = connect_db()
    if conn:
        processar_arquivo(conn, caminho_arquivo, separador)
        conn.close()

if __name__ == '__main__':
    main()
