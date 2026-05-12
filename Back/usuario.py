import mysql.connector
from Conectar_Banco import conectar_banco 

conexao = conectar_banco()
cursor = conexao.cursor(dictionary=True, buffered=True)

class Usuario:
    

    def __init__(self, data):
        self.id = data['ID']
        self.nome = data['Nome']
        self.turma = data['Turma']
        self.pontos = data['Pontuacao']
    
  
    def verificar_logins(nome, turma):
        sql = "SELECT * FROM USUARIO WHERE Nome = %s AND Turma = %s"
        cursor.execute(sql, (nome,turma))
        return cursor.fetchone()
    

    def salvar_login(nome, turma):
        sql = "INSERT INTO Usuario (Nome,Turma,Pontuacao) VALUES (%s, %s, 0)"
        cursor.execute(sql, (nome,turma))
        conexao.commit()
        
    
  
    def login():
        nome = input("Nome Completo: ").strip()
        turma = input("Turma: ").strip().upper()
        
        logins = Usuario.verificar_logins(nome,turma)
        
        if logins:
            print(f"Login Realizado com sucesso! Bem vindo, {nome}!")
            return Usuario(logins)

        else:
            print("Usuário não encontrado.")
            return None
    
    
    def cadastrar():
        nome = input("Nome Completo: ").strip()
        turma = input("Turma: ").strip().upper()

        usuario_existente = Usuario.verificar_logins(nome, turma)

        if usuario_existente:
            print("Usuário já cadastrado")
            print(f"Login realizado com sucesso! Bem vindo {nome}")
            return Usuario(usuario_existente)
        
        Usuario.salvar_login(nome, turma)
        print(f"Usuário {nome} cadastrado com sucesso!")
        dados = Usuario.verificar_logins(nome,turma)
        return Usuario(dados)


if __name__ == "__main__":
    print("=== Sistema de Login ===")
    print("1 - Login")
    print("2 - Cadastrar")
    opcao = input("Escolha uma opção: ")



    if opcao == "1":
        usuario = Usuario.login()
    elif opcao == "2":
        usuario = Usuario.cadastrar()
    else:
        print("Opção inválida.")




