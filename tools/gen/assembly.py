"""Workshop hologram: an exploded wireframe of Ayush's own hardware — the
ESP32 field node — hovering over an emitter and assembling itself part by
part, with an assembly sequence on the left and spec callouts on the right.
Drawn as a projection: same dark screen in both themes."""
import math
import random

from .theme import *

W, H = 900, 360
CX, CY = 450, 232          # iso origin (bottom centre of the device)
COS, SIN = math.cos(math.radians(30)), math.sin(math.radians(30))


def iso(x, y, z):
    return CX + (x - y) * COS, CY + (x + y) * SIN - z


def poly(pts, stroke, fill="none", sw=1.2, op=1.0, extra=""):
    d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{op}" stroke-linejoin="round" {extra}/>'


def box(x, y, z, w, d, h, stroke, fill, sw=1.2):
    """Isometric wireframe box with faint face fills. Origin at (x,y,z), size w (x), d (y), h (z)."""
    p = {k: iso(*v) for k, v in {
        "a": (x, y, z), "b": (x + w, y, z), "c": (x + w, y + d, z), "d": (x, y + d, z),
        "e": (x, y, z + h), "f": (x + w, y, z + h), "g": (x + w, y + d, z + h), "h": (x, y + d, z + h)}.items()}
    out = [poly([p["e"], p["f"], p["g"], p["h"]], stroke, fill=fill, sw=sw, extra='fill-opacity=".18"'),   # top
           poly([p["d"], p["c"], p["g"], p["h"]], stroke, fill=fill, sw=sw, extra='fill-opacity=".10"'),   # front-left
           poly([p["b"], p["c"], p["g"], p["f"]], stroke, fill=fill, sw=sw, extra='fill-opacity=".06"'),   # front-right
           poly([p["a"], p["b"], p["c"], p["d"]], stroke, sw=sw * .7, op=.45)]                              # bottom (hidden edges)
    return "\n".join(out)


def build(t: Theme) -> str:
    S = SCREEN
    cyan, gold, red, green = S["cyan"], S["gold"], S["red"], S["green"]
    rnd = random.Random(3)
    # parts: (name, exploded z-offset, drawing function)
    PARTS = [
        ("base", 0), ("battery", 34), ("pcb", 56), ("esp32", 74), ("probes", 86), ("antenna", 92), ("lid", 104),
    ]
    style = ["""
    .holo { animation: hover 7s ease-in-out infinite; }
    @keyframes hover { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-6px) } }
    .flick { animation: flick 11s steps(1) infinite; }
    @keyframes flick { 0%,100% { opacity:1 } 37% { opacity:1 } 38% { opacity:.55 } 39% { opacity:1 } 81% { opacity:1 } 82% { opacity:.7 } 83% { opacity:1 } }
    .ring { transform-box: fill-box; transform-origin: center; animation: spin 20s linear infinite; }
    .ring2 { transform-box: fill-box; transform-origin: center; animation: spin 32s linear infinite reverse; }
    @keyframes spin { to { transform: rotate(360deg) } }
    .march { animation: march 6s linear infinite; }
    .march2 { animation: march 9s linear infinite reverse; }
    @keyframes march { to { stroke-dashoffset: -200 } }
    .emit { animation: emit 2.2s ease-in-out infinite; }
    @keyframes emit { 0%,100% { opacity:.6 } 50% { opacity:1 } }
    .scan { animation: scan 4s linear infinite; }
    @keyframes scan { from { transform: translateY(-40px) } to { transform: translateY(300px) } }
    .mote { animation: mote 6s ease-in-out infinite alternate; }
    @keyframes mote { to { transform: translateY(-18px) } }
    .step { animation: step 12s ease-in-out infinite; }
    @keyframes step { 0%,8% { opacity:.35 } 12%,100% { opacity:1 } }
    .fill { transform-box: fill-box; transform-origin: left; animation: fill 12s ease-in-out infinite; }
    @keyframes fill { 0% { transform: scaleX(0) } 45% { transform: scaleX(1) } 62% { transform: scaleX(1) } 70% { transform: scaleX(0) } 100% { transform: scaleX(0) } }
    .call { animation: call 12s ease-in-out infinite; }
    @keyframes call { 0%,40% { opacity:.35 } 48%,62% { opacity:1 } 70%,100% { opacity:.35 } }
    """]
    # one keyframe set per part: exploded -> assembled (staggered) -> hold -> exploded
    for i, (name, dz) in enumerate(PARTS):
        s0 = 6 + i * 5            # % when this part starts moving down
        s1 = s0 + 10
        style.append(f".p-{name} {{ animation: as-{name} 12s cubic-bezier(.4,0,.2,1) infinite; }}\n"
                     f"@keyframes as-{name} {{ 0%,{s0}% {{ transform: translateY(-{dz}px) }} {s1}%,60% {{ transform: translateY(0) }} "
                     f"72%,100% {{ transform: translateY(-{dz}px) }} }}")
    defs = (f'<radialGradient id="dot"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="{cyan}"/><stop offset="1" stop-color="{cyan}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="coneG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cyan}" stop-opacity="0"/><stop offset="1" stop-color="{cyan}" stop-opacity=".22"/></linearGradient>'
            f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cyan}" stop-opacity="0"/><stop offset="1" stop-color="{cyan}" stop-opacity=".22"/></linearGradient>'
            f'<pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="{cyan}" stroke-opacity=".07"/></pattern>'
            f'<clipPath id="screen"><rect x="0" y="0" width="{W}" height="{H}" rx="5"/></clipPath>'
            f'<clipPath id="stage"><rect x="230" y="-60" width="440" height="{H + 40}"/></clipPath>'
            f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
            f'<filter id="glowT" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    o = [svg_open(W, H, t, bg=False, style="\n".join(style), extra_defs=defs,
                  aria="Workshop hologram: the ESP32 field node assembling itself part by part")]
    o.append('<g clip-path="url(#screen)">')
    o.append(rect(0, 0, W, H, fill=S["bg"], r=5))
    o.append(rect(0, 0, W, H, fill="url(#grid)"))
    o.append(f'<circle cx="{CX}" cy="{CY - 60}" r="170" fill="{cyan}" fill-opacity=".06" filter="url(#blur)"/>')
    # HUD corners + header
    for (x, y, sx, sy) in [(12, 12, 1, 1), (W - 12, 12, -1, 1), (12, H - 12, 1, -1), (W - 12, H - 12, -1, -1)]:
        o.append(f'<path d="M{x} {y + 14 * sy} V{y} H{x + 14 * sx}" fill="none" stroke="{cyan}" stroke-opacity=".7" stroke-width="1.5"/>')
    o.append(text(30, 34, "WORKSHOP · HOLOGRAPHIC ASSEMBLY", size=11, fill=S["text"], family=MONO, weight=700, ls="2", extra='filter="url(#glowT)"'))
    o.append(text(W - 30, 34, "UNIT: FIELD NODE · ESP32 · REV 2026.09", size=10, fill=S["muted"], family=MONO, anchor="end", ls="1"))

    # ---- emitter + cone
    ex, ey = CX, H - 26
    o.append(f'<ellipse class="march" cx="{ex}" cy="{ey}" rx="150" ry="11" fill="none" stroke="{cyan}" stroke-opacity=".6" stroke-dasharray="6 12 60 12"/>')
    o.append(f'<ellipse class="march2" cx="{ex}" cy="{ey}" rx="110" ry="8" fill="none" stroke="{gold}" stroke-opacity=".6" stroke-dasharray="40 14 4 14"/>')
    o.append(f'<ellipse cx="{ex}" cy="{ey}" rx="60" ry="4.5" fill="none" stroke="{cyan}" stroke-opacity=".8"/>')
    o.append(f'<circle class="emit" cx="{ex}" cy="{ey}" r="10" fill="url(#dot)"/>')
    o.append(f'<polygon points="{ex - 30},{ey - 2} {ex + 30},{ey - 2} {CX + 120},{60} {CX - 120},{60}" fill="url(#coneG)"/>')

    # ---- the device (exploded wireframe)
    o.append(f'<g transform="translate({CX} {CY + 6}) scale(1.38) translate({-CX} {-CY})"><g class="holo"><g class="flick" clip-path="url(#stage)">')
    # guide axis
    o.append(f'<line x1="{CX}" y1="{CY - 200}" x2="{CX}" y2="{CY + 10}" stroke="{cyan}" stroke-opacity=".25" stroke-dasharray="3 5"/>')
    parts_svg = {
        "base": box(-60, -45, 0, 120, 90, 14, cyan, cyan),
        "battery": box(-52, -36, 16, 36, 70, 16, gold, gold) + "\n" + "".join(
            f'<line x1="{iso(-52 + 6 + k * 8, -36, 32)[0]:.1f}" y1="{iso(-52 + 6 + k * 8, -36, 32)[1]:.1f}" x2="{iso(-52 + 6 + k * 8, 34, 32)[0]:.1f}" y2="{iso(-52 + 6 + k * 8, 34, 32)[1]:.1f}" stroke="{gold}" stroke-opacity=".35"/>' for k in range(4)),
        "pcb": box(-10, -40, 16, 66, 80, 3, green, green) + "\n" + "".join(
            box(4 + (k % 3) * 18, 20 - (k // 3) * 22, 19, 10, 8, 4, green, green, sw=.9) for k in range(4)),
        "esp32": box(6, -34, 19, 28, 40, 6, cyan, cyan) + "\n" + "".join(
            f'<line x1="{iso(6, -34 + 4 + k * 5, 19)[0]:.1f}" y1="{iso(6, -34 + 4 + k * 5, 19)[1]:.1f}" x2="{iso(0, -34 + 4 + k * 5, 19)[0]:.1f}" y2="{iso(0, -34 + 4 + k * 5, 19)[1]:.1f}" stroke="{cyan}" stroke-opacity=".7"/>' for k in range(7)),
        "probes": "".join(
            f'<line x1="{iso(70, -30 + k * 24, 12)[0]:.1f}" y1="{iso(70, -30 + k * 24, 12)[1]:.1f}" x2="{iso(70, -30 + k * 24, -30)[0]:.1f}" y2="{iso(70, -30 + k * 24, -30)[1]:.1f}" stroke="{red}" stroke-width="2" stroke-linecap="round"/>'
            f'<circle cx="{iso(70, -30 + k * 24, 12)[0]:.1f}" cy="{iso(70, -30 + k * 24, 12)[1]:.1f}" r="3" fill="none" stroke="{red}"/>' for k in range(3)),
        "antenna": (f'<line x1="{iso(-40, 30, 22)[0]:.1f}" y1="{iso(-40, 30, 22)[1]:.1f}" x2="{iso(-40, 30, 74)[0]:.1f}" y2="{iso(-40, 30, 74)[1]:.1f}" stroke="{cyan}" stroke-width="2" stroke-linecap="round"/>'
                    f'<circle cx="{iso(-40, 30, 76)[0]:.1f}" cy="{iso(-40, 30, 76)[1]:.1f}" r="4" fill="{cyan}"/>'
                    f'<circle cx="{iso(-40, 30, 76)[0]:.1f}" cy="{iso(-40, 30, 76)[1]:.1f}" r="10" fill="none" stroke="{cyan}" stroke-opacity=".5"><animate attributeName="r" values="6;16" dur="1.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".7;0" dur="1.6s" repeatCount="indefinite"/></circle>'),
        "lid": box(-60, -45, 14, 120, 90, 8, cyan, cyan) + "\n" + poly([iso(-36, -28, 22), iso(36, -28, 22), iso(36, 28, 22), iso(-36, 28, 22)], cyan, sw=.9, op=.6, extra='stroke-dasharray="3 3"'),
    }
    for name, dz in PARTS:
        o.append(f'<g class="p-{name}">{parts_svg[name]}</g>')
    # floating motes
    for k in range(14):
        x = CX + rnd.uniform(-150, 150); y = CY - rnd.uniform(-10, 190)
        o.append(f'<circle class="mote" style="animation-delay:{rnd.uniform(-6, 0):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([1, 1, 1.5])}" fill="{cyan}" fill-opacity=".6"/>')
    o.append('</g></g></g>')
    # scan bar across the stage
    o.append(f'<g clip-path="url(#stage)"><rect class="scan" x="250" y="20" width="400" height="40" fill="url(#scanG)"/></g>')

    # ---- left: assembly sequence
    steps = [("01", "Mount base plate", 0), ("02", "Seat Li-ion pack", 1), ("03", "Drop PCB on standoffs", 2),
             ("04", "Flash ESP32 firmware", 3), ("05", "Wire soil / temp probes", 4), ("06", "Fit antenna + close lid", 6)]
    o.append(text(30, 70, "ASSEMBLY SEQUENCE", size=9.5, fill=cyan, family=MONO, weight=700, ls="2"))
    for i, (n, lab, pi) in enumerate(steps):
        y = 92 + i * 34
        s0 = 6 + pi * 5
        o.append(f'<g class="step" style="animation-delay:{s0 * .12:.2f}s">')
        o.append(text(30, y, n, size=10, fill=gold, family=MONO, weight=700))
        o.append(text(52, y, lab, size=11.5, fill=S["text"]))
        o.append(f'<rect x="30" y="{y + 7}" width="190" height="2" fill="{cyan}" fill-opacity=".15"/>')
        o.append(f'<rect class="fill" style="animation-delay:{(s0 - 6) * .12:.2f}s" x="30" y="{y + 7}" width="190" height="2" fill="{cyan}"/>')
        o.append('</g>')
    o.append(text(30, H - 34, "STATUS", size=8.5, fill=S["muted"], family=MONO, ls="1.5"))
    o.append(text(82, H - 34, "assembling · looping every 12 s", size=10, fill=green, family=MONO))

    # ---- right: spec callouts
    o.append(text(W - 30, 70, "SPECIFICATION", size=9.5, fill=cyan, family=MONO, weight=700, ls="2", anchor="end"))
    specs = [("MCU", "ESP32 · Wi-Fi + BLE · 240 MHz", cyan), ("SENSING", "soil moisture · temp · humidity", red),
             ("POWER", "Li-ion pack · deep-sleep duty cycle", gold), ("UPLINK", "MQTT → Python service → dashboard", cyan),
             ("ENCLOSURE", "IP-rated shell · vented lid", cyan), ("SOFTWARE", "Flask API · SQLite · alerts", green)]
    for i, (k, v, col) in enumerate(specs):
        y = 92 + i * 34
        o.append(f'<g class="call" style="animation-delay:{i * .4:.1f}s">')
        o.append(text(W - 30, y, k, size=9, fill=col, family=MONO, weight=700, ls="1.5", anchor="end"))
        o.append(text(W - 30, y + 14, v, size=11, fill=S["text"], anchor="end"))
        o.append(f'<line x1="{W - 226}" y1="{y + 20}" x2="{W - 30}" y2="{y + 20}" stroke="{col}" stroke-opacity=".3"/>')
        o.append(f'<circle cx="{W - 226}" cy="{y + 20}" r="2" fill="{col}"/>')
        o.append('</g>')
    o.append(rect(0.5, 0.5, W - 1, H - 1, stroke=S["edge"], r=5))
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
