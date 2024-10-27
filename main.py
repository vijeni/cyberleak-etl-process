import os
from urllib.parse import urlparse

def extract_credentials(folder_path, user_output_file, password_output_file):
    """
    Função para extrair domínio, nome de usuário e senha de arquivos .txt em uma pasta e
    salvá-los em dois arquivos CSV separados: um para usuário e outro para senha.
    """
    user_credentials = []
    password_credentials = []

    # Percorre todos os arquivos na pasta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Considera apenas arquivos com extensão .txt
            file_path = os.path.join(folder_path, file_name)
            print(f"Lendo o arquivo: {file_name}")

            # Abre o arquivo e lê as linhas
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()  # Remove espaços e quebras de linha

                        # Extrai o domínio da URL e as credenciais
                        if "|" in line:
                            parts = line.split("|", 2)
                            if len(parts) == 3:
                                url = parts[0]
                                username = parts[1]
                                password = parts[2]

                        elif ":" in line:
                            parts = line.split(":", 2)
                            if len(parts) == 3:
                                url = parts[0]
                                username = parts[1]
                                password = parts[2]

                        # Extraindo domínio da URL
                        domain = urlparse(url).netloc  # Extrai o domínio

                        # Adiciona as informações aos CSVs separados
                        user_credentials.append(f"{domain},{username}")
                        password_credentials.append(f"{domain},{password}")

            except Exception as e:
                print(f"Erro ao ler o arquivo '{file_name}': {e}")

    # Escreve as credenciais de usuário em um arquivo de saída
    with open(user_output_file, 'w', encoding='utf-8') as user_output:
        user_output.write("domain,username\n")  # Cabeçalho do CSV para usuários
        for credential in user_credentials:
            user_output.write(credential + "\n")

    print(f"Credenciais de usuário extraídas e salvas em '{user_output_file}'.")

    # Escreve as credenciais de senha em um arquivo de saída
    with open(password_output_file, 'w', encoding='utf-8') as password_output:
        password_output.write("domain,password\n")  # Cabeçalho do CSV para senhas
        for credential in password_credentials:
            password_output.write(credential + "\n")

    print(f"Credenciais de senha extraídas e salvas em '{password_output_file}'.")

def main():
    # Diretório onde os arquivos estão localizados
    folder_path = "input"  # Substitua pelo caminho da pasta onde estão os arquivos

    # Caminhos dos arquivos de saída
    user_output_file = "usuarios.csv"
    password_output_file = "senhas.csv"

    # Extrair credenciais e salvá-las em arquivos separados
    extract_credentials(folder_path, user_output_file, password_output_file)

if __name__ == "__main__":
    main()
