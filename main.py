import os
from db.db_connection import connect_db
from scripts.extract_info import processar_arquivo


def main():
    diretorio = './input'
    arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    print("Arquivos disponíveis:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}. {arquivo}")

    escolha = int(input("Escolha um arquivo para processar: ")) - 1
    separador = input("Escolha o separador do arquivo (| , :): ")

    caminho_arquivo = os.path.join(diretorio, arquivos[escolha])

    db = connect_db()
    if db:
        processar_arquivo(db, caminho_arquivo, separador)
        db.close()

if __name__ == '__main__':
    main()
