import markdown
import subprocess
import os
import sys
from pathlib import Path

base = Path(r"C:\Users\Fury IT\Dan\07_CONSTRUCTION\Complex_20m")
md_file = base / "HANDOVER_Prorab_Inzhener.md"
html_file = base / "HANDOVER_Prorab_Inzhener.html"
pdf_file = base / "HANDOVER_Prorab_Inzhener.pdf"

with open(md_file, "r", encoding="utf-8") as f:
    md_text = f.read()

html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"],
)

css = """
@page { size: A4; margin: 18mm 15mm; }
* { box-sizing: border-box; }
body {
    font-family: "Segoe UI", "Calibri", "Arial", sans-serif;
    font-size: 10.5pt;
    line-height: 1.45;
    color: #1a1a1a;
    max-width: 100%;
}
h1 { font-size: 20pt; color: #0d3b66; border-bottom: 2px solid #0d3b66;
     padding-bottom: 6px; margin-top: 18px; page-break-after: avoid; }
h2 { font-size: 15pt; color: #144d77; border-bottom: 1px solid #b0c4d8;
     padding-bottom: 4px; margin-top: 22px; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #1d6091; margin-top: 16px; page-break-after: avoid; }
h4 { font-size: 11pt; color: #245a82; margin-top: 12px; page-break-after: avoid; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0 6px 22px; padding: 0; }
li { margin-bottom: 3px; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
th, td {
    border: 1px solid #95a5b3;
    padding: 5px 7px;
    text-align: left;
    vertical-align: top;
}
th { background: #d8e4ef; color: #0d3b66; font-weight: 600; }
tr:nth-child(even) td { background: #f4f8fb; }
code { background: #f0f2f5; padding: 1px 4px; border-radius: 3px;
       font-family: "Consolas", monospace; font-size: 9.5pt; }
pre { background: #f6f8fa; padding: 10px; border-radius: 5px;
      border-left: 3px solid #0d3b66; overflow-x: auto;
      font-size: 9.5pt; page-break-inside: avoid; }
blockquote { border-left: 4px solid #f0a830; padding: 4px 12px;
             background: #fff8e6; margin: 8px 0; color: #5a3e0c; }
hr { border: 0; border-top: 1px solid #c0ccda; margin: 16px 0; }
strong { color: #0d3b66; }
a { color: #1d6091; text-decoration: none; }
"""

html_full = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Передача проекта — Многофункциональный комплекс 20×10 м</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_full)

print(f"HTML written: {html_file}")

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
edge = next((p for p in edge_paths if os.path.exists(p)), None)
if not edge:
    print("ERROR: Edge not found")
    sys.exit(1)

cmd = [
    edge,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_file}",
    html_file.as_uri(),
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
if pdf_file.exists():
    size_kb = pdf_file.stat().st_size / 1024
    print(f"PDF created: {pdf_file} ({size_kb:.1f} KB)")
else:
    print("ERROR: PDF not created")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    sys.exit(1)
