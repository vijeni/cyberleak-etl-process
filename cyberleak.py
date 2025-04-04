# main.py
import os
from db.database import connect_db
from scripts.processamento import processar_arquivo
import shutil


def main():
    while True:
        diretorio = './files/input'
        arquivos = [f for f in os.listdir(
            diretorio) if os.path.isfile(os.path.join(diretorio, f))]

        if len(arquivos) > 0:
            print("Arquivos disponíveis:")
            for i, arquivo in enumerate(arquivos):
                print(f"{i + 1}. {arquivo}")
                caminho_arquivo = os.path.join(diretorio, arquivos[i])
                if arquivo.endswith('.csv'):
                    separador = ','
                elif arquivo.endswith('.txt'):
                    separador = ';'
                db = connect_db()
                if db:
                    try:
                        linhas_processadas = processar_arquivo(
                            db, caminho_arquivo, separador)
                        db.close()
                        print(
                            f"\nProcesso concluído com sucesso, linhas processadas: {linhas_processadas}")
                        shutil.move(caminho_arquivo, f'./files/processado/{arquivo}')
                    except Exception as e:
                        print("Ocorreu um erro: ", e)


if __name__ == '__main__':
    main()
