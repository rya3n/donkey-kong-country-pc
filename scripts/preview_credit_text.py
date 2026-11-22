"""Preview original credits text with PT-BR accents and a monospaced width guide."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ACCENTED_LETTERS = "ÁÀÂÃÇÉÊÍÓÔÕÚÜ"
PT_BR_LETTERS = frozenset(ACCENTED_LETTERS + ACCENTED_LETTERS.lower())

PAGE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prévia de créditos em PT-BR</title>
<style>
  :root { color-scheme: dark; font: 16px system-ui, sans-serif; background: #12211f; color: #ecf2e7; }
  body { margin: 0; padding: clamp(1rem, 5vw, 3.5rem); }
  main { max-width: 700px; margin: auto; }
  h1 { margin: 0; font-size: clamp(1.4rem, 4vw, 2rem); }
  p { color: #c7d8cb; }
  #viewport { height: min(48vh, 340px); position: relative; overflow: hidden; background: #081210;
    border: 1px solid #526761; border-radius: 10px; font: clamp(.65rem, 2.9vw, 1.15rem)/1.6 "Courier New", monospace; }
  #guide { position: absolute; inset: 0; margin: auto; width: min(var(--columns) * 1ch, 100%);
    border-inline: 1px dashed #799188; pointer-events: none; }
  #credits { position: absolute; inset-inline: 0; margin: 0; text-align: center; white-space: pre; }
  #credits div { min-height: 1.6em; }
  .wide { color: #ffd28e; }
  .controls { display: flex; gap: .75rem; align-items: center; margin: 1rem 0; }
  button { border: 0; border-radius: 6px; padding: .55rem .85rem; background: #daf0bd; color: #12211f;
    font: inherit; font-weight: 650; cursor: pointer; }
  input { flex: 1; min-width: 3rem; accent-color: #daf0bd; }
  output { min-width: 4ch; text-align: end; font-variant-numeric: tabular-nums; }
  aside { padding-block: .45rem; color: #c7d8cb; }
  summary { cursor: pointer; }
  li { margin-block: .35rem; }
</style>
</head>
<body>
<main>
  <h1>Prévia de créditos em PT-BR</h1>
  <p>As guias marcam uma referência de __COLUMNS__ caracteres por linha. __SUMMARY__</p>
  <div id="viewport" style="--columns: __COLUMNS__" aria-label="Prévia da rolagem">
    <div id="guide"></div>
    <div id="credits">__ROWS__</div>
  </div>
  <div class="controls">
    <button id="toggle" type="button">Reproduzir</button>
    <input id="position" type="range" min="0" max="1000" value="0" aria-label="Posição da rolagem">
    <output id="percentage" for="position">0%</output>
  </div>
  __DETAILS__
</main>
<script>
  const viewport = document.getElementById("viewport");
  const credits = document.getElementById("credits");
  const toggle = document.getElementById("toggle");
  const position = document.getElementById("position");
  const percentage = document.getElementById("percentage");
  const speed = 26;
  let animation = null;
  let previousTime = null;
  let progress = viewport.clientHeight * 0.65 / distance();

  function distance() {
    return viewport.clientHeight + credits.offsetHeight;
  }

  function render() {
    credits.style.transform = "translateY(" + (viewport.clientHeight - distance() * progress) + "px)";
    position.value = Math.round(progress * 1000);
    percentage.value = Math.round(progress * 100) + "%";
  }

  function pause() {
    if (animation !== null) cancelAnimationFrame(animation);
    animation = null;
    previousTime = null;
    toggle.textContent = "Reproduzir";
  }

  function tick(time) {
    if (previousTime !== null) {
      progress = Math.min(1, progress + (time - previousTime) * speed / (1000 * distance()));
    }
    previousTime = time;
    render();
    if (progress === 1) pause();
    else animation = requestAnimationFrame(tick);
  }

  toggle.addEventListener("click", () => {
    if (animation !== null) {
      pause();
      return;
    }
    if (progress === 1) progress = 0;
    toggle.textContent = "Pausar";
    animation = requestAnimationFrame(tick);
  });

  position.addEventListener("input", () => {
    progress = Number(position.value) / 1000;
    previousTime = null;
    render();
  });

  window.addEventListener("resize", render);
  render();
</script>
</body>
</html>
"""


def read_lines(path: Path) -> list[str]:
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(document, list) or not document:
        raise ValueError("Use uma lista JSON de linhas de texto.")
    lines = []
    for number, value in enumerate(document, 1):
        if not isinstance(value, str):
            raise ValueError(f"Linha {number}: esperado texto.")
        line = unicodedata.normalize("NFC", value)
        if any(not (" " <= char <= "~" or char in PT_BR_LETTERS) for char in line):
            raise ValueError(f"Linha {number}: caractere fora do conjunto de prévia.")
        lines.append(line)
    if not any(line.strip() for line in lines):
        raise ValueError("Inclua pelo menos uma linha com texto.")
    return lines


def render_preview(lines: list[str], columns: int) -> str:
    wide = [(number, len(line)) for number, line in enumerate(lines, 1) if len(line) > columns]
    wide_numbers = {number for number, _ in wide}
    rows = []
    for number, line in enumerate(lines, 1):
        mark = ' class="wide"' if number in wide_numbers else ""
        rows.append(f"<div{mark}>{html.escape(line)}</div>")
    summary = "Todas as linhas cabem na referência."
    details = ""
    if wide:
        summary = f"{len(wide)} de {len(lines)} linhas ultrapassam a referência."
        items = "".join(f"<li>Linha {number} com {length} caracteres</li>" for number, length in wide)
        details = "<aside><details open><summary>Linhas largas</summary><ul>" + items + "</ul></details></aside>"
    return PAGE.replace("__COLUMNS__", str(columns)).replace("__SUMMARY__", summary).replace(
        "__DETAILS__", details).replace("__ROWS__", "".join(rows))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Arquivo JSON com uma lista de linhas")
    parser.add_argument("--columns", required=True, type=int, help="Largura de referência em caracteres")
    parser.add_argument("--out", required=True, type=Path, help="Arquivo HTML dentro de evidence/ ou experimental/")
    args = parser.parse_args()
    if not 1 <= args.columns <= 32:
        parser.error("Informe de 1 a 32 colunas.")
    out = args.out.resolve()
    if out.suffix.lower() != ".html" or not any(
        out.is_relative_to(ROOT / folder) for folder in ("evidence", "experimental")
    ):
        parser.error("Use um arquivo .html dentro de evidence/ ou experimental/.")
    try:
        lines = read_lines(args.input)
        page = render_preview(lines, args.columns)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(page)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({
        "lines": len(lines),
        "reference_columns": args.columns,
        "lines_over_reference": sum(len(line) > args.columns for line in lines),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
