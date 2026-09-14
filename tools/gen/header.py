"""Hero banner: minimal Stark-style identity on the left, a hovering round
portrait on the right — reactor rings, gold/red glow and a flickering
lightning aura. Everything animates on its own (CSS/SMIL only)."""
import base64
import pathlib
import random

from .theme import *

_here = pathlib.Path(__file__).resolve()
PORTRAIT = next((c for c in [_here.parent.parent / "assets" / "portrait.jpg",
                             _here.parent.parent.parent / "assets" / "portrait.jpg"] if c.exists()), None)


def portrait_data():
    if PORTRAIT:
        return "data:image/jpeg;base64," + base64.b64encode(PORTRAIT.read_bytes()).decode()
    return None


def bolt_path(rnd, cx, cy, r0, r1, ang):
    """A jagged lightning segment radiating from radius r0 to r1 at angle ang."""
    import math
    pts = []
    n = 5
    for i in range(n + 1):
        r = r0 + (r1 - r0) * i / n
        a = math.radians(ang + rnd.uniform(-9, 9) * (0 if i in (0, n) else 1))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    # a short branch
    bx, by = pts[3]
    a = math.radians(ang + rnd.choice([-35, 35]))
    d += f" M{bx:.1f},{by:.1f} L{bx + 14 * math.cos(a):.1f},{by + 14 * math.sin(a):.1f}"
    return d


def build(t: Theme) -> str:
    W, H = 900, 320
    arc, bolt, red, gold = ARC[t.name], BOLT[t.name], RED[t.name], GOLD[t.name]
    roles = ["Machine learning & computer vision", "Python developer", "IoT & embedded builder"]
    rnd = random.Random(721)
    cx, cy, R = 700, 150, 78
    style = f"""
    .fade {{ animation: fadeUp .9s cubic-bezier(.2,.7,.2,1) both; }}
    @keyframes fadeUp {{ from {{ opacity:0; transform: translateY(8px);}} to {{ opacity:1; transform:none;}} }}
    .line {{ stroke-dasharray: 300; stroke-dashoffset: 300; animation: draw 1.4s .6s ease-out forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .role {{ opacity:0; animation: roles 12s infinite; }}
    .role:nth-child(2) {{ animation-delay: 4s; }}
    .role:nth-child(3) {{ animation-delay: 8s; }}
    @keyframes roles {{ 0%{{opacity:0}} 6%{{opacity:1}} 30%{{opacity:1}} 36%{{opacity:0}} 100%{{opacity:0}} }}
    .drift1 {{ animation: d1 14s ease-in-out infinite alternate; }}
    .drift2 {{ animation: d2 18s ease-in-out infinite alternate; }}
    @keyframes d1 {{ to {{ transform: translate(30px, 16px);}} }}
    @keyframes d2 {{ to {{ transform: translate(-40px, -12px);}} }}
    .chip {{ animation: fadeUp .7s both; }}
    .hover {{ animation: hover 5s ease-in-out infinite; }}
    @keyframes hover {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(-9px) }} }}
    .shadow {{ transform-box: fill-box; transform-origin: center; animation: shadow 5s ease-in-out infinite; }}
    @keyframes shadow {{ 0%,100% {{ transform: scale(1); opacity:.45 }} 50% {{ transform: scale(.8); opacity:.25 }} }}
    .ringA {{ transform-box: fill-box; transform-origin: center; animation: spin 22s linear infinite; }}
    .ringB {{ transform-box: fill-box; transform-origin: center; animation: spin 34s linear infinite reverse; }}
    @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
    .pulse {{ animation: pulse 3s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity:.45 }} 50% {{ opacity:.9 }} }}
    .bolt {{ opacity:0; animation: flick 7s infinite; }}
    @keyframes flick {{ 0%,100% {{ opacity:0 }} 2% {{ opacity:1 }} 3% {{ opacity:.2 }} 4% {{ opacity:1 }} 7% {{ opacity:0 }} }}
    .tick {{ animation: tick 1.4s steps(1) infinite; }}
    @keyframes tick {{ 50% {{ opacity:.3 }} }}
    """
    defs = (f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
            f'<path d="M24 0H0V24" fill="none" stroke="{t.muted}" stroke-opacity=".14"/></pattern>'
            f'<clipPath id="clip"><rect x="0" y="0" width="{W}" height="{H}" rx="5"/></clipPath>'
            f'<clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
            f'<radialGradient id="gGold"><stop offset="0" stop-color="{gold}" stop-opacity="{t.glow}"/><stop offset="1" stop-color="{gold}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gRed"><stop offset="0" stop-color="{red}" stop-opacity="{t.glow * .8}"/><stop offset="1" stop-color="{red}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gArc"><stop offset="0" stop-color="{arc}" stop-opacity=".55"/><stop offset="1" stop-color="{arc}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="rg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{red}"/><stop offset="1" stop-color="{gold}"/></linearGradient>'
            f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
            f'<filter id="glowB" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.6" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o = [svg_open(W, H, t, extra_defs=defs, style=style, bg=False,
                  aria="Ayush Jena — machine learning, computer vision and IoT developer")]
    o.append('<g clip-path="url(#clip)">')
    o.append(rect(0, 0, W, H, fill=t.bg, r=5))
    o.append(rect(0, 0, W, H, fill="url(#grid)"))
    o.append(f'<g class="drift1"><circle cx="{cx + 40}" cy="{cy - 60}" r="230" fill="url(#gGold)"/></g>')
    o.append(f'<g class="drift2"><circle cx="{cx - 90}" cy="{cy + 120}" r="210" fill="url(#gRed)"/></g>')
    # thin red/gold top rule
    o.append(rect(0, 0, W, 3, fill="url(#rg)"))
    o.append(rect(0.5, 0.5, W - 1, H - 1, stroke=t.border, r=5))

    # ---- left: identity
    o.append(text(48, 86, "PROFILE ONLINE · ALL SYSTEMS NOMINAL", size=11, fill=gold, family=MONO, weight=700, ls="2.5", cls="fade"))
    o.append(text(48, 140, "Ayush Jena", size=52, fill=t.text, weight=800, cls="fade",
                  extra='style="animation-delay:.15s" letter-spacing="-1.5"'))
    o.append(f'<line class="line" x1="50" y1="156" x2="250" y2="156" stroke="url(#rg)" stroke-width="3" stroke-linecap="round"/>')
    o.append(text(48, 192, "›", size=20, fill=red, weight=700, family=MONO))
    o.append('<g>')
    for r in roles:
        o.append(text(64, 192, r, size=19, fill=t.text, weight=500, cls="role"))
    o.append('</g>')
    x = 48
    for i, (lab, col) in enumerate([("Python", gold), ("TensorFlow / Keras", red), ("OpenCV", arc),
                                   ("scikit-learn", gold), ("ESP32 · Raspberry Pi", red)]):
        s, w = chip(t, x, 220, lab, color=col, delay=0.5 + i * 0.12)
        o.append(s)
        x += w + 8
    o.append(f'<g class="fade" style="animation-delay:1s">')
    o.append(f'<path d="M52 271 c0-4 3-7 7-7s7 3 7 7c0 5-7 12-7 12s-7-7-7-12z" fill="none" stroke="{t.muted}" stroke-width="1.4"/>'
             f'<circle cx="59" cy="271" r="2" fill="{t.muted}"/>')
    o.append(text(72, 276, "India", size=13, fill=t.muted))
    o.append(text(122, 276, "·", size=13, fill=t.muted))
    o.append(text(134, 276, "@ayush-jena-721", size=13, fill=t.muted, family=MONO))
    o.append(text(272, 276, "·", size=13, fill=t.muted))
    o.append(text(284, 276, "build → break → understand → ship", size=13, fill=t.muted))
    o.append('</g>')

    # ---- right: hovering portrait
    o.append(f'<ellipse class="shadow" cx="{cx}" cy="{cy + R + 46}" rx="70" ry="9" fill="{t.text}" fill-opacity=".35" filter="url(#blur)"/>')
    o.append('<g class="hover">')
    o.append(f'<circle class="pulse" cx="{cx}" cy="{cy}" r="{R + 34}" fill="url(#gArc)"/>')
    # lightning aura
    for i in range(7):
        ang = i * (360 / 7) + rnd.uniform(-12, 12)
        d = bolt_path(rnd, cx, cy, R + 12, R + 12 + rnd.uniform(26, 44), ang)
        delay = rnd.uniform(0, 7)
        o.append(f'<path class="bolt" style="animation-delay:{delay:.2f}s" d="{d}" fill="none" stroke="{bolt}" '
                 f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" filter="url(#glowB)"/>')
    # HUD reticle: crosshair + arc segments
    o.append(f'<line x1="{cx - R - 48}" y1="{cy}" x2="{cx - R - 16}" y2="{cy}" stroke="{arc}" stroke-opacity=".7"/>')
    o.append(f'<line x1="{cx + R + 16}" y1="{cy}" x2="{cx + R + 48}" y2="{cy}" stroke="{arc}" stroke-opacity=".7"/>')
    o.append(f'<line x1="{cx}" y1="{cy - R - 48}" x2="{cx}" y2="{cy - R - 16}" stroke="{arc}" stroke-opacity=".7"/>')
    o.append(f'<line x1="{cx}" y1="{cy + R + 16}" x2="{cx}" y2="{cy + R + 40}" stroke="{arc}" stroke-opacity=".7"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 40}" fill="none" stroke="{arc}" stroke-opacity=".35" stroke-dasharray="40 200" stroke-width="3"/>')
    # rings
    o.append(f'<g class="ringA"><circle cx="{cx}" cy="{cy}" r="{R + 22}" fill="none" stroke="{gold}" stroke-opacity=".75" stroke-width="1.5" stroke-dasharray="3 9 52 9"/></g>')
    o.append(f'<g class="ringB"><circle cx="{cx}" cy="{cy}" r="{R + 11}" fill="none" stroke="{red}" stroke-opacity=".7" stroke-width="1" stroke-dasharray="70 14 4 14"/></g>')
    # reactor ticks
    import math
    for k in range(24):
        a = math.radians(k * 15)
        r0 = R + 5
        r1 = R + 9 if k % 6 else R + 13
        o.append(f'<line x1="{cx + r0 * math.cos(a):.1f}" y1="{cy + r0 * math.sin(a):.1f}" x2="{cx + r1 * math.cos(a):.1f}" y2="{cy + r1 * math.sin(a):.1f}" '
                 f'stroke="{arc}" stroke-opacity=".8" stroke-width="{2 if k % 6 == 0 else 1}"/>')
    # portrait
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 2}" fill="{t.card}" stroke="url(#rg)" stroke-width="3"/>')
    pd = portrait_data()
    if pd:
        o.append(f'<image clip-path="url(#pc)" href="{pd}" x="{cx - R}" y="{cy - R}" width="{2 * R}" height="{2 * R}" preserveAspectRatio="xMidYMid slice"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{arc}" stroke-opacity=".9" stroke-width="1.5"/>')
    # status pill under the portrait
    o.append(rect(cx - 46, cy + R + 14, 92, 20, fill=t.card, stroke=t.border, r=10))
    o.append(f'<circle class="tick" cx="{cx - 33}" cy="{cy + R + 24}" r="3.5" fill="{t.green}"/>')
    o.append(text(cx - 24, cy + R + 28, "ONLINE · 2026", size=9.5, fill=t.muted, family=MONO, ls="1"))
    o.append('</g>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
