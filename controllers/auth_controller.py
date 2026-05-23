# =========================================================
# auth_controller.py
# Controla:
# - Login aluno
# - Login professor
# - Cadastro
# - Autenticação
# =========================================================

from PySide6.QtWidgets import (
    QMessageBox,
    QLineEdit,
)

# =========================================================
# DADOS MOCKADOS
# =========================================================

usuarios = [

    {
        "nome": "João Silva",
        "email": "joao.silva@aluno.cps.gov.br",
        "senha": "senha1234+",
        "tipo": "aluno",
    },

    {
        "nome": "Maria Souza",
        "email": "maria.souza@prof.cps.gov.br",
        "senha": "prof1234",
        "tipo": "professor",
    },
]


# =========================================================
# AUTH CONTROLLER
# =========================================================

class AuthController:

    def __init__(self, main):

        self.main = main
        self.window = main.window

        self.setup()

    # =====================================================
    # SETUP
    # =====================================================

    def setup(self):

        w = self.window

        # =================================================
        # LOGIN ALUNO
        # =================================================

        w.input_loginaluno.setEchoMode(QLineEdit.Normal)

        w.input_senhaaluno.setEchoMode(QLineEdit.Password)

        w.btn_voltarperfil2.clicked.connect(
            lambda: self.main.ir_para(w.pg_perfil)
        )

        w.btn_entraraluno.clicked.connect(
            self.login_aluno
        )

        w.input_senhaaluno.returnPressed.connect(
            self.login_aluno
        )

        w.btn_cadastroaluno.clicked.connect(
            self.msg_cadastro_aluno
        )

        # =================================================
        # LOGIN PROFESSOR
        # =================================================

        w.input_loginprof.setEchoMode(QLineEdit.Normal)

        w.input_senhaprof.setEchoMode(QLineEdit.Password)

        w.btn_voltarperfil3.clicked.connect(
            lambda: self.main.ir_para(w.pg_perfil)
        )

        w.btn_entrarprof.clicked.connect(
            self.login_professor
        )

        w.input_senhaprof.returnPressed.connect(
            self.login_professor
        )

        w.btn_cadastroprof.clicked.connect(
            lambda: self.main.ir_para(w.pg_cadastroprof)
        )

        # =================================================
        # CADASTRO
        # =================================================

        w.input_loginprof_2.setEchoMode(QLineEdit.Normal)

        w.input_senhaprof_2.setEchoMode(QLineEdit.Password)

        w.btn_voltarperfil3_2.clicked.connect(
            lambda: self.main.ir_para(w.pg_loginprof)
        )

        w.btn_entrarprof_2.clicked.connect(
            self.cadastrar_usuario
        )

    # =====================================================
    # VERIFICAR USUÁRIO
    # =====================================================

    def verificar_usuario(self, email, senha, tipo):

        for usuario in usuarios:

            if (
                usuario["email"] == email
                and usuario["senha"] == senha
                and usuario["tipo"] == tipo
            ):
                return usuario

        return None

    # =====================================================
    # LOGIN ALUNO
    # =====================================================

    def login_aluno(self):

        w = self.window

        email = w.input_loginaluno.text().strip()
        senha = w.input_senhaaluno.text().strip()

        if not email or not senha:

            QMessageBox.warning(
                w,
                "Atenção",
                "Preencha o e-mail e a senha."
            )

            return

        usuario = self.verificar_usuario(
            email,
            senha,
            "aluno"
        )

        if usuario:

            self.main.usuario_logado = usuario

            QMessageBox.information(
                w,
                "Bem-vindo",
                f"Olá, {usuario['nome']}!"
            )

            w.input_senhaaluno.clear()

            self.main.ir_para(w.pg_modos)

        else:

            QMessageBox.warning(
                w,
                "Erro de autenticação",
                "E-mail ou senha incorretos."
            )

            w.input_senhaaluno.clear()

    # =====================================================
    # LOGIN PROFESSOR
    # =====================================================

    def login_professor(self):

        w = self.window

        email = w.input_loginprof.text().strip()
        senha = w.input_senhaprof.text().strip()

        if not email or not senha:

            QMessageBox.warning(
                w,
                "Atenção",
                "Preencha o e-mail e a senha."
            )

            return

        usuario = self.verificar_usuario(
            email,
            senha,
            "professor"
        )

        if usuario:

            self.main.usuario_logado = usuario

            QMessageBox.information(
                w,
                "Bem-vindo",
                f"Olá, {usuario['nome']}!"
            )

            w.input_senhaprof.clear()

            self.main.ir_para(w.pg_areaprof)

        else:

            QMessageBox.warning(
                w,
                "Erro de autenticação",
                "E-mail ou senha incorretos."
            )

            w.input_senhaprof.clear()

    # =====================================================
    # CADASTRO
    # =====================================================

    def cadastrar_usuario(self):

        w = self.window

        email = w.input_loginprof_2.text().strip()
        senha = w.input_senhaprof_2.text().strip()

        if not email or not senha:

            QMessageBox.warning(
                w,
                "Atenção",
                "Preencha o e-mail e a senha."
            )

            return

        # verifica duplicado
        for usuario in usuarios:

            if usuario["email"] == email:

                QMessageBox.warning(
                    w,
                    "Cadastro",
                    "Este e-mail já está cadastrado."
                )

                return

        # define tipo
        tipo = (
            "professor"
            if "prof" in email
            else "aluno"
        )

        novo_usuario = {

            "nome": email.split("@")[0]
            .replace(".", " ")
            .title(),

            "email": email,
            "senha": senha,
            "tipo": tipo,
        }

        usuarios.append(novo_usuario)

        QMessageBox.information(
            w,
            "Cadastro realizado",
            "Usuário cadastrado com sucesso!"
        )

        w.input_loginprof_2.clear()
        w.input_senhaprof_2.clear()

        self.main.ir_para(w.pg_loginprof)

    # =====================================================
    # MENSAGEM CADASTRO ALUNO
    # =====================================================

    def msg_cadastro_aluno(self):

        QMessageBox.information(
            self.window,
            "Cadastro",
            "Entre em contato com seu professor "
            "para solicitar o cadastro."
        )