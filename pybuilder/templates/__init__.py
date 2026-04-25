"""Base CSS template injected into every export."""
from __future__ import annotations


def base_css(theme: dict[str, str]) -> str:
    return f""":root {{
  --pb-primary: {theme['primary']};
  --pb-secondary: {theme['secondary']};
  --pb-bg: {theme['bg']};
  --pb-fg: {theme['fg']};
  --pb-muted: {theme['muted']};
  --pb-radius: {theme['radius']};
  --pb-font: {theme['font']};
}}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  font-family: var(--pb-font);
  background: var(--pb-bg);
  color: var(--pb-fg);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--pb-primary); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
img {{ max-width: 100%; display: block; }}

/* ---------- Layout ---------- */
.pb-section {{
  max-width: 1100px;
  margin: 0 auto;
  padding: 64px 24px;
}}
.pb-section__title {{
  font-size: 2rem;
  margin: 0 0 32px;
  text-align: center;
}}

/* ---------- Navbar ---------- */
.pb-navbar {{
  background: var(--nav-bg, #0f172a);
  color: var(--nav-fg, #f8fafc);
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 2px 12px rgba(0,0,0,.08);
}}
.pb-navbar__inner {{
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}
.pb-navbar__brand {{
  color: inherit;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: .3px;
}}
.pb-navbar__links {{
  list-style: none;
  display: flex;
  gap: 24px;
  margin: 0;
  padding: 0;
}}
.pb-navbar__links a {{
  color: inherit;
  font-weight: 500;
  position: relative;
}}
.pb-navbar__links a:hover {{
  color: var(--nav-accent, #22d3ee);
  text-decoration: none;
}}

/* ---------- Hero ---------- */
.pb-hero {{ padding: 96px 24px; }}
.pb-hero__inner {{ max-width: 900px; margin: 0 auto; }}
.pb-hero__title {{
  font-size: clamp(2rem, 4vw, 3.4rem);
  margin: 0 0 18px;
  font-weight: 800;
  letter-spacing: -.02em;
}}
.pb-hero__subtitle {{
  font-size: 1.15rem;
  opacity: .92;
  margin: 0 0 28px;
}}

/* ---------- Buttons ---------- */
.pb-btn {{
  display: inline-block;
  padding: 12px 22px;
  border-radius: var(--pb-radius);
  font-weight: 600;
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}}
.pb-btn:hover {{ transform: translateY(-2px); text-decoration: none; }}
.pb-btn--primary {{
  background: var(--pb-primary);
  color: #fff;
  box-shadow: 0 8px 20px -8px var(--pb-primary);
}}
.pb-btn--secondary {{
  background: var(--pb-secondary);
  color: #062a30;
}}
.pb-btn--ghost {{
  background: transparent;
  color: inherit;
  border: 2px solid currentColor;
}}
.pb-btn-wrap {{ margin: 16px 0; }}

/* ---------- Headings & paragraphs ---------- */
.pb-heading {{
  max-width: 1100px;
  margin: 32px auto 12px;
  padding: 0 24px;
}}
.pb-paragraph {{
  max-width: 800px;
  margin: 0 auto 16px;
  padding: 0 24px;
  color: var(--pb-fg);
}}

/* ---------- Image ---------- */
.pb-image {{
  max-width: 1100px;
  margin: 24px auto;
  padding: 0 24px;
}}
.pb-image--rounded img {{
  border-radius: var(--pb-radius);
  box-shadow: 0 20px 50px -25px rgba(0,0,0,.35);
}}

/* ---------- Card grid ---------- */
.pb-grid {{ display: grid; gap: 22px; }}
.pb-grid--cols-2 {{ grid-template-columns: repeat(2, 1fr); }}
.pb-grid--cols-3 {{ grid-template-columns: repeat(3, 1fr); }}
.pb-grid--cols-4 {{ grid-template-columns: repeat(4, 1fr); }}
@media (max-width: 880px) {{
  .pb-grid {{ grid-template-columns: 1fr !important; }}
}}
.pb-card {{
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: var(--pb-radius);
  padding: 24px;
  transition: transform .2s ease, box-shadow .2s ease;
}}
.pb-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 18px 40px -20px rgba(15,23,42,.25);
}}
.pb-card__icon {{
  font-size: 1.8rem;
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  border-radius: 12px;
  background: color-mix(in srgb, var(--pb-primary) 15%, transparent);
  color: var(--pb-primary);
  margin-bottom: 14px;
}}
.pb-card h3 {{ margin: 0 0 8px; }}
.pb-card p {{ margin: 0; color: var(--pb-muted); }}

/* ---------- Divider ---------- */
.pb-divider {{ border: none; height: 1px; background: #e2e8f0; max-width: 1100px; margin: 24px auto; }}
.pb-divider--small {{ margin: 12px auto; }}
.pb-divider--large {{ margin: 56px auto; }}

/* ---------- Footer ---------- */
.pb-footer {{
  padding: 28px 24px;
  text-align: center;
  font-size: .95rem;
}}
.pb-footer p {{ margin: 0; }}
"""
