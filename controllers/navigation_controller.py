# =========================================================
# navigation_controller.py
# =========================================================

from PySide6.QtWidgets import QMessageBox


class NavigationController:

    def __init__(self, main):
        self.main = main
        self.window = main.window
        self.stack = main.window.stack

        self.PAGINAS_PROF = frozenset({
            "pg_areaprof",
            "pg_editarperguntas",
            "pg_editarpergunta_detalhe",
            "pg_questao_edicao",
            "pg_questao_adicionar",
            "pg_ranking",
            "pg_rankinggeral",
            "pg_rankingturmas",
            "pg_relatoriogeral",
            "pg_relatorioturmas",
            "pg_relatorioindividual",
        })

    def ir_para(self, pagina):

        nome = pagina.objectName()

        if nome in self.PAGINAS_PROF:
            usuario = self.main.usuario_logado
            if not usuario or usuario.get("tipo") != "professor":
                QMessageBox.warning(
                    self.window,
                    "Acesso restrito",
                    "Esta área é exclusiva para professores."
                )
                return

        self.stack.setCurrentWidget(pagina)
        print(f"[nav] {nome}")
