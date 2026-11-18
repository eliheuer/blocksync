"""Build a portable two-axis proof using the release font and the project's samples."""
from html import escape
from pathlib import Path
import shutil
import tomllib

from fgtools import project
from design_proof import write as write_design_proof

family = project.load()
out = family.root / "output/proof"
out.mkdir(parents=True, exist_ok=True)
font, = (family.fonts / "variable").glob("*.ttf")
shutil.copy2(font, out / font.name)
samples = tomllib.loads((family.sources / "proof-samples.toml").read_text())["sample"]
sections = []
for weight in (400, 700, 900):
    for width in (75, 100, 125):
        lines = "".join(f"<p>{escape(sample['text'])}</p>" for sample in samples.values())
        sections.append(f'<section style="--wght:{weight};--wdth:{width}">'
                        f"<h2>Weight {weight} · Width {width}</h2>{lines}</section>")
(out / "widths.html").write_text(f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Blocksync · Width and weight</title>
<style>
@font-face {{font-family:Blocksync;src:url("{font.name}");font-weight:400 900;font-stretch:75% 125%}}
body {{margin:clamp(1rem,4vw,4rem);font:1rem system-ui;color:#151515}}
main {{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(23rem,100%),1fr));gap:2rem}}
section {{border-top:1px solid;padding-top:.5rem}} h2 {{font:500 1rem system-ui}}
p {{font:clamp(1.35rem,2.5vw,2rem)/1.3 Blocksync;margin:.5em 0;
font-variation-settings:"wght" var(--wght),"wdth" var(--wdth)}}
</style><h1>Blocksync</h1><main>{''.join(sections)}</main></html>""")
print(out / "widths.html")

write_design_proof(font, out)
