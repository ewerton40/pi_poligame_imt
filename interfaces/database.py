from dotenv import load_dotenv
import os
import json
import mysql.connector

load_dotenv()

class Database():
    def __init__(self):
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")  
        self.port = os.getenv("PORT")
        self.conexao = None  # Initialize conexao and cursor
        self.cursor = None

    # Tenta fazer a conexão com o banco de dados.
    def connect(self):
        try:
            if self.conexao is None or not self.conexao.is_connected():
                self.conexao = mysql.connector.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    database=self.database,
                    port=self.port,
                )
                self.cursor = self.conexao.cursor(buffered=True)
                print("Conexão bem sucedida!")
            return self.conexao
        except mysql.connector.Error as err:
            print(f"Falha na conexão! {err}")
            self.conexao = None
            self.cursor = None
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()
            self.conexao = None
            print("Conexão com o banco de dados fechada.")

    # Pega e retorna o usuário do banco de dados.
    def get_aluno(self, email: str, password: str):
        try:
            # Ensure connection is active
            self.connect() 
            sql = ("SELECT idAluno, EmailAluno, SenhaAluno FROM Aluno WHERE EmailAluno=%s AND SenhaAluno=%s")
            self.cursor.execute(sql, (email, password)) # Use parameterized query
            # self.conexao.commit() # No need to commit for SELECT statements
            user = self.cursor.fetchone()
            return user
        except Exception as e:
            print(e)
            return None
        # You might want to close connection here or manage it externally if this is a short-lived query

    # Pega e retorna o email do usuário do banco de dados.
    def get_aluno_email(self, email: str):
        try:
            self.connect()
            sql = ("SELECT Aluno.EmailAluno FROM Aluno WHERE Aluno.EmailAluno=%s")
            self.cursor.execute(sql, (email,)) # Use parameterized query
            # self.conexao.commit()
            email = self.cursor.fetchone()[0]
            return email
        except Exception as e:
            print(e)
            return None
        # You might want to close connection here or manage it externally if this is a short-lived query

    # Adiciona um usuário ao banco de dados.
    def add_aluno(self, nome: str, email: str, password: str) -> bool:
        try:
            self.connect()
            sql = "INSERT INTO Aluno (NomeAluno, EmailAluno, SenhaAluno) VALUES (%s, %s,%s)"
            self.cursor.execute(sql, (nome,email, password))
            self.conexao.commit()
            print("Aluno adicionado com sucesso ao banco.")
            return True
        except Exception as e:
            print(f"Erro ao adicionar aluno: {e}")
            return False
        # You might want to close connection here or manage it externally

    def add_professor(self, nome: str, email: str, password: str) -> bool:
        try:
            self.connect()
            sql = "INSERT INTO Professor (NomeProfessor, EmailProfessor, SenhaProfessor) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (nome, email, password))
            self.conexao.commit()

            print("Professor adicionado com sucesso ao banco.")
            return True
        except Exception as e:
            print(f"Erro ao adicionar professor: {e}")
            return False


    # Atualiza um usuário no banco de dados.
    def update_aluno(self, email: str, password: str, old_email: str): # Added old_email to identify the record
        try:
            self.connect()
            sql = "UPDATE Aluno SET EmailAluno=%s, SenhaAluno=%s WHERE EmailAluno=%s"
            self.cursor.execute(sql, (email, password, old_email)) # Parameterized query
            self.conexao.commit()
        except Exception as e:
            print(e)
        # You might want to close connection here or manage it externally

    # Deleta um usuário do banco de dados.
    def delete_aluno(self, email: str):
        try:
            self.connect()
            sql = ("DELETE FROM Aluno WHERE EmailAluno = %s")
            self.cursor.execute(sql, (email,)) # Parameterized query
            self.conexao.commit()
        except Exception as e:
            print(e)
        # You might want to close connection here or manage it externally

    def get_all_questoes_json(self) -> str:
        try:
            self.connect()
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
            # self.conexao.commit() # No need to commit for SELECT
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
        # You might want to close connection here or manage it externally

    # Adiciona uma questão ao banco de dados.
    def add_questao(self, Enunciado: str, DificuldadePergunta: str, idMateria: int, alter1: str, alter2: str, alter3: str, answer: str):
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO Perguntas (Enunciado, DificuldadePergunta, Materia_idMateria) VALUES (%s, %s, %s)",
                (Enunciado, DificuldadePergunta, idMateria)
            )
            idPerguntas = self.cursor.lastrowid

            alternativas = [
                (alter1, False),
                (alter2, False),
                (alter3, False),
                (answer, True)
            ]

            for texto, correta in alternativas:
                self.cursor.execute("INSERT INTO Respostas (TextoResposta) VALUES (%s)", (texto,))
                idResposta = self.cursor.lastrowid
                self.cursor.execute(
                    "INSERT INTO Pergunta_Resposta (Perguntas_idPerguntas, Respostas_idRespostas, Correta) VALUES (%s, %s, %s)",
                    (idPerguntas, idResposta, correta)
                )

            self.conexao.commit()
            print("Questão adicionada!")
        except Exception as e:
            print("Erro ao adicionar questão no banco:", e)
        # You might want to close connection here or manage it externally

    # Deleta uma questão do banco de dados.
    
    def delete_questao(self, idPerguntas: int):
        """
        Deleta uma questão do banco de dados, incluindo suas associações e respostas.
        """
        try:
            self.connect()

            # 1. Obter os idRespostas associados a esta pergunta
            sql_select_respostas = "SELECT Respostas_idRespostas FROM Pergunta_Resposta WHERE Perguntas_idPerguntas = %s"
            self.cursor.execute(sql_select_respostas, (idPerguntas,))
            respostas_ids = [row[0] for row in self.cursor.fetchall()]

            # 2. Deletar registros da tabela Pergunta_Resposta
            sql_delete_pr = "DELETE FROM Pergunta_Resposta WHERE Perguntas_idPerguntas = %s"
            self.cursor.execute(sql_delete_pr, (idPerguntas,))

            # 3. Deletar as respostas da tabela Respostas
            if respostas_ids: # Garante que há IDs para deletar
                # Cria uma string com placeholders para a cláusula IN
                placeholders = ','.join(['%s'] * len(respostas_ids))
                sql_delete_respostas = f"DELETE FROM Respostas WHERE idRespostas IN ({placeholders})"
                self.cursor.execute(sql_delete_respostas, tuple(respostas_ids))

            # 4. Deletar a questão da tabela Perguntas
            sql_delete_q = "DELETE FROM Perguntas WHERE idPerguntas = %s"
            self.cursor.execute(sql_delete_q, (idPerguntas,))
            
            self.conexao.commit()
            print(f"Questão {idPerguntas} e suas respostas associadas deletadas com sucesso!")
        except Exception as e:
            print(f"Erro ao deletar questão e respostas: {e}")

    def get_all_questoes(self):
        try:
            self.connect()
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
            # self.conexao.commit() # No need to commit for SELECT
            return questions
        except Exception as e:
            print("Erro ao buscar perguntas:", e)
            return []
        # You might want to close connection here or manage it externally

    def login_usuario(self, email: str, senha: str):
        try:
            self.connect()
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
        # You might want to close connection here or manage it externally

    def get_questao_materia(self) -> str:
        try:
            self.connect()
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
            # self.conexao.commit() # No need to commit for SELECT

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
        # You might want to close connection here or manage it externally
        
    def get_questoes_por_materia(self, idMateria: int) -> str:
        try:
            self.connect()
            sql = """
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
            """
            self.cursor.execute(sql, (idMateria,))
            questions = self.cursor.fetchall()
            
            questions_json = []
            for question in questions:
                answers = json.loads(question[2]) if question[2] else []
                questions_json.append({
                    "id": question[0],
                    "question": question[1],
                    "answers": answers
                })
            return json.dumps(questions_json)

        except Exception as e:
            print("Erro ao buscar questões por matéria:", e)
            return "Error ao buscar questões por matéria!"
        # You might want to close connection here or manage it externally

    def get_questoes_por_materia_json(self, id_materia: int) -> str:
        try:
            self.connect()
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
            # self.conexao.commit() # No need to commit for SELECT

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
        # You might want to close connection here or manage it externally

    def get_rank_partidas(self): # <--- Adicione 'self' aqui para torná-la um método de instância
        """
        Busca o e-mail do aluno, a pontuação da partida e o nome da matéria do banco de dados.
        Retorna uma lista de tuplas (EmailAluno, PontuacaoPartida, NomeMateria).
        """
        self.connect() # Garante que a conexão está ativa
        try:
            sql = """
                SELECT
                    A.EmailAluno,
                    A.NomeAluno,
                    P.PontuacaoPartida,
                    M.NomeMateria
                FROM Aluno AS A
                JOIN Partida AS P ON A.idAluno = P.Aluno_idAluno
                JOIN Materia AS M ON P.Materia_idMateria = M.idMateria
                ORDER BY P.PontuacaoPartida DESC;
            """
            self.cursor.execute(sql) # Usa o cursor da instância da classe
            resultados = self.cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"Falha na consulta ao banco de dados: {err}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao buscar ranking: {e}")
            return []
        finally:
            # Para métodos de busca que podem ser chamados várias vezes,
            # é melhor deixar o fechamento da conexão para o chamador da classe Database.
            # No entanto, se esta é uma operação isolada, você pode fechá-la aqui.
            # Se for uma operação isolada, é ideal ter um `with` statement ou um método de close explícito.
            # Por simplicidade para este método, vou omitir o close aqui, 
            # assumindo que a instância de Database será fechada externamente
            # quando não for mais necessária (por exemplo, no final do programa).
            pass

    def get_all_questions_details(self):
        """
        Retorna todas as perguntas com Enunciado, Materia_idMateria e DificuldadePergunta.
        Retorna uma lista de dicionários, cada um representando uma pergunta.
        """
        try:
            self.connect()
            sql = """
                SELECT 
                    idPerguntas, 
                    Enunciado, 
                    DificuldadePergunta, 
                    Materia_idMateria
                FROM Perguntas;
            """
            self.cursor.execute(sql)
            questions_raw = self.cursor.fetchall()
            
            questions_list = []
            for q_id, enunciado, dificuldade, id_materia in questions_raw:
                questions_list.append({
                    "id": q_id,
                    "enunciado": enunciado,
                    "dificuldade": dificuldade,
                    "materia_id": id_materia
                })
            return questions_list
        except Exception as e:
            print(f"Erro ao buscar detalhes das perguntas: {e}")
            return []
        
    def get_questions_by_materia(self, materia_id):
        try:
            self.connect()
            sql = """
                SELECT 
                    idPerguntas, 
                    Enunciado, 
                    DificuldadePergunta, 
                    Materia_idMateria
                FROM Perguntas
                WHERE Materia_idMateria = %s;
            """
            self.cursor.execute(sql, (materia_id,))
            questions_raw = self.cursor.fetchall()
            
            questions_list = []
            for q_id, enunciado, dificuldade, id_materia in questions_raw:
                questions_list.append({
                    "id": q_id,
                    "enunciado": enunciado,
                    "dificuldade": dificuldade,
                    "materia_id": id_materia
                })
            return questions_list
        except Exception as e:
            print(f"Erro ao buscar perguntas por matéria: {e}")
            return []
    def get_materias(self):
        try:
            self.connect()
            sql = "SELECT idMateria, NomeMateria FROM Materia;"
            self.cursor.execute(sql)
            resultados = self.cursor.fetchall()
            return [{"id": row[0], "nome": row[1]} for row in resultados]
        except Exception as e:
            print(f"Erro ao buscar matérias: {e}")
            return []
