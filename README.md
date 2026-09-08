# Programação de Banco de Dados

Repositório com o conteúdo prático desenvolvido na disciplina de Programação de Banco de Dados, ministrada pelo professor Mateus de Paula. O projeto abrange desde manipulação de banco de dados relacional com Python até conteinerização de ambiente corporativo com Docker.

## Resumo das Atividades
### 1 Automação e CRUD com Python (SQLite)
* Configuração do ambiente virtual (`venv`) e `.gitignore`.
* Operações de CRUD (Create, Read, Update, Delete) no script `aula1.py`.

### 2 Modelagem Relacional e Consultas Avançadas
* Criação de relacionamentos com Chave Estrangeira (`FOREIGN KEY`) em `aula2.py`.
* Execução de consultas com `WHERE`, `INNER JOIN`, `GROUP BY` e `HAVING`.

### 3 Povoamento em Lote e Agregação
* Estruturação e povoamento das tabelas `country` e `city` em `atividade.py`.
* Uso de funções de agregação (`SUM`, `AVG`, `COUNT`) e ordenação (`ORDER BY`).

### 4 Infraestrutura com Docker Compose
* Configuração do `docker-compose.yml` para orquestração de serviços em rede `bridge`.
* Subida de contêineres do PostgreSQL (com volume persistente `pgdata`) e pgAdmin 4.
* Criação e manipulação da tabela `alunos` no banco de dados (`aula_0309.sql`). 

### 5 Resolução de Exercícios de Banco de Dados - PostgreSQL & Python
Este repositório contém a resolução prática da lista de exercícios de Banco de Dados utilizando Python, PostgreSQL e Docker.


## Como Executar o Projeto
1. **Subir os containers do PostgreSQL e pgAdmin:**
   ```bash
   docker compose up -d