"""Hardware / desktop / experimental work that lives outside the public ML repos."""
from .theme import *
from .icons import icon

ITEMS = [
    ("Intelligent Agro Management System", "leaf", "green", "IoT · environmental control",
     ["ESP32", "Sensors", "Python", "Web dashboard"], "Deployed"),
    ("Inventory Management System", "box", "a1", "Desktop app · computer vision",
     ["Python", "Tkinter", "OpenCV", "SQLite", "QR"], "Operational"),
    ("Computer vision experiments", "eye", "a2", "Research · prototypes",
     ["OpenCV", "Deep learning", "Python"], "Ongoing"),
    ("Python applications & tooling", "term", "amber", "Fundamentals · CLI",
     ["OOP", "CLI", "Modules"], "Ongoing"),
]


def build(t: Theme) -> str:
    W = 900
    n = len(ITEMS)
    gap = 14
    cols = 2
    cw = (W - gap * (cols - 1)) / cols
    rh = 150
    H = rh * 2 + gap
    style = """
    .c { animation: up .6s cubic-bezier(.2,.8,.2,1) both; }
    @keyframes up { from { transform: translateY(6px)} to { transform:none } }
    .chip { animation: up .5s both; }
    .pulse { animation: pulse 2.4s ease-in-out infinite; transform-origin: center; }
    @keyframes pulse { 0%,100% { opacity:.55 } 50% { opacity:1 } }
    """
    o = [svg_open(W, H, t, bg=False, style=style, aria="Other engineering work: IoT, desktop and vision prototypes")]
    for i, (title, ic, colkey, kind, tags, status) in enumerate(ITEMS):
        col = getattr(t, colkey)
        x0 = (i % cols) * (cw + gap)
        y0 = (i // cols) * (rh + gap)
        o.append(f'<g transform="translate(0 {y0})"><g class="c" style="animation-delay:{i * .12}s">')
        o.append(card(t, x0 + 0.5, 0.5, cw - 1, rh - 1))
        o.append(rect(x0 + 16, 18, 32, 32, fill=t.card2, stroke=t.border, r=8))
        o.append(icon(ic, x0 + 20, 22, col, scale=1.0))
        # status pill top-right
        sw = len(status) * 6.8 + 24
        o.append(rect(x0 + cw - 16 - sw, 22, sw, 20, fill=t.card2, stroke=t.border, r=10))
        o.append(f'<circle class="pulse" cx="{x0 + cw - 16 - sw + 10}" cy="32" r="3" fill="{col}"/>')
        o.append(text(x0 + cw - 16 - sw + 18, 36, status, size=11, fill=t.muted, weight=600))
        # title (wrap at ~ 2 lines by splitting on words)
        words = title.split()
        lines, cur = [], ""
        for w in words:
            if len(cur + " " + w) > 40 and cur:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for li, ln in enumerate(lines):
            o.append(text(x0 + 60, 40 + li * 18, ln, size=16, fill=t.text, weight=700))
        o.append(text(x0 + 60, 40 + len(lines) * 18, kind, size=12, fill=t.muted))
        # tags
        x, y = x0 + 16, 96
        for j, tg in enumerate(tags):
            est = int(len(tg) * 12 * 0.6 + 20)
            if x + est > x0 + cw - 12 and x > x0 + 16:
                x = x0 + 16; y += 26
            if y > rh - 30:
                break
            s, w = chip(t, x, y, tg, color=col, size=12, h=24, delay=0.3 + i * .12 + j * .06)
            o.append(s)
            x += w + 5
        o.append('</g></g>')
    o.append(svg_close())
    return "\n".join(o)
