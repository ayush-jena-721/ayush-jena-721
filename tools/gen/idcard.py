"""Rotating engineering ID card. A Y-axis spin is simulated with scaleX
keyframes (no JavaScript — GitHub strips it), lingering on each face.
The card itself stays dark on both themes; only the surround changes."""
import base64
import pathlib

from .theme import *
from .icons import icon

_here = pathlib.Path(__file__).resolve()
AVATAR = next((c for c in [_here.parent.parent / "assets" / "avatar.jpg",
                          _here.parent.parent.parent / "assets" / "avatar.jpg"] if c.exists()), None)

# card palette (fixed, premium dark)
C_BG1, C_BG2, C_EDGE, C_TXT, C_MUTED, C_CYAN, C_VIOLET, C_AMBER = (
    "#0b1220", "#141c2f", "#2a3650", "#e8eefc", "#8d9bb8", "#5be0f0", "#ff4d4d", "#f5c451")

PERIOD = 10  # seconds per full rotation


def avatar_data():
    if AVATAR and AVATAR.exists():
        return "data:image/jpeg;base64," + base64.b64encode(AVATAR.read_bytes()).decode()
    return None


def build(t: Theme) -> str:
    W, H = 440, 300
    cw, ch = 380, 236
    cx, cy = W / 2, H / 2
    x0, y0 = cx - cw / 2, cy - ch / 2
    # linger 35%, flip 15%, linger 35%, flip 15%
    style = f"""
    .card {{ transform-box: fill-box; transform-origin: center; }}
    .front {{ animation: front {PERIOD}s cubic-bezier(.65,0,.35,1) infinite; }}
    .back  {{ animation: back  {PERIOD}s cubic-bezier(.65,0,.35,1) infinite; }}
    @keyframes front {{
      0%   {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
      35%  {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
      42.5%{{ transform: scaleX(0.02) skewY(-4deg); opacity:1 }}
      42.6%{{ opacity:0 }}
      57.4%{{ opacity:0 }}
      57.5%{{ transform: scaleX(0.02) skewY(4deg); opacity:1 }}
      65%  {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
      100% {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
    }}
    @keyframes back {{
      0%   {{ transform: scaleX(0.02) skewY(4deg); opacity:0 }}
      42.4%{{ opacity:0 }}
      42.5%{{ transform: scaleX(0.02) skewY(-4deg); opacity:1 }}
      50%  {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
      85%  {{ transform: scaleX(1) skewY(0deg); opacity:1 }}
      92.5%{{ transform: scaleX(0.02) skewY(4deg); opacity:1 }}
      92.6%{{ opacity:0 }}
      100% {{ opacity:0 }}
    }}
    .sheen {{ animation: sheen {PERIOD}s linear infinite; }}
    @keyframes sheen {{ 0%{{transform:translateX(-420px)}} 35%{{transform:translateX(-420px)}} 50%{{transform:translateX(420px)}} 85%{{transform:translateX(420px)}} 100%{{transform:translateX(-420px)}} }}
    .ring {{ transform-box: fill-box; transform-origin:center; animation: spin 24s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
    .ring2 {{ transform-box: fill-box; transform-origin:center; animation: spin 36s linear infinite reverse; }}
    .scan {{ animation: scan 4s ease-in-out infinite; }}
    @keyframes scan {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(150px) }} }}
    .blink {{ animation: blink 2s steps(2) infinite; }}
    @keyframes blink {{ 50% {{ opacity:.25 }} }}
    .tick {{ animation: tick 1.2s steps(1) infinite; }}
    @keyframes tick {{ 50% {{ opacity:0 }} }}
    """
    defs = (
        f'<linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C_BG2}"/><stop offset="1" stop-color="{C_BG1}"/></linearGradient>'
        f'<linearGradient id="holo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C_VIOLET}"/><stop offset=".55" stop-color="{C_AMBER}"/><stop offset="1" stop-color="{C_CYAN}"/></linearGradient>'
        f'<linearGradient id="sheenG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="cardclip"><rect x="{x0}" y="{y0}" width="{cw}" height="{ch}" rx="5"/></clipPath>'
        f'<clipPath id="photo"><rect x="{x0 + 18}" y="{y0 + 48}" width="112" height="150" rx="10"/></clipPath>'
        f'<pattern id="grid" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M12 0H0V12" fill="none" stroke="{C_CYAN}" stroke-opacity=".08"/></pattern>'
        f'<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="10"/></filter>'
    )
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs,
                  aria="Rotating engineering ID card for Ayush Jena")]
    o.append(rect(0, 0, W, H, fill=t.bg, r=5))
    # holographic rings behind the card
    o.append(f'<g class="ring"><circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{t.a1}" stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 10 40 10"/></g>')
    o.append(f'<g class="ring2"><circle cx="{cx}" cy="{cy}" r="138" fill="none" stroke="{t.a2}" stroke-opacity=".16" stroke-width="1" stroke-dasharray="60 20 6 20"/></g>')
    o.append(f'<ellipse cx="{cx}" cy="{cy + 8}" rx="170" ry="110" fill="{t.a1}" fill-opacity=".10" filter="url(#soft)"/>')

    def face_base():
        return (rect(x0, y0, cw, ch, fill="url(#cardbg)", stroke=C_EDGE, r=5)
                + f'<g clip-path="url(#cardclip)">'
                + rect(x0, y0, cw, ch, fill="url(#grid)")
                + rect(x0, y0, cw, 4, fill="url(#holo)")
                + f'<rect class="sheen" x="{x0}" y="{y0}" width="{cw}" height="{ch}" fill="url(#sheenG)"/>'
                + '</g>')

    # ---------- FRONT ----------
    o.append('<g class="card front">')
    o.append(face_base())
    o.append(f'<g clip-path="url(#cardclip)">')
    o.append(text(x0 + 18, y0 + 30, "ENGINEERING ACCESS", size=10, fill=C_CYAN, family=MONO, weight=700, ls="2"))
    o.append(text(x0 + cw - 18, y0 + 30, "ID · AJ-721", size=10, fill=C_MUTED, family=MONO, anchor="end", ls="1"))
    # photo
    av = avatar_data()
    o.append(rect(x0 + 18, y0 + 48, 112, 150, fill=C_BG1, stroke=C_EDGE, r=10))
    if av:
        o.append(f'<g clip-path="url(#photo)"><image href="{av}" x="{x0 + 18}" y="{y0 + 48}" width="112" height="150" preserveAspectRatio="xMidYMin slice"/>'
                 f'<rect class="scan" x="{x0 + 18}" y="{y0 + 48}" width="112" height="2" fill="{C_CYAN}" fill-opacity=".7"/></g>')
    o.append(rect(x0 + 18, y0 + 48, 112, 150, stroke=C_CYAN, r=10, extra='stroke-opacity=".5"'))
    # corner brackets on photo
    for (bx, by, sx, sy) in [(x0 + 18, y0 + 48, 1, 1), (x0 + 130, y0 + 48, -1, 1), (x0 + 18, y0 + 198, 1, -1), (x0 + 130, y0 + 198, -1, -1)]:
        o.append(f'<path d="M{bx} {by + 12 * sy} V{by} H{bx + 12 * sx}" fill="none" stroke="{C_CYAN}" stroke-width="2"/>')
    # identity block
    tx = x0 + 150
    o.append(text(tx, y0 + 78, "AYUSH", size=28, fill=C_TXT, weight=800, ls="1"))
    o.append(text(tx, y0 + 108, "JENA", size=28, fill=C_TXT, weight=800, ls="1"))
    o.append(rect(tx, y0 + 118, 60, 2, fill="url(#holo)"))
    o.append(text(tx, y0 + 140, "Software · AI / ML · IoT", size=12, fill=C_MUTED))
    o.append(text(tx, y0 + 160, "@ayush-jena-721", size=12, fill=C_CYAN, family=MONO))
    # status row
    o.append(f'<circle class="blink" cx="{tx + 5}" cy="{y0 + 184}" r="4" fill="#3fdc7a"/>')
    o.append(text(tx + 15, y0 + 188, "STATUS  ACTIVE", size=10, fill=C_MUTED, family=MONO, ls="1"))
    o.append(text(tx, y0 + 208, "REGION  INDIA", size=10, fill=C_MUTED, family=MONO, ls="1"))
    # barcode-ish decoration bottom right
    bx = x0 + cw - 18 - 90
    import random
    rnd = random.Random(721)
    xx = bx
    while xx < x0 + cw - 18:
        w = rnd.choice([1, 1, 2, 3])
        o.append(rect(xx, y0 + ch - 30, w, 16, fill=C_MUTED, extra='fill-opacity=".55"'))
        xx += w + rnd.choice([1, 2, 2, 3])
    o.append(text(x0 + cw - 18, y0 + ch - 8, "BUILD SOMETHING REAL", size=8, fill=C_MUTED, family=MONO, anchor="end", ls="1.5"))
    o.append('</g></g>')

    # ---------- BACK ----------
    o.append('<g class="card back">')
    o.append(face_base())
    o.append(f'<g clip-path="url(#cardclip)">')
    o.append(text(x0 + 18, y0 + 30, "TECHNICAL PROFILE", size=10, fill=C_VIOLET, family=MONO, weight=700, ls="2"))
    o.append(text(x0 + cw - 18, y0 + 30, "REV 2026.09", size=10, fill=C_MUTED, family=MONO, anchor="end", ls="1"))
    rows = [("ROLE", "Software developer · AI/ML explorer"),
            ("FOCUS", "Deep learning, computer vision, IoT"),
            ("STACK", "Python · TensorFlow · OpenCV · ESP32"),
            ("SHIPPED", "5 ML repos · IoT & desktop systems"),
            ("LINKS", "github.com/ayush-jena-721")]
    for i, (k, v) in enumerate(rows):
        yy = y0 + 58 + i * 26
        o.append(text(x0 + 18, yy, k, size=9.5, fill=C_MUTED, family=MONO, ls="1.5"))
        o.append(text(x0 + 88, yy, v, size=12, fill=C_TXT, weight=500))
        o.append(f'<line x1="{x0 + 18}" y1="{yy + 8}" x2="{x0 + cw - 18}" y2="{yy + 8}" stroke="{C_EDGE}" stroke-opacity=".7"/>')
    # skills as small bars (no invented percentages: equal-width tags)
    skills = ["Python", "TensorFlow/Keras", "scikit-learn", "OpenCV", "NLTK", "Flask", "SQLite", "ESP32", "Raspberry Pi"]
    x, yy = x0 + 18, y0 + 190
    for s in skills:
        w = int(len(s) * 6.2 + 14)
        if x + w > x0 + cw - 18:
            break
        o.append(rect(x, yy, w, 18, fill=C_BG1, stroke=C_EDGE, r=4))
        o.append(text(x + 7, yy + 12.5, s, size=9.5, fill=C_CYAN, family=MONO))
        x += w + 6
    o.append(f'<text class="tick" x="{x0 + 18}" y="{y0 + ch - 10}" font-family="{MONO}" font-size="9" fill="{C_MUTED}" letter-spacing="1">▮ SYSTEMS NOMINAL</text>')
    o.append(text(x0 + cw - 18, y0 + ch - 10, "ayushjena0412@gmail.com", size=9, fill=C_MUTED, family=MONO, anchor="end"))
    o.append('</g></g>')

    o.append(rect(0.5, 0.5, W - 1, H - 1, stroke=t.border, r=5))
    o.append(svg_close())
    return "\n".join(o)
