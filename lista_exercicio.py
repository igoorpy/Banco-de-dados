import psycopg2

DB_PARAMS = {
    "dbname": "meubanco",
    "user": "admin",
    "password": "adminpassword",
    "host": "localhost",
    "port": "5432",
}


def executar_exercicios():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        print("conexao ok")

        # questao 5: cria tabelas aluno, curso e relacao
        cursor.execute(
            """
            DROP TABLE IF EXISTS Relacao1, Aluno, Curso CASCADE;
            CREATE TABLE Aluno (
                id_aluno SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL
            );
            CREATE TABLE Curso (
                id_curso SERIAL PRIMARY KEY,
                nome_curso VARCHAR(100) NOT NULL
            );
            CREATE TABLE Relacao1 (
                id_aluno INT REFERENCES Aluno(id_aluno) ON DELETE CASCADE,
                id_curso INT REFERENCES Curso(id_curso) ON DELETE CASCADE,
                PRIMARY KEY (id_aluno, id_curso)
            );
        """
        )

        # questao 10: cria tabelas de vendas e roda consultas
        cursor.execute(
            """
            DROP TABLE IF EXISTS venda, produto, vendedor CASCADE;
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
        """
        )

        cursor.execute("SELECT * FROM vendedor;")
        print("questao 10 a:", cursor.fetchall())

        cursor.execute("SELECT * FROM vendedor ORDER BY nome ASC;")
        print("questao 10 b:", cursor.fetchall())

        cursor.execute("SELECT nome FROM vendedor WHERE nome ILIKE '%na%';")
        print("questao 10 c:", cursor.fetchall())

        cursor.execute("SELECT SUM(valor) FROM venda;")
        print("questao 10 d:", cursor.fetchall()[0][0])

        cursor.execute(
            "SELECT id_vendedor, SUM(valor) FROM venda GROUP BY id_vendedor;"
        )
        print("questao 10 e:", cursor.fetchall())

        cursor.execute(
            "SELECT DISTINCT v.nome, v.data_nascimento FROM vendedor v JOIN venda ve ON v.id = ve.id_vendedor;"
        )
        print("questao 10 f:", cursor.fetchall())

        cursor.execute(
            """
            SELECT DISTINCT v.nome FROM vendedor v
            JOIN venda ve ON v.id = ve.id_vendedor
            JOIN produto p ON p.id = ve.id_produto
            WHERE p.nome ILIKE 'martelo';
        """
        )
        print("questao 10 g:", cursor.fetchall())

        cursor.execute("SELECT COUNT(*) FROM vendedor;")
        print("questao 10 h:", cursor.fetchall()[0][0])

        cursor.execute(
            """
            UPDATE vendedor SET salario = salario + 100 
            WHERE id IN (SELECT id_vendedor FROM venda GROUP BY id_vendedor HAVING SUM(valor) > 1000);
        """
        )
        conn.commit()

        # questao 14 e 15: cria tabela medico e faz buscas de altura
        cursor.execute(
            """
            DROP TABLE IF EXISTS Medico CASCADE;
            CREATE TABLE Medico (
                id INT PRIMARY KEY,
                nome VARCHAR(50),
                altura DECIMAL(3,2)
            );
            INSERT INTO Medico (id, nome, altura) VALUES
            (1, 'M1', 1.70), (2, 'M2', 1.80), (3, 'M3', 1.90), (4, 'M4', 1.68);
        """
        )

        cursor.execute(
            "SELECT nome FROM Medico WHERE altura IN (SELECT MAX(altura) FROM Medico);"
        )
        print("questao 14:", cursor.fetchall())

        cursor.execute(
            "INSERT INTO Medico (id, nome, altura) VALUES (5, 'M5', 1.68);"
        )
        cursor.execute(
            "SELECT nome FROM Medico WHERE altura IN (SELECT MIN(altura) FROM Medico);"
        )
        print("questao 15:", cursor.fetchall())

        # questao 16, 17, 18 e 20: cria tabelas paciente e consulta e faz buscas
        cursor.execute(
            """
            DROP TABLE IF EXISTS Consulta, Paciente CASCADE;
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
        """
        )

        cursor.execute(
            """
            SELECT nome FROM Medico 
            WHERE id IN (SELECT idMedico FROM Consulta WHERE data BETWEEN '2016-12-01' AND '2016-12-31');
        """
        )
        print("questao 16:", cursor.fetchall())

        cursor.execute(
            """
            ALTER TABLE Paciente ADD COLUMN Idade INT;
            UPDATE Paciente SET Idade = 10 WHERE id = 1;
            UPDATE Paciente SET Idade = 22 WHERE id = 2;
            UPDATE Paciente SET Idade = 38 WHERE id = 3;
        """
        )
        cursor.execute(
            """
            SELECT nome FROM Paciente 
            WHERE Idade > 21 AND id IN (SELECT idPaciente FROM Consulta);
        """
        )
        print("questao 17:", cursor.fetchall())

        cursor.execute(
            "SELECT nome FROM Paciente WHERE Idade > ANY (SELECT Idade FROM Paciente);"
        )
        print("questao 18:", cursor.fetchall())

        cursor.execute(
            "INSERT INTO Paciente (id, nome, Idade) VALUES (4, 'P4', 44);"
        )

        cursor.execute(
            "SELECT nome FROM Paciente p WHERE EXISTS (SELECT 1 FROM Consulta c WHERE c.idPaciente = p.id);"
        )
        print("questao 20 a:", cursor.fetchall())

        cursor.execute(
            "SELECT nome FROM Paciente WHERE id IN (SELECT idPaciente FROM Consulta);"
        )
        print("questao 20 b:", cursor.fetchall())

        # questao 19: cria tabela especialidade e faz busca com all
        cursor.execute(
            """
            DROP TABLE IF EXISTS Especialidade CASCADE;
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
        """
        )

        cursor.execute(
            """
            SELECT nome FROM Medico 
            WHERE salario > ALL (
                SELECT salario FROM Medico 
                WHERE idEspecialidade IN (SELECT Id FROM Especialidade WHERE nome ILIKE 'Pediatria')
            );
        """
        )
        print("questao 19:", cursor.fetchall())

        conn.commit()
        cursor.close()
        conn.close()
        print("fim")

    except Exception as e:
        print(f"erro: {e}")


if __name__ == "__main__":
    executar_exercicios()