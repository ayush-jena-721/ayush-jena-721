"""One card per repository — floating panel with depth shadow, animated
gradient edge, scan sweep, glowing metric ring, features and links.
Metrics are the ones published in each repo's README."""
from .theme import *
from .icons import icon

PROJECTS = [
    dict(key="digits", icon="pen", title="Handwritten Digit Recognizer", repo="handwritten-digit-recognizer",
         desc="Keras CNN on MNIST — 225k parameters, about a minute to train on a CPU.",
         feats=["Conv/pool stack with dropout", "Confusion matrix + misclassified gallery", "predict.py on any image"],
         stack=["TensorFlow", "Keras", "NumPy"], metric="99.03%", label="test accuracy", pct=99.03, colkey="a1"),
    dict(key="spam", icon="shield", title="Spam Email Classifier", repo="spam-email-classifier",
         desc="Two classic NLP models trained, compared and shipped with a command-line predictor.",
         feats=["TF-IDF features", "Naive Bayes vs. linear SVM", "Top spam-words + length analysis"],
         stack=["scikit-learn", "pandas", "Matplotlib"], metric="98.6%", label="accuracy · F1 0.94", pct=98.6, colkey="green"),
    dict(key="fruit", icon="image", title="Fruit Image Classifier", repo="fruit-image-classifier",
         desc="Image CNN over 8 fruit classes, with stress tests and an analysis of what the network learned.",
         feats=["CNN with flip/rotation augmentation", "Stress test + mean-colour analysis", "predict.py on your own photo"],
         stack=["TensorFlow", "Keras", "OpenCV"], metric="100%", label="accuracy · 8 classes", pct=100, colkey="amber"),
    dict(key="speech", icon="mic", title="Speech-to-Text Transcription", repo="speech-to-text-transcription",
         desc="Three recognition engines benchmarked by word error rate — offline Whisper tiny.en runs at 8× real-time.",
         feats=["Whisper · Sphinx · Google engines", "WER evaluation on real + synthetic audio", "Speed comparison plot"],
         stack=["Whisper", "SpeechRecognition", "PyTorch"], metric="8.8%", label="word error rate ↓", pct=91.2, colkey="a2"),
    dict(key="sentiment", icon="chat", title="Twitter Sentiment Analysis", repo="twitter-sentiment-analysis",
         desc="VADER lexicon vs. ML models trained on 45 000 real tweets — negative, neutral, positive.",
         feats=["NLTK preprocessing pipeline", "VADER vs. logistic regression / linear SVM", "Class-balance + word analysis"],
         stack=["NLTK", "scikit-learn", "pandas"], metric="0.60", label="macro-F1 · 3 classes", pct=60, colkey="rose"),
]

W, H = 900, 150   # full-width rows: readable on phones, one per line


def ring(t, cx, cy, r, pct, col, delay):
    C = 2 * 3.14159 * r
    off = C * (1 - pct / 100)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t.faint}" stroke-width="6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round" '
            f'transform="rotate(-90 {cx} {cy})" stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}">'
            f'<animate attributeName="stroke-dashoffset" from="{C:.1f}" to="{off:.1f}" begin="{delay}s" dur="1.4s" '
            f'fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1"/></circle>')


def one(t: Theme, p) -> str:
    col = getattr(t, p["colkey"])
    style = f"""
    .float {{ animation: float 6s ease-in-out infinite; }}
    @keyframes float {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(-3px) }} }}
    .edge {{ stroke-dasharray: 260 1900; animation: edge 9s linear infinite; }}
    @keyframes edge {{ to {{ stroke-dashoffset: -2160 }} }}
    .scan {{ animation: scan 8s ease-in-out infinite; }}
    @keyframes scan {{ 0%,55% {{ transform: translateX(-160px); opacity:0 }} 57% {{ opacity:1 }} 92% {{ transform: translateX(1000px); opacity:1 }} 93%,100% {{ opacity:0 }} }}
    .halo {{ animation: halo 3.6s ease-in-out infinite; }}
    @keyframes halo {{ 0%,100% {{ opacity:.22 }} 50% {{ opacity:.55 }} }}
    .arrow {{ animation: nudge 2.4s ease-in-out infinite; }}
    @keyframes nudge {{ 0%,100% {{ transform: translateX(0) }} 50% {{ transform: translateX(4px) }} }}
    .chip {{ animation: rise .6s cubic-bezier(.2,.8,.2,1) both; }}
    @keyframes rise {{ from {{ transform: translateY(4px) }} to {{ transform:none }} }}
    """
    defs = (f'<linearGradient id="edgeG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="scanG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{col}" stop-opacity=".14"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
            f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="{.45 if t.name == "dark" else .14}"/></filter>'
            f'<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12"/></filter>'
            f'<clipPath id="cc"><rect x="6" y="6" width="{W - 12}" height="{H - 14}" rx="5"/></clipPath>')
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs, aria=f"{p['title']} — {p['metric']} {p['label']}")]
    o.append('<g class="float">')
    o.append(rect(6, 6, W - 12, H - 14, fill=t.card, stroke=t.border, r=5, extra='filter="url(#shadow)"'))
    o.append(f'<g clip-path="url(#cc)">')
    o.append(f'<circle class="halo" cx="{W - 84}" cy="{H / 2 - 4}" r="62" fill="{col}" filter="url(#soft)"/>')
    o.append(f'<rect class="scan" x="6" y="6" width="160" height="{H}" fill="url(#scanG)"/>')
    o.append('</g>')
    o.append(f'<rect class="edge" x="6.5" y="6.5" width="{W - 13}" height="{H - 15}" rx="5" fill="none" stroke="url(#edgeG)" stroke-width="1.5"/>')
    o.append(rect(6, 30, 4, H - 62, fill=col, r=2))
    # icon + title + repo
    o.append(rect(26, 24, 42, 42, fill=t.card2, stroke=t.border, r=11))
    o.append(icon(p["icon"], 32, 30, col, scale=1.25))
    o.append(text(84, 44, p["title"], size=19, fill=t.text, weight=700))
    o.append(text(84, 63, p['repo'], size=12, fill=t.muted, family=MONO))
    # description (one line, larger)
    o.append(text(26, 92, p["desc"], size=13.5, fill=t.muted))
    # features in a row
    x = 26
    for f in p["feats"]:
        o.append(f'<path d="M{x} 113 l3.5 3.5 6-7" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(text(x + 15, 117, f, size=12.5, fill=t.text))
        x += int(len(f) * 6.6) + 34
    # stack chips right of the title area
    x = 470
    for i, s_ in enumerate(p["stack"]):
        c, w = chip(t, x, 30, s_, color=col, size=11.5, h=24, delay=0.2 + i * 0.1)
        o.append(c)
        x += w + 6
    # metric ring
    o.append(ring(t, W - 84, H / 2 - 4, 36, p["pct"], col, 0.3))
    o.append(text(W - 84, H / 2 + 2, p["metric"], size=17, fill=t.text, weight=800, anchor="middle", family=MONO))
    o.append(text(W - 84, H - 14, p["label"], size=11, fill=t.muted, anchor="middle"))
    # open link
    o.append(text(W - 166, 63, "Open repo", size=12.5, fill=col, weight=700, anchor="end"))
    o.append(f'<g class="arrow">{icon("arrow", W - 162, 52, col, scale=0.7)}</g>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)


def more_card(t: Theme) -> str:
    style = """
    .dash { stroke-dasharray: 6 6; animation: march 1.6s linear infinite; }
    @keyframes march { to { stroke-dashoffset: -12 } }
    .arrow { animation: nudge 2s ease-in-out infinite; }
    @keyframes nudge { 0%,100% { transform: translateX(0) } 50% { transform: translateX(6px) } }
    .orbit { transform-box: fill-box; transform-origin: center; animation: spin 18s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg) } }
    """
    o = [svg_open(W, H, t, bg=False, style=style, aria="See all repositories")]
    o.append(rect(6.5, 6.5, W - 13, H - 15, fill=t.bg, stroke=t.border, r=5, extra='class="dash"'))
    o.append(rect(26, 24, 42, 42, fill=t.card2, stroke=t.border, r=11))
    o.append(icon("folder", 32, 30, t.a1, scale=1.25))
    o.append(text(84, 44, "All repositories", size=19, fill=t.text, weight=700))
    o.append(text(84, 63, "github.com/ayush-jena-721?tab=repositories", size=12, fill=t.muted, family=MONO))
    o.append(text(26, 92, "Every project ships with a README, a reproducible training script, saved metrics and an MIT license.", size=13.5, fill=t.muted))
    o.append(text(26, 117, "Also on GitHub: IoT builds, desktop tools and the experiments that never became products.", size=12.5, fill=t.muted))
    o.append(text(W - 166, 63, "Browse the code", size=12.5, fill=t.a1, weight=700, anchor="end"))
    o.append(f'<g class="arrow">{icon("arrow", W - 162, 52, t.a1, scale=0.7)}</g>')
    o.append(f'<g class="orbit"><circle cx="{W - 84}" cy="{H / 2 - 4}" r="36" fill="none" stroke="{t.a2}" stroke-opacity=".6" stroke-dasharray="4 8 30 8"/></g>')
    o.append(f'<circle cx="{W - 84}" cy="{H / 2 - 4}" r="22" fill="none" stroke="{t.a1}" stroke-opacity=".6"/>')
    o.append(icon("github", W - 98, H / 2 - 18, t.text, scale=1.15))
    o.append(svg_close())
    return "\n".join(o)


def build(t: Theme):
    out = {f"project-{p['key']}": one(t, p) for p in PROJECTS}
    out["project-more"] = more_card(t)
    return out
