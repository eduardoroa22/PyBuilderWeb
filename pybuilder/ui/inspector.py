"""Properties inspector: edit the selected node's properties (data binding)."""
from __future__ import annotations

from tkinter import colorchooser
from typing import Callable

import customtkinter as ctk

from ..core import Node, Site
from .theme import Theme


class InspectorPanel(ctk.CTkFrame):
    """Right-side panel. Two modes:
       * No node selected -> shows site/page settings.
       * Node selected    -> shows the node's editable properties.
    """

    def __init__(self, master, site: Site,
                 on_change: Callable[[], None]):
        super().__init__(master, fg_color=Theme.BG_PANEL,
                         corner_radius=0, width=320)
        self.site = site
        self.on_change = on_change
        self.node: Node | None = None
        self.pack_propagate(False)

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=14, pady=(14, 6))
        self.title = ctk.CTkLabel(
            self.header, text="⚙  Inspector",
            font=Theme.FONT_TITLE, text_color=Theme.FG,
        )
        self.title.pack(side="left")
        self.subtitle = ctk.CTkLabel(
            self, text="", font=("Segoe UI", 10),
            text_color=Theme.FG_DIM, anchor="w", justify="left",
        )
        self.subtitle.pack(fill="x", padx=14, pady=(0, 8))

        self.body = ctk.CTkScrollableFrame(
            self, fg_color=Theme.BG_PANEL_2,
            corner_radius=Theme.RADIUS,
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.PRIMARY,
        )
        self.body.pack(fill="both", expand=True, padx=10, pady=10)

        self.show_site_settings()

    # ------------------------------------------------------------------
    def _clear_body(self) -> None:
        for w in self.body.winfo_children():
            w.destroy()

    # ------------------------------------------------------------------
    def show_site_settings(self) -> None:
        self.node = None
        self.title.configure(text="⚙  Site Settings")
        self.subtitle.configure(
            text="Global settings for the whole project. Pick a component to edit it."
        )
        self._clear_body()

        self._section_label("Project")
        self._text_field("Name", self.site.name,
                         lambda v: setattr(self.site, "name", v))
        self._text_field("Description", self.site.description,
                         lambda v: setattr(self.site, "description", v),
                         multiline=True)
        self._text_field("Author", self.site.author,
                         lambda v: setattr(self.site, "author", v))

        self._section_label("Theme")
        for key, label in [
            ("primary", "Primary color"),
            ("secondary", "Secondary color"),
            ("bg", "Page background"),
            ("fg", "Text color"),
            ("muted", "Muted text"),
        ]:
            self._color_field(label, self.site.theme[key],
                              lambda v, k=key: self.site.theme.update({k: v}))

        self._text_field("Border radius (e.g. 14px)",
                         self.site.theme["radius"],
                         lambda v: self.site.theme.update({"radius": v}))
        self._text_field("CSS font-family",
                         self.site.theme["font"],
                         lambda v: self.site.theme.update({"font": v}))

    # ------------------------------------------------------------------
    def show_node(self, node: Node) -> None:
        self.node = node
        self.title.configure(text=f"{node.icon}  {node.label}")
        self.subtitle.configure(text=f"id: {node.id}")
        self._clear_body()

        if not node.schema:
            ctk.CTkLabel(
                self.body, text="This component has no editable properties.",
                text_color=Theme.FG_DIM, font=("Segoe UI", 10),
                wraplength=260, justify="left",
            ).pack(padx=10, pady=10, anchor="w")
            return

        for field in node.schema:
            key = field["key"]
            label = field["label"]
            ftype = field.get("type", "text")
            value = node.props.get(key, "")

            if ftype == "color":
                self._color_field(label, value,
                                  lambda v, k=key: self._set(k, v))
            elif ftype == "textarea":
                self._text_field(label, value,
                                 lambda v, k=key: self._set(k, v),
                                 multiline=True)
            elif ftype == "choice":
                self._choice_field(label, value, field["options"],
                                   lambda v, k=key: self._set(k, v))
            elif ftype == "bool":
                self._bool_field(label, bool(value),
                                 lambda v, k=key: self._set(k, v))
            else:
                self._text_field(label, value,
                                 lambda v, k=key: self._set(k, v))

    def _set(self, key: str, value) -> None:
        if self.node is None:
            return
        self.node.set_prop(key, value)
        self.on_change()

    # ------------------------------------------------------------------
    # Field builders
    # ------------------------------------------------------------------
    def _section_label(self, text: str) -> None:
        ctk.CTkLabel(
            self.body, text=text.upper(),
            font=("Segoe UI Semibold", 10), text_color=Theme.SECONDARY,
            anchor="w", justify="left",
        ).pack(fill="x", padx=10, pady=(14, 4))

    def _label(self, text: str):
        ctk.CTkLabel(
            self.body, text=text, font=("Segoe UI", 10),
            text_color=Theme.FG_MUTED, anchor="w", justify="left",
        ).pack(fill="x", padx=10, pady=(8, 2))

    def _text_field(self, label: str, value: str,
                    setter: Callable[[str], None],
                    multiline: bool = False) -> None:
        self._label(label)
        if multiline:
            box = ctk.CTkTextbox(
                self.body, height=90, fg_color=Theme.BG_CARD,
                text_color=Theme.FG, border_width=1,
                border_color=Theme.BORDER, corner_radius=Theme.RADIUS,
                font=Theme.FONT,
            )
            box.pack(fill="x", padx=10)
            box.insert("1.0", value or "")

            def _on_key(_e, b=box, s=setter):
                s(b.get("1.0", "end-1c"))

            box.bind("<KeyRelease>", _on_key)
        else:
            entry = ctk.CTkEntry(
                self.body, fg_color=Theme.BG_CARD, text_color=Theme.FG,
                border_width=1, border_color=Theme.BORDER,
                corner_radius=Theme.RADIUS, font=Theme.FONT,
            )
            entry.pack(fill="x", padx=10)
            entry.insert(0, value or "")

            def _on_key(_e, e=entry, s=setter):
                s(e.get())

            entry.bind("<KeyRelease>", _on_key)

    def _color_field(self, label: str, value: str,
                     setter: Callable[[str], None]) -> None:
        self._label(label)
        row = ctk.CTkFrame(self.body, fg_color="transparent")
        row.pack(fill="x", padx=10)

        swatch = ctk.CTkButton(
            row, text="", width=34, height=30,
            fg_color=value or "#000000",
            hover_color=value or "#000000",
            corner_radius=8, border_width=1,
            border_color=Theme.BORDER,
        )
        swatch.pack(side="left")

        entry = ctk.CTkEntry(
            row, fg_color=Theme.BG_CARD, text_color=Theme.FG,
            border_width=1, border_color=Theme.BORDER,
            corner_radius=Theme.RADIUS, font=Theme.FONT_MONO,
        )
        entry.pack(side="left", fill="x", expand=True, padx=(8, 0))
        entry.insert(0, value or "#000000")

        def _apply(new: str) -> None:
            try:
                swatch.configure(fg_color=new, hover_color=new)
            except Exception:
                return
            setter(new)

        def _on_key(_e, e=entry):
            v = e.get().strip()
            if v.startswith("#") and len(v) in (4, 7):
                _apply(v)

        entry.bind("<KeyRelease>", _on_key)

        def _pick():
            chosen = colorchooser.askcolor(
                color=entry.get() or "#ffffff",
                parent=self.winfo_toplevel(),
                title=label,
            )
            if chosen and chosen[1]:
                entry.delete(0, "end")
                entry.insert(0, chosen[1])
                _apply(chosen[1])

        swatch.configure(command=_pick)

    def _choice_field(self, label: str, value: str, options: list[str],
                      setter: Callable[[str], None]) -> None:
        self._label(label)
        var = ctk.StringVar(value=value)
        menu = ctk.CTkOptionMenu(
            self.body, variable=var, values=options,
            fg_color=Theme.BG_CARD,
            button_color=Theme.PRIMARY,
            button_hover_color=Theme.PRIMARY_HOVER,
            text_color=Theme.FG, dropdown_fg_color=Theme.BG_CARD,
            dropdown_text_color=Theme.FG,
            dropdown_hover_color=Theme.PRIMARY,
            corner_radius=Theme.RADIUS, font=Theme.FONT,
            command=lambda v, s=setter: s(v),
        )
        menu.pack(fill="x", padx=10)

    def _bool_field(self, label: str, value: bool,
                    setter: Callable[[bool], None]) -> None:
        var = ctk.BooleanVar(value=value)
        sw = ctk.CTkSwitch(
            self.body, text=label, variable=var,
            text_color=Theme.FG_MUTED, font=("Segoe UI", 10),
            progress_color=Theme.PRIMARY,
            command=lambda: setter(bool(var.get())),
        )
        sw.pack(fill="x", padx=10, pady=(10, 2), anchor="w")
