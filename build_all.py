"""Rebuild every asset. `python tools/build_all.py`"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mk_character, mk_banner, mk_contributions, mk_panels

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "..", "assets", "character.png")) \
            or "--character" in sys.argv:
        mk_character.cutout()
        print("character.png rebuilt")
    mk_banner.main()
    mk_contributions.main()
    mk_panels.main()
    print("done")
