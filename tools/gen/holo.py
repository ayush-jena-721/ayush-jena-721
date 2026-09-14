"""Hovering holographic ID screen: a translucent glass pane projected from
an emitter at the base, drifting gently, with scanlines, corner brackets
and Ayush's profile data. Same look in both themes (it's a projection)."""
import base64
import math
import pathlib

from .theme import *
from .icons import icon

_here = pathlib.Path(__file__).resolve()
PORTRAIT = next((c for c in [_here.parent.parent / "assets" / "portrait.jpg",
                             _here.parent.parent.parent / "assets" / "portrait.jpg"] if c.exists()), None)


def build(t: Theme) -> str:
    S = SCREEN
    W, H = 440, 300
    cyan, cyan2, gold, red = S["cyan"], S["cyan2"], S["gold"], S["red"]
    px, py, pw, ph = 40, 28, 360, 208   # pane
    style = """
    .pane { animation: hover 6s ease-in-out infinite; }
    @keyframes hover { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
    .cone { animation: cone 6s ease-in-out infinite; transform-box: fill-box; transform-origin: bottom center; }
    @keyframes cone { 0%,100% { opacity:.55; transform: scaleY(1) } 50% { opacity:.8; transform: scaleY(1.03) } }
    .scan { animation: scan 3.2s linear infinite; }
    @keyframes scan { from { transform: translateY(0) } to { transform: translateY(208px) } }
    .flicker { animation: flicker 9s steps(1) infinite; }
    @keyframes flicker { 0%,100% { opacity:1 } 41% { opacity:1 } 42% { opacity:.6 } 43% { opacity:1 } 77% { opacity:1 } 78% { opacity:.75 } 79% { opacity:1 } }
    .ring { transform-box: fill-box; transform-origin: center; animation: spin 18s linear infinite; }
    .ring2 { transform-box: fill-box; transform-origin: center; animation: spin 28s linear infinite reverse; }
    @keyframes spin { to { transform: rotate(360deg) } }
    .march { animation: march 6s linear infinite; }
    .march2 { animation: march 9s linear infinite reverse; }
    @keyframes march { to { stroke-dashoffset: -200 } }
    .bar { transform-box: fill-box; transform-origin: left; animation: bar 4s ease-in-out infinite alternate; }
    @keyframes bar { from { transform: scaleX(.55) } to { transform: scaleX(1) } }
    .blink { animation: blink 1.6s steps(2) infinite; }
    @keyframes blink { 50% { opacity:.2 } }
    .type { animation: show .6s both; }
    .t2 { animation-delay:.3s } .t3 { animation-delay:.6s } .t4 { animation-delay:.9s } .t5 { animation-delay:1.2s } .t6 { animation-delay:1.5s }
    @keyframes show { from { opacity:0 } to { opacity:1 } }
    .emit { animation: emit 2s ease-in-out infinite; }
    @keyframes emit { 0%,100% { opacity:.6 } 50% { opacity:1 } }
    """
    defs = (f'<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cyan}" stop-opacity=".16"/>'
            f'<stop offset="1" stop-color="{cyan}" stop-opacity=".05"/></linearGradient>'
            f'<linearGradient id="coneG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cyan}" stop-opacity=".0"/>'
            f'<stop offset="1" stop-color="{cyan}" stop-opacity=".35"/></linearGradient>'
            f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cyan}" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="{cyan}" stop-opacity=".35"/></linearGradient>'
            f'<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{cyan}" fill-opacity=".07"/></pattern>'
            f'<clipPath id="paneclip"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8"/></clipPath>'
            f'<clipPath id="pc"><circle cx="{px + 48}" cy="{py + 62}" r="30"/></clipPath>'
            f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>'
            f'<filter id="glowT" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.2" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            f'<radialGradient id="dot"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="{cyan}"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>')
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs, aria="Holographic ID screen for Ayush Jena")]
    # ---- emitter base
    bx, by_ = W / 2, H - 22
    o.append(f'<ellipse cx="{bx}" cy="{by_}" rx="120" ry="8" fill="{cyan}" fill-opacity=".10" filter="url(#blur)"/>')
    o.append(f'<ellipse class="march" cx="{bx}" cy="{by_}" rx="96" ry="7" fill="none" stroke="{cyan}" stroke-opacity=".7" stroke-dasharray="6 10 40 10"/>')
    o.append(f'<ellipse class="march2" cx="{bx}" cy="{by_}" rx="70" ry="5" fill="none" stroke="{gold}" stroke-opacity=".7" stroke-dasharray="30 12 3 12"/>')
    o.append(f'<ellipse cx="{bx}" cy="{by_}" rx="40" ry="3.5" fill="none" stroke="{cyan}" stroke-opacity=".8"/>')
    o.append(f'<circle class="emit" cx="{bx}" cy="{by_}" r="9" fill="url(#dot)"/>')
    # projection cone from emitter to pane
    o.append(f'<polygon class="cone" points="{bx - 26},{by_ - 2} {bx + 26},{by_ - 2} {px + pw},{py + ph} {px},{py + ph}" fill="url(#coneG)"/>')
    # ---- pane
    o.append('<g class="pane">')
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="{S["bg"]}" fill-opacity=".55"/>')
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="url(#glass)" stroke="{cyan}" stroke-opacity=".55" stroke-width="1"/>')
    o.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" fill="url(#lines)"/>')
    # corner brackets
    for (cx, cy, sx, sy) in [(px, py, 1, 1), (px + pw, py, -1, 1), (px, py + ph, 1, -1), (px + pw, py + ph, -1, -1)]:
        o.append(f'<path d="M{cx + 16 * sx} {cy} L{cx} {cy} L{cx} {cy + 16 * sy}" fill="none" stroke="{cyan}" stroke-width="2"/>')
    o.append('<g class="flicker">')
    # header
    o.append(text(px + 16, py + 20, "IDENT · HOLO-PROJECTION", size=9.5, fill=cyan, family=MONO, weight=700, ls="2", extra='filter="url(#glowT)"'))
    o.append(text(px + pw - 16, py + 20, "AJ-721", size=9.5, fill=S["muted"], family=MONO, anchor="end", ls="1.5"))
    o.append(f'<line x1="{px + 16}" y1="{py + 28}" x2="{px + pw - 16}" y2="{py + 28}" stroke="{cyan}" stroke-opacity=".35"/>')
    # portrait (round, wireframe ring)
    ccx, ccy = px + 48, py + 62
    if PORTRAIT:
        data = "data:image/jpeg;base64," + base64.b64encode(PORTRAIT.read_bytes()).decode()
        o.append(f'<image clip-path="url(#pc)" href="{data}" x="{ccx - 30}" y="{ccy - 30}" width="60" height="60" preserveAspectRatio="xMidYMid slice" opacity=".92"/>')
    o.append(f'<circle cx="{ccx}" cy="{ccy}" r="30" fill="url(#glass)" stroke="{cyan}" stroke-opacity=".9"/>')
    o.append(f'<g class="ring"><circle cx="{ccx}" cy="{ccy}" r="36" fill="none" stroke="{gold}" stroke-opacity=".8" stroke-dasharray="2 6 24 6"/></g>')
    # name + role
    o.append(text(px + 100, py + 56, "AYUSH JENA", size=20, fill=S["text"], weight=800, ls="1", cls="type", extra='filter="url(#glowT)"'))
    o.append(text(px + 100, py + 76, "Software · AI / ML · IoT", size=12, fill=cyan, cls="type t2"))
    o.append(f'<circle class="blink" cx="{px + 104}" cy="{py + 92}" r="3.5" fill="{S["green"]}"/>')
    o.append(text(px + 114, py + 96, "ONLINE  ·  INDIA  ·  @ayush-jena-721", size=9.5, fill=S["muted"], family=MONO, ls="1", cls="type t3"))
    # data rows
    rows = [("FOCUS", "Deep learning · computer vision · IoT", "t4"),
            ("STACK", "Python · TensorFlow · OpenCV · ESP32", "t5"),
            ("SHIPPED", "5 ML repos · IoT + desktop systems", "t6")]
    for i, (k, v, c) in enumerate(rows):
        yy = py + 122 + i * 22
        o.append(text(px + 16, yy, k, size=9, fill=S["muted"], family=MONO, ls="1.5", cls=f"type {c}"))
        o.append(text(px + 78, yy, v, size=11.5, fill=S["text"], cls=f"type {c}"))
        o.append(f'<line x1="{px + 16}" y1="{yy + 7}" x2="{px + pw - 16}" y2="{yy + 7}" stroke="{cyan}" stroke-opacity=".18"/>')
    # signal bars (decorative telemetry) + footer
    for i, (lab, col) in enumerate([("CORE", cyan), ("VISION", gold), ("EDGE", red)]):
        x = px + 16 + i * 116
        o.append(text(x, py + ph - 20, lab, size=8, fill=S["muted"], family=MONO, ls="1.5"))
        o.append(f'<rect x="{x}" y="{py + ph - 14}" width="96" height="3" fill="{cyan}" fill-opacity=".15"/>')
        o.append(f'<rect class="bar" style="animation-delay:{i * .7}s" x="{x}" y="{py + ph - 14}" width="96" height="3" fill="{col}"/>')
    o.append('</g>')
    # scanline sweep
    o.append(f'<g clip-path="url(#paneclip)"><rect class="scan" x="{px}" y="{py - 28}" width="{pw}" height="28" fill="url(#scanG)"/></g>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
