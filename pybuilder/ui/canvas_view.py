"""WYSIWYG canvas: renders the current page as styled wireframe blocks."""
from __future__ import annotations

from typing import Callable

import customtkinter as ctk

from ..core import Node, Page
from .theme import Theme


def _rgb(hex_color: str) -> tuple[int, int, int]:
    c = (hex_color or "#000000").lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) < 6:
        c = (c + "000000")[:6]
    try:
        return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    except ValueError:
        return 0, 0, 0


def _is_dark(hex_color: str) -> bool:
    """Return True if the given hex color is "dark" (so we use white text)."""
    r, g, b = _rgb(hex_color)
    return (0.299 * r + 0.587 * g + 0.114 * b) < 140


def _shade(hex_color: str, factor: float) -> str:
    """Lighten (factor>0) or darken (factor<0) a hex color. Range -1..1."""
    r, g, b = _rgb(hex_color)
    if factor >= 0:
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
    else:
        f = 1 + factor
        r, g, b = int(r * f), int(g * f), int(b * f)
    r = max(0, min(255, r)); g = max(0, min(255, g)); b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"


class CanvasView(ctk.CTkFrame):
    """Center area where each node is shown as a colored block summarizing it.

    The look approximates the final HTML output without rendering it. The user
    sees the structure of the page in real time, including order, colors and
    text content.
    """

    def __init__(self, master, on_select: Callable[[Node], None],
                 on_move: Callable[[str, int], None],
                 on_delete: Callable[[str], None]):
        super().__init__(master, fg_color=Theme.BG_DEEP, corner_radius=0)
        self.on_select = on_select
        self.on_move = on_move
        self.on_delete = on_delete
        self.page: Page | None = None
        self.selected_id: str | None = None

        self._build_toolbar()
        self._build_workspace()

    # ------------------------------------------------------------------
    def _build_toolbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=Theme.BG_PANEL, corner_radius=0, height=52)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            bar, text="Home", font=Theme.FONT_TITLE,
            text_color=Theme.FG, anchor="w",
        )
        self.title_label.pack(side="left", padx=18)

        self.url_label = ctk.CTkLabel(
            bar, text="/", font=Theme.FONT_MONO,
            text_color=Theme.SECONDARY,
        )
        self.url_label.pack(side="left", padx=4)

        self.count_label = ctk.CTkLabel(
            bar, text="0 components", font=("Segoe UI", 10),
            text_color=Theme.FG_DIM,
        )
        self.count_label.pack(side="right", padx=18)

    def _build_workspace(self) -> None:
        # Outer area resembles a browser window
        outer = ctk.CTkFrame(self, fg_color=Theme.BG_DEEP, corner_radius=0)
        outer.pack(fill="both", expand=True, padx=24, pady=24)

        browser = ctk.CTkFrame(
            outer, fg_color="#ffffff",
            corner_radius=Theme.RADIUS_LG,
            border_color=Theme.BORDER, border_width=1,
        )
        browser.pack(fill="both", expand=True)

        # Browser chrome (the colored "traffic-light" dots)
        chrome = ctk.CTkFrame(browser, fg_color="#f1f5f9",
                              height=34, corner_radius=0)
        chrome.pack(fill="x")
        chrome.pack_propagate(False)
        for color in ("#ef4444", "#f59e0b", "#22c55e"):
            dot = ctk.CTkLabel(chrome, text=" ", width=14, height=14,
                               corner_radius=7, fg_color=color)
            dot.pack(side="left", padx=(8, 0), pady=10)
        self.address = ctk.CTkLabel(
            chrome, text=" mysite.com/ ",
            fg_color="#ffffff", corner_radius=8,
            text_color="#475569", font=Theme.FONT_MONO,
            anchor="w",
        )
        self.address.pack(side="left", fill="x", expand=True, padx=14, pady=6)

        # Scrollable page content
        self.scroll = ctk.CTkScrollableFrame(
            browser, fg_color="#ffffff", corner_radius=0,
            scrollbar_button_color="#cbd5e1",
            scrollbar_button_hover_color=Theme.PRIMARY,
        )
        self.scroll.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    def show_page(self, page: Page, url: str = "/") -> None:
        self.page = page
        self.selected_id = None
        self.title_label.configure(text=page.title)
        self.url_label.configure(text=url)
        self.address.configure(text=f" mysite.com{url} ")
        self.count_label.configure(
            text=f"{len(page.nodes)} components" if len(page.nodes) != 1
            else "1 component"
        )
        self._render()

    def select(self, node_id: str | None) -> None:
        self.selected_id = node_id
        self._render()

    # ------------------------------------------------------------------
    def _clear(self) -> None:
        for w in self.scroll.winfo_children():
            w.destroy()

    def _render(self) -> None:
        self._clear()
        if not self.page:
            return

        if not self.page.nodes:
            self._render_empty_state()
            return

        for i, node in enumerate(self.page.nodes):
            self._render_block(node, i)

    def _render_empty_state(self) -> None:
        wrap = ctk.CTkFrame(self.scroll, fg_color="transparent")
        wrap.pack(expand=True, fill="both", pady=80)
        ctk.CTkLabel(
            wrap, text="✨", font=("Segoe UI", 56), text_color="#cbd5e1",
        ).pack()
        ctk.CTkLabel(
            wrap, text="This page is empty",
            font=("Segoe UI Semibold", 18), text_color="#475569",
        ).pack(pady=(10, 4))
        ctk.CTkLabel(
            wrap,
            text="Pick a component on the left to start building.",
            font=("Segoe UI", 11), text_color="#94a3b8",
        ).pack()

    def _render_block(self, node: Node, index: int) -> None:
        bg = node.preview_color()
        dark = _is_dark(bg)
        fg = "#ffffff" if dark else "#0f172a"
        # Opaque "translucent" overlay color for chips/buttons sitting on the block.
        overlay = _shade(bg, -0.25) if dark else _shade(bg, -0.15)
        overlay_hover = _shade(bg, -0.4) if dark else _shade(bg, -0.3)
        is_selected = (self.selected_id == node.id)

        outer = ctk.CTkFrame(
            self.scroll,
            fg_color=Theme.PRIMARY if is_selected else "transparent",
            corner_radius=Theme.RADIUS_LG,
        )
        outer.pack(fill="x", padx=14, pady=6)

        # The block itself sits inside a 2px "selection ring" frame.
        block = ctk.CTkFrame(
            outer, fg_color=bg, corner_radius=Theme.RADIUS,
            height=node.preview_height(),
        )
        block.pack(fill="x", padx=(2 if is_selected else 0),
                   pady=(2 if is_selected else 0))
        block.pack_propagate(False)

        # Type label (top-left chip)
        chip = ctk.CTkLabel(
            block, text=f"  {node.icon}  {node.label}  ",
            fg_color=overlay, text_color=fg,
            corner_radius=8, font=("Segoe UI", 9, "bold"),
        )
        chip.place(x=10, y=8)

        # Action buttons (top-right): up, down, delete
        actions = ctk.CTkFrame(block, fg_color="transparent")
        actions.place(relx=1.0, x=-8, y=6, anchor="ne")

        def _btn(parent, text, hover, cmd):
            return ctk.CTkButton(
                parent, text=text, width=24, height=24,
                corner_radius=6, font=("Segoe UI", 11, "bold"),
                fg_color=overlay, hover_color=hover,
                text_color=fg, command=cmd,
            )

        _btn(actions, "▲", overlay_hover,
             lambda: self.on_move(node.id, -1)).pack(side="left", padx=2)
        _btn(actions, "▼", overlay_hover,
             lambda: self.on_move(node.id, +1)).pack(side="left", padx=2)
        _btn(actions, "✕", Theme.DANGER,
             lambda: self.on_delete(node.id)).pack(side="left", padx=2)

        # Main content: the summary text
        content = ctk.CTkLabel(
            block, text=node.preview_summary(),
            font=Theme.FONT_BOLD, text_color=fg,
            wraplength=900, justify="left", anchor="w",
        )
        content.place(relx=0.5, rely=0.5, anchor="center")

        # Whole block is clickable to select.
        def _click(_e, n=node):
            self.on_select(n)

        for w in (block, chip, content):
            w.bind("<Button-1>", _click)
            try:
                w.configure(cursor="hand2")
            except Exception:
                pass
