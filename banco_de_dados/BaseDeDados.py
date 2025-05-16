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

     # Pega e retorna todos os usuários do banco de dados.
    def get_all_users(self):
        try:
            sql = ("SELECT Aluno.EmailAluno, role_name FROM tb_role INNER JOIN tb_user ON tb_user.role_id = tb_role.role_id WHERE role_name != 'Admin'")
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
            self.conexao.commit()
            return users
        except Exception as e:
            print(e)

        # Adiciona um usuário ao banco de dados.
    def add_user(self, email:str, password:str, role:str):
        try:
            sql = ("INSERT INTO tb_user (user_email, user_password, role_id) SELECT '%s', '%s', role_id FROM tb_role WHERE tb_role.role_name = '%s'" % (email, password, role))
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    # Atualiza um usuário no banco de dados.
    def update_user(self, email:str, password:str, role:str):
        try:
            if (email and password and role):
                sql = ("UPDATE tb_user JOIN tb_role ON tb_role.role_name = '%s' SET tb_user.user_email = '%s', tb_user.user_password = '%s', tb_user.role_id = tb_role.role_id WHERE tb_user.user_email = '%s'" % (role, email, password, email))
                self.cursor.execute(sql)
                self.conexao.commit()
            elif (email and role):
                sql = ("UPDATE tb_user JOIN tb_role ON tb_role.role_name = '%s' SET tb_user.user_email = '%s', tb_user.role_id = tb_role.role_id WHERE tb_user.user_email = '%s'" % (role, email, email))
                self.cursor.execute(sql)
                self.conexao.commit()
        except Exception as e:
            print(e)

    # Deleta um usuário do banco de dados.
    def delete_user(self, email:str):
        try:
            sql = ("DELETE FROM tb_user WHERE user_email = '%s'" % email)
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as e:
            print(e)

    
    