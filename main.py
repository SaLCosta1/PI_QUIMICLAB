# =========================================================
# IMPORTAÇÕES GERAIS DO PROJETO
# =========================================================
# Aqui são importados:
# - Qt (interface gráfica)
# - carregamento da UI (.ui do Qt Designer)
# - utilitários de escala e ícone
# - todos os controllers (responsáveis pela lógica do sistema)
#
# IMPORTANTE:
# Cada controller cuida de uma parte do sistema:
# - auth → login/cadastro
# - navigation → troca de telas
# - question → lógica do jogo
# - professor → área do professor
# - ranking → rankings
# - animation/editor → melhorias visuais e edição
# =========================================================

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from app.utils.ui_loader import carregar_ui, aplicar_icone
from app.utils.scaler import aplicar_escala

from app.controllers.navigation_controller import NavigationController
from app.controllers.auth_controller import AuthController
from app.controllers.question_controller import QuestionController
from app.controllers.professor_controller import ProfessorController
from app.controllers.ranking_controller import RankingController
from app.controllers.animation_controller import AnimationController
from app.controllers.editor_controller import EditorController


# =========================================================
# CLASSE PRINCIPAL DA APLICAÇÃO
# =========================================================
# Essa classe funciona como o "centro do sistema".
#
# Ela:
# - guarda a janela principal
# - inicializa todos os controllers
# - centraliza estado global (ex: usuário logado)
# - controla a navegação inicial
# =========================================================

class Main:
    def __init__(self, window):

        # Janela principal da interface (UI carregada do Qt Designer)
        self.window = window

        # Stack de telas (QStackedWidget)
        self.stack = window.stack

        # Usuário logado (preenchido após login)
        self.usuario_logado: dict | None = None

        # -----------------------------------------------------
        # CONTROLLERS (ordem IMPORTA)
        # -----------------------------------------------------
        # NavigationController precisa ser o primeiro porque
        # outros controllers usam self.ir_para()
        # -----------------------------------------------------

        self.navigation = NavigationController(self)

        # Atalho global para troca de telas
        self.ir_para = self.navigation.ir_para

        # Controle de autenticação (login/cadastro)
        self.auth_controller = AuthController(self)

        # Lógica do jogo (perguntas, respostas, sessão)
        self.question_controller = QuestionController(self)

        # Área do professor (relatórios, desempenho etc.)
        self.professor_controller = ProfessorController(self)

        # Ranking de alunos e turmas
        self.ranking_controller = RankingController(self)

        # Editor de conteúdo (provavelmente criação/edição)
        self.editor_controller = EditorController(self)

        # Controlador de animações visuais da interface
        # IMPORTANTE: vem por último porque pode "varrer" todos os botões
        self.animation_controller = AnimationController(self)

        # -----------------------------------------------------
        # TELA INICIAL
        # -----------------------------------------------------
        # Define a primeira tela exibida ao abrir o sistema
        # -----------------------------------------------------

        self.ir_para(window.pg_inicio)


# =========================================================
# INICIALIZAÇÃO DO PROGRAMA (ENTRY POINT)
# =========================================================
# Aqui o sistema realmente começa a rodar.
#
# Ordem de execução:
# 1. Cria QApplication (Qt precisa disso)
# 2. Carrega UI (.ui do Qt Designer)
# 3. Aplica ícone da janela
# 4. Cria classe Main (controllers + lógica)
# 5. Aplica escala da interface
# 6. Exibe janela maximizada
# 7. Inicia loop do Qt (app.exec)
# =========================================================

if __name__ == "__main__":

    # Cria aplicação Qt (obrigatório para qualquer GUI Qt)
    app = QApplication(sys.argv)

    # Caminho base do projeto
    base_dir = Path(__file__).resolve().parent

    # Carrega interface gráfica (.ui)
    window = carregar_ui(base_dir)

    # Define ícone da janela
    aplicar_icone(window, base_dir)

    # Inicializa controllers e lógica do sistema
    controller = Main(window)

    # Ajusta interface para resolução do monitor
    aplicar_escala(app, window)

    # Abre janela em tela cheia maximizada
    window.showMaximized()

    # Inicia loop da aplicação (Qt fica rodando aqui)
    sys.exit(app.exec())