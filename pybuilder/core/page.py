"""Page: ordered container of nodes with metadata and a hierarchical slug."""
from __future__ import annotations

import re
import uuid
from typing import Any

from .components import create_component
from .node import Node


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"ñ", "n", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "page"


class Page:
    """A site page. Holds its title, slug and tree of nodes."""

    def __init__(self, title: str = "Home", slug: str | None = None,
                 page_id: str | None = None):
        self.id = page_id or f"p_{uuid.uuid4().hex[:8]}"
        self.title = title
        self.slug = slug if slug is not None else slugify(title)
        self.description = ""
        self.nodes: list[Node] = []
        self.children: list[Page] = []  # subpages (categories -> subcategories)

    # ---- node management ------------------------------------------------
    def add_node(self, node: Node, index: int | None = None) -> Node:
        if index is None:
            self.nodes.append(node)
        else:
            self.nodes.insert(index, node)
        return node

    def remove_node(self, node_id: str) -> None:
        self.nodes = [n for n in self.nodes if n.id != node_id]

    def find_node(self, node_id: str) -> Node | None:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def move_node(self, node_id: str, delta: int) -> None:
        for i, n in enumerate(self.nodes):
            if n.id == node_id:
                j = max(0, min(len(self.nodes) - 1, i + delta))
                if i != j:
                    self.nodes.pop(i)
                    self.nodes.insert(j, n)
                return

    # ---- subpages -------------------------------------------------------
    def add_child(self, page: "Page") -> "Page":
        self.children.append(page)
        return page

    def remove_child(self, page_id: str) -> None:
        self.children = [p for p in self.children if p.id != page_id]

    # ---- serialization --------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "description": self.description,
            "nodes": [n.to_dict() for n in self.nodes],
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Page":
        page = cls(title=data.get("title", "Home"),
                   slug=data.get("slug"),
                   page_id=data.get("id"))
        page.description = data.get("description", "")
        for nd in data.get("nodes", []):
            page.nodes.append(create_component(nd["type"], nd.get("props"), nd.get("id")))
        for cd in data.get("children", []):
            page.children.append(cls.from_dict(cd))
        return page
