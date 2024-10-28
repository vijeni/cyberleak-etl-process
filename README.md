
Arquivos do ./input sempre vao seguir os padroes:

YYYY-MM-DD_Plataforma-origem.txt
YYYY-MM-DD_Plataforma-origem.csv

Script irá ler o arquivo escolhido, e dar um prompt ao usuario para escolher o separador. Considerando que o arquivo contem 3 informações: URL, usuario, senha. O script deve separar essas informacoes, de acordo o separadores escolhido (| , :) e inserir em um banco de dados na seguinte ordem.

- dim_dominio - com as URLs encontrada
- dim_email - com os emails encontrados
- dim_fonte_vazamento - com a "Plataforma-origem" do nome do arquivo
- dim_senha - com as senhas encontradas
- dim_tempo - com a data no nome do arquivo, caso a mesma não exista
- fato_vazamentos_email - com os IDs dos itens adicionados anteriormente
- fato_vazamentos_senha - com os IDs dos itens adicionados anteriormente

Esses inserts precisam acontecer sequencialmente, recuperando os IDs a cada insert, para poder fazer a inserção do fato_vazamentos_senha e fatos_vazamentos_email

