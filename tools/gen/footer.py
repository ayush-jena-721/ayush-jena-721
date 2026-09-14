"""Closing panel with a flowing gradient wave and a short call to action."""
from .theme import *
from .icons import icon


def build(t: Theme) -> str:
    W, H = 900, 150
    style = """
    .w1 { animation: slide 12s linear infinite; }
    .w2 { animation: slide 19s linear infinite reverse; }
    @keyframes slide { to { transform: translateX(-300px) } }
    .in { animation: fade .9s .2s both; }
    @keyframes fade { from { transform: translateY(4px) } to { transform:none } }
    .spark { animation: twinkle 3s ease-in-out infinite; transform-origin: center; }
    @keyframes twinkle { 0%,100% { opacity:.4 } 50% { opacity:1 } }
    """
    defs = f'<clipPath id="fc"><rect x="0" y="0" width="{W}" height="{H}" rx="5"/></clipPath>'
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs,
                  aria="Open to internships, collaborations and interesting problems")]
    o.append('<g clip-path="url(#fc)">')
    o.append(rect(0, 0, W, H, fill=t.card, r=5))
    # two repeating waves; each path spans 300px and repeats 4x so the slide is seamless
    def wave(amp, base, cls, col, op):
        seg = "".join(f"c75,-{amp} 75,{amp} 150,0 " for _ in range(8))
        return (f'<path class="{cls}" d="M-300,{base} {seg}" fill="none" stroke="{col}" '
                f'stroke-width="1.5" stroke-opacity="{op}"/>')
    o.append(wave(18, 108, "w1", t.a1, 0.55))
    o.append(wave(12, 118, "w2", t.a2, 0.45))
    # soft glow behind copy
    o.append(f'<circle cx="120" cy="40" r="180" fill="url(#glow1)"/>')
    o.append(rect(0.5, 0.5, W - 1, H - 1, stroke=t.border, r=5))
    o.append('<g class="in">')
    o.append(f'<g class="spark">{icon("sparkles", 40, 34, t.amber, scale=0.9)}</g>')
    o.append(text(76, 52, "Let's build something real.", size=22, fill=t.text, weight=700, ls="-0.3"))
    o.append(text(76, 76, "Open to internships, ML / computer-vision collaborations, IoT and automation work — or a good technical argument.",
                  size=13, fill=t.muted))
    o.append('</g>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
