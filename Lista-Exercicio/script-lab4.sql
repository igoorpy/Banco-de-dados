-- LAB 4: EXERCÍCIOS DE BANCO DE DADOS (POSTGRESQL / PGADMIN 4)
-- Limpeza preventiva de tabelas anteriores para evitar conflitos
DROP TABLE IF EXISTS Consulta, Paciente, Medico, Especialidade, venda, produto, vendedor, Relacao1, Aluno, Curso CASCADE;
-- QUESTÃO 10: TABELAS DE VENDAS E CONSULTAS PRÁTICAS

CREATE TABLE vendedor (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    salario DECIMAL(10,2) DEFAULT 0.00
);

CREATE TABLE produto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

CREATE TABLE venda (
    id SERIAL PRIMARY KEY,
    id_vendedor INT REFERENCES vendedor(id),
    id_produto INT REFERENCES produto(id),
    valor DECIMAL(10,2) NOT NULL,
    data_venda DATE
);

INSERT INTO vendedor (nome, data_nascimento, salario) VALUES
('Ana Silva', '1990-05-15', 1500.00),
('Carlos Nogueira', '1985-08-20', 1800.00),
('Renata Costa', '1995-03-10', 2000.00);

INSERT INTO produto (nome, preco) VALUES
('martelo', 25.50),
('chave de fenda', 15.00),
('alicate', 30.00);

INSERT INTO venda (id_vendedor, id_produto, valor, data_venda) VALUES
(1, 1, 500.00, '2026-01-10'),
(1, 2, 600.00, '2026-02-15'),
(2, 1, 25.50, '2026-03-01'),
(3, 3, 300.00, '2026-03-05');

-- Consultas da Questão 10:
SELECT * FROM vendedor;
SELECT * FROM vendedor ORDER BY nome ASC;
SELECT nome FROM vendedor WHERE nome ILIKE '%na%';
SELECT SUM(valor) AS total_vendas FROM venda;
SELECT id_vendedor, SUM(valor) FROM venda GROUP BY id_vendedor;
SELECT DISTINCT v.nome, v.data_nascimento FROM vendedor v JOIN venda ve ON v.id = ve.id_vendedor;
SELECT DISTINCT v.nome FROM vendedor v JOIN venda ve ON v.id = ve.id_vendedor JOIN produto p ON p.id = ve.id_produto WHERE p.nome ILIKE 'martelo';
SELECT COUNT(*) AS total_vendedores FROM vendedor;

UPDATE vendedor SET salario = salario + 100 
WHERE id IN (SELECT id_vendedor FROM venda GROUP BY id_vendedor HAVING SUM(valor) > 1000);

-- QUESTÃO 14 & 15: MÉDICOS E ALTURAS (SUBQUERIES COM IN)

CREATE TABLE Medico (
    id INT PRIMARY KEY,
    nome VARCHAR(50),
    altura DECIMAL(3,2)
);

INSERT INTO Medico (id, nome, altura) VALUES
(1, 'M1', 1.70),
(2, 'M2', 1.80),
(3, 'M3', 1.90),
(4, 'M4', 1.68);

-- Questão 14: Médico com maior altura
SELECT nome 
FROM Medico 
WHERE altura IN (SELECT MAX(altura) FROM Medico);

-- Questão 15: Inserir M5 e buscar médico com menor altura
INSERT INTO Medico (id, nome, altura) VALUES (5, 'M5', 1.68);

SELECT nome 
FROM Medico 
WHERE altura IN (SELECT MIN(altura) FROM Medico);

-- QUESTÃO 16 & 17: PACIENTES E CONSULTAS
CREATE TABLE Paciente (
    id INT PRIMARY KEY,
    nome VARCHAR(50)
);

INSERT INTO Paciente (id, nome) VALUES (1, 'P1'), (2, 'P2'), (3, 'P3');

CREATE TABLE Consulta (
    id INT PRIMARY KEY,
    idPaciente INT REFERENCES Paciente(id),
    idMedico INT REFERENCES Medico(id),
    data DATE
);

INSERT INTO Consulta (id, idPaciente, idMedico, data) VALUES
(1, 1, 1, '2016-10-10'),
(2, 2, 1, '2016-12-05'),
(3, 3, 2, '2017-02-03'),
(4, 1, 3, '2016-12-15');

-- Questão 16: Médicos com consultas em Dezembro de 2016
SELECT nome 
FROM Medico 
WHERE id IN (
    SELECT idMedico 
    FROM Consulta 
    WHERE data BETWEEN '2016-12-01' AND '2016-12-31'
);

-- Questão 17: Adicionar Idade e consultar pacientes > 21 com consulta
ALTER TABLE Paciente ADD COLUMN Idade INT;

UPDATE Paciente SET Idade = 10 WHERE id = 1;
UPDATE Paciente SET Idade = 22 WHERE id = 2;
UPDATE Paciente SET Idade = 38 WHERE id = 3;

SELECT nome 
FROM Paciente 
WHERE Idade > 21 
  AND id IN (SELECT idPaciente FROM Consulta);
  
-- QUESTÃO 18, 19 & 20: PREDICADOS ANY, ALL E EXISTS
-- Questão 18: Uso do predicado ANY

SELECT nome 
FROM Paciente 
WHERE Idade > ANY (SELECT Idade FROM Paciente);

-- Questão 19: Especialidades e uso do predicado ALL
CREATE TABLE Especialidade (
    Id INT PRIMARY KEY,
    nome VARCHAR(50)
);

INSERT INTO Especialidade (Id, nome) VALUES
(1, 'Cardiologia'), (2, 'Ortopedia'), (3, 'Pediatria');

ALTER TABLE Medico ADD COLUMN salario DECIMAL(10,2);
ALTER TABLE Medico ADD COLUMN idEspecialidade INT REFERENCES Especialidade(Id);

UPDATE Medico SET salario = 1000, idEspecialidade = 3 WHERE id = 1;
UPDATE Medico SET salario = 5000, idEspecialidade = 2 WHERE id = 2;
UPDATE Medico SET salario = 10000, idEspecialidade = 1 WHERE id = 3;
UPDATE Medico SET salario = 12000, idEspecialidade = 3 WHERE id = 4;
UPDATE Medico SET salario = 15000, idEspecialidade = 1 WHERE id = 5;

SELECT nome 
FROM Medico 
WHERE salario > ALL (
    SELECT salario 
    FROM Medico 
    WHERE idEspecialidade IN (
        SELECT Id FROM Especialidade WHERE nome ILIKE 'Pediatria'
    )
);

-- Questão 20: Inserir P4 e consultar com EXISTS e IN
INSERT INTO Paciente (id, nome, Idade) VALUES (4, 'P4', 44);

-- Questão 20 a) com EXISTS:
SELECT nome 
FROM Paciente p
WHERE EXISTS (SELECT 1 FROM Consulta c WHERE c.idPaciente = p.id);

-- Questão 20 b) com IN:
SELECT nome 
FROM Paciente 
WHERE id IN (SELECT idPaciente FROM Consulta);