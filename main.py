import sys
import re
import hashlib
from pathlib import Path
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

# ==============================================
# BANCO DE DADOS
# ==============================================
import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="SenhaPI@1234",
            database="quimic_lab"
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print("Erro ao conectar com o Banco de Dados:", e)
        return None


def hash_senha(senha: str) -> str:
    """Gera SHA-256 da senha. Ajuste se o back usar bcrypt ou outro hash."""
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_usuario(email: str, senha: str, tipo: str):
    """
    Autentica pelo email + senha_hash + tipo ('aluno' ou 'professor').
    A senha padrão de todos os alunos é 'senha1234+'.
    """
    conexao = conectar_banco()
    if not conexao:
        return None
    try:
        cursor = conexao.cursor(dictionary=True, buffered=True)
        sql = """
            SELECT * FROM usuario
            WHERE email = %s AND senha_hash = %s AND tipo = %s
        """
        cursor.execute(sql, (email, hash_senha(senha), tipo))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro na autenticação:", e)
        return None
    finally:
        cursor.close()
        conexao.close()


# ==============================================
# CONTROLLER
# ==============================================

class Main:
    def __init__(self, window):
        self.window = window
        self.stack = window.btn_altA_sodicaexp  # QStackedWidget
        self.usuario_logado = None

        # ================================================
        # TELA 1: pagina_inicio
        # ================================================
        window.btn_jogar_inicio.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_perfildeuso)
        )

        # ================================================
        # TELA 2: pagina_perfildeuso
        # ================================================
        window.btn_voltarparainicio.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_inicio)
        )
        window.btn_comojogar_perfildeuso.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_comojogar)
        )
        window.btn_soualuno_perfildeuso.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_loginaluno)
        )
        window.btn_souprof_perfildeuso.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_loginprof)
        )

        # ================================================
        # TELA 3: pagina_comojogar
        # ================================================
        window.btn_voltar_paraperfildeuso1.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_perfildeuso)
        )

        # ================================================
        # TELA 4: pagina_loginaluno
        # Campo login = Email  |  Campo senha = Senha
        # ================================================
        window.btn_voltar_paraperfildeuso2.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_perfildeuso)
        )
        window.btn_entrar_loginaluno.clicked.connect(self.login_aluno)
        window.lineedit_senha_loginaluno.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================================================
        # TELA 5: pagina_loginprof
        # Campo login = Email  |  Campo senha = Senha
        # ================================================
        window.btn_voltarparaperfildeuso3.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_perfildeuso)
        )
        window.btn_entrar_loginprof.clicked.connect(self.login_prof)
        window.lineedit_senha_loginprof.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ================================================
        # TELA 6: pagina_modos
        # ================================================
        window.bnt_voltar_paraperfildeuso4.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_perfildeuso)
        )
        window.btn_facil_modos.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_3)
        )
        window.btn_medio_modos.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_6)
        )
        window.btn_dificil_modos.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_4)
        )
        window.btn_shuffle_modos.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_7)
        )

        # ================================================
        # TELA 7: pagina_areaprof
        # ================================================
        window.btn_voltar_paraloginprof.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_loginprof)
        )
        window.btn_editpergunta_areaprof.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_editarperguntas)
        )
        window.btn_relatorio_areaprof.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page)
        )
        window.btn_ranking_areaprof.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_2)
        )

        # ================================================
        # TELA 8: pagina_editarperguntas
        # ================================================
        window.btn_voltar_paraareaprof.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_areaprof)
        )
        window.btn_relatorio_areaprof_2.clicked.connect(
            lambda: QMessageBox.information(self.window, "Em breve", "Adicionar Perguntas — em desenvolvimento.")
        )
        window.btn_editpergunta_areaprof_2.clicked.connect(
            lambda: QMessageBox.information(self.window, "Em breve", "Modificar Perguntas — em desenvolvimento.")
        )
        window.btn_ranking_areaprof_2.clicked.connect(
            lambda: QMessageBox.information(self.window, "Em breve", "Remover Perguntas — em desenvolvimento.")
        )

        # ================================================
        # TELA 9: page (Relatório Geral)
        # ================================================
        window.btn_voltar_paraareaprof_2.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_areaprof)
        )
        window.btn_relatorioturma_relatorio.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_12)
        )
        window.btn_relatorioalunos_relatorio.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_9)
        )

        # ================================================
        # TELA 10: page_2 (Ranking)
        # ================================================
        window.btn_voltar_paraareaprof_3.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_areaprof)
        )
        window.btn_rankingturma_ranking.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_11)
        )
        window.btn_rankingaluno_ranking.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_13)
        )

        # ================================================
        # TELA 11: page_3 (Questão Fácil — 2 dicas)
        # ================================================
        window.btn_dicaexp_2dicas.clicked.connect(
            lambda: QMessageBox.information(self.window, "Dica", "Dica explicativa aqui.")
        )
        window.btn_eliminar_2dicas.clicked.connect(
            lambda: QMessageBox.information(self.window, "Eliminar", "Eliminar alternativa.")
        )
        for btn in [window.btn_altA_2dicas, window.btn_altB_2dicas,
                    window.btn_altC_2dicas, window.btn_altD_2dicas]:
            btn.clicked.connect(lambda: self.stack.setCurrentWidget(window.page_5))

        # ================================================
        # TELA 12: page_7 (Questão Shuffle — só eliminar)
        # ================================================
        window.btn_eliminar_soeliminar.clicked.connect(
            lambda: QMessageBox.information(self.window, "Eliminar", "Eliminar alternativa.")
        )
        for btn in [window.btn_altA_soeliminar, window.btn_altB_soeliminar,
                    window.btn_altC_soeliminar, window.btn_altD_soeliminar]:
            btn.clicked.connect(lambda: self.stack.setCurrentWidget(window.page_5))

        # ================================================
        # TELA 13: page_6 (Questão Médio — 2 dicas + texto)
        # ================================================
        window.btn_dicaexp_2dicascomtexto.clicked.connect(
            lambda: QMessageBox.information(self.window, "Dica", "Dica explicativa aqui.")
        )
        window.btn_eliminar_2dicascomtexto.clicked.connect(
            lambda: QMessageBox.information(self.window, "Eliminar", "Eliminar alternativa.")
        )
        for btn in [window.btn_altA_2dicascomtexto, window.btn_altB_2dicascomtexto,
                    window.btn_altC_2dicascomtexto, window.btn_altD_2dicascomtexto]:
            btn.clicked.connect(lambda: self.stack.setCurrentWidget(window.page_5))

        # ================================================
        # TELA 14: page_4 (Questão Difícil — só dica exp)
        # ================================================
        window.btn_eliminar_sodicaexp.clicked.connect(
            lambda: QMessageBox.information(self.window, "Eliminar", "Eliminar alternativa.")
        )
        for btn in [window.btn_altA_sodicaexp_2, window.btn_altB_sodicaexp,
                    window.btn_altC_comresposta_2, window.btn_altD_sodicaexp]:
            btn.clicked.connect(lambda: self.stack.setCurrentWidget(window.page_5))

        # ================================================
        # TELA 15: page_5 (Feedback)
        # ================================================
        window.btn_voltar_paraquestao.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_modos)
        )
        window.btn_entrar_paragabarito.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.page_8)
        )
        window.btn_rankingaluno_ranking_5.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_modos)
        )

        # ================================================
        # TELA 16: page_8 (Gabarito)
        # ================================================
        window.pushButton.clicked.connect(
            lambda: self.stack.setCurrentWidget(window.pagina_modos)
        )

        # ================================================
        # TELA 17: page_9 (Relatório Alunos)
        # ================================================
        for btn in [window.pushButton_2, window.pushButton_3,
                    window.pushButton_4, window.pushButton_5, window.pushButton_6]:
            btn.clicked.connect(lambda: self.stack.setCurrentWidget(window.page_10))

        # ================================================
        # TELA 19: page_11 (Ranking Turmas)
        # ================================================
        for btn in [window.pushButton_7, window.pushButton_8, window.pushButton_9,
                    window.pushButton_10, window.pushButton_11]:
            btn.clicked.connect(
                lambda: QMessageBox.information(self.window, "Ranking", "Detalhes da turma — em desenvolvimento.")
            )

        # ================================================
        # TELA 20: page_13 (Ranking Alunos)
        # ================================================
        for btn in [window.pushButton_17, window.pushButton_18, window.pushButton_19,
                    window.pushButton_20, window.pushButton_21]:
            btn.clicked.connect(
                lambda: QMessageBox.information(self.window, "Ranking", "Detalhes do aluno — em desenvolvimento.")
            )

        # ================================================
        # TELA 21: page_12 (Relatório Turmas)
        # ================================================
        for btn in [window.pushButton_12, window.pushButton_13, window.pushButton_14,
                    window.pushButton_15, window.pushButton_16]:
            btn.clicked.connect(
                lambda: QMessageBox.information(self.window, "Relatório", "Detalhes da turma — em desenvolvimento.")
            )

        self.stack.setCurrentWidget(window.pagina_inicio)

    # ================================================
    # LOGIN ALUNO
    # Email: nome.sobrenome@aluno.cps.gov.br
    # Senha padrão: senha1234+
    # ================================================
    def login_aluno(self):
        email = self.window.lineedit_login_loginaluno.text().strip()
        senha = self.window.lineedit_senha_loginaluno.text().strip()

        if not email or not senha:
            QMessageBox.warning(self.window, "Atenção", "Preencha email e senha.")
            return

        resultado = verificar_usuario(email, senha, tipo="aluno")

        if resultado:
            self.usuario_logado = resultado
            QMessageBox.information(self.window, "Bem-vindo!", f"Olá, {resultado['nome']}!")
            self.stack.setCurrentWidget(self.window.pagina_modos)
        else:
            QMessageBox.warning(self.window, "Erro", "Email ou senha incorretos.")

    # ================================================
    # LOGIN PROFESSOR
    # ================================================
    def login_prof(self):
        email = self.window.lineedit_login_loginprof.text().strip()
        senha = self.window.lineedit_senha_loginprof.text().strip()

        if not email or not senha:
            QMessageBox.warning(self.window, "Atenção", "Preencha email e senha.")
            return

        resultado = verificar_usuario(email, senha, tipo="professor")

        if resultado:
            self.usuario_logado = resultado
            QMessageBox.information(self.window, "Bem-vindo!", f"Olá, {resultado['nome']}!")
            self.stack.setCurrentWidget(self.window.pagina_areaprof)
        else:
            QMessageBox.warning(self.window, "Erro", "Email ou senha incorretos.")


# ==============================================
# CARREGAMENTO DO .UI
# ==============================================

def corrigir_caminhos_ui(ui_path: Path) -> str:
    content = ui_path.read_text(encoding="utf-8")
    images_dir = ui_path.parent.parent / "images"

    def fix(m):
        nome = Path(m.group(2)).name.replace(" ", "_")
        novo = str(images_dir / nome).replace("\\", "/")
        return m.group(1) + novo + m.group(3)

    content = re.sub(r'(<(?:pixmap|string)>)(.*?\.(?:png|jpg|jpeg))(</(?:pixmap|string)>)', fix, content, flags=re.IGNORECASE)
    content = re.sub(r'(<normaloff>)(.*?)(</normaloff>)', fix, content)
    return content


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_path = Path(__file__).parent / "app" / "ui" / "Apresentacao_PI.ui"
    ui_corrigido = corrigir_caminhos_ui(ui_path)

    ui_temp = ui_path.parent / "_temp_ui.ui"
    ui_temp.write_text(ui_corrigido, encoding="utf-8")

    loader = QUiLoader()
    window = loader.load(str(ui_temp))
    ui_temp.unlink()

    if window is None:
        print("Erro ao carregar o .ui")
        sys.exit(1)

    controller = Main(window)
    window.show()

    sys.exit(app.exec())
