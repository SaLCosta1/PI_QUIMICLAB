# =========================================================
# SCALER — RESPONSÁVEL POR AJUSTAR A INTERFACE AO MONITOR
# =========================================================
#
# Objetivo:
# ----------
# Esse módulo ajusta automaticamente o tamanho e posição
# de TODOS os widgets da interface com base no tamanho da tela.
#
# Design base do projeto:
# - 1920 x 1080 (Full HD)
#
# Quando a tela do usuário é menor ou maior,
# tudo é redimensionado proporcionalmente.
#
# =========================================================

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QRect

# Tamanho base usado no design da interface
DESIGN_W = 1920
DESIGN_H = 1080


# =========================================================
# FUNÇÃO INTERNA: ESCALAR WIDGETS
# =========================================================
# Essa função percorre todos os widgets filhos da janela
# e ajusta posição e tamanho proporcionalmente.
#
# IMPORTANTE:
# - Ela altera diretamente "geometry"
# - Isso significa posição (x, y) e tamanho (width, height)
# =========================================================

def _escalar_widgets(widget: QWidget, fx: float, fy: float):
    """
    Aplica escala em todos os widgets filhos de forma recursiva.

    Parâmetros:
      widget → janela principal ou container
      fx     → fator de escala horizontal
      fy     → fator de escala vertical
    """

    # Percorre todos os widgets filhos da interface
    for child in widget.findChildren(QWidget):

        # Pega posição e tamanho atual do widget
        geo = child.geometry()

        # Calcula nova posição/tamanho proporcional
        novo = QRect(
            round(geo.x()      * fx),
            round(geo.y()      * fy),
            round(geo.width()  * fx),
            round(geo.height() * fy),
        )

        # Aplica nova geometria ao widget
        child.setGeometry(novo)


# =========================================================
# FUNÇÃO PRINCIPAL: APLICAR ESCALA GLOBAL
# =========================================================
# Essa função é chamada quando a aplicação inicia.
# Ela detecta o tamanho da tela e ajusta toda a UI.
# =========================================================

def aplicar_escala(app, window):
    """
    Ajusta a interface inteira para o tamanho do monitor atual.

    Fluxo:
    1. Detecta resolução do monitor
    2. Calcula fatores de escala (fx, fy)
    3. Redimensiona todos os widgets
    4. Ajusta tamanho da janela principal
    """

    # Pega a tela principal do sistema
    screen = app.primaryScreen()

    # Se não encontrar tela, não faz nada
    if screen is None:
        return

    # Área disponível da tela (exclui barra do sistema)
    disponivel = screen.availableGeometry()

    # Largura e altura reais do monitor
    mon_w = disponivel.width()
    mon_h = disponivel.height()

    # Calcula proporção entre design e tela atual
    fx = mon_w / DESIGN_W   # escala horizontal
    fy = mon_h / DESIGN_H   # escala vertical

    # Aplica escala em todos os widgets antes de mostrar a janela
    _escalar_widgets(window, fx, fy)

    # Remove restrição de tamanho mínimo (evita travamento visual)
    window.setMinimumSize(0, 0)

    # Ajusta janela para ocupar toda a tela
    window.resize(mon_w, mon_h)