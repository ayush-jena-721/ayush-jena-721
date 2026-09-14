"""Contribution matrix, lit column by column by a repulsor beam.

Reads data/contributions.json (written by tools/fetch_github.py in the daily
Action; seeded from public commit history until the first run). Every cell
is real activity — the repulsor is the metaphor, the data underneath is not.
"""
import json
import pathlib
import datetime

from .theme import *

_here = pathlib.Path(__file__).resolve()
DATA = next((c for c in [_here.parent.parent / "data" / "contributions.json",
                         _here.parent.parent.parent / "data" / "contributions.json"] if c.exists()), None)

CELL, GAP = 11, 3
SWEEP = 6.0          # seconds for the beam to cross the grid
START = 1.6          # charge-up before firing


def load():
    if DATA:
        return json.loads(DATA.read_text())
    return {"total": 0, "weeks": [], "synced": None, "from": "", "to": ""}


def build(t: Theme) -> str:
    d = load()
    weeks = d.get("weeks") or []
    ncols = max(len(weeks), 53)
    gx = 118                       # grid origin x
    gy = 58
    W = gx + ncols * (CELL + GAP) + 24
    H = gy + 7 * (CELL + GAP) + 48
    dark = True
    S = SCREEN
    lvl = {  # cell fills per level
        0: "#1a2338",
        1: "#5a4416" if dark else "#f3e2a8",
        2: "#9a7420" if dark else "#e2bf5a",
        3: "#d1a12a" if dark else "#b8860b",
        4: "#f5c451" if dark else "#8a5a00",
    }
    beam = S['cyan']
    style = f"""
    .core {{ transform-box: fill-box; transform-origin: center; animation: charge {START}s ease-in both, idle 3s {START}s ease-in-out infinite; }}
    @keyframes charge {{ from {{ transform: scale(.4); opacity:.2 }} to {{ transform: scale(1); opacity:1 }} }}
    @keyframes idle {{ 0%,100% {{ opacity:.85 }} 50% {{ opacity:1 }} }}
    .r1 {{ transform-box: fill-box; transform-origin:center; animation: spin 12s linear infinite; }}
    .r2 {{ transform-box: fill-box; transform-origin:center; animation: spin 20s linear infinite reverse; }}
    @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
    .beam {{ animation: beam {SWEEP}s {START}s linear both; }}
    @keyframes beam {{ 0% {{ transform: translateX(0); opacity:0 }} 3% {{ opacity:1 }} 97% {{ opacity:1 }} 100% {{ transform: translateX({ncols * (CELL + GAP)}px); opacity:0 }} }}
    .flash {{ animation: flash .9s {START}s ease-out both; }}
    @keyframes flash {{ 0% {{ opacity:0 }} 20% {{ opacity:1 }} 100% {{ opacity:0 }} }}
    .lit {{ animation: lit .5s ease-out both; }}
    @keyframes lit {{ 0% {{ opacity:.08; transform: scale(1) }} 40% {{ opacity:1; transform: scale(1.35) }} 100% {{ opacity:1; transform: scale(1) }} }}
    .glow {{ animation: glow 3.2s ease-in-out infinite; }}
    @keyframes glow {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:.8 }} }}
    .hud {{ animation: hud 1.2s ease-out both; }}
    @keyframes hud {{ from {{ opacity:0 }} to {{ opacity:1 }} }}
    """
    defs = (f'<radialGradient id="core"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="{beam}"/>'
            f'<stop offset="1" stop-color="{beam}" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="beamG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{beam}" stop-opacity="0"/>'
            f'<stop offset=".7" stop-color="{beam}" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
            f'<filter id="blur2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.2"/></filter>'
            f'<clipPath id="gridclip"><rect x="{gx - 2}" y="{gy - 2}" width="{ncols * (CELL + GAP) + 4}" height="{7 * (CELL + GAP) + 4}"/></clipPath>')
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs,
                  aria=f"Contribution matrix: {d.get('total', 0)} contributions in the last year, lit by a repulsor beam")]
    o.append(rect(0.5, 0.5, W - 1, H - 1, fill=S['bg'], stroke=S['edge'], r=5))
    # HUD corners
    for (x, y, sx, sy) in [(10, 10, 1, 1), (W - 10, 10, -1, 1), (10, H - 10, 1, -1), (W - 10, H - 10, -1, -1)]:
        o.append(f'<path d="M{x} {y + 14 * sy} V{y} H{x + 14 * sx}" fill="none" stroke="{beam}" stroke-opacity=".6" stroke-width="1.5"/>')
    # header line
    o.append('<g class="hud">')
    o.append(text(gx, 30, "CONTRIBUTION MATRIX", size=11, fill=S['text'], family=MONO, weight=700, ls="2"))
    o.append(text(gx + 172, 30, f"· last 12 months · {d.get('total', 0)} contributions", size=11, fill=S['muted'], family=MONO))
    synced = d.get("synced")
    src = f"synced {synced[:10]} via GitHub API" if synced else "seeded from public commits · daily sync via Actions"
    o.append(text(W - 24, 30, src, size=10, fill=S['muted'], family=MONO, anchor="end"))
    o.append('</g>')

    # repulsor (left)
    rx, ry = 56, gy + 3.5 * (CELL + GAP)
    o.append(f'<g class="r1"><circle cx="{rx}" cy="{ry}" r="34" fill="none" stroke="{beam}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="3 6 20 6"/></g>')
    o.append(f'<g class="r2"><circle cx="{rx}" cy="{ry}" r="27" fill="none" stroke="{S["gold"]}" stroke-opacity=".5" stroke-width="1" stroke-dasharray="14 8 2 8"/></g>')
    o.append(f'<circle cx="{rx}" cy="{ry}" r="21" fill="none" stroke="{beam}" stroke-opacity=".35" stroke-width="6"/>')
    for k in range(10):
        import math
        a = k * 36
        o.append(f'<line x1="{rx + 17 * math.cos(math.radians(a)):.1f}" y1="{ry + 17 * math.sin(math.radians(a)):.1f}" '
                 f'x2="{rx + 25 * math.cos(math.radians(a)):.1f}" y2="{ry + 25 * math.sin(math.radians(a)):.1f}" stroke="{beam}" stroke-opacity=".7" stroke-width="2"/>')
    o.append(f'<g class="core"><circle cx="{rx}" cy="{ry}" r="18" fill="url(#core)"/><circle class="glow" cx="{rx}" cy="{ry}" r="12" fill="{beam}" filter="url(#blur)"/></g>')
    # muzzle flash toward the grid
    o.append(f'<g class="flash"><rect x="{rx + 22}" y="{ry - 5}" width="{gx - rx - 26}" height="10" fill="url(#beamG)" filter="url(#blur2)"/></g>')
    o.append(text(rx, H - 16, "REPULSOR", size=8.5, fill=S['muted'], family=MONO, anchor="middle", ls="2"))

    # weekday labels
    for i, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        o.append(text(gx - 8, gy + i * (CELL + GAP) + CELL - 1, lab, size=9, fill=S['muted'], anchor="end"))
    # month labels
    seen = set()
    for ci, wk in enumerate(weeks):
        if not wk:
            continue
        dt = datetime.date.fromisoformat(wk[0]["date"])
        key = (dt.year, dt.month)
        if key not in seen and dt.day <= 7:
            seen.add(key)
            o.append(text(gx + ci * (CELL + GAP), gy - 8, dt.strftime("%b"), size=9, fill=S['muted']))

    # cells
    o.append('<g clip-path="url(#gridclip)">')
    for ci in range(ncols):
        wk = weeks[ci] if ci < len(weeks) else []
        tcol = START + SWEEP * (ci + 0.5) / ncols
        for ri in range(7):
            x = gx + ci * (CELL + GAP)
            y = gy + ri * (CELL + GAP)
            cell = wk[ri] if ri < len(wk) else None
            if cell is None:
                continue
            L = cell["level"]
            if L == 0:
                o.append(rect(x, y, CELL, CELL, fill=lvl[0], r=2.5))
            else:
                o.append(rect(x, y, CELL, CELL, fill=lvl[0], r=2.5))
                o.append(f'<rect class="lit" style="animation-delay:{tcol:.2f}s;transform-box:fill-box;transform-origin:center" '
                         f'x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{lvl[L]}"/>')
                if L >= 3:
                    o.append(f'<rect class="glow" x="{x - 2}" y="{y - 2}" width="{CELL + 4}" height="{CELL + 4}" rx="4" fill="{lvl[4]}" '
                             f'filter="url(#blur2)" style="animation-delay:{tcol + .5:.2f}s;opacity:0"/>')
    # the beam: a vertical bar sweeping across the grid
    gh = 7 * (CELL + GAP)
    o.append(f'<g class="beam"><rect x="{gx - 6}" y="{gy - 4}" width="6" height="{gh + 6}" fill="{beam}" filter="url(#blur)" opacity=".9"/>'
             f'<rect x="{gx - 3}" y="{gy - 4}" width="1.5" height="{gh + 6}" fill="#fff"/></g>')
    o.append('</g>')

    # legend
    lx = W - 24 - 5 * (CELL + 4) - 60
    o.append(text(lx - 6, H - 16, "Less", size=9, fill=S['muted'], anchor="end"))
    for i in range(5):
        o.append(rect(lx + i * (CELL + 4), H - 25, CELL, CELL, fill=lvl[i], r=2.5))
    o.append(text(lx + 5 * (CELL + 4) + 4, H - 16, "More", size=9, fill=S['muted']))
    o.append(svg_close())
    return "\n".join(o)
