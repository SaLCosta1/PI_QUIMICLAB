from PySide6.QtWidgets import QMessageBox

from app.services.auth_service import (
    login_aluno,
    login_prof,
    cadastrar_prof,
    cadastrar_aluno,
)

class AuthController:
    def __init__(self, main):
        self.main = main
        w = main.window
        ir = main.ir_para
        w.btn_jogar.clicked.connect(
            lambda: w.fundo_comojogar_2.show()
        )
        w.btn_comojogar.clicked.connect(
            lambda: w.fundo_comojogar_2.show()
        )
        w.btn_recusar.clicked.connect(
            lambda: w.fundo_comojogar_2.hide()
        )
        w.btn_aceitar.clicked.connect(
            self._aceitar_termos
        )
        w.btn_voltarinicio.clicked.connect(
            lambda: ir(w.pg_inicio)
        )
        w.btn_soualuno.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )
        w.btn_souprof.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )
        w.btn_voltarperfil2.clicked.connect(
            lambda: ir(w.pg_perfil)
        )
        w.btn_entraraluno.clicked.connect(
            self._entrar_aluno
        )
        w.btn_cadastroaluno.clicked.connect(
            lambda: ir(w.pg_cadastro_aluno)
        )
        w.btn_alterarsenha_aluno.clicked.connect(
            lambda: ir(w.pg_trocasenha_aluno)
        )
        w.btn_voltarperfil3.clicked.connect(
            lambda: ir(w.pg_perfil)
        )
        w.btn_entrarprof.clicked.connect(
            self._entrar_prof
        )
        w.btn_cadastroprof.clicked.connect(
            lambda: ir(w.pg_cadastro)
        )
        w.btn_alterarsenha_prof.clicked.connect(
            lambda: ir(w.pg_trocasenha_prof)
        )
        w.btn_voltarperfil3_3.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )
        w.btn_cadastrar_aluno.clicked.connect(
            self._cadastrar_aluno
        )
        w.btn_voltarperfil3_2.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )
        w.btn_entrarprof_2.clicked.connect(
            self._cadastrar_prof
        )
        w.btn_voltarperfil2_2.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )
        w.btn_entraraluno_2.clicked.connect(
            self._trocar_senha_aluno
        )
        w.btn_voltarperfil2_3.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )
        w.btn_entraraluno_3.clicked.connect(
            self._trocar_senha_prof
        )
        w.btn_voltarperfil.clicked.connect(
            lambda: ir(w.pg_inicio)
        )
        w.fundo_comojogar_2.hide()
        w.checkBox.setEnabled(False)
        barra = w.txt_comojogar_2.verticalScrollBar()
        barra.valueChanged.connect(
            self._verificar_scroll_termos
        )

    def _aceitar_termos(self):
        w = self.main.window
        if not w.checkBox.isChecked():
            self._aviso(
                "Voce precisa aceitar os termos."
            )
            return
        w.fundo_comojogar_2.hide()
        self.main.ir_para(w.pg_perfil)

    def _entrar_aluno(self):
        w = self.main.window
        login = w.input_loginaluno.text().strip()
        senha = w.input_senhaaluno.text().strip()
        if not login or not senha:
            self._aviso(
                "Preencha login e senha."
            )
            return
        usuario, erro = login_aluno(login, senha)
        if erro:
            self._aviso(erro)
            return
        self.main.usuario_logado = usuario
        w.input_loginaluno.clear()
        w.input_senhaaluno.clear()
        self.main.ir_para(w.pg_tipo_jogo)

    def _entrar_prof(self):
        w = self.main.window
        login = w.input_loginprof.text().strip()
        senha = w.input_senhaprof.text().strip()
        if not login or not senha:
            self._aviso(
                "Preencha login e senha."
            )
            return
        usuario, erro = login_prof(login, senha)
        if erro:
            self._aviso(erro)
            return
        self.main.usuario_logado = usuario
        w.input_loginprof.clear()
        w.input_senhaprof.clear()
        self.main.ir_para(w.pg_areaprof)

    def _cadastrar_prof(self):
        w = self.main.window
        login = w.input_loginprof_2.text().strip()
        if not login:
            self._aviso(
                "Informe um login para cadastro."
            )
            return
        usuario, erro = cadastrar_prof(login, login)
        if erro:
            self._aviso(erro)
            return
        self._info(
            "Cadastro realizado com sucesso!"
        )
        w.input_loginprof_2.clear()
        self.main.ir_para(w.pg_loginprof)

    def _cadastrar_aluno(self):
        w = self.main.window
        nome = w.input_nomealuno.text().strip()
        email = w.input_emailaluno.text().strip()
        senha = w.input_senha_cadastroaluno.text().strip() if hasattr(w, 'input_senha_cadastroaluno') else ''
        turma = w.input_turmaaluno.text().strip()
        if not nome or not email or not turma:
            self._aviso(
                "Preencha nome, e-mail e turma."
            )
            return
        try:
            usuario, erro = cadastrar_aluno(nome, email, turma, senha or None)
        except Exception as exc:
            self._aviso(f"Erro inesperado ao cadastrar aluno: {exc}")
            return
        if erro:
            self._aviso(erro)
            return
        self._info(
            "Cadastro de aluno realizado com sucesso!"
        )
        w.input_nomealuno.clear()
        w.input_emailaluno.clear()
        w.input_turmaaluno.clear()
        self.main.ir_para(w.pg_loginaluno)

    def _trocar_senha_aluno(self):
        w = self.main.window
        login = w.input_loginaluno_2.text().strip()
        nova = w.input_senhaaluno_2.text().strip()
        if not login or not nova:
            self._aviso(
                "Preencha todos os campos."
            )
            return
        self._info(
            "Senha alterada com sucesso!"
        )
        w.input_loginaluno_2.clear()
        w.input_senhaaluno_2.clear()
        self.main.ir_para(w.pg_loginaluno)

    def _trocar_senha_prof(self):
        w = self.main.window
        login = w.input_loginaluno_3.text().strip()
        nova = w.input_senhaaluno_3.text().strip()
        if not login or not nova:
            self._aviso(
                "Preencha todos os campos."
            )
            return
        self._info(
            "Senha alterada com sucesso!"
        )
        w.input_loginaluno_3.clear()
        w.input_senhaaluno_3.clear()
        self.main.ir_para(w.pg_loginprof)

    def _verificar_scroll_termos(self):
        w = self.main.window
        barra = w.txt_comojogar_2.verticalScrollBar()
        chegou_final = (
            barra.value() >= barra.maximum()
        )
        w.checkBox.setEnabled(
            chegou_final
        )

    def _aviso(self, texto):
        QMessageBox.warning(
            self.main.window,
            "Atencao",
            texto
        )

    def _info(self, texto):
        QMessageBox.information(
            self.main.window,
            "Informacao",
            texto
        )
