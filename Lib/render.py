import json
from pathlib import Path
import streamlit.components.v1 as components

TPL = Path(__file__).parent.parent / "templates"

def render_page(body_name: str, data: dict | None = None, height: int = 900):
    head = (TPL / "head.html").read_text(encoding="utf-8")
    body = (TPL / f"{body_name}.html").read_text(encoding="utf-8")
    html = head.replace("</head>", f"<body>{body}</body></html>")

    if data:
        inject = (
            "<script>window.PAGE_DATA = "
            + json.dumps(data, ensure_ascii=False)
            + ";</script></head>"
        )
        html = html.replace("</head>", inject, 1)

    components.html(html, height=height, scrolling=True)