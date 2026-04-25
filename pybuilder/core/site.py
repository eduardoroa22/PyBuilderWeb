"""Site: hierarchical collection of pages plus global metadata."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

from .page import Page


class Site:
    """Represents the whole project."""

    def __init__(self, name: str = "My Site"):
        self.name = name
        self.description = "Generated with PyBuilderWeb"
        self.author = ""
        # Global theme (injected as CSS variables)
        self.theme: dict[str, str] = {
            "primary": "#6366f1",
            "secondary": "#22d3ee",
            "bg": "#ffffff",
            "fg": "#0f172a",
            "muted": "#64748b",
            "radius": "14px",
            "font": "'Inter', system-ui, -apple-system, Segoe UI, sans-serif",
        }
        # Root page represents "/" (index.html)
        self.root: Page = Page(title="Home", slug="")

    # ---- iteration ------------------------------------------------------
    def walk(self) -> Iterator[tuple[Page, list[Page]]]:
        """Iterate (page, ancestors)."""
        def _walk(page: Page, ancestors: list[Page]):
            yield page, ancestors
            for child in page.children:
                yield from _walk(child, ancestors + [page])
        yield from _walk(self.root, [])

    def find_page(self, page_id: str) -> tuple[Page, Page | None] | tuple[None, None]:
        """Returns (page, parent) or (None, None)."""
        def _search(page: Page, parent: Page | None):
            if page.id == page_id:
                return page, parent
            for c in page.children:
                r = _search(c, page)
                if r:
                    return r
            return None
        result = _search(self.root, None)
        return result if result else (None, None)

    def page_url(self, page: Page) -> str:
        """Build the /category/sub/ path for a page."""
        for p, ancestors in self.walk():
            if p is page:
                slugs = [a.slug for a in ancestors if a.slug] + (
                    [p.slug] if p.slug else []
                )
                if not slugs:
                    return "/"
                return "/" + "/".join(slugs) + "/"
        return "/"

    # ---- serialization --------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "author": self.author,
            "theme": dict(self.theme),
            "root": self.root.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Site":
        site = cls(name=data.get("name", "My Site"))
        site.description = data.get("description", "")
        site.author = data.get("author", "")
        site.theme.update(data.get("theme", {}))
        site.root = Page.from_dict(data["root"])
        return site

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
                              encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Site":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)
