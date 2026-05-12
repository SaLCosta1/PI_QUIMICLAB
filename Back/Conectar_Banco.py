import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SenhaPI@1234",
            database="quimic_lab"
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print("Erro ao conectar:", e)
        return None
