from dotenv import load_dotenv
import os
import json
import mysql.connector

load_dotenv()

class BaseDeDados():
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
    def add_aluno(self, nome:str, email:str, password:str):
        try:
            sql = ("INSERT INTO Aluno (NomeAluno, EmailAluno, SenhaAluno) VALUES (%s, %s, %s)" % (nome, email, password))
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    # Atualiza um usuário no banco de dados.
    def update_aluno(self, nome:str, email:str, password:str):
        try:
                sql = ("UPDATE Aluno SET NomeAluno= %s, EmailAluno=%s, SenhaAluno=%s" % (nome, email, password))
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

    def get_all_questions_json(self) -> str:
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
    def delete_question(self, idPerguntas:int):
        try:
            sql = ("DELETE FROM Perguntas WHERE idPerguntas = '%s'" % (idPerguntas))
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

            

    
    