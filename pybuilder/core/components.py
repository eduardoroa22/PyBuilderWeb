"""Catalog of components available to build pages.

Each component:
  * Defines its `schema` (editable fields shown in the inspector).
  * Knows how to render its final HTML.
  * Provides a friendly visual representation for the WYSIWYG canvas.
"""
from __future__ import annotations

from typing import Any

from .node import Node, escape


# -------------------------------------------------------------------
# Components
# -------------------------------------------------------------------
class Navbar(Node):
    type_name = "navbar"
    label = "Navigation Bar"
    icon = "☰"
    default_props = {
        "brand": "MySite",
        "links": "Home, Services, Blog, Contact",
        "bg": "#0f172a",
        "fg": "#f8fafc",
        "accent": "#22d3ee",
    }
    schema = [
        {"key": "brand", "label": "Brand", "type": "text"},
        {"key": "links", "label": "Links (comma separated)", "type": "text"},
        {"key": "bg", "label": "Background", "type": "color"},
        {"key": "fg", "label": "Text", "type": "color"},
        {"key": "accent", "label": "Accent", "type": "color"},
    ]

    def render_html(self) -> str:
        items = [l.strip() for l in self.props["links"].split(",") if l.strip()]
        lis = "\n      ".join(
            f'<li><a href="#{escape(l.lower().replace(" ", "-"))}">{escape(l)}</a></li>'
            for l in items
        )
        return f'''<nav class="pb-navbar" id="{self.id}">
  <div class="pb-navbar__inner">
    <a class="pb-navbar__brand" href="#">{escape(self.props["brand"])}</a>
    <ul class="pb-navbar__links">
      {lis}
    </ul>
  </div>
</nav>'''

    def render_css(self) -> str:
        return f'''#{self.id} {{
  --nav-bg: {self.props["bg"]};
  --nav-fg: {self.props["fg"]};
  --nav-accent: {self.props["accent"]};
}}'''

    def preview_summary(self) -> str:
        return f"☰  {self.props['brand']}   ·   {self.props['links']}"

    def preview_color(self) -> str:
        return self.props["bg"]

    def preview_height(self) -> int:
        return 56


class Hero(Node):
    type_name = "hero"
    label = "Hero Section"
    icon = "★"
    default_props = {
        "title": "Build websites without writing code",
        "subtitle": "A magical tool made 100% in Python.",
        "cta_text": "Get started",
        "cta_link": "#",
        "bg": "#6366f1",
        "fg": "#ffffff",
        "align": "center",
    }
    schema = [
        {"key": "title", "label": "Title", "type": "text"},
        {"key": "subtitle", "label": "Subtitle", "type": "textarea"},
        {"key": "cta_text", "label": "Button text", "type": "text"},
        {"key": "cta_link", "label": "Button link", "type": "text"},
        {"key": "bg", "label": "Background", "type": "color"},
        {"key": "fg", "label": "Text", "type": "color"},
        {"key": "align", "label": "Alignment", "type": "choice",
         "options": ["left", "center", "right"]},
    ]

    def render_html(self) -> str:
        return f'''<section class="pb-hero" id="{self.id}">
  <div class="pb-hero__inner">
    <h1 class="pb-hero__title">{escape(self.props["title"])}</h1>
    <p class="pb-hero__subtitle">{escape(self.props["subtitle"])}</p>
    <a class="pb-btn pb-btn--primary" href="{escape(self.props["cta_link"])}">{escape(self.props["cta_text"])}</a>
  </div>
</section>'''

    def render_css(self) -> str:
        return f'''#{self.id} {{
  background: linear-gradient(135deg, {self.props["bg"]}, color-mix(in srgb, {self.props["bg"]} 60%, #000 40%));
  color: {self.props["fg"]};
  text-align: {self.props["align"]};
}}'''

    def preview_summary(self) -> str:
        return f"★  {self.props['title']}"

    def preview_color(self) -> str:
        return self.props["bg"]

    def preview_height(self) -> int:
        return 140


class Heading(Node):
    type_name = "heading"
    label = "Heading"
    icon = "H"
    default_props = {"text": "A bold headline", "level": "h2", "align": "left"}
    schema = [
        {"key": "text", "label": "Text", "type": "text"},
        {"key": "level", "label": "Level", "type": "choice",
         "options": ["h1", "h2", "h3", "h4"]},
        {"key": "align", "label": "Alignment", "type": "choice",
         "options": ["left", "center", "right"]},
    ]

    def render_html(self) -> str:
        lvl = self.props["level"]
        return (f'<{lvl} class="pb-heading" id="{self.id}" '
                f'style="text-align:{self.props["align"]}">'
                f'{escape(self.props["text"])}</{lvl}>')

    def preview_summary(self) -> str:
        return f"H · {self.props['text']}"

    def preview_color(self) -> str:
        return "#0ea5e9"

    def preview_height(self) -> int:
        return 60


class Paragraph(Node):
    type_name = "paragraph"
    label = "Paragraph"
    icon = "¶"
    default_props = {
        "text": "Write your content here. Tell your story, describe a service "
                "or explain any idea you want to share with your visitors.",
        "align": "left",
    }
    schema = [
        {"key": "text", "label": "Text", "type": "textarea"},
        {"key": "align", "label": "Alignment", "type": "choice",
         "options": ["left", "center", "right", "justify"]},
    ]

    def render_html(self) -> str:
        return (f'<p class="pb-paragraph" id="{self.id}" '
                f'style="text-align:{self.props["align"]}">'
                f'{escape(self.props["text"])}</p>')

    def preview_summary(self) -> str:
        text = self.props["text"]
        return "¶ " + (text[:80] + "…" if len(text) > 80 else text)

    def preview_color(self) -> str:
        return "#64748b"

    def preview_height(self) -> int:
        return 80


class Button(Node):
    type_name = "button"
    label = "Button"
    icon = "◉"
    default_props = {
        "text": "Click me",
        "link": "#",
        "style": "primary",
        "align": "left",
    }
    schema = [
        {"key": "text", "label": "Text", "type": "text"},
        {"key": "link", "label": "Link", "type": "text"},
        {"key": "style", "label": "Style", "type": "choice",
         "options": ["primary", "secondary", "ghost"]},
        {"key": "align", "label": "Alignment", "type": "choice",
         "options": ["left", "center", "right"]},
    ]

    def render_html(self) -> str:
        return (f'<div class="pb-btn-wrap" style="text-align:{self.props["align"]}">'
                f'<a class="pb-btn pb-btn--{self.props["style"]}" id="{self.id}" '
                f'href="{escape(self.props["link"])}">{escape(self.props["text"])}</a></div>')

    def preview_summary(self) -> str:
        return f"◉  [ {self.props['text']} ]"

    def preview_color(self) -> str:
        return "#22c55e"

    def preview_height(self) -> int:
        return 56


class Image(Node):
    type_name = "image"
    label = "Image"
    icon = "🖼"
    default_props = {
        "src": "https://picsum.photos/1200/500",
        "alt": "Illustrative image",
        "rounded": True,
    }
    schema = [
        {"key": "src", "label": "Image URL", "type": "text"},
        {"key": "alt", "label": "Alt text", "type": "text"},
        {"key": "rounded", "label": "Rounded corners", "type": "bool"},
    ]

    def render_html(self) -> str:
        cls = "pb-image" + (" pb-image--rounded" if self.props["rounded"] else "")
        return (f'<figure class="{cls}" id="{self.id}">'
                f'<img src="{escape(self.props["src"])}" alt="{escape(self.props["alt"])}">'
                f'</figure>')

    def preview_summary(self) -> str:
        return f"🖼  {self.props['alt']}"

    def preview_color(self) -> str:
        return "#a855f7"

    def preview_height(self) -> int:
        return 110


class CardGrid(Node):
    type_name = "cardgrid"
    label = "Card Grid"
    icon = "▦"
    default_props = {
        "title": "Our services",
        "cards": (
            "Web Design | Modern and responsive interfaces. | ✦\n"
            "Development | Clean, scalable code. | ⚙\n"
            "Support | Continuous companionship. | ♥"
        ),
        "columns": "3",
    }
    schema = [
        {"key": "title", "label": "Section title", "type": "text"},
        {"key": "cards", "label": "Cards (title | description | icon, one per line)",
         "type": "textarea"},
        {"key": "columns", "label": "Columns", "type": "choice",
         "options": ["2", "3", "4"]},
    ]

    def _parse_cards(self) -> list[tuple[str, str, str]]:
        out = []
        for line in self.props["cards"].splitlines():
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split("|", 2)]
            parts += [""] * (3 - len(parts))
            title, description, icon = parts
            out.append((title, description, icon))
        return out

    def render_html(self) -> str:
        cards_html = "\n    ".join(
            f'<article class="pb-card"><div class="pb-card__icon">{escape(icon)}</div>'
            f'<h3>{escape(t)}</h3><p>{escape(d)}</p></article>'
            for t, d, icon in self._parse_cards()
        )
        return f'''<section class="pb-section" id="{self.id}">
  <h2 class="pb-section__title">{escape(self.props["title"])}</h2>
  <div class="pb-grid pb-grid--cols-{self.props["columns"]}">
    {cards_html}
  </div>
</section>'''

    def preview_summary(self) -> str:
        n = len(self._parse_cards())
        return f"▦  {self.props['title']}  ({n} cards, {self.props['columns']} cols)"

    def preview_color(self) -> str:
        return "#f59e0b"

    def preview_height(self) -> int:
        return 130


class Divider(Node):
    type_name = "divider"
    label = "Divider"
    icon = "—"
    default_props = {"space": "medium"}
    schema = [
        {"key": "space", "label": "Spacing", "type": "choice",
         "options": ["small", "medium", "large"]},
    ]

    def render_html(self) -> str:
        return f'<hr class="pb-divider pb-divider--{self.props["space"]}" id="{self.id}">'

    def preview_summary(self) -> str:
        return "— — — — — — — — — —"

    def preview_color(self) -> str:
        return "#94a3b8"

    def preview_height(self) -> int:
        return 30


class Footer(Node):
    type_name = "footer"
    label = "Footer"
    icon = "▁"
    default_props = {
        "text": "© 2026 MySite. Made with PyBuilderWeb.",
        "bg": "#0f172a",
        "fg": "#cbd5e1",
    }
    schema = [
        {"key": "text", "label": "Text", "type": "text"},
        {"key": "bg", "label": "Background", "type": "color"},
        {"key": "fg", "label": "Text", "type": "color"},
    ]

    def render_html(self) -> str:
        return (f'<footer class="pb-footer" id="{self.id}">'
                f'<p>{escape(self.props["text"])}</p></footer>')

    def render_css(self) -> str:
        return (f'#{self.id} {{ background: {self.props["bg"]}; '
                f'color: {self.props["fg"]}; }}')

    def preview_summary(self) -> str:
        return f"▁  {self.props['text']}"

    def preview_color(self) -> str:
        return self.props["bg"]

    def preview_height(self) -> int:
        return 60


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
COMPONENT_REGISTRY: dict[str, type[Node]] = {
    cls.type_name: cls for cls in [
        Navbar, Hero, Heading, Paragraph, Button, Image, CardGrid, Divider, Footer
    ]
}


def create_component(type_name: str, props: dict[str, Any] | None = None,
                     node_id: str | None = None) -> Node:
    cls = COMPONENT_REGISTRY.get(type_name)
    if cls is None:
        raise ValueError(f"Unknown component type: {type_name!r}")
    return cls(props=props, node_id=node_id)
