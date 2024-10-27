import os

def read_files_in_folder(folder_path):
    """
    Função para ler e exibir o conteúdo de todos os arquivos .txt em uma pasta.
    """
    if not os.path.isdir(folder_path):
        print(f"A pasta '{folder_path}' não foi encontrada.")
        return

    # Percorre todos os arquivos na pasta
    for file_name in os.listdir(folder_path):
        # Verifica se o arquivo tem extensão .txt
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            print(f"\nLendo o arquivo: {file_name}")

            # Tenta abrir e ler o arquivo
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(content)
            except Exception as e:
                print(f"Erro ao ler o arquivo '{file_name}': {e}")

def main():
    # Diretório onde os arquivos estão localizados
    folder_path = "input"  # Substitua pelo caminho da pasta

    # Ler e exibir o conteúdo de todos os arquivos .txt na pasta
    read_files_in_folder(folder_path)

if __name__ == "__main__":
    main()
