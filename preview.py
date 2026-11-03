#!/usr/bin/env python3
"""Render README.md exactly via GitHub's markdown API (gh) into preview.html with GitHub dark styling."""
import subprocess, webbrowser
from pathlib import Path
root = Path(__file__).parent
md = (root / "README.md").read_text(encoding="utf-8")
html = subprocess.run(["gh", "api", "markdown", "-f", f"text={md}", "-f", "mode=gfm"],
                      capture_output=True, text=True, check=True).stdout
css = """body{background:#0d1117;color:#e6edf3;font-family:-apple-system,'Segoe UI',sans-serif;max-width:1012px;margin:24px auto;padding:0 32px}
pre{background:#161b22;padding:16px;border-radius:6px;font:13.6px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace;overflow:auto}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:#343942;padding:.2em .4em;border-radius:6px}
pre code{background:none;padding:0} img{max-width:100%}"""
out = root / "preview.html"
out.write_text(f"<!doctype html><meta charset=utf-8><title>README preview</title><style>{css}</style>{html}", encoding="utf-8")
webbrowser.open(out.as_uri())
print(out)
