"""Base node of the virtual DOM.

Every visual building block in a page is a `Node` with editable properties.
Nodes know how to render themselves to HTML, generate optional instance CSS
and serialize to JSON.
"""
from __future__ import annotations

import copy
import html
import uuid
from typing import Any, ClassVar


def escape(text: str | None) -> str:
    """Escape text for HTML, preserving line breaks as <br>."""
    if text is None:
        return ""
    return html.escape(str(text)).replace("\n", "<br>")


class Node:
    """Represents a visual component in a page.

    Attributes:
        type_name: identifier of the component type (e.g. "hero").
        label: human readable name shown in the UI.
        props: dictionary of editable properties.
        schema: description of editable fields, consumed by the inspector.
    """

    type_name: ClassVar[str] = "node"
    label: ClassVar[str] = "Node"
    icon: ClassVar[str] = "▭"
    schema: ClassVar[list[dict[str, Any]]] = []
    default_props: ClassVar[dict[str, Any]] = {}

    def __init__(self, props: dict[str, Any] | None = None, node_id: str | None = None):
        self.id = node_id or f"n_{uuid.uuid4().hex[:8]}"
        self.props = self._build_props(props)

    def _build_props(self, props: dict[str, Any] | None) -> dict[str, Any]:
        values = copy.deepcopy(self.default_props)
        if props:
            values.update(props)
        return values

    # ---- API that each component may override ---------------------------
    def render_html(self) -> str:
        return (
            f'<div class="pb-node pb-node--{self.type_name}" id="{self.id}">'
            f'{escape(self.props.get("text", self.label))}</div>'
        )

    def render_css(self) -> str:
        """Per-instance CSS (optional)."""
        return ""

    # ---- Visual representation in the Tkinter canvas --------------------
    def preview_summary(self) -> str:
        """Short text describing the node in the wireframe."""
        return self.props.get("text") or self.label

    def preview_color(self) -> str:
        """Accent color used for the wireframe block."""
        return "#3b82f6"

    def preview_height(self) -> int:
        return 90

    # ---- Serialization --------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "type": self.type_name, "props": dict(self.props)}

    # ---- Helpers --------------------------------------------------------
    def get_prop(self, key: str, default: Any = None) -> Any:
        return self.props.get(key, default)

    def set_prop(self, key: str, value: Any) -> None:
        self.props[key] = value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} type={self.type_name} props={self.props!r}>"
