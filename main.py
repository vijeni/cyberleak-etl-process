import os
from urllib.parse import urlparse

def extract_credentials(folder_path, output_file):
    credentials = []
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

                        # Extrai o domínio da URL, e as credenciais com "|" ou ":"
                        if "|" in line:
                            # Divide em URL e partes de credenciais com "|"
                            parts = line.split("|", 2)
                            if len(parts) == 3:
                                url = parts[0]
                                username = parts[1]
                                password = parts[2]

                        elif ":" in line:
                            # Divide em URL e partes de credenciais com ":"
                            parts = line.split(":", 2)
                            if len(parts) == 3:
                                url = parts[0]
                                username = parts[1]
                                password = parts[2]

                        # Extraindo domínio da URL
                        domain = urlparse(url).netloc  # Extrai o domínio

                        # Adiciona as informações ao CSV
                        credentials.append(f"{domain},{username},{password}")

            except Exception as e:
                print(f"Erro ao ler o arquivo '{file_name}': {e}")

    # Escreve todas as credenciais extraídas em um único arquivo de saída
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("domain,username,password\n")  # Cabeçalho do CSV
        for credential in credentials:
            output.write(credential + "\n")

    print(f"Credenciais extraídas e salvas em '{output_file}'.")

def main():
    # Diretório onde os arquivos estão localizados
    folder_path = "input"  # Substitua pelo caminho da pasta onde estão os arquivos

    # Caminho do arquivo consolidado
    output_file = "credenciais_consolidadas.csv"

    # Extrair credenciais e consolidá-las
    extract_credentials(folder_path, output_file)

if __name__ == "__main__":
    main()
