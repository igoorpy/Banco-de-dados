# Banco de Dados - PostgreSQL e pgAdmin 4 via Docker

Este repositorio contem os scripts e projetos de Banco de Dados desenvolvidos para as atividades praticas da disciplina ministrada pelo professor Mateus de Paula.

## Resumo das Atividades em Sala de Aula

1. Automacao e CRUD com Python (SQLite)
   * Configuracao de venv e .gitignore.
   * Operacoes de CRUD (Create, Read, Update, Delete) no arquivo aula1.py.

2. Modelagem Relacional e Consultas Avancadas
   * Criacao de relacionamentos com FOREIGN KEY no arquivo aula2.py.
   * Consultas com WHERE, INNER JOIN, GROUP BY e HAVING.

3. Povoamento em Lote e Agregacao
   * Povoamento das tabelas country e city.
   * Funcoes de agregacao (SUM, AVG, COUNT) e ordenacao (ORDER BY).

## Lista de Exercicios (Questoes 10, 14 a 20)

Atividade focada na execucao de queries e subconsultas SQL diretamente na interface do pgAdmin 4 via Docker Compose.

### Estrutura do Projeto

* docker-compose.yml: Configuracao dos servicos PostgreSQL e pgAdmin 4.
* script_lab4.sql: Script SQL das questoes 10 e 14 a 20 (criacao de tabelas, insercoes e subconsultas).
* script_lab5.sql: Script SQL do Lab 5 (modelagem ERD e relacionamentos).

#### Consultas e Agregacao (Questao 10)
![Resultado Questao 10](png/Junção%20de%20Tabelas%20e%20Agregação%20(Questão%2010).png)

#### Subconsultas com IN e MAX (Questao 14)
![Resultado Questao 14](png/Subconsulta%20com%20IN%20e%20MAX%20(Questão%2014).png)

#### Subconsultas com Predicado EXISTS (Questao 20)
![Resultado Questao 20](png/Subconsulta%20com%20Predicado%20EXISTS%20(Questão%2020).png)
