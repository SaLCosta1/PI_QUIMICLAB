class NavigationController:
    def __init__(self, main):
        self.main = main
        self.stack = main.stack
        w = main.window
        w.btn_comojogar.clicked.connect(
            lambda: self.ir_para(w.pg_comojogar)
        )
        w.btn_voltarperfil.clicked.connect(
            lambda: self.ir_para(w.pg_inicio)
        )
        w.btn_jogar.clicked.connect(
            lambda: self.ir_para(w.pg_termos)
        )
        w.btn_aceitar.clicked.connect(
            lambda: self.ir_para(w.pg_login)
        )
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
