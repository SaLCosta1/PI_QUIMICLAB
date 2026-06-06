class NavigationController:
    def __init__(self, main):
        self.main = main
        self.stack = main.stack
        w = main.window
        # Troca de páginas da tela inicial/termos. O AuthController faz o
        # complemento (mostrar/ocultar o overlay de termos `fundo_comojogar_2`,
        # que vive dentro de pg_termos, e validar o checkbox no "Aceitar").
        w.btn_comojogar.clicked.connect(
            lambda: self.ir_para(w.pg_comojogar)
        )
        w.btn_voltarperfil.clicked.connect(
            lambda: self.ir_para(w.pg_inicio)
        )
        # "Jogar" precisa trocar para pg_termos para que o overlay de termos
        # (filho dessa página) possa aparecer; o .show() é feito pelo AuthController.
        w.btn_jogar.clicked.connect(
            lambda: self.ir_para(w.pg_termos)
        )
        # "Aceitar" NÃO navega aqui: quem decide o destino é
        # AuthController._aceitar_termos (valida o checkbox e vai para pg_perfil).
        # A conexão antiga apontava para `pg_login`, página que não existe mais.
        w.btn_recusar.clicked.connect(
            lambda: self.ir_para(w.pg_inicio)
        )

    def ir_para(self, pagina):
        if isinstance(pagina, str):
            pagina = getattr(
                self.main.window,
                pagina,
                None
            )
        if pagina is not None:
            self.stack.setCurrentWidget(pagina)
