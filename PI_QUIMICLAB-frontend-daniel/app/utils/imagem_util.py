# -*- coding: utf-8 -*-
"""Conversão de BLOB (banco) para exibição em QLabel (Qt)."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


def pixmap_de_blob(imagem: bytes | bytearray | memoryview | None) -> QPixmap | None:
    """Converte bytes de imagem do banco em QPixmap. Retorna None se vazio ou inválido."""
    if not imagem:
        return None
    if isinstance(imagem, memoryview):
        imagem = imagem.tobytes()
    elif not isinstance(imagem, (bytes, bytearray)):
        return None
    pix = QPixmap()
    if not pix.loadFromData(bytes(imagem)):
        return None
    return pix


def aplicar_pixmap_no_label(lbl, pix: QPixmap | None) -> None:
    """Exibe imagem redimensionada no QLabel ou esconde o label se não houver imagem."""
    if pix is None or pix.isNull():
        lbl.clear()
        lbl.hide()
        return
    lbl.setPixmap(
        pix.scaled(
            lbl.width(),
            lbl.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    )
    lbl.show()
