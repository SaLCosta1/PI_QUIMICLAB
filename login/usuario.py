class Usuario:
    
    def __init__(self, nome, turma):
        self.nome = nome
        self.turma = turma
    
  
    def ler_logins():
        try:
            with open("C:\Users\pedro\OneDrive - Instituto Mauá de Tecnologia\PI código\login", "r") as f:
                return f.readlines()
        except FileNotFoundError:
            return []
    

    def salvar_login(nome, turma):
        with open("C:\Users\pedro\OneDrive - Instituto Mauá de Tecnologia\PI código\login", "a") as f:
            f.write(f"{nome},{turma}\n")
    
  
    def login():
        nome = input("Nome Completo: ").strip()
        turma = input("Turma: ").strip()
        
        logins = Usuario.ler_logins()
        
        for linha in logins:
            dados = linha.strip().split(",")
            if dados[0] == nome and dados[1] == turma:
                print(f"Login realizado com sucesso! Bem-vindo, {nome}!")
                return Usuario(nome, turma)
        
        print("Usuário não encontrado.")
        return None
    
    
    def cadastrar():
        nome = input("Nome Completo: ").strip()
        turma = input("Turma: ").strip()
        
        Usuario.salvar_login(nome, turma)
        print(f"Usuário {nome} cadastrado com sucesso!")
        return Usuario(nome, turma)


# Exemplo de uso
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



ler_logins()