<<<<<<< HEAD
import mysql.connector
from mysql.connector import Error
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password = "tinCTrom",
            database = "jogoetec"
        )

        if conexao.is_connected():
            print("Conexão realizada com suceso.")
            return conexao
    except Error as e:
        print("Erro ao conectar com o Banco de Dados: ",e)
        return None
    
=======
import mysql.connector
from mysql.connector import Error
def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password = "tinCTrom",
            database = "jogoetec"
        )

        if conexao.is_connected():
            print("Conexão realizada com suceso.")
            return conexao
    except Error as e:
        print("Erro ao conectar com o Banco de Dados: ",e)
        return None
    
>>>>>>> 66ba91564e7fb655c9df26d46278a64f1a976b55
