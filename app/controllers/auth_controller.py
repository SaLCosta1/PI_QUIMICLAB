from PySide6.QtWidgets import QMessageBox, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor

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

        # Mascara as senhas (•••) e adiciona o botão de olho mostrar/ocultar
        for _campo in (
            'input_senhaaluno', 'input_senhaprof',
            'input_senha_cadastroaluno',
            'input_senhaaluno_2', 'input_senhaaluno_3',
        ):
            if hasattr(w, _campo):
                self._configurar_senha(getattr(w, _campo))

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

    def _icone_olho(self, aberto, cor="#921913", tam=30):
        """Desenha o ícone de olho: aberto = contorno + pupila; fechado = contorno + traço diagonal."""
        pix = QPixmap(tam, tam)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        caneta = QPen(QColor(cor))
        caneta.setWidth(2)
        p.setPen(caneta)
        p.setBrush(Qt.BrushStyle.NoBrush)
        # contorno do olho
        p.drawEllipse(QRectF(3, tam * 0.30, tam - 6, tam * 0.40))
        if aberto:
            p.setBrush(QColor(cor))
            r = tam * 0.11
            p.drawEllipse(QRectF(tam / 2 - r, tam / 2 - r, 2 * r, 2 * r))
        else:
            p.drawLine(5, tam - 5, tam - 5, 5)
        p.end()
        return QIcon(pix)

    def _configurar_senha(self, campo):
        """Mascara a senha (•••) e adiciona um botão de olho para mostrar/ocultar o texto."""
        campo.setEchoMode(QLineEdit.EchoMode.Password)

        parent = campo.parentWidget()
        if parent is None:
            return

        g = campo.geometry()
        tam = min(max(g.height() - 16, 24), 44)
        btn = QPushButton(parent)
        btn.setGeometry(
            g.x() + g.width() - tam - 12,
            g.y() + (g.height() - tam) // 2,
            tam,
            tam,
        )
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("QPushButton { border: none; background: transparent; }")
        btn.setIconSize(QSize(tam - 6, tam - 6))
        btn.setIcon(self._icone_olho(False))  # senha oculta -> olho fechado
        # Abre espaço à direita para o texto não passar por baixo do olho
        campo.setTextMargins(0, 0, tam + 16, 0)

        def alternar():
            if campo.echoMode() == QLineEdit.EchoMode.Password:
                campo.setEchoMode(QLineEdit.EchoMode.Normal)
                btn.setIcon(self._icone_olho(True))
            else:
                campo.setEchoMode(QLineEdit.EchoMode.Password)
                btn.setIcon(self._icone_olho(False))

        btn.clicked.connect(alternar)
        btn.show()

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
