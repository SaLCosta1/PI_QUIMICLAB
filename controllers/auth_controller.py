# =========================================================
# controllers/auth_controller.py
# =========================================================
from PySide6.QtWidgets import QMessageBox, QLineEdit, QToolButton
from PySide6.QtCore import Qt
from services.auth_service import (
    login_aluno, login_prof,
    cadastrar_prof, trocar_senha,
)
 
 
class AuthController:
    def __init__(self, main):
        self.main = main
        w = main.window
 
        # Olho de ver/ocultar senha em todos os campos de senha
        campos_senha = [
            getattr(w, nome, None) for nome in (
                'input_senhaaluno', 'input_senhaaluno_2', 'input_senhaaluno_3',
                'input_senhaprof',  'input_senhaprof_2',
            )
        ]
        for campo in campos_senha:
            if campo:
                self._add_toggle_senha(campo)
 
        # Login aluno (3 páginas usam os mesmos campos com sufixo)
        w.btn_entraraluno.clicked.connect(self._login_aluno)
        if hasattr(w, 'btn_entraraluno_2'):
            w.btn_entraraluno_2.clicked.connect(self._login_aluno)
        if hasattr(w, 'btn_entraraluno_3'):
            w.btn_entraraluno_3.clicked.connect(self._login_aluno)
 
        # Login professor
        w.btn_entrarprof.clicked.connect(self._login_prof)
 
        # "Não Possui Cadastro?" → só navega para a tela de cadastro
        w.btn_cadastroprof.clicked.connect(
            lambda: self.main.ir_para(w.pg_cadastroprof)
        )
        # Botão "Cadastrar" dentro da pg_cadastroprof → salva no banco
        if hasattr(w, 'btn_entrarprof_2'):
            w.btn_entrarprof_2.clicked.connect(self._cadastrar_prof)
 
        # Troca de senha
        if hasattr(w, 'btn_alterarsenha_aluno'):
            w.btn_alterarsenha_aluno.clicked.connect(self._trocar_senha_aluno)
        if hasattr(w, 'btn_alterarsenha_prof'):
            w.btn_alterarsenha_prof.clicked.connect(self._trocar_senha_prof)
 
    # --------------------------------------------------
    def _add_toggle_senha(self, campo: QLineEdit):
        """
        Cria um QToolButton flutuante sobre o QLineEdit para alternar
        visibilidade da senha. Não toca no styleSheet do campo,
        preservando borda, border-radius e fundo originais.
        """
        btn = QToolButton(campo)
        btn.setText("●●●")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            "QToolButton { background: transparent; border: none; "
            "font-size: 13px; font-weight: bold; color: #921913; }"
        )
        btn.setFixedSize(104, 88)
        btn.raise_()
 
        def _reposicionar():
            btn.move(
                campo.width() - btn.width() - 10,
                (campo.height() - btn.height()) // 2,
            )
 
        _resize_original = campo.resizeEvent
        def _resize(event):
            _reposicionar()
            _resize_original(event)
        campo.resizeEvent = _resize
 
        _reposicionar()
 
        def _toggle():
            if campo.echoMode() == QLineEdit.EchoMode.Password:
                campo.setEchoMode(QLineEdit.EchoMode.Normal)
                btn.setText("VER")
            else:
                campo.setEchoMode(QLineEdit.EchoMode.Password)
                btn.setText("●●●")
 
        btn.clicked.connect(_toggle)
        btn.show()
 
    # --------------------------------------------------
    def _get_login_aluno(self):
        """Pega email/senha da página de login aluno ativa."""
        w = self.main.window
        pagina = w.stack.currentWidget()
        for sufixo in ('', '_2', '_3'):
            inp_email = getattr(w, f'input_loginaluno{sufixo}', None)
            inp_senha = getattr(w, f'input_senhaaluno{sufixo}', None)
            if inp_email and inp_senha and pagina is getattr(w, f'pg_loginaluno{"" if sufixo == "" else sufixo}', None):
                return inp_email.text().strip(), inp_senha.text().strip(), inp_email, inp_senha
        return (w.input_loginaluno.text().strip(),
                w.input_senhaaluno.text().strip(),
                w.input_loginaluno, w.input_senhaaluno)
 
    def _login_aluno(self):
        w = self.main.window
        email, senha, campo_email, campo_senha = self._get_login_aluno()
 
        if not email or not senha:
            QMessageBox.warning(w, "Atenção", "Preencha e-mail e senha.")
            return
 
        dados, erro = login_aluno(email, senha)
        if erro:
            QMessageBox.warning(w, "Erro", erro)
            return
 
        self.main.usuario_logado = dados
        campo_email.clear()
        campo_senha.clear()
        self.main.ir_para(w.pg_tipo_jogo)
 
    # --------------------------------------------------
    def _login_prof(self):
        w = self.main.window
        email = w.input_loginprof.text().strip()
        senha = w.input_senhaprof.text().strip()
 
        if not email or not senha:
            QMessageBox.warning(w, "Atenção", "Preencha e-mail e senha.")
            return
 
        dados, erro = login_prof(email, senha)
        if erro:
            QMessageBox.warning(w, "Erro", erro)
            return
 
        self.main.usuario_logado = dados
        w.input_loginprof.clear()
        w.input_senhaprof.clear()
        self.main.ir_para(w.pg_areaprof)
 
    # --------------------------------------------------
    def _cadastrar_prof(self):
        w = self.main.window
        campo_email = getattr(w, 'input_loginprof_2', None)
        campo_senha = getattr(w, 'input_senhaprof_2', None)
 
        if not campo_email or not campo_senha:
            QMessageBox.warning(w, "Atenção", "Campos de cadastro não encontrados.")
            return
 
        email_txt = campo_email.text().strip()
        senha_txt = campo_senha.text().strip()
 
        if not email_txt or not senha_txt:
            QMessageBox.warning(w, "Atenção", "Preencha e-mail e senha.")
            return
 
        # cadastrar_prof(nome, email) — usa e-mail como nome provisório
        # a senha digitada é ignorada; o serviço define senha1234+ por padrão
        dados, erro = cadastrar_prof(email_txt, email_txt)
        if erro:
            QMessageBox.warning(w, "Erro", erro)
            return
 
        QMessageBox.information(
            w, "Cadastro realizado",
            f"Professor cadastrado!\nE-mail: {email_txt}\nSenha inicial: senha1234+"
        )
        campo_email.clear()
        campo_senha.clear()
        self.main.ir_para(w.pg_loginprof)
 
    # --------------------------------------------------
    def _trocar_senha_aluno(self):
        w = self.main.window
        if not self.main.usuario_logado:
            return
        atual = getattr(w, 'input_senhaatual_aluno', None)
        nova  = getattr(w, 'input_novasenha_aluno',  None)
        conf  = getattr(w, 'input_confirmar_aluno',  None)
 
        if not all([atual, nova, conf]):
            QMessageBox.warning(w, "Atenção", "Widgets de troca de senha não encontrados.")
            return
 
        if nova.text() != conf.text():
            QMessageBox.warning(w, "Atenção", "As senhas não coincidem.")
            return
 
        ok, erro = trocar_senha(self.main.usuario_logado["id_usuario"],
                                atual.text(), nova.text())
        if not ok:
            QMessageBox.warning(w, "Erro", erro)
            return
 
        QMessageBox.information(w, "Sucesso", "Senha alterada!")
        for le in [atual, nova, conf]:
            le.clear()
        self.main.ir_para(w.pg_tipo_jogo)
 
    # --------------------------------------------------
    def _trocar_senha_prof(self):
        w = self.main.window
        if not self.main.usuario_logado:
            return
        atual = getattr(w, 'input_senhaatual_prof', None)
        nova  = getattr(w, 'input_novasenha_prof',  None)
        conf  = getattr(w, 'input_confirmar_prof',  None)
 
        if not all([atual, nova, conf]):
            QMessageBox.warning(w, "Atenção", "Widgets de troca de senha não encontrados.")
            return
 
        if nova.text() != conf.text():
            QMessageBox.warning(w, "Atenção", "As senhas não coincidem.")
            return
 
        ok, erro = trocar_senha(self.main.usuario_logado["id_usuario"],
                                atual.text(), nova.text())
        if not ok:
            QMessageBox.warning(w, "Erro", erro)
            return
 
        QMessageBox.information(w, "Sucesso", "Senha alterada!")
        for le in [atual, nova, conf]:
            le.clear()
        self.main.ir_para(w.pg_areaprof)