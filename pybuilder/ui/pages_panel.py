"""Pages panel: tree view of the site hierarchy."""
from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import Callable

import customtkinter as ctk

from ..core import Page, Site
from ..core.page import slugify
from .theme import Theme


class PagesPanel(ctk.CTkFrame):
    """Left-side panel that shows the site as a tree of pages."""

    def __init__(self, master, site: Site, on_select: Callable[[Page], None]):
        super().__init__(master, fg_color=Theme.BG_PANEL, corner_radius=0)
        self.site = site
        self.on_select = on_select
        self.current: Page | None = None

        self._build_header()
        self._build_tree()
        self.refresh()

    # ------------------------------------------------------------------
    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(14, 6))

        ctk.CTkLabel(
            header, text="✦  Site Pages",
            font=Theme.FONT_TITLE, text_color=Theme.FG,
        ).pack(side="left")

        ctk.CTkButton(
            header, text="+ Page", width=70, height=28,
            corner_radius=Theme.RADIUS,
            fg_color=Theme.PRIMARY, hover_color=Theme.PRIMARY_HOVER,
            font=Theme.FONT_BOLD,
            command=self._add_root_page,
        ).pack(side="right")

        ctk.CTkLabel(
            self,
            text="Click a page to edit it. Right-click for actions.",
            font=("Segoe UI", 9), text_color=Theme.FG_DIM,
            justify="left", anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 8))

    def _build_tree(self) -> None:
        # Native ttk.Treeview is themed manually for the dark style.
        from tkinter import ttk

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Pages.Treeview",
            background=Theme.BG_PANEL,
            foreground=Theme.FG,
            fieldbackground=Theme.BG_PANEL,
            bordercolor=Theme.BG_PANEL,
            lightcolor=Theme.BG_PANEL,
            darkcolor=Theme.BG_PANEL,
            rowheight=30,
            font=Theme.FONT,
            borderwidth=0,
        )
        style.map(
            "Pages.Treeview",
            background=[("selected", Theme.PRIMARY)],
            foreground=[("selected", "#ffffff")],
        )
        style.layout("Pages.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        container = ctk.CTkFrame(self, fg_color=Theme.BG_PANEL_2,
                                  corner_radius=Theme.RADIUS)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(container, style="Pages.Treeview", show="tree")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Button-3>", self._on_right_click)

    # ------------------------------------------------------------------
    def refresh(self, select_id: str | None = None) -> None:
        self.tree.delete(*self.tree.get_children())

        def insert(page: Page, parent: str = "") -> None:
            label = ("🏠  " if parent == "" and page is self.site.root else "📄  ") + page.title
            iid = self.tree.insert(parent, "end", iid=page.id, text=label, open=True)
            for child in page.children:
                insert(child, iid)

        insert(self.site.root)

        target = select_id or (self.current.id if self.current else self.site.root.id)
        if self.tree.exists(target):
            self.tree.selection_set(target)
            self.tree.focus(target)

    # ------------------------------------------------------------------
    def _on_select(self, _evt) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        page, _ = self.site.find_page(sel[0])
        if page:
            self.current = page
            self.on_select(page)

    def _on_right_click(self, event) -> None:
        iid = self.tree.identify_row(event.y)
        if not iid:
            return
        self.tree.selection_set(iid)
        page, parent = self.site.find_page(iid)
        if not page:
            return

        menu = tk.Menu(self, tearoff=0,
                       bg=Theme.BG_CARD, fg=Theme.FG,
                       activebackground=Theme.PRIMARY,
                       activeforeground="#ffffff", bd=0)
        menu.add_command(label="➕  Add subpage",
                         command=lambda: self._add_subpage(page))
        menu.add_command(label="✎  Rename",
                         command=lambda: self._rename(page))
        if page is not self.site.root:
            menu.add_separator()
            menu.add_command(label="🗑  Delete",
                             command=lambda: self._delete(page, parent))
        menu.tk_popup(event.x_root, event.y_root)

    # ------------------------------------------------------------------
    def _add_root_page(self) -> None:
        self._add_subpage(self.site.root)

    def _add_subpage(self, parent: Page) -> None:
        title = simpledialog.askstring(
            "New page", "Page title:", parent=self.winfo_toplevel())
        if not title:
            return
        new = Page(title=title, slug=slugify(title))
        parent.add_child(new)
        self.refresh(select_id=new.id)
        self.current = new
        self.on_select(new)

    def _rename(self, page: Page) -> None:
        title = simpledialog.askstring(
            "Rename page", "New title:", initialvalue=page.title,
            parent=self.winfo_toplevel())
        if not title:
            return
        page.title = title
        if page is not self.site.root:
            page.slug = slugify(title)
        self.refresh(select_id=page.id)
        self.on_select(page)

    def _delete(self, page: Page, parent: Page | None) -> None:
        if not parent:
            return
        if not messagebox.askyesno(
                "Delete page",
                f"Delete '{page.title}' and all its subpages?",
                parent=self.winfo_toplevel()):
            return
        parent.remove_child(page.id)
        self.current = parent
        self.refresh(select_id=parent.id)
        self.on_select(parent)
