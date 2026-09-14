"""Toolkit grid: four columns, each with an icon, a heading and wrapped chips."""
from .theme import *
from .icons import icon

GROUPS = [
    ("Machine learning", "brain", "a2",
     ["TensorFlow", "Keras", "scikit-learn", "NLTK", "pandas", "NumPy", "Matplotlib", "Whisper"]),
    ("Vision & audio", "eye", "green",
     ["OpenCV", "CNNs", "Image classification", "SpeechRecognition", "Word-error-rate eval"]),
    ("Software", "code", "a1",
     ["Python", "Flask", "Vue", "SQLite", "Tkinter", "Streamlit", "CLI tooling"]),
    ("Hardware & ops", "chip", "amber",
     ["ESP32", "Raspberry Pi", "Sensors", "Automation", "Git & GitHub", "GitHub Actions"]),
]


def build(t: Theme) -> str:
    W = 900
    cols = 4
    gap = 14
    cw = (W - gap * (cols - 1)) / cols  # ~214
    pad = 16
    style = """
    .chip { animation: pop .5s cubic-bezier(.2,.8,.2,1) both; }
    @keyframes pop { from { transform: translateY(4px) } to { transform:none } }
    .hd { animation: pop .6s both; }
    .ic { animation: hue 6s ease-in-out infinite; transform-origin: center; }
    """
    # measure heights first
    layouts = []
    maxh = 0
    for gi, (title, ic, colkey, items) in enumerate(GROUPS):
        x0 = gi * (cw + gap)
        x, y = x0 + pad, 74
        placed = []
        for it in items:
            est = int(len(it) * 11 * 0.6 + 20)
            if x + est > x0 + cw - pad and x > x0 + pad:
                x = x0 + pad
                y += 30
            placed.append((x, y, it))
            x += est + 6
        h = y + 24 + pad
        maxh = max(maxh, h)
        layouts.append((x0, title, ic, colkey, placed))
    H = maxh
    o = [svg_open(W, H, t, bg=False, style=style, aria="Ayush Jena's toolkit")]
    k = 0
    for gi, (x0, title, ic, colkey, placed) in enumerate(layouts):
        col = getattr(t, colkey)
        o.append(card(t, x0 + 0.5, 0.5, cw - 1, H - 1))
        # accent top bar
        o.append(rect(x0 + 16, 0, cw - 32, 2, fill=col, r=1))
        o.append(f'<g class="hd" style="animation-delay:{gi * .1}s">')
        o.append(rect(x0 + pad, 18, 30, 30, fill=t.card2, stroke=t.border, r=8))
        o.append(icon(ic, x0 + pad + 4, 22, col, scale=0.9))
        o.append(text(x0 + pad + 40, 38, title, size=14, fill=t.text, weight=600))
        o.append('</g>')
        for (x, y, it) in placed:
            s, w = chip(t, x, y, it, color=col, size=11, h=24, delay=0.15 + k * 0.045)
            o.append(s)
            k += 1
    o.append(svg_close())
    return "\n".join(o)
