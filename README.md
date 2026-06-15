<div align="center">

<h1>◆ PyBuilderWeb</h1>

<p><strong>No-Code · WYSIWYG · Static Site Generator</strong></p>

<p>
  Build complete, multi-page websites visually — no HTML, no CSS, no JavaScript knowledge required.<br>
  Compose pages by clicking components, edit their properties live, organise them in a hierarchical site<br>
  and export a clean, responsive, production-ready folder in one click.
</p>

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="CustomTkinter" src="https://img.shields.io/badge/UI-CustomTkinter-7c5cff?style=flat-square">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-22c55e?style=flat-square">
  <img alt="Made by" src="https://img.shields.io/badge/Made%20by-Eduardo%20Roa-f59e0b?style=flat-square">
</p>

</div>

---

## ✨ Features

| Feature | Description | new | 
|---|---|
| 🖼 **WYSIWYG Canvas** | Every component is rendered as a live wireframe block that mirrors the final HTML output |
| 🗂 **Hierarchical Pages** | Organise pages in a tree — `category/subcategory/…` — and they export as nested folders |
| ⚡ **Live Data Binding** | Edit a property in the inspector and the canvas updates instantly |
| 🧩 **9 Built-in Components** | Navbar, Hero, Heading, Paragraph, Button, Image, Card Grid, Divider, Footer |
| 💾 **Save & Load Projects** | Projects are stored as portable `.pbw` (JSON) files |
| 🎨 **Theme System** | Global CSS variables for colors, radius and font — one change, site-wide effect |
| 📤 **Clean HTML Export** | Outputs valid, responsive HTML5 + CSS3 with flexbox, grid and hover transitions |
| 🔌 **Extensible** | Add a new component by subclassing `Node` — it appears in the sidebar automatically |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11 or higher** — [Download](https://www.python.org/downloads/)
- **pip** (bundled with Python)
- A terminal: **PowerShell** on Windows, **Bash / Zsh** on Linux/macOS

---

### 🪟 Windows

```powershell
# 1. Clone the repository
git clone https://github.com/eduardoroa22/PyBuilderWeb.git
cd PyBuilderWeb

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python -m pybuilder
```

> **Tip:** If you get a script execution error, run this first:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```

---

### 🐧 Linux / macOS

```bash
# 1. Clone the repository
git clone https://github.com/your-username/PyBuilderWeb.git
cd PyBuilderWeb

# 2. Create a virtual environment
python3 -m venv .venv

# 3. Activate it
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python -m pybuilder
```

> **Note for Linux:** Tkinter may not be installed by default. Install it with:
> ```bash
> # Ubuntu / Debian
> sudo apt install python3-tk
>
> # Fedora
> sudo dnf install python3-tkinter
>
> # Arch
> sudo pacman -S tk
> ```

---

## 🏗 How to Use

1. **Add pages** — Use the *Site Pages* panel on the left. Right-click a page to add a subpage, rename or delete it.
2. **Add components** — Click any block in the *Components* panel to drop it onto the current page.
3. **Edit properties** — Select a component on the canvas; the *Inspector* panel on the right will show all its editable fields (text, colors, links, etc.).
4. **Reorder components** — Use the ▲ ▼ arrows on each canvas block.
5. **Save your project** — Click **Save** to write a `.pbw` file you can reload later.
6. **Export the site** — Click **✨ Export Site**, choose an output folder, and open the result directly in your browser.

---

## 📁 Project Structure

```
PyBuilderWeb/
├── pybuilder/
│   ├── core/
│   │   ├── node.py           # Base virtual-DOM node
│   │   ├── components.py     # Built-in components (Hero, Navbar, CardGrid, …)
│   │   ├── page.py           # Page = ordered list of nodes + child pages
│   │   ├── site.py           # Site = root page + theme + metadata
│   │   └── exporter.py       # Writes the HTML/CSS folder tree
│   ├── templates/
│   │   └── __init__.py       # Base CSS template (variables + utilities)
│   ├── ui/
│   │   ├── theme.py          # Color & typography tokens for the editor
│   │   ├── pages_panel.py    # Left panel — site page tree
│   │   ├── components_sidebar.py  # Left panel — component catalog
│   │   ├── canvas_view.py    # Center WYSIWYG canvas
│   │   ├── inspector.py      # Right panel — property inspector
│   │   └── app.py            # Main application window
│   └── __main__.py           # Entry point: `python -m pybuilder`
├── requirements.txt
└── README.md
```

---

## 📤 Exported Site Structure

```
output/
├── index.html          ← Home page  /
├── assets/
│   └── style.css       ← Single shared stylesheet
├── services/
│   ├── index.html      ← /services/
│   └── pricing/
│       └── index.html  ← /services/pricing/
└── blog/
    └── index.html      ← /blog/
```

---

## 🧩 Adding a Custom Component

```python
# pybuilder/core/components.py

class Testimonial(Node):
    type_name = "testimonial"
    label     = "Testimonial"
    icon      = "❝"
    default_props = {"quote": "Amazing product!", "author": "Jane Doe"}
    schema = [
        {"key": "quote",  "label": "Quote",  "type": "textarea"},
        {"key": "author", "label": "Author", "type": "text"},
    ]

    def render_html(self) -> str:
        return (f'<blockquote class="pb-testimonial" id="{self.id}">'
                f'<p>{escape(self.props["quote"])}</p>'
                f'<cite>{escape(self.props["author"])}</cite></blockquote>')

# Register it ↓
COMPONENT_REGISTRY["testimonial"] = Testimonial
```

That's it — the component will appear in the sidebar immediately.

---

## 🛠 Tech Stack

- **Python 3.10+** — core language
- **Tkinter** — built-in GUI toolkit
- **CustomTkinter** — modern dark-themed widgets
- **Pillow** — image support

No Electron. No Node.js. No web server. Pure Python.

---

## 📄 License

MIT © 2026 **Eduardo Roa**

---

<div align="center">
  <sub>Built with ◆ PyBuilderWeb · Made by <strong>Eduardo Roa</strong></sub>
</div>
