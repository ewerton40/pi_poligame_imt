from dotenv import load_dotenv
import os
import json
import mysql.connector

load_dotenv()

class Database():
    def __init__(self):
        self.host =os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")  
        self.port = os.getenv("PORT")

        # Tenta fazer a conexão com o banco de dados.
    def connect(self):
        try:
            self.conexao = mysql.connector.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                database = self.database,
                port = self.port,
            )
            print("Conexão bem sucedida!")
            self.cursor = self.conexao.cursor(buffered=True)
            return self.conexao
        except mysql.connector.Error as err:
            print(f"Falha na conexão! {err}")
            return None

        # Pega e retorna o usuário do banco de dados.
    def get_aluno(self, email:str, password:str):
        try:
            sql = ("SELECT idAluno, EmailAluno, SenhaAluno FROM Aluno WHERE EmailAluno='%s' AND SenhaAluno='%s'" % (email, password))
            self.cursor.execute(sql)
            self.conexao.commit()
            user = self.cursor.fetchone()
            return user
        except Exception as e:
            print(e)
            return None
            
    # Pega e retorna o email do usuário do banco de dados.
    def get_aluno_email(self, email:str):
        try:
            sql = ("SELECT Aluno.EmailAluno FROM Aluno WHERE Aluno.EmailAluno='%s'" % email)
            self.cursor.execute(sql)
            self.conexao.commit()
            email = self.cursor.fetchone()[0]
            return email
        except Exception as e:
            print(e)

        # Adiciona um usuário ao banco de dados.
    def add_aluno(self, email:str, password:str):
        try:
            sql = ("INSERT INTO Aluno ( EmailAluno, SenhaAluno) VALUES (%s, %s)" % (email, password))
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    # Atualiza um usuário no banco de dados.
    def update_aluno(self, email:str, password:str):
        try:
                sql = ("UPDATE Aluno SET EmailAluno=%s, SenhaAluno=%s" % (email, password))
                self.cursor.execute(sql)
                self.conexao.commit()
        except Exception as e:
            print(e)

    # Deleta um usuário do banco de dados.
    def delete_aluno(self, email:str):
        try:
            sql = ("DELETE FROM Aluno WHERE EmailAluno = '%s'" % email)
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    def get_all_questoes_json(self) -> str:
        try:
            """
                Create an sql query that returns all questions and their answers like this:
                {
                    "id": 0,
                    "question": "Qual dessas opções é um tópico que deve ser abordado no parágrafo introdutório de redação modelo ENEM?",
                    "answers": [
                    {
                        "id": 0,
                        "text": "Repertório de abertura",
                        "correct": true
                    },
                    {
                        "id": 1,
                        "text": "Tese",
                        "correct": false
                    },
                    {
                        "id": 2,
                        "text": "Conclusão do texto",
                        "correct": false
                    },
                    {
                        "id": 3,
                        "text": "Argumentação detalhada",
                        "correct": false
                    }
                    ]
                },
            """
            sql = ("""
                SELECT
                    p.idPerguntas AS question_id,
                    p.Enunciado AS question_text,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'answer_id', r.idRespostas,
                            'answer_text', r.TextoResposta,
                            'is_true', pr.Correta
                        )
                    ) AS answers
                FROM Perguntas p
                JOIN Pergunta_Resposta pr ON p.idPerguntas = pr.Perguntas_idPerguntas
                JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                GROUP BY p.idPerguntas
            """)

            self.cursor.execute(sql)
            questions = self.cursor.fetchall()
            self.conexao.commit()
            questions_json = []
            for question in questions:
                question_dict = {
                    "id": question[0],
                    "question": question[1],
                    "answers": []
                }
                answers = json.loads(question[2])
                for answer in answers:
                    answer_dict = {
                        "id": answer["answer_id"],
                        "text": answer["answer_text"],
                        "correct": answer["is_true"]
                    }
                    question_dict["answers"].append(answer_dict)
                questions_json.append(question_dict)

            return json.dumps(questions_json)
        except Exception as e:
            print(e)
            return "Error ao buscar perguntas!"
    
     # Adiciona uma questão ao banco de dados.
    def add_questao(self, Enunciado: str, DificuldadePergunta: str, idMateria: int, alter1: str, alter2: str, alter3: str, answer: str):
        try:
            self.cursor.execute("INSERT INTO Perguntas (Enunciado, DificuldadePergunta, Materia_idMateria) VALUES (%s, %s, %s)" % (Enunciado, DificuldadePergunta, idMateria))
            idPerguntas = self.cursor.lastrowid
             
            alternativas = [
                (alter1, False, idPerguntas),
                (alter2, False, idPerguntas),
                (alter3, False, idPerguntas),
                (answer, True, idPerguntas)
            ]
            for texto, correta in alternativas:
                self.cursor.executemany("INSERT INTO Respostas (TextoResposta) VALUES (%s)" % (texto))
                idResposta = self.cursor.lastrowid
                self.cursor.execute("INSERT INTO Pergunta_Resposta (Perguntas_idPerguntas, Respostas_idRespostas, Correta) VALUES (%s, %s, %s)", (idPerguntas, idResposta, correta))
            
            self.conexao.commit()
            print("Questão adicionada!")
        except Exception as e:
            print(e)


     # Deleta uma questão do banco de dados.
    def delete_questao(self, idPerguntas:int):
        try:
            sql = ("DELETE FROM Perguntas WHERE idPerguntas = '%s'" % (idPerguntas))
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    def get_all_questoes(self):
        try:
            sql = ("""
                SELECT 
                    p.idPerguntas AS pergunta_id,
                    p.Enunciado AS pergunta,
                    (
                        SELECT TextoResposta
                        FROM Pergunta_Resposta pr 
                        JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                        WHERE pr.Perguntas_idPerguntas = p.idPerguntas AND pr.Correta = FALSE
                        LIMIT 1 OFFSET 0
                    ) AS alternativa1,
                    (
                        SELECT TextoResposta 
                        FROM Pergunta_Resposta pr 
                        JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                        WHERE pr.Perguntas_idPerguntas = p.idPerguntas AND pr.Correta = FALSE
                        LIMIT 1 OFFSET 1
                    ) AS alternativa2,
                    (
                        SELECT TextoResposta 
                        FROM Pergunta_Resposta pr 
                        JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                        WHERE pr.Perguntas_idPerguntas = p.idPerguntas AND pr.Correta = FALSE
                        LIMIT 1 OFFSET 2
                    ) AS alternativa3,
                    (
                        SELECT TextoResposta 
                        FROM Pergunta_Resposta pr 
                        JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                        WHERE pr.Perguntas_idPerguntas = p.idPerguntas AND pr.Correta = TRUE
                        LIMIT 1
                    ) AS resposta_correta
                FROM Perguntas p
            """)
            self.cursor.execute(sql)
            questions = self.cursor.fetchall()
            self.conexao.commit()
            return questions
        except Exception as e:
            print("Erro ao buscar perguntas:", e)

        
    def login_usuario(self, email: str, senha: str):
        try:
            # Verifica se é um aluno
            sql_aluno = ("SELECT idAluno FROM Aluno WHERE EmailAluno=%s AND SenhaAluno=%s")
            self.cursor.execute(sql_aluno, (email, senha))
            aluno = self.cursor.fetchone()
            if aluno:
                return {"tipo": "Aluno", "id": aluno[0]}
            
            # Verifica se é um professor
            sql_professor = ("SELECT idProfessor FROM Professor WHERE EmailProfessor=%s AND SenhaProfessor=%s")
            self.cursor.execute(sql_professor, (email, senha))
            professor = self.cursor.fetchone()
            if professor:
                return {"tipo": "Professor", "id": professor[0]}
            
            return None
        except Exception as e:
            print("Erro ao tentar login:", e)
            return None 
        
    def get_questao_materia(self) -> str:
        try:
            sql = """
                SELECT 
                    m.idMateria AS materia_id,
                    m.NomeMateria AS materia_nome,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'idPergunta', p.idPerguntas,
                            'enunciado', p.Enunciado,
                            'dificuldade', p.DificuldadePergunta
                        )
                    ) AS perguntas
                FROM Materia m
                LEFT JOIN Perguntas p ON p.Materia_idMateria = m.idMateria
                GROUP BY m.idMateria
                ORDER BY m.NomeMateria;
            """
            self.cursor.execute(sql)
            materias = self.cursor.fetchall()
            self.conexao.commit()

            materias_json = []
            for materia in materias:
                perguntas = json.loads(materia[2]) if materia[2] else []
                materias_json.append({
                    "idMateria": materia[0],
                    "nomeMateria": materia[1],
                    "perguntas": perguntas
                })
            return json.dumps(materias_json)

        except Exception as e:
            print("Erro ao buscar matéria com perguntas:", e)
            return "Erro ao buscar matéria com perguntas"
        


    def get_questoes_por_materia_json(self, id_materia: int) -> str:
        try:
            sql = ("""
                SELECT
                    p.idPerguntas AS question_id,
                    p.Enunciado AS question_text,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'answer_id', r.idRespostas,
                            'answer_text', r.TextoResposta,
                            'is_true', pr.Correta
                        )
                    ) AS answers
                FROM Perguntas p
                JOIN Pergunta_Resposta pr ON p.idPerguntas = pr.Perguntas_idPerguntas
                JOIN Respostas r ON pr.Respostas_idRespostas = r.idRespostas
                WHERE p.Materia_idMateria = %s
                GROUP BY p.idPerguntas
            """)

            self.cursor.execute(sql, (id_materia,))
            perguntas = self.cursor.fetchall()
            self.conexao.commit()

            questoes_json = []
            for pergunta in perguntas:
                pergunta_dict = {
                    "id": pergunta[0],
                    "question": pergunta[1],
                    "answers": []
                }
                answers = json.loads(pergunta[2])
                for answer in answers:
                    answer_dict = {
                        "id": answer["answer_id"],
                        "text": answer["answer_text"],
                        "correct": answer["is_true"]
                    }
                    pergunta_dict["answers"].append(answer_dict)
                questoes_json.append(pergunta_dict)

            return json.dumps(questoes_json)
        except Exception as e:
            print("Erro ao buscar questões por matéria:", e)
            return "Erro"
        

    def criar_dica_para_partida(self, id_partida):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "INSERT INTO Dica (IdPartida, MeioaMeio, PularDica) VALUES (%s, FALSE, FALSE)",
                (id_partida,)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print("Erro ao criar dica para a partida:", e)
            return False

    def get_dica_por_partida(self, id_partida):
        sql = "SELECT MeioaMeio, PularDica FROM Dica WHERE Partida_idPartida = %s"
        self.cursor.execute(sql, (id_partida,))
        resultado = self.cursor.fetchone()
        if resultado:
            return {
                "MeioaMeio": False,
                "PularDica": True
            }
        return None

    def usar_meio_a_meio(self, id_partida):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE Dica SET MeioaMeio = TRUE WHERE IdPartida = %s", (id_partida,)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print("Erro ao marcar meio a meio como usado:", e)
            return False

    def usar_pular_dica(self, id_partida):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE Dica SET PularDica = TRUE WHERE IdPartida = %s", (id_partida,)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print("Erro ao marcar pular dica como usado:", e)
            return False
        
    def criar_partida(self, id_aluno: int, id_materia: int):
        try:
            sql = "INSERT INTO Partida (PontuacaoPartida, Materia_idMateria, Aluno_idAluno) VALUES (0, %s, %s)"
            self.cursor.execute(sql, (id_materia, id_aluno))
            self.conexao.commit()
            return self.cursor.lastrowid  # <- Aqui retorna o id gerado
        except Exception as e:
            print("Erro ao criar partida:", e)
            return None
    


    def add_pontuacao_real(self, id_partida, acertos):
        try:
            print(f"Salvando pontuação: {acertos} para a partida {id_partida}")
            cursor = self.conexao.cursor()
            cursor.execute("UPDATE Partida SET PontuacaoPartida = %s WHERE idPartida = %s", (acertos, id_partida))
            self.conexao.commit()
        except Exception as e:
            print(f"Erro ao salvar pontuação real: {e}")