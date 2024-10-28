# main.py
import os
from db.database import connect_db
from scripts.processamento import processar_arquivo


def main():
    diretorio = './input'
    arquivos = [f for f in os.listdir(
        diretorio) if os.path.isfile(os.path.join(diretorio, f))]

    print("Arquivos disponíveis:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}. {arquivo}")

    escolha = int(input("Escolha um arquivo para processar: ")) - 1
    print("\n")
    separador = input("Escolha o separador do arquivo (| , :): ")
    print("\n")
    caminho_arquivo = os.path.join(diretorio, arquivos[escolha])

    db = connect_db()
    if db:
        try:
            linhas_processadas = processar_arquivo(
                db, caminho_arquivo, separador)
            db.close()
            print(
                f"\nProcesso concluído com sucesso, linhas processadas: {linhas_processadas}")
        except Exception as e:
            print("Ocorreu um erro: ", e)


if __name__ == '__main__':
    main()
