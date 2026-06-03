# =========================================================
# NAVIGATION CONTROLLER
# =========================================================
# Responsável pela navegação entre as telas da aplicação.
#
# Este controller centraliza as trocas de páginas do sistema,
# evitando repetir código em diferentes partes do projeto.
#
# O sistema utiliza um QStackedWidget chamado "stack",
# onde cada página da interface é exibida individualmente.
# =========================================================


class NavigationController:

    def __init__(self, main):

        # Referência para a classe principal da aplicação.
        # Permite acessar:
        # - a janela principal
        # - páginas da interface
        # - métodos globais
        self.main = main

        # Stack responsável por armazenar todas as páginas.
        self.stack = main.stack

        # Atalho para acessar os widgets da interface.
        w = main.window

        # =================================================
        # COMO JOGAR
        # =================================================
        # Define a navegação relacionada à tela
        # "Como Jogar".
        # =================================================

        # Ao clicar no botão "Como Jogar",
        # o sistema abre a página correspondente.
        w.btn_comojogar.clicked.connect(
            lambda: self.ir_para(w.pg_comojogar)
        )

        # Botão de retorno para voltar à tela inicial.
        w.btn_voltarperfil.clicked.connect(
            lambda: self.ir_para(w.pg_inicio)
        )

        # =================================================
        # TERMOS DE USO
        # =================================================
        # Controle das páginas relacionadas aos
        # termos de uso da plataforma.
        # =================================================

        # Abre a página de termos antes do login.
        w.btn_jogar.clicked.connect(
            lambda: self.ir_para(w.pg_termos)
        )

        # Se o usuário aceitar os termos,
        # segue para a tela de login.
        w.btn_aceitar.clicked.connect(
            lambda: self.ir_para(w.pg_login)
        )

        # Se o usuário recusar os termos,
        # retorna para a tela inicial.
        w.btn_recusar.clicked.connect(
            lambda: self.ir_para(w.pg_inicio)
        )

    # =====================================================
    # NAVEGAÇÃO GENÉRICA
    # =====================================================
    # Método reutilizável para trocar de página.
    #
    # Esse método pode receber:
    # - o próprio widget da página
    # - ou o nome da página em formato string
    #
    # Exemplo:
    # self.ir_para(w.pg_inicio)
    #
    # ou:
    # self.ir_para("pg_inicio")
    # =====================================================

    def ir_para(self, pagina):

        # Verifica se foi passado o nome da página
        # em formato string.
        if isinstance(pagina, str):

            # Busca dinamicamente o atributo dentro
            # da janela principal.
            pagina = getattr(
                self.main.window,
                pagina,
                None
            )

        # Só troca de tela se a página existir.
        if pagina is not None:

            # Define a página atual do stack.
            self.stack.setCurrentWidget(pagina)