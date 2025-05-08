import mysql.connector
import pymysql



class Conexao:
    def __init__(self, banco, usr, senha, host, port):
        self.banco = banco
        self.usr= usr
        self.senha= senha
        self.host= host
        self.port= port

    def abrirConexao(self):

        try:
            self.conexao = pymysql.connect(
                host=self.host,
                user=self.usr,
                password=self.senha,
                database=self.banco,
                port=self.port
            )

            self.cursor = self.conexao.cursor()
        except Exception as erro:
            print("Erro ao abrir conexão", erro)

    def executar(self, sql):
        try:
            self.cursor.execute(sql)
            self.conexao.commit()
        except Exception as erro:
            print("Erro ao executar", erro)

    def retornar(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Exception as erro:
            print("Erro ao executar", erro)