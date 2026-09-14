"""How I work: a seven-stage loop with a pulse travelling along it."""
from .theme import *
from .icons import icon

STAGES = [("Idea", "bulb"), ("Build", "hammer"), ("Break", "bug"), ("Debug", "search"),
          ("Understand", "brain"), ("Improve", "trend"), ("Ship", "rocket")]


def build(t: Theme) -> str:
    W, H = 900, 130
    n = len(STAGES)
    x0, x1 = 70, W - 70
    step = (x1 - x0) / (n - 1)
    cy = 52
    period = 9.0
    style = f"""
    .node {{ animation: show .6s both; }}
    @keyframes show {{ from {{ opacity:.35 }} to {{ opacity:1 }} }}
    """
    o = [svg_open(W, H, t, bg=False, style=style, aria="Workflow: idea, build, break, debug, understand, improve, ship")]
    o.append(card(t, 0.5, 0.5, W - 1, H - 1))
    # base track
    o.append(f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{t.border}" stroke-width="2"/>')
    # gradient trail drawn once
    L = x1 - x0
    o.append(f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="url(#accent)" stroke-width="2" '
             f'stroke-dasharray="{L}" stroke-dashoffset="{L}">'
             f'<animate attributeName="stroke-dashoffset" from="{L}" to="0" dur="{period * .8}s" begin="0.3s" fill="freeze"/></line>')
    # travelling pulse (loops)
    o.append(f'<circle r="6" fill="{t.a1}" opacity="0.35"><animateMotion dur="{period}s" begin="0.3s" repeatCount="indefinite" '
             f'path="M{x0},{cy} L{x1},{cy}"/><animate attributeName="r" values="6;10;6" dur="1.2s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle r="3.5" fill="url(#accent)"><animateMotion dur="{period}s" begin="0.3s" repeatCount="indefinite" '
             f'path="M{x0},{cy} L{x1},{cy}"/></circle>')
    for i, (name, ic) in enumerate(STAGES):
        x = x0 + i * step
        delay = 0.3 + (i / (n - 1)) * period * .8
        col = t.a1 if i < n - 1 else t.green
        o.append(f'<g class="node" style="animation-delay:{delay:.2f}s">')
        o.append(f'<circle cx="{x:.1f}" cy="{cy}" r="19" fill="{t.card2}" stroke="{col}" stroke-width="1.5"/>')
        o.append(icon(ic, x - 11, cy - 11, col, scale=0.9))
        o.append(text(x, cy + 44, name, size=12.5, fill=t.text, weight=600, anchor="middle"))
        o.append('</g>')
        if i < n - 1:
            o.append(text(x + step / 2, cy + 4, "›", size=13, fill=t.muted, anchor="middle", family=MONO))
    # loop-back arrow (ship -> idea)
    o.append(f'<path d="M{x1},{cy + 26} C{x1},{cy + 62} {x0},{cy + 62} {x0},{cy + 26}" fill="none" stroke="{t.border}" '
             f'stroke-width="1.2" stroke-dasharray="3 4"/>')
    o.append(text(W / 2, cy + 66, "…and back to the next idea", size=11, fill=t.muted, anchor="middle",
                  extra='font-style="italic"'))
    o.append(svg_close())
    return "\n".join(o)
