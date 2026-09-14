"""Shared palette + tiny SVG helpers for the profile assets.

Every builder takes a Theme and returns an SVG string. build.py writes each
one twice: assets/<name>-dark.svg and assets/<name>-light.svg.
"""
from dataclasses import dataclass
from xml.sax.saxutils import escape

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str          # page canvas (matches GitHub)
    card: str        # panel fill
    card2: str       # slightly raised panel
    border: str
    text: str
    muted: str
    faint: str       # hairlines / grid
    a1: str          # accent gradient start (blue)
    a2: str          # accent gradient end (violet)
    green: str
    amber: str
    rose: str
    glow: float      # opacity of glow blobs


DARK = Theme(
    name="dark",
    # J.A.R.V.I.S. HUD: near-black navy, electric cyan readouts, amber alerts
    bg="#060b14", card="#0b1524", card2="#0f1c30", border="#1d3a55",
    text="#dbf4ff", muted="#7fa6bf", faint="#12243a",
    a1="#38d9f5", a2="#ffb020", green="#34d399", amber="#ffb020", rose="#ff6b6b",
    glow=0.5,
)

LIGHT = Theme(
    name="light",
    # The same HUD in daylight: ice-white canvas, cyan-ink frames, deep amber
    bg="#f6fafd", card="#ffffff", card2="#eaf4fa", border="#a9cddf",
    text="#0b2233", muted="#43667c", faint="#dcebf4",
    a1="#0891b2", a2="#b45309", green="#15803d", amber="#b45309", rose="#dc2626",
    glow=0.34,
)

THEMES = [DARK, LIGHT]

# Arc-reactor / lightning accents (Thor), used sparingly next to red + gold
ARC = {"dark": "#38d9f5", "light": "#0891b2"}
BOLT = {"dark": "#bff3ff", "light": "#0ea5e9"}
RED = {"dark": "#ffb020", "light": "#b45309"}
GOLD = {"dark": "#ffb020", "light": "#b45309"}



def esc(s: str) -> str:
    return escape(str(s), {'"': "&quot;"})


def text(x, y, s, size=14, fill=None, weight=400, family=SANS, anchor="start",
         extra="", opacity=None, cls=None, ls=None):
    attrs = [f'x="{x}"', f'y="{y}"', f'font-family="{family}"', f'font-size="{size}"',
             f'font-weight="{weight}"']
    if fill:
        attrs.append(f'fill="{fill}"')
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        attrs.append(f'opacity="{opacity}"')
    if cls:
        attrs.append(f'class="{cls}"')
    if ls:
        attrs.append(f'letter-spacing="{ls}"')
    if extra:
        attrs.append(extra)
    return f"<text {' '.join(attrs)}>{esc(s)}</text>"


def rect(x, y, w, h, fill="none", stroke="none", r=0, sw=1, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def card(t: Theme, x, y, w, h, r=5, fill=None, extra=""):
    return rect(x, y, w, h, fill=fill or t.card, stroke=t.border, r=r, extra=extra)


def svg_open(w, h, t: Theme, extra_defs="", style="", bg=True, aria=""):
    """Root element. Background is transparent by default so the SVG sits on
    GitHub's own canvas; panels carry their own fills."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(aria)}">',
        "<defs>",
        f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t.a1}"/><stop offset="1" stop-color="{t.a2}"/></linearGradient>',
        f'<linearGradient id="accentV" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t.a1}"/><stop offset="1" stop-color="{t.a2}"/></linearGradient>',
        f'<radialGradient id="glow1"><stop offset="0" stop-color="{t.a1}" stop-opacity="{t.glow}"/>'
        f'<stop offset="1" stop-color="{t.a1}" stop-opacity="0"/></radialGradient>',
        f'<radialGradient id="glow2"><stop offset="0" stop-color="{t.a2}" stop-opacity="{t.glow}"/>'
        f'<stop offset="1" stop-color="{t.a2}" stop-opacity="0"/></radialGradient>',
        extra_defs,
        "</defs>",
        f"<style>{style}</style>",
    ]
    if bg:
        parts.append(rect(0, 0, w, h, fill=t.bg, r=0))
    return "\n".join(parts)


def svg_close():
    return "</svg>"


def chip(t: Theme, x, y, label, color=None, mono=False, size=12, pad=10, h=24, delay=None):
    """Rounded pill. Returns (svg, width). Width is estimated from glyph count."""
    est = len(label) * (size * (0.64 if mono else 0.6)) + pad * 2
    w = int(est)
    color = color or t.a1
    anim = f' style="animation-delay:{delay}s"' if delay is not None else ""
    s = (f'<g class="chip"{anim}>'
         + rect(x, y, w, h, fill=t.card2, stroke=t.border, r=h / 2)
         + f'<circle cx="{x + pad}" cy="{y + h / 2}" r="3" fill="{color}"/>'
         + text(x + pad + 9, y + h / 2 + size * 0.36, label, size=size, fill=t.text,
                family=MONO if mono else SANS, weight=500)
         + "</g>")
    return s, w

# Fixed "screen" palette for panels that are monitors/holograms in both themes
SCREEN = dict(bg="#050d1a", bg2="#0a1628", edge="#1d3a55", text="#dbf4ff", muted="#7fa6bf",
              cyan="#38d9f5", cyan2="#1fa7c4", gold="#ffb020", red="#ff6b6b", green="#34d399")


# ---------------------------------------------------------------- J.A.R.V.I.S. chrome
import re as _re

HUD_H = 40   # height of the system bar added above every panel


def _chamfer(x, y, w, h, c=14):
    """Panel outline with cut corners (top-left, bottom-right) — HUD frame."""
    return (f"M{x + c},{y} H{x + w} V{y + h - c} L{x + w - c},{y + h} H{x} V{y + c} Z")


def hudify(svg: str, t: Theme, module: str, voice: str, code: str) -> str:
    """Post-process a finished panel: add a J.A.R.V.I.S. system bar with a
    typed voice line and a speaking waveform, and a chamfered HUD frame."""
    m = _re.search(r'viewBox="0 0 (\d+) (\d+)" width="(\d+)" height="(\d+)"', svg)
    W, H = int(m.group(1)), int(m.group(2))
    NH = H + HUD_H
    svg = svg.replace(m.group(0), f'viewBox="0 0 {W} {NH}" width="{W}" height="{NH}"', 1)
    head, rest = svg.split("</style>", 1)
    body, tail = rest.rsplit("</svg>", 1)
    cw = 6.75
    vx = 150
    reserved = 10 * 5 + len(code) * 8.0 + 56          # waveform + module code + gaps
    if W < 600:                                        # narrow panel: drop the module code
        code = ""
        reserved = 10 * 5 + 40
    max_chars = int((W - vx - 8 - reserved) / cw)
    if len(voice) > max_chars:
        voice = voice[:max(0, max_chars - 1)].rstrip() + "…"
    n = len(voice)
    steps = ";".join(str(round(k * cw, 1)) for k in range(n + 1))
    dur = max(1.2, n * 0.035)
    bx0 = W - 16 - (len(code) * 8.0 + 16 if code else 0) - 50
    bars = "".join(
        f'<rect class="wv" style="animation-delay:{-(i * .13):.2f}s" x="{bx0 + i * 5}" y="14" width="3" height="12" rx="1" fill="{t.a1}"/>'
        for i in range(10))
    style = f"""
    .wv {{ transform-box: fill-box; transform-origin: center; animation: wv 1.1s ease-in-out infinite alternate; }}
    @keyframes wv {{ from {{ transform: scaleY(.2) }} to {{ transform: scaleY(1) }} }}
    .jv-caret {{ animation: jvc 1s steps(2) infinite; }}
    @keyframes jvc {{ 50% {{ opacity:0 }} }}
    .jv-dot {{ animation: jvd 2.4s ease-in-out infinite; }}
    @keyframes jvd {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}
    """
    chrome = f"""
    <g id="jarvis-bar">
      <path d="{_chamfer(0.5, 0.5, W - 1, HUD_H - 1, 12)}" fill="{t.card2}" stroke="{t.a1}" stroke-opacity=".55"/>
      <path d="M0.5 {HUD_H - .5} H{W - .5}" stroke="{t.a1}" stroke-opacity=".35"/>
      <circle class="jv-dot" cx="18" cy="20" r="4" fill="{t.a1}"/>
      <circle cx="18" cy="20" r="7" fill="none" stroke="{t.a1}" stroke-opacity=".5"/>
      <text x="32" y="24" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{t.a1}" letter-spacing="2">J.A.R.V.I.S.</text>
      <text x="{vx - 6}" y="24" font-family="{MONO}" font-size="11" fill="{t.muted}">▸</text>
      <clipPath id="jv-clip"><rect x="{vx + 8}" y="6" width="0" height="28">
        <animate attributeName="width" values="{steps}" calcMode="discrete" begin="0.4s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>
      <g clip-path="url(#jv-clip)"><text x="{vx + 8}" y="24" font-family="{MONO}" font-size="11" fill="{t.text}">{esc(voice)}</text></g>
      <rect class="jv-caret" x="{vx + 8}" y="12" width="6" height="14" fill="{t.a1}" opacity=".9">
        <animate attributeName="x" values="{steps}" calcMode="discrete" begin="0.4s" dur="{dur:.2f}s" fill="freeze" additive="sum"/></rect>
      {bars}
      <text x="{W - 16}" y="24" font-family="{MONO}" font-size="10" fill="{t.muted}" text-anchor="end" letter-spacing="1.5">{esc(code)}</text>
    </g>
    <g transform="translate(0 {HUD_H})">{body}</g>
    <path d="{_chamfer(0.5, 0.5, W - 1, NH - 1, 14)}" fill="none" stroke="{t.a1}" stroke-opacity=".45" stroke-width="1"/>
    <path d="M{W - 60} {NH - .5} H{W - 14.5} V{NH - 46}" fill="none" stroke="{t.a1}" stroke-width="2" stroke-opacity=".9"/>
    <path d="M0.5 46 V14.5 H46" fill="none" stroke="{t.a1}" stroke-width="2" stroke-opacity=".9"/>
    """
    return head + style + "</style>" + chrome + "</svg>" + tail
