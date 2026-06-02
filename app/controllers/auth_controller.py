# -*- coding: utf-8 -*-
# =========================================================
# AUTH CONTROLLER
# =========================================================
#
# Responsável por:
# • Controle de login de aluno e professor
# • Navegação entre telas de autenticação
# • Cadastro de professor
# • Alteração de senha
# • Controle do overlay de termos de uso
#
# Este controller centraliza todas as ações ligadas
# ao acesso do usuário no sistema.
# =========================================================

from PySide6.QtWidgets import QMessageBox

from app.services.auth_service import (
    login_aluno,
    login_prof,
    cadastrar_prof,
    cadastrar_aluno,
)


class AuthController:

    # =====================================================
    # CONSTRUTOR
    # =====================================================
    #
    # Recebe a instância principal da aplicação (main)
    # e conecta os botões da interface aos métodos
    # responsáveis pelas ações de autenticação.
    # =====================================================

    def __init__(self, main):

        self.main = main
        w = main.window
        ir = main.ir_para

        # =================================================
        # TELA INICIAL (pg_inicio)
        # =================================================
        #
        # Os botões "Jogar" e "Como Jogar" exibem
        # o overlay com os termos de uso.
        # =================================================

        w.btn_jogar.clicked.connect(
            lambda: w.fundo_comojogar_2.show()
        )

        w.btn_comojogar.clicked.connect(
            lambda: w.fundo_comojogar_2.show()
        )

        # =================================================
        # TERMOS DE USO
        # =================================================
        #
        # • Recusar → fecha o overlay
        # • Aceitar → valida checkbox e continua
        # =================================================

        w.btn_recusar.clicked.connect(
            lambda: w.fundo_comojogar_2.hide()
        )

        w.btn_aceitar.clicked.connect(
            self._aceitar_termos
        )

        # =================================================
        # TELA DE PERFIL
        # =================================================
        #
        # Permite escolher entre perfil:
        # • aluno
        # • professor
        # =================================================

        w.btn_voltarinicio.clicked.connect(
            lambda: ir(w.pg_inicio)
        )

        w.btn_soualuno.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )

        w.btn_souprof.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )

        # =================================================
        # LOGIN DE ALUNO
        # =================================================

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

        # =================================================
        # LOGIN DE PROFESSOR
        # =================================================

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

        # =================================================
        # CADASTRO DE PROFESSOR
        # =================================================

        w.btn_voltarperfil3_2.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )

        w.btn_entrarprof_2.clicked.connect(
            self._cadastrar_prof
        )

        # =================================================
        # TROCA DE SENHA - ALUNO
        # =================================================

        w.btn_voltarperfil2_2.clicked.connect(
            lambda: ir(w.pg_loginaluno)
        )

        w.btn_entraraluno_2.clicked.connect(
            self._trocar_senha_aluno
        )

        # =================================================
        # TROCA DE SENHA - PROFESSOR
        # =================================================

        w.btn_voltarperfil2_3.clicked.connect(
            lambda: ir(w.pg_loginprof)
        )

        w.btn_entraraluno_3.clicked.connect(
            self._trocar_senha_prof
        )

        # =================================================
        # COMO JOGAR
        # =================================================

        w.btn_voltarperfil.clicked.connect(
            lambda: ir(w.pg_inicio)
        )

        # =================================================
        # CONFIGURAÇÕES INICIAIS
        # =================================================
        #
        # Overlay inicia escondido
        # Checkbox inicia desabilitado
        # =================================================

        w.fundo_comojogar_2.hide()

        w.checkBox.setEnabled(False)

        # =================================================
        # CONTROLE DE SCROLL DOS TERMOS
        # =================================================
        #
        # O checkbox só é habilitado quando
        # o usuário chega ao final do texto.
        # =================================================

        barra = w.txt_comojogar_2.verticalScrollBar()

        barra.valueChanged.connect(
            self._verificar_scroll_termos
        )

    # =====================================================
    # ACEITAR TERMOS
    # =====================================================
    #
    # Verifica se o usuário marcou o checkbox
    # de aceitação dos termos antes de continuar.
    # =====================================================

    def _aceitar_termos(self):

        w = self.main.window

        # Verifica se os termos foram aceitos
        if not w.checkBox.isChecked():

            self._aviso(
                "Voce precisa aceitar os termos."
            )

            return

        # Fecha o overlay
        w.fundo_comojogar_2.hide()

        # Navega para a tela de perfil
        self.main.ir_para(w.pg_perfil)

    # =====================================================
    # LOGIN DE ALUNO
    # =====================================================
    #
    # Realiza validação simples de login e senha.
    # =====================================================

    def _entrar_aluno(self):

        w = self.main.window

        login = w.input_loginaluno.text().strip()
        senha = w.input_senhaaluno.text().strip()

        # Validação de campos vazios
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

        # Limpa os campos
        w.input_loginaluno.clear()
        w.input_senhaaluno.clear()

        # Vai para a tela do jogo
        self.main.ir_para(w.pg_tipo_jogo)

    # =====================================================
    # LOGIN DE PROFESSOR
    # =====================================================

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

    # =====================================================
    # CADASTRO DE PROFESSOR
    # =====================================================

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

    # =====================================================
    # CADASTRO DE ALUNO
    # =====================================================

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

    # =====================================================
    # TROCA DE SENHA - ALUNO
    # =====================================================

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

    # =====================================================
    # TROCA DE SENHA - PROFESSOR
    # =====================================================

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

    # =====================================================
    # VERIFICAÇÃO DO SCROLL DOS TERMOS
    # =====================================================
    #
    # Habilita o checkbox apenas quando o usuário
    # chega ao final do texto de termos de uso.
    # =====================================================

    def _verificar_scroll_termos(self):

        w = self.main.window

        barra = w.txt_comojogar_2.verticalScrollBar()

        chegou_final = (
            barra.value() >= barra.maximum()
        )

        w.checkBox.setEnabled(
            chegou_final
        )

    # =====================================================
    # MENSAGEM DE AVISO
    # =====================================================
    #
    # Exibe popup de atenção para o usuário.
    # =====================================================

    def _aviso(self, texto):

        QMessageBox.warning(
            self.main.window,
            "Atencao",
            texto
        )

    # =====================================================
    # MENSAGEM INFORMATIVA
    # =====================================================
    #
    # Exibe popup de informação ao usuário.
    # =====================================================

    def _info(self, texto):

        QMessageBox.information(
            self.main.window,
            "Informacao",
            texto
        )