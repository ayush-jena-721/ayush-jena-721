"""Animated terminal that 'types' commands and prints the real metrics from
Ayush's project READMEs. Loops."""
from .theme import *

# (kind, text)  kind: cmd | out | ok
LINES = [
    ("jv",  "JARVIS ▸ initiating training run"),
    ("cmd", "python train_cnn.py --dataset mnist"),
    ("out", "epoch 5/5   loss 0.021   val_acc 0.991"),
    ("ok",  "test accuracy 99.03%   params 225k   ~1 min on CPU"),
    ("cmd", "python spam_classifier.py"),
    ("ok",  "accuracy 98.6%   spam F1 0.94   train 3 s"),
    ("jv",  "JARVIS ▸ audio benchmark, three engines"),
    ("cmd", "python transcribe.py samples/"),
    ("ok",  "whisper tiny.en   mean WER 8.8%   8x real-time"),
    ("cmd", "python train_fruit_cnn.py"),
    ("ok",  "8 classes   test accuracy 100%"),
]

CW = 7.25   # monospace glyph width at 12px (estimate, generous)
LH = 21
TYPE_SPEED = 0.045  # s per char
LOOP = 22           # total loop length (s)


def build(t: Theme) -> str:
    S = SCREEN
    W = 440
    H = 52 + LH * (len(LINES) + 1) + 20
    o = [svg_open(W, H, t, bg=False, aria="Terminal showing real results from Ayush's ML projects",
                  extra_defs=f'<clipPath id="win"><rect x="0" y="0" width="{W}" height="{H}" rx="5"/></clipPath>')]
    o.append('<g clip-path="url(#win)">')
    o.append(rect(0, 0, W, H, fill=S['bg'], r=5))
    o.append(rect(0, 0, W, 34, fill=S['bg2']))
    o.append(f'<line x1="0" y1="34.5" x2="{W}" y2="34.5" stroke="{S["edge"]}"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        o.append(f'<circle cx="{18 + i * 18}" cy="17" r="5.5" fill="{c}"/>')
    o.append(text(W / 2, 21, "ayush@lab — jarvis-shell", size=12, fill=S["muted"], family=MONO, anchor="middle"))
    o.append(rect(0.5, 0.5, W - 1, H - 1, stroke=S['edge'], r=5))

    tsec = 0.6
    y = 34 + 30
    for kind, s in LINES:
        if kind == "cmd":
            n = len(s)
            dur = n * TYPE_SPEED
            steps = ";".join(str(round(k * CW, 1)) for k in range(n + 1))
            o.append(text(18, y, "$", size=12, fill=S["green"], family=MONO, weight=700,
                          extra=f'opacity="0"><animate attributeName="opacity" to="1" begin="{tsec:.2f}s" dur="0.01s" fill="freeze"/'))
            # typed text revealed via a clip rect whose width steps char by char
            cid = f"cmd{LINES.index((kind, s))}"
            o.append(f'<clipPath id="{cid}"><rect x="30" y="{y - 14}" width="0" height="{LH}">'
                     f'<animate attributeName="width" values="{steps}" calcMode="discrete" begin="{tsec:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
                     f'</rect></clipPath>')
            o.append(f'<g clip-path="url(#{cid})">' + text(30, y, s, size=12, fill=S['text'], family=MONO) + '</g>')
            # caret that follows while typing then disappears
            o.append(f'<rect x="30" y="{y - 12}" width="7" height="15" fill="{S["cyan"]}" opacity="0">'
                     f'<animate attributeName="opacity" values="0;1;0;1;0" begin="{tsec:.2f}s" dur="{dur:.2f}s" fill="freeze" repeatCount="1"/>'
                     f'<animate attributeName="x" values="{steps}" calcMode="discrete" begin="{tsec:.2f}s" dur="{dur:.2f}s" fill="freeze" additive="sum"/>'
                     f'</rect>')
            tsec += dur + 0.35
        else:
            col = {"ok": S['green'], "jv": S['cyan']}.get(kind, S['muted'])
            prefix = {"ok": "✓ ", "jv": "◈ "}.get(kind, "  ")
            o.append(text(30, y, prefix + s, size=12, fill=col, family=MONO,
                          extra=f'opacity="0"><animate attributeName="opacity" to="1" begin="{tsec:.2f}s" dur="0.15s" fill="freeze"/'))
            tsec += 0.55
        y += LH
    # idle prompt with blinking caret after everything printed
    o.append(text(18, y, "$", size=12, fill=S["green"], family=MONO, weight=700,
                  extra=f'opacity="0"><animate attributeName="opacity" to="1" begin="{tsec:.2f}s" dur="0.01s" fill="freeze"/'))
    o.append(f'<rect x="30" y="{y - 12}" width="7" height="15" fill="{S["cyan"]}" opacity="0">'
             f'<animate attributeName="opacity" values="1;0" begin="{tsec:.2f}s" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
