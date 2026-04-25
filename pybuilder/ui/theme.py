"""Tema visual centralizado para la GUI (paleta moderna estilo "violet glass")."""
from __future__ import annotations


class Theme:
    # Fondos
    BG_DEEP = "#0b1020"        # ventana
    BG_PANEL = "#11172b"       # paneles
    BG_PANEL_2 = "#161d36"     # paneles secundarios
    BG_CARD = "#1b2342"        # tarjetas / items
    BG_HOVER = "#222b50"

    # Bordes
    BORDER = "#28335c"
    BORDER_SOFT = "#1f2848"

    # Texto
    FG = "#e6ecff"
    FG_MUTED = "#8a96c4"
    FG_DIM = "#5e6a96"

    # Acentos
    PRIMARY = "#7c5cff"        # violeta
    PRIMARY_HOVER = "#8f72ff"
    SECONDARY = "#22d3ee"      # cyan
    SUCCESS = "#22c55e"
    DANGER = "#ef4444"
    WARNING = "#f59e0b"

    # Tipografía
    FONT = ("Segoe UI", 11)
    FONT_BOLD = ("Segoe UI Semibold", 11)
    FONT_TITLE = ("Segoe UI Semibold", 14)
    FONT_HERO = ("Segoe UI Semibold", 18)
    FONT_MONO = ("Cascadia Mono", 10)

    # Radios
    RADIUS = 10
    RADIUS_LG = 14
