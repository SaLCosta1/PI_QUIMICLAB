import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SenhaPI@1234",
        database="quimic_lab",
        charset="utf8mb4",
        use_unicode=True,
    )
