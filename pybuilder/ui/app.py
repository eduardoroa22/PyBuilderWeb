"""Main application window for PyBuilderWeb."""
from __future__ import annotations

import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ..core import Exporter, Page, Site, create_component
from .canvas_view import CanvasView
from .components_sidebar import ComponentsSidebar
from .inspector import InspectorPanel
from .pages_panel import PagesPanel
from .theme import Theme


class App(ctk.CTk):
    """Top-level window orchestrating all UI panels and the site model."""

    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("PyBuilderWeb  ·  No-Code Static Site Generator")
        self.geometry("1480x880")
        self.minsize(1180, 720)
        self.configure(fg_color=Theme.BG_DEEP)

        self.site = Site(name="My Site")
        self.current_page: Page = self.site.root
        self.project_path: Path | None = None

        self._build_topbar()
        self._build_layout()
        self._refresh_canvas()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_topbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=Theme.BG_PANEL_2,
                           corner_radius=0, height=58)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Brand
        brand = ctk.CTkFrame(bar, fg_color="transparent")
        brand.pack(side="left", padx=18)
        ctk.CTkLabel(
            brand, text="◆", font=("Segoe UI", 22, "bold"),
            text_color=Theme.PRIMARY,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            brand, text="PyBuilderWeb",
            font=("Segoe UI Semibold", 16), text_color=Theme.FG,
        ).pack(side="left")
        ctk.CTkLabel(
            brand, text="  ·  no-code site builder",
            font=("Segoe UI", 11), text_color=Theme.FG_DIM,
        ).pack(side="left")

        # Actions (right side)
        actions = ctk.CTkFrame(bar, fg_color="transparent")
        actions.pack(side="right", padx=14)

        def _btn(text, color, hover, cmd, primary=False):
            return ctk.CTkButton(
                actions, text=text, height=34,
                corner_radius=Theme.RADIUS,
                fg_color=color, hover_color=hover,
                text_color="#ffffff" if primary else Theme.FG,
                font=Theme.FONT_BOLD, command=cmd,
            )

        _btn("New", Theme.BG_CARD, Theme.BG_HOVER,
             self._new_project).pack(side="left", padx=4)
        _btn("Open", Theme.BG_CARD, Theme.BG_HOVER,
             self._open_project).pack(side="left", padx=4)
        _btn("Save", Theme.BG_CARD, Theme.BG_HOVER,
             self._save_project).pack(side="left", padx=4)
        _btn("✨ Export Site", Theme.PRIMARY, Theme.PRIMARY_HOVER,
             self._export_site, primary=True).pack(side="left", padx=(10, 0))

    def _build_layout(self) -> None:
        body = ctk.CTkFrame(self, fg_color=Theme.BG_DEEP, corner_radius=0)
        body.pack(fill="both", expand=True)

        # Left column: pages + components stacked
        left = ctk.CTkFrame(body, fg_color=Theme.BG_PANEL,
                            corner_radius=0, width=280)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        self.pages_panel = PagesPanel(left, self.site, self._on_page_selected)
        self.pages_panel.pack(fill="x")

        sep = ctk.CTkFrame(left, fg_color=Theme.BORDER_SOFT,
                           height=1, corner_radius=0)
        sep.pack(fill="x", padx=14, pady=4)

        self.components_sidebar = ComponentsSidebar(left, self._add_component)
        self.components_sidebar.configure(width=280)
        self.components_sidebar.pack(fill="both", expand=True)

        # Center: canvas
        self.canvas = CanvasView(
            body,
            on_select=self._on_node_selected,
            on_move=self._on_node_move,
            on_delete=self._on_node_delete,
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        # Right: inspector
        self.inspector = InspectorPanel(body, self.site, self._on_inspector_change)
        self.inspector.pack(side="right", fill="y")

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_page_selected(self, page: Page) -> None:
        self.current_page = page
        self.inspector.show_site_settings()
        self._refresh_canvas()

    def _on_node_selected(self, node) -> None:
        self.canvas.select(node.id)
        self.inspector.show_node(node)

    def _on_node_move(self, node_id: str, delta: int) -> None:
        self.current_page.move_node(node_id, delta)
        self._refresh_canvas(keep_selection=node_id)

    def _on_node_delete(self, node_id: str) -> None:
        self.current_page.remove_node(node_id)
        self.inspector.show_site_settings()
        self._refresh_canvas()

    def _on_inspector_change(self) -> None:
        keep = self.canvas.selected_id
        self._refresh_canvas(keep_selection=keep)

    def _add_component(self, type_name: str) -> None:
        node = create_component(type_name)
        self.current_page.add_node(node)
        self._refresh_canvas(keep_selection=node.id)
        self.inspector.show_node(node)

    # ------------------------------------------------------------------
    # Refresh helpers
    # ------------------------------------------------------------------
    def _refresh_canvas(self, keep_selection: str | None = None) -> None:
        url = self.site.page_url(self.current_page)
        self.canvas.show_page(self.current_page, url=url)
        if keep_selection:
            self.canvas.select(keep_selection)

    # ------------------------------------------------------------------
    # File / project actions
    # ------------------------------------------------------------------
    def _new_project(self) -> None:
        if not messagebox.askyesno(
                "New project",
                "Discard current project and start a new one?",
                parent=self):
            return
        self.site = Site(name="My Site")
        self.current_page = self.site.root
        self.project_path = None
        self.pages_panel.site = self.site
        self.pages_panel.current = self.site.root
        self.pages_panel.refresh(select_id=self.site.root.id)
        self.inspector.site = self.site
        self.inspector.show_site_settings()
        self._refresh_canvas()

    def _open_project(self) -> None:
        path = filedialog.askopenfilename(
            parent=self, title="Open project",
            filetypes=[("PyBuilderWeb project", "*.pbw"), ("JSON", "*.json")],
        )
        if not path:
            return
        try:
            self.site = Site.load(path)
        except Exception as ex:
            messagebox.showerror("Open failed", str(ex), parent=self)
            return
        self.project_path = Path(path)
        self.current_page = self.site.root
        self.pages_panel.site = self.site
        self.pages_panel.current = self.site.root
        self.pages_panel.refresh(select_id=self.site.root.id)
        self.inspector.site = self.site
        self.inspector.show_site_settings()
        self._refresh_canvas()

    def _save_project(self) -> None:
        path = self.project_path
        if path is None:
            chosen = filedialog.asksaveasfilename(
                parent=self, title="Save project",
                defaultextension=".pbw",
                filetypes=[("PyBuilderWeb project", "*.pbw")],
            )
            if not chosen:
                return
            path = Path(chosen)
        try:
            self.site.save(path)
            self.project_path = path
            messagebox.showinfo("Saved", f"Project saved to:\n{path}",
                                parent=self)
        except Exception as ex:
            messagebox.showerror("Save failed", str(ex), parent=self)

    def _export_site(self) -> None:
        folder = filedialog.askdirectory(
            parent=self, title="Choose export folder",
        )
        if not folder:
            return

        out_root = Path(folder)
        # If the user picked an empty folder, use it directly. Otherwise,
        # create a subfolder named after the site to avoid clobbering files.
        try:
            non_empty = any(out_root.iterdir())
        except Exception:
            non_empty = False
        if non_empty:
            sub = out_root / (self.site.name.lower().replace(" ", "-") or "site")
            target = sub
        else:
            target = out_root

        try:
            generated = Exporter(self.site).export(target, clean=False)
        except Exception as ex:
            messagebox.showerror("Export failed", str(ex), parent=self)
            return

        if messagebox.askyesno(
                "Export complete",
                f"Site exported to:\n{generated}\n\nOpen index.html in your browser?",
                parent=self):
            webbrowser.open((generated / "index.html").as_uri())


def run() -> None:
    App().mainloop()
