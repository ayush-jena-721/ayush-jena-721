"""Engineering blueprint: how a project gets built, drawn as a sheet —
sensor node → data → model → app, with dimension lines and a title block.
Strokes draw themselves in on load. A blueprint is blue in both themes."""
from .theme import *
from .icons import icon

W, H = 900, 350


def build(t: Theme) -> str:
    dark = t.name == "dark"
    paper = "#0b2447" if dark else "#1d4ed8"
    paper2 = "#0e2d5a" if dark else "#2559e0"
    ink = "#bfe3ff" if dark else "#eaf2ff"
    ink2 = "#7fb8e8" if dark else "#c7dbff"
    gold = "#f5c451"
    red = "#ff6b6b"
    style = """
    .draw { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: draw 2.6s ease-out forwards; }
    .d2 { animation-delay: .6s } .d3 { animation-delay: 1.2s } .d4 { animation-delay: 1.8s } .d5 { animation-delay: 2.4s }
    @keyframes draw { to { stroke-dashoffset: 0 } }
    .lbl { animation: show .8s both; } .l2 { animation-delay: 1.2s } .l3 { animation-delay: 1.8s } .l4 { animation-delay: 2.4s } .l5 { animation-delay: 3s }
    @keyframes show { from { opacity: 0 } to { opacity: 1 } }
    .flow { stroke-dasharray: 4 8; animation: flow 1.6s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: -24 } }
    .pkt { animation: none }
    .cursor { animation: cur 6s ease-in-out infinite; }
    @keyframes cur { 0%,100% { transform: translate(0,0) } 30% { transform: translate(420px, 40px) } 60% { transform: translate(220px, 120px) } }
    .rot { transform-box: fill-box; transform-origin: center; animation: spin 10s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg) } }
    """
    defs = (f'<pattern id="bp" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{ink}" stroke-opacity=".14"/></pattern>'
            f'<pattern id="bp2" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="{ink}" stroke-opacity=".28"/></pattern>'
            f'<clipPath id="sheet"><rect x="0" y="0" width="{W}" height="{H}" rx="5"/></clipPath>'
            f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{ink}"/></marker>'
            f'<marker id="dim" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M2 2L8 8M2 8L8 2" stroke="{ink2}" stroke-width="1.5"/></marker>')
    o = [svg_open(W, H, t, bg=False, style=style, extra_defs=defs, aria="Blueprint: sensor node to data to model to application")]
    o.append('<g clip-path="url(#sheet)">')
    o.append(rect(0, 0, W, H, fill=paper, r=5))
    o.append(rect(0, 0, W, H, fill="url(#bp)"))
    o.append(rect(0, 0, W, H, fill="url(#bp2)"))
    # sheet border (double line)
    o.append(rect(10, 10, W - 20, H - 20, stroke=ink, r=2, extra='stroke-opacity=".9"'))
    o.append(rect(16, 16, W - 32, H - 32, stroke=ink, r=1, extra='stroke-opacity=".35"'))
    # header strip
    o.append(text(30, 40, "SHEET 01 · HOW A PROJECT GETS BUILT", size=12, fill=ink, family=MONO, weight=700, ls="2"))
    o.append(text(W - 30, 40, "A. JENA · REV 2026.09 · SCALE NTS", size=10.5, fill=ink2, family=MONO, anchor="end", ls="1"))
    o.append(f'<line x1="30" y1="50" x2="{W - 30}" y2="50" stroke="{ink}" stroke-opacity=".6"/>')

    lw = 1.6
    def box(x, y, w, h, title, sub, cls, lcls, ic=None):
        out = [f'<rect class="draw {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{paper2}" fill-opacity=".6" stroke="{ink}" stroke-width="{lw}"/>']
        # corner ticks
        for (cx, cy, sx, sy) in [(x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)]:
            out.append(f'<path class="draw {cls}" d="M{cx + 8 * sx} {cy} L{cx} {cy} L{cx} {cy + 8 * sy}" fill="none" stroke="{gold}" stroke-width="1.5"/>')
        out.append(f'<g class="lbl {lcls}">')
        if ic:
            out.append(icon(ic, x + w / 2 - 12, y + 12, ink, scale=1.0, sw=1.5))
        out.append(text(x + w / 2, y + 54, title, size=12.5, fill=ink, family=MONO, weight=700, anchor="middle", ls="1"))
        out.append(text(x + w / 2, y + 70, sub, size=10, fill=ink2, anchor="middle"))
        out.append('</g>')
        return "\n".join(out)

    bw, bh, by = 150, 84, 90
    xs = [40, 250, 460, 670]
    stages = [("SENSOR NODE", "ESP32 · sensors · MQTT", "chip", "", ""),
              ("DATA PIPELINE", "Python · pandas · cleaning", "code", "d2", "l2"),
              ("MODEL", "Keras CNN / scikit-learn", "brain", "d3", "l3"),
              ("APPLICATION", "Flask · desktop · dashboard", "term", "d4", "l4")]
    for (x, (ttl, sub, ic, c, l)) in zip(xs, stages):
        o.append(box(x, by, bw, bh, ttl, sub, c, l, ic))
    # arrows with flowing dashes
    for i in range(3):
        x1 = xs[i] + bw + 6; x2 = xs[i + 1] - 6; y = by + bh / 2
        o.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ink}" stroke-opacity=".5" stroke-width="1.2" marker-end="url(#ar)"/>')
        o.append(f'<line class="flow" x1="{x1}" y1="{y}" x2="{x2 - 8}" y2="{y}" stroke="{gold}" stroke-width="2"/>')
        # data packet riding the arrow
        o.append(f'<circle r="3" fill="{gold}"><animateMotion dur="2.4s" begin="{i * .8}s" repeatCount="indefinite" path="M{x1},{y} L{x2 - 8},{y}"/></circle>')
    # feedback loop (evaluate -> retrain) under the model
    o.append(f'<path class="draw d4" d="M{xs[3] + bw / 2} {by + bh} V{by + bh + 26} H{xs[2] + bw / 2} V{by + bh + 2}" fill="none" stroke="{red}" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
    o.append(text((xs[2] + xs[3] + bw) / 2, by + bh + 40, "evaluate → retrain (confusion matrix, WER, F1)", size=10, fill=red, family=MONO, anchor="middle", cls="lbl l4"))
    # dimension line across the whole pipeline
    dy = by - 22
    o.append(f'<line class="draw d2" x1="{xs[0]}" y1="{dy}" x2="{xs[3] + bw}" y2="{dy}" stroke="{ink2}" stroke-width="1" marker-start="url(#dim)" marker-end="url(#dim)"/>')
    o.append(text((xs[0] + xs[3] + bw) / 2, dy - 6, "idea → shipped · typically 1–3 weekends", size=10, fill=ink2, family=MONO, anchor="middle", cls="lbl l2"))
    # detail callouts (bottom left): section view of an ESP32 node
    cx0, cy0 = 40, 258
    o.append(text(cx0, cy0 - 14, "DETAIL A · FIELD NODE", size=10, fill=ink, family=MONO, weight=700, ls="1.5", cls="lbl l3"))
    o.append(f'<rect class="draw d3" x="{cx0}" y="{cy0}" width="120" height="56" rx="3" fill="none" stroke="{ink}" stroke-width="{lw}"/>')
    for i in range(6):
        o.append(f'<rect class="draw d3" x="{cx0 + 8 + i * 18}" y="{cy0 - 6}" width="6" height="6" fill="none" stroke="{ink2}"/>')
        o.append(f'<rect class="draw d3" x="{cx0 + 8 + i * 18}" y="{cy0 + 56}" width="6" height="6" fill="none" stroke="{ink2}"/>')
    o.append(f'<rect class="draw d3" x="{cx0 + 36}" y="{cy0 + 14}" width="48" height="28" fill="none" stroke="{gold}" stroke-width="1.2"/>')
    o.append(text(cx0 + 60, cy0 + 32, "ESP32", size=9, fill=gold, family=MONO, anchor="middle", cls="lbl l3"))
    o.append(f'<line class="draw d3" x1="{cx0 + 120}" y1="{cy0 + 10}" x2="{cx0 + 170}" y2="{cy0 + 10}" stroke="{ink2}" stroke-width="1"/>')
    o.append(text(cx0 + 174, cy0 + 13, "temp · humidity · soil probes", size=9.5, fill=ink2, cls="lbl l3"))
    o.append(f'<line class="draw d3" x1="{cx0 + 120}" y1="{cy0 + 44}" x2="{cx0 + 170}" y2="{cy0 + 44}" stroke="{ink2}" stroke-width="1"/>')
    o.append(text(cx0 + 174, cy0 + 47, "Wi-Fi → MQTT → Python service", size=9.5, fill=ink2, cls="lbl l3"))
    # detail B: model section (bottom middle)
    mx, my = 420, 250
    o.append(text(mx, my, "DETAIL B · CNN STACK", size=10, fill=ink, family=MONO, weight=700, ls="1.5", cls="lbl l4"))
    layers = [("conv 32", 26), ("pool", 18), ("conv 64", 26), ("pool", 18), ("dense", 22), ("softmax", 30)]
    x = mx
    for i, (nm, w) in enumerate(layers):
        hh = 46 - i * 4
        o.append(f'<rect class="draw d4" x="{x}" y="{my + 10 + (46 - hh) / 2}" width="{w}" height="{hh}" fill="{paper2}" stroke="{ink}" stroke-width="1.2"/>')
        o.append(text(x + w / 2, my + 70, nm, size=8, fill=ink2, family=MONO, anchor="middle", cls="lbl l4"))
        x += w + 8
    # rotating gear + title block (bottom right)
    tbx, tby = 640, 250
    o.append(rect(tbx, tby, W - 30 - tbx, H - 30 - tby, stroke=ink, r=2, extra='stroke-opacity=".9"'))
    o.append(f'<line x1="{tbx}" y1="{tby + 22}" x2="{W - 30}" y2="{tby + 22}" stroke="{ink}" stroke-opacity=".6"/>')
    o.append(f'<line x1="{tbx}" y1="{tby + 44}" x2="{W - 30}" y2="{tby + 44}" stroke="{ink}" stroke-opacity=".6"/>')
    o.append(text(tbx + 8, tby + 15, "PROJECT", size=8, fill=ink2, family=MONO, ls="1.5"))
    o.append(text(tbx + 70, tby + 15, "Intelligent systems", size=10, fill=ink, family=MONO))
    o.append(text(tbx + 8, tby + 37, "DRAWN BY", size=8, fill=ink2, family=MONO, ls="1.5"))
    o.append(text(tbx + 70, tby + 37, "Ayush Jena", size=10, fill=ink, family=MONO))
    o.append(text(tbx + 8, tby + 59, "STATUS", size=8, fill=ink2, family=MONO, ls="1.5"))
    o.append(text(tbx + 70, tby + 59, "iterating", size=10, fill=gold, family=MONO))
    o.append(f'<g class="rot"><circle cx="{W - 52}" cy="{tby + 55}" r="11" fill="none" stroke="{ink}" stroke-width="1.5" stroke-dasharray="4 3"/>'
             f'<circle cx="{W - 52}" cy="{tby + 55}" r="4" fill="none" stroke="{ink}"/></g>')
    o.append('</g>')
    o.append(svg_close())
    return "\n".join(o)
