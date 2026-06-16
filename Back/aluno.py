from Back.Conectar_Banco import conectar_banco

# Não abrir conexão ao importar o módulo — cria uma conexão por operação.
senha_padrao = 'senha1234+'

def _get_conn_cursor():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True, buffered=True)
    return conexao, cursor

def email_valido(email):
    email = email.strip().lower()
    return email.endswith('@aluno.cps.sp.gov.br')

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nome = data['nome']
        self.email = data['email']
        self.tipo = data['tipo']
        self.turma = data['turma']

    @staticmethod
    def buscar(email, senha):
        conexao, cursor = _get_conn_cursor()
        try:
            cursor.execute(
                "SELECT * FROM usuario WHERE email = %s AND senha_hash = %s AND tipo = 'aluno'",
                (email, senha)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"[aluno.buscar] Erro ao buscar usuário: {e}")
            return None
        finally:
            cursor.close()
            conexao.close()

    @staticmethod
    def login(email, senha):
        try:
            if not email_valido(email):
                return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.sp.gov.br"
            dados = Usuario.buscar(email, senha)
            if not dados:
                return None, "E-mail ou senha incorretos."
            return Usuario(dados), None
        except Exception as e:
            print(f"[aluno.login] Erro ao fazer login: {e}")
            return None, f"Erro ao fazer login: {str(e)}"

    @staticmethod
    def cadastrar(nome, email, turma, senha=None):
        try:
            if not email_valido(email):
                return None, "E-mail inválido. Use nome.sobrenome@aluno.cps.sp.gov.br"

            senha_a_usar = senha if senha else senha_padrao

            conexao, cursor = _get_conn_cursor()
            try:
                cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (email,))
                if cursor.fetchone():
                    return None, "E-mail já cadastrado."
                cursor.execute(
                    "INSERT INTO usuario (nome, email, senha_hash, tipo, turma) VALUES (%s, %s, %s, 'aluno', %s)",
                    (nome, email, senha_a_usar, turma)
                )
                conexao.commit()

                cursor.execute("SELECT * FROM usuario WHERE email = %s AND senha_hash = %s", (email, senha_a_usar))
                dados = cursor.fetchone()
                if not dados:
                    return None, "Erro ao criar usuário."
                return Usuario(dados), None
            finally:
                cursor.close()
                conexao.close()
        except Exception as e:
            print(f"[aluno.cadastrar] Erro ao cadastrar usuário: {e}")
            return None, f"Erro ao cadastrar: {str(e)}"

    @staticmethod
    def atualizar_senha(email, nova_senha):
        try:
            email = email.strip().lower()
            if not email_valido(email):
                return False, "E-mail inválido. Use nome.sobrenome@aluno.cps.sp.gov.br"
            if not nova_senha:
                return False, "Informe a nova senha."

            conexao, cursor = _get_conn_cursor()
            try:
                cursor.execute(
                    "UPDATE usuario SET senha_hash = %s WHERE email = %s AND tipo = 'aluno'",
                    (nova_senha, email),
                )
                conexao.commit()
                if cursor.rowcount == 0:
                    return False, "Nenhum aluno encontrado com esse e-mail."
                return True, None
            finally:
                cursor.close()
                conexao.close()
        except Exception as e:
            print(f"[aluno.atualizar_senha] Erro ao atualizar senha: {e}")
            return False, f"Erro ao atualizar senha: {str(e)}"

    @staticmethod
    def menu():
        opcao = input("1 - Login\n2 - Cadastrar\nOpção: ").strip()

        if opcao == "1":
            email = input("E-mail: ").strip()
            senha = input("Senha: ").strip()
            res = Usuario.login(email, senha)
            try:
                user, status = res
            except Exception:
                print('Erro.')
                return None
            if user:
                return user
            else:
                print(status)
                return None

        elif opcao == "2":
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            turma = input("Turma: ").strip()
            res = Usuario.cadastrar(nome, email, turma)
            try:
                user, status = res
            except Exception:
                if res:
                    print(res)
                    return None
                else:
                    print('Erro.')
                    return None
            if user:
                return user
            else:
                print(status)
                return None