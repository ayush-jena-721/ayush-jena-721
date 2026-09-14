# Profile README — how it's put together

The profile is styled as a J.A.R.V.I.S. console: every panel carries a system bar with a typed
"voice line", a speaking waveform and a module code. The lines live in `tools/build.py` (`VOICE`);
the bar itself is `hudify()` in `tools/gen/theme.py`, applied to every SVG at build time.

Everything visual lives in `assets/` as plain SVG (CSS + SMIL animation, no JavaScript),
one dark and one light version of each panel. GitHub picks the right one through
`<picture>` / `prefers-color-scheme`.

## Regenerate the panels

```bash
python tools/build.py            # rebuild every SVG
python tools/build.py projects   # rebuild only the project cards
```

Requires Python 3.10+ and nothing else.

## Where to edit

| File | What it controls |
|:--|:--|
| `tools/gen/theme.py` | Colours for both themes (red / gold / arc-blue) plus the fixed dark `SCREEN` palette used by the terminal, holograms and matrix in both themes |
| `tools/gen/header.py` | Hero: name, cycling roles, chips, hovering round portrait (`assets/portrait.jpg`) with reactor rings + lightning |
| `tools/gen/holo.py` | Hovering holographic ID screen (portrait from `assets/portrait.jpg`) |
| `tools/gen/terminal.py` | The lines the terminal "types" |
| `tools/gen/skills.py` | Toolkit groups and chips |
| `tools/gen/projects.py` | One card per repo — title, blurb, stack, metric |
| `tools/gen/assembly.py` | Workshop hologram: exploded ESP32 field node assembling itself |
| `tools/gen/otherwork.py` | IoT / desktop / experimental work (2×2 grid) |
| `tools/gen/matrix.py` | Repulsor contribution matrix (reads `data/contributions.json`) |
| `tools/gen/workflow.py` | The idea → ship loop |
| `tools/gen/footer.py` | Closing panel |

Metrics on the project cards come from each repository's own README — keep them in sync
if a model is retrained.

## Snake animation

`.github/workflows/snake.yml` runs daily and on push, and publishes
`github-snake.svg` / `github-snake-dark.svg` to the `output` branch. The README already
points there; the image appears after the first successful run (Actions tab →
"contribution snake" → Run workflow to trigger it immediately).

Repository setting needed once: **Settings → Actions → General → Workflow permissions →
Read and write permissions.**

## Contribution matrix — real data

`tools/fetch_github.py` reads the GitHub GraphQL API and writes `data/contributions.json`;
`tools/gen/matrix.py` turns it into the repulsor panel. `.github/workflows/profile-sync.yml`
runs both daily (and on push to `tools/` or `data/`) and commits the result, so the matrix
always shows the real calendar.

The JSON shipped here is a **seed built from the public commit history** of the five ML
repositories (so the panel isn't empty on day one). The first Actions run replaces it with
the account's full calendar — issues, PRs, private-repo contributions and all.

Note: GitHub renders README images with JavaScript removed and no mouse events, so
everything animates on its own (CSS / SMIL). Hover and click-to-rotate are not possible
on a profile README.

## Replacing the old files

This tree replaces the previous "AYUSH OS" set. Before copying it in, delete from the repo
root: the loose `*.svg` files, `character.png`, `hud.yml`, `build_all.py`, `check.py`,
`deploy.sh`, `fetch_github.py` and `.github/workflows/django.yml` (it fails on a profile
repo). Then copy in `README.md`, `SETUP.md`, `assets/`, `data/`, `tools/` and `.github/`.

## Mobile

GitHub strips all CSS from a README, so the only responsive tool is the image itself.
Every panel here is a single full-width SVG with large type, and the project cards are
one-per-row instead of a two-column table, so phones get the same layout at a smaller
scale rather than half-width columns. The ID card / terminal pair and the four stat cards
are the only two-column tables left; they shrink on phones but stay legible.

## Stat cards (external, real data)

`github-readme-stats` (stats + languages), `streak-stats.demolab.com`,
`github-profile-trophy`, `github-readme-activity-graph` and the `komarev` profile-views
counter are all public services keyed on the username — nothing to configure. Each one is
given the same red / gold / dark or light palette through URL parameters and switched with
`<picture>`.
