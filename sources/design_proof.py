"""Render the current quality-review examples from shaped, interpolated outlines."""

from html import escape
from itertools import product

from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
import pathops
import uharfbuzz as hb


def svg_path(outline, color):
    pen = SVGPathPen(None)
    outline.draw(pen)
    return f'<path fill="{color}" d="{pen.getCommands()}"/>'


def pair_figure(font, face, text, width, weight):
    location = {"wdth": width, "wght": weight}
    glyphs = font.getGlyphSet(location=location)
    hb_font = hb.Font(face)
    hb_font.set_variations(location)
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(hb_font, buffer)
    outlines = []
    cursor = 0
    for info, pos in zip(buffer.glyph_infos, buffer.glyph_positions):
        outline = pathops.Path()
        pen = DecomposingRecordingPen(glyphs)
        glyphs[font.getGlyphName(info.codepoint)].draw(pen)
        pen.replay(TransformPen(outline.getPen(), (1, 0, 0, 1, cursor + pos.x_offset, pos.y_offset)))
        outlines.append(outline)
        cursor += pos.x_advance
    first, second = outlines
    intersection = pathops.op(first, second, pathops.PathOp.INTERSECTION)
    left = min(first.bounds[0], second.bounds[0]) - 10
    right = max(first.bounds[2], second.bounds[2]) + 10
    drawing = ''.join(svg_path(outline, '#111') for outline in outlines)
    drawing += svg_path(intersection, '#dc2727')
    caption = f'{text} · width {width} · weight {weight}'
    return (f'<figure><figcaption>{caption}</figcaption>'
            f'<svg role="img" aria-label="{caption}" viewBox="{left} -830 {right-left} 850">'
            f'<g transform="scale(1,-1)">{drawing}</g></svg>'
            f'<small>Overlapping ink: {abs(intersection.area):,.0f} square font units</small></figure>')


def write(font_path, out):
    face = hb.Face(font_path.read_bytes())
    with TTFont(font_path) as font:
        pairs = ''.join(pair_figure(font, face, *case) for case in
                        [('AF', 75, 400), ('TA', 100, 900), ('WA', 125, 900)])
    weights = ''.join(f'<figure><figcaption>Width {width} · weight {weight}</figcaption>'
                      f'<p class="font" style="--w:{width};--g:{weight}">HAMBURGEFONTS<br>KNOWLEDGE</p>'
                      '</figure>' for weight, width in product((400, 700, 900), (75, 100, 125)))
    letters = [('Z Ʒ', 'Z and Ezh'), ('F ſ', 'F and long s'), ('G Ǥ', 'G and G with stroke'),
               ('O Ơ', 'O and O with horn'), ('U Ư', 'U and U with horn'), ('N Ŋ', 'N and Eng')]
    identities = ''.join(f'<figure><figcaption>{label}</figcaption><p class="font identity">{text}</p>'
                         '</figure>' for text, label in letters)
    (out / 'design.html').write_text(f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Blocksync design review</title>
<style>
@font-face{{font-family:Blocksync;src:url("{escape(font_path.name)}");font-weight:400 900;font-stretch:75% 125%}}
body{{max-width:78rem;margin:2rem auto;padding:0 1.25rem;font:1rem/1.4 system-ui;color:#171717;background:#fff}}
section{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1rem}}
figure{{margin:0;border-top:1px solid #bbb;padding:.6rem 0}} figcaption,small{{font-size:.9rem}}
svg{{display:block;height:8rem;max-width:100%;margin:.6rem 0}}
.font{{font:2.25rem/1.1 Blocksync;margin:.45rem 0;font-variation-settings:"wdth" var(--w,100),"wght" var(--g,400)}}
.identity{{font-size:3.5rem}}
</style><main><h1>Blocksync design review</h1>
<h2>Letters that touch</h2><p>Red marks ink shared by two letters after kerning.</p><section>{pairs}</section>
<h2>Weight progression</h2><p>Compare Regular, Bold and Black at each width.</p><section>{weights}</section>
<h2>Character identity</h2><p>Each pair has two distinct Unicode characters. Compare the letterforms.</p>
<section>{identities}</section></main></html>""", encoding='utf-8')
