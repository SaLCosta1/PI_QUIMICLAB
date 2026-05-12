import mysql.connector
from mysql.connector import Error
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password = "SenhaPI@1234",
            database = "projeto"
        )

        if conexao.is_connected():
            print("Conexão realizada com suceso.")
            return conexao
    except Error as e:
        print("Erro ao conectar com o Banco de Dados: ",e)
        return None
    
