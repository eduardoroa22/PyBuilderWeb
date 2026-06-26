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

Props = dict[str, Any]
SchemaField = dict[str, Any]


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
    schema: ClassVar[list[SchemaField]] = []
    default_props: ClassVar[Props] = {}

    def __init__(self, props: Props | None = None, node_id: str | None = None):
        self.id = node_id or f"n_{uuid.uuid4().hex[:8]}"
        self.props = self._build_props(props)

    def _build_props(self, props: Props | None) -> Props:
        values = copy.deepcopy(self.default_props)
        if props:
            values.update(props)
        return values

    @staticmethod
    def generate_id(prefix: str = "n") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:8]}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Node":
        return cls(props=data.get("props"), node_id=data.get("id"))

    def duplicate(self, node_id: str | None = None,
                  overrides: Props | None = None) -> "Node":
        props = dict(self.props)
        if overrides:
            props.update(overrides)
        return self.__class__(props=props, node_id=node_id)

    def update_props(self, props: Props) -> None:
        self.props.update(props)

    def reset_props(self) -> None:
        self.props = self._build_props(None)

    def __getitem__(self, key: str) -> Any:
        return self.props[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.props[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.props

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
