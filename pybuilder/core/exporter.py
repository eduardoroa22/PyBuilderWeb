"""Exporter: turns a `Site` into an actual folder tree of HTML/CSS files."""
from __future__ import annotations

import shutil
from pathlib import Path

from ..templates import base_css
from .page import Page
from .site import Site


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title}</title>
  <link rel="stylesheet" href="{css_path}">
</head>
<body>
{body}
</body>
</html>
"""


class Exporter:
    """Generates the site files on disk.

    Resulting structure:
        output/
          index.html
          assets/style.css
          category/
            index.html
            subcategory/
              index.html
    """

    def __init__(self, site: Site):
        self.site = site

    # ------------------------------------------------------------------
    def export(self, output_dir: str | Path, clean: bool = False) -> Path:
        out = Path(output_dir).resolve()
        if clean and out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True, exist_ok=True)

        # 1. Build the global CSS plus per-node CSS.
        css = self._build_global_css()
        assets = out / "assets"
        assets.mkdir(exist_ok=True)
        (assets / "style.css").write_text(css, encoding="utf-8")

        # 2. Walk the page tree and create folders + index.html.
        self._render_page(self.site.root, out, depth=0)
        return out

    # ------------------------------------------------------------------
    def _build_global_css(self) -> str:
        css = [base_css(self.site.theme)]
        for page, _ in self.site.walk():
            for node in page.nodes:
                snippet = node.render_css()
                if snippet:
                    css.append(snippet)
        return "\n\n".join(css)

    def _render_page(self, page: Page, base_dir: Path, depth: int) -> None:
        # The root page lives in base_dir; children live in subfolders named after their slug.
        if depth == 0:
            page_dir = base_dir
        else:
            page_dir = base_dir / page.slug
            page_dir.mkdir(parents=True, exist_ok=True)

        css_relative = ("../" * depth) + "assets/style.css" if depth else "assets/style.css"
        body_parts = [node.render_html() for node in page.nodes]
        body = "\n".join(body_parts) if body_parts else (
            '<main style="padding:80px;text-align:center;color:#64748b">'
            '<h1>Empty page</h1><p>Add components to see them here.</p></main>'
        )

        html = HTML_TEMPLATE.format(
            title=page.title or self.site.name,
            description=page.description or self.site.description,
            css_path=css_relative,
            body=body,
        )
        (page_dir / "index.html").write_text(html, encoding="utf-8")

        for child in page.children:
            self._render_page(child, page_dir, depth + 1)
