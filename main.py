import os

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

                        # Delimita apenas credenciais reais com '|' ou ':' sem se confundir com a URL
                        if "|" in line:
                            # Foco em extrair nome de usuário e senha pelo delimitador "|"
                            parts = line.rsplit("|", 2)  # Divide a partir do final
                            if len(parts) == 3:
                                username = parts[1]  # Parte central é o nome de usuário
                                password = parts[2]  # Última parte é a senha
                                credentials.append(f"{username},{password}")

                        elif ":" in line:
                            # Foco em extrair nome de usuário e senha pelo delimitador ":"
                            parts = line.rsplit(":", 2)  # Divide a partir do final
                            if len(parts) == 3:
                                username = parts[1]  # Parte central é o nome de usuário
                                password = parts[2]  # Última parte é a senha
                                credentials.append(f"{username},{password}")

            except Exception as e:
                print(f"Erro ao ler o arquivo '{file_name}': {e}")

    # Escreve todas as credenciais extraídas em um único arquivo de saída
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write("username,password\n")  # Cabeçalho opcional para o CSV
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
