"""Components sidebar: catalog of building blocks the user can add."""
from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from ..core import COMPONENT_REGISTRY
from .theme import Theme


class ComponentsSidebar(ctk.CTkFrame):
    """Vertical list of components with a card per item."""

    def __init__(self, master, on_add: Callable[[str], None]):
        super().__init__(master, fg_color=Theme.BG_PANEL, corner_radius=0, width=240)
        self.on_add = on_add
        self.pack_propagate(False)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(14, 6))
        ctk.CTkLabel(
            header, text="✨  Components",
            font=Theme.FONT_TITLE, text_color=Theme.FG,
        ).pack(side="left")

        ctk.CTkLabel(
            self,
            text="Click any block to add it to the current page.",
            font=("Segoe UI", 9), text_color=Theme.FG_DIM,
            justify="left", anchor="w", wraplength=210,
        ).pack(fill="x", padx=14, pady=(0, 8))

        # Scrollable list of cards
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_PANEL_2,
            corner_radius=Theme.RADIUS,
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.PRIMARY,
        )
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        for type_name, cls in COMPONENT_REGISTRY.items():
            self._build_card(scroll, type_name, cls)

    # ------------------------------------------------------------------
    def _build_card(self, parent, type_name: str, cls) -> None:
        card = ctk.CTkFrame(
            parent, fg_color=Theme.BG_CARD,
            corner_radius=Theme.RADIUS, height=64,
        )
        card.pack(fill="x", padx=4, pady=5)
        card.pack_propagate(False)

        # Icon badge
        badge = ctk.CTkLabel(
            card, text=cls.icon, width=44, height=44,
            corner_radius=10,
            fg_color=Theme.PRIMARY, text_color="#ffffff",
            font=("Segoe UI", 20, "bold"),
        )
        badge.pack(side="left", padx=10, pady=10)

        # Text
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=(0, 6))
        ctk.CTkLabel(
            info, text=cls.label, font=Theme.FONT_BOLD,
            text_color=Theme.FG, anchor="w", justify="left",
        ).pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(
            info, text=type_name, font=("Segoe UI", 9),
            text_color=Theme.FG_DIM, anchor="w", justify="left",
        ).pack(fill="x")

        # Add button
        add_btn = ctk.CTkButton(
            card, text="＋", width=32, height=32,
            corner_radius=8, font=("Segoe UI", 16, "bold"),
            fg_color=Theme.BG_HOVER, hover_color=Theme.PRIMARY,
            text_color=Theme.FG,
            command=lambda t=type_name: self.on_add(t),
        )
        add_btn.pack(side="right", padx=10)

        # Make the whole card clickable
        def _click(_e, t=type_name):
            self.on_add(t)

        for w in (card, badge, info, *info.winfo_children()):
            w.bind("<Button-1>", _click)
            try:
                w.configure(cursor="hand2")
            except Exception:
                pass
