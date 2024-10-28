import re
import os

def read_files(diretorio):
    # Verifica se o diretório existe
    if not os.path.exists(diretorio):
        print(f"O diretório {diretorio} não existe.")
        return

    # Itera sobre todos os arquivos do diretório
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)

        # Verifica se é um arquivo (não um subdiretório)
        if os.path.isfile(caminho_arquivo):
            print(caminho_arquivo)
            # with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            #     conteudo = arquivo.read()
                # print(f"Conteúdo do arquivo {nome_arquivo}:\n{conteudo}\n")


# Função para processar o arquivo e extrair colunas para listas individuais
def processar_linhas(nome_arquivo):
    urls = []
    usuarios = []
    senhas = []
    
    try:
        # Abre o arquivo no modo de leitura ('r' - read)
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                
                # Caso a linha esteja no formato com '|'
                if '|' in linha:
                    try:
                        url, usuario, senha = linha.split('|')
                    except ValueError:
                        print(f"Formato inválido (esperado '|'): {linha}")
                        continue
                
                # Caso a linha esteja no formato com ':'
                elif ':' in linha:
                    # Separar a linha em no máximo 3 partes, da direita para a esquerda
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
                
                # Verificação de campos vazios e tamanho do usuário
                if not usuario or not senha:
                    print(f"Usuário ou senha vazios: {linha}")
                    continue
                
                if len(usuario) > 20:
                    print(f"Usuário com mais de 20 caracteres: {linha}")
                    continue

                # Adiciona os valores extraídos às listas
                urls.append(url)
                usuarios.append(usuario)
                senhas.append(senha)
        
        return urls, usuarios, senhas
    
    except FileNotFoundError:
        print(f"Erro: O arquivo {nome_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# nome_arquivo = './input/gabriel.txt'
# user_output_file = './output/users.csv'
# password_output_file = './output/senhas.csv'
# urls, usuarios, senhas = processar_linhas(nome_arquivo)

#   # Escreve as credenciais de usuário em um arquivo de saída
# with open(user_output_file, 'w', encoding='utf-8') as user_output:
#     user_output.write("domain,username\n")  # Cabeçalho do CSV para usuários
#     for credential in usuarios:
#         user_output.write(credential + "\n")

# print(f"Credenciais de usuário extraídas e salvas em '{user_output_file}'.")

# # Escreve as credenciais de senha em um arquivo de saída
# with open(password_output_file, 'w', encoding='utf-8') as password_output:
#     password_output.write("domain,password\n")  # Cabeçalho do CSV para senhas
#     for credential in senhas:
#         password_output.write(credential + "\n")

# print(f"Credenciais de senha extraídas e salvas em '{password_output_file}'.")
# print("URLs:", urls)
# print("Usuários:", usuarios)
# print("Senhas:", senhas)
