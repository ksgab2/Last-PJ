import json
from pathlib import Path
import streamlit.components.v1 as components

TPL = Path(__file__).parent.parent / "templates"

def render_page(body_name: str, data: dict | None = None, height: int = 900):
    head = (TPL / "head.html").read_text(encoding="utf-8")
    body = (TPL / f"{body_name}.html").read_text(encoding="utf-8")

    # 1. 데이터가 있으면 </head> 앞에 스크립트 주입
    if data:
        inject = (
            "<script>window.PAGE_DATA = "
            + json.dumps(data, ensure_ascii=False)
            + ";</script>"
        )
        head = head.replace("</head>", f"{inject}\n</head>")

    # 2. 그 다음에 body를 합침
    html = head.replace("</head>", f"<body>{body}</body></html>")

    components.html(html, height=height, scrolling=True)