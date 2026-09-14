"""Regenerate every SVG in ./assets (dark + light). Usage: python build.py"""
import importlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gen.theme import THEMES, hudify

BUILDERS = ["header", "holo", "terminal", "skills", "projects", "otherwork", "assembly", "matrix", "workflow", "footer"]

VOICE = {
    "header":            ("Good evening. Loading Ayush Jena's engineering profile…", "SYS 01 · BOOT"),
    "holo":              ("Identity verified. Displaying credentials.", "MOD 02 · IDENT"),
    "terminal":          ("Replaying the last training runs, sir.", "MOD 03 · LOG"),
    "skills":            ("Capability matrix online. All modules responding.", "MOD 04 · CAPABILITIES"),
    "project-digits":    ("Project file: Handwritten Digit Recognizer. Metrics verified.", "MOD 05.1 · PROJECT"),
    "project-spam":      ("Project file: Spam Email Classifier. Metrics verified.", "MOD 05.2 · PROJECT"),
    "project-fruit":     ("Project file: Fruit Image Classifier. Metrics verified.", "MOD 05.3 · PROJECT"),
    "project-speech":    ("Project file: Speech-to-Text Transcription. Metrics verified.", "MOD 05.4 · PROJECT"),
    "project-sentiment": ("Project file: Twitter Sentiment Analysis. Metrics verified.", "MOD 05.5 · PROJECT"),
    "project-more":      ("The full archive is available on request.", "MOD 05.6 · ARCHIVE"),
    "assembly":          ("Rendering the field node. Assembling in three, two, one…", "MOD 06 · WORKSHOP"),
    "otherwork":         ("Additional systems on file.", "MOD 07 · SYSTEMS"),
    "workflow":          ("This is how he works. I merely keep the lights on.", "MOD 08 · PROTOCOL"),
    "matrix":            ("Charging repulsor. Targeting the contribution matrix.", "MOD 09 · ACTIVITY"),
    "footer":            ("Shall I open a channel?", "MOD 10 · COMMS"),
}

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

only = sys.argv[1:]
for name in BUILDERS:
    if only and name not in only:
        continue
    try:
        mod = importlib.import_module(f"gen.{name}")
    except ModuleNotFoundError:
        continue
    for t in THEMES:
        result = mod.build(t)
        items = result if isinstance(result, dict) else {name: result}
        for key, svg in items.items():
            voice, code = VOICE.get(key, ("Module online.", "MOD · " + key.upper()))
            svg = hudify(svg, t, key, voice, code)
            p = OUT / f"{key}-{t.name}.svg"
            p.write_text(svg, encoding="utf-8")
            print(f"wrote {p.name:32} {len(svg)/1024:6.1f} KB")
