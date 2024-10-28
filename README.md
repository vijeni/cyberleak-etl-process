
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

Segue o SQL de estrutura do banco de dados

CREATE TABLE dim_tempo (
    id_tempo SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    ano INT NOT NULL,
    mes INT NOT NULL,
    dia INT NOT NULL
);

CREATE TABLE dim_dominio (
    id_dominio SERIAL PRIMARY KEY,
    dominio VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE dim_email (
    id_email SERIAL PRIMARY KEY,
    endereco VARCHAR(255) UNIQUE NOT NULL,
    validado BOOLEAN
);

CREATE TABLE dim_senha (
    id_senha SERIAL PRIMARY KEY,
    senha TEXT NOT NULL,
    complexidade VARCHAR(50),
);

CREATE TABLE dim_fonte_vazamento (
    id_fonte_vazamento SERIAL PRIMARY KEY,
    nome_fonte VARCHAR(255) NOT NULL,
    descricao TEXT
);

-- Create the fact tables
CREATE TABLE fato_vazamentos_email (
    id_vazamento_email SERIAL PRIMARY KEY,
    id_tempo INT REFERENCES dim_tempo(id_tempo),
    id_plataforma INT REFERENCES dim_plataforma(id_plataforma),
    id_dominio INT REFERENCES dim_dominio(id_dominio),
    id_email INT REFERENCES dim_email(id_email),
    id_fonte_vazamento INT REFERENCES dim_fonte_vazamento(id_fonte_vazamento) -- new column to link source of the leak
);

CREATE TABLE fato_vazamentos_senha (
    id_vazamento_senha SERIAL PRIMARY KEY,
    id_plataforma INT REFERENCES dim_plataforma(id_plataforma),
    id_dominio INT REFERENCES dim_dominio(id_dominio),
    id_senha INT REFERENCES dim_senha(id_senha),
    id_fonte_vazamento INT REFERENCES dim_fonte_vazamento(id_fonte_vazamento) -- optional, added if needed
);