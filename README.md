# GFMR reference website

A local, Markdown-based publication of the **Generic FUNaK-Fuelled Thermal Molten Salt Reactor (GFMR)** reference model by Thomas Sclauzero and Lubomír Bureš.

**IMPORTANT:** This model describes a generic reference design. It is NOT the proprietary Saltfoss reactor design. It is provided as a benchmark and educational tool for the broader nuclear engineering community.

## Disclaimer

This model is provided “as is”, without any representation or warranty of any kind, express or implied, including but not limited to the warranties of merchantability, accuracy, completeness, usefulness, fitness for a particular purpose and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in contract, tort or otherwise, arising out of or in connection with this model or its use.


## Preview locally

Requires Python 3.10 or newer. From this directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
bash scripts/preview.sh
```

Open **http://127.0.0.1:8000/**. Markdown and styling changes reload automatically. Stop the server with Ctrl+C.

On Windows, create the environment with `python -m venv .venv`, then run:

```powershell
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\mkdocs serve --dev-addr 127.0.0.1:8000
```

## Build a portable copy

```bash
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_site.py
```

The result is in `site/`. You can open `site/index.html` directly: fonts, images, styles, scripts, and search are bundled locally. The local server is preferable while editing and enables browser-managed PNG downloads; when opened from disk, image download links open the original PNG instead. The generated `site/` folder is not committed.

## Edit the website

| Location | Purpose |
| --- | --- |
| `docs/index.md` | Homepage text and layout |
| `docs/overview.md` | Full supplied text and reference introduction |
| `docs/parameters.md` | Design and control rod dimensions |
| `docs/hydraulics.md` | Channel velocities and pressure losses |
| `docs/lifetime.md` | Core lifetime criterion |
| `docs/geometry.md` | Original figures and captions |
| `docs/materials.md` | Material properties and OpenMC excerpts |
| `docs/references.md` | Reference bibliography |
| `docs/disclaimer.md` | Prominent disclaimer page |
| `includes/notice.md`, `includes/disclaimer.md` | Exact original notices, reused in pages and footer |
| `mkdocs.yml` | Navigation, site URL, theme, and Markdown settings |
| `docs/stylesheets/extra.css` | Colours, typography, responsive layout |
| `overrides/` | Small Material theme overrides |

The website uses **MkDocs + Material**, with Markdown content in `docs/`, as in [Morana](https://github.com/tannhorn/morana). The spacing, neutral palette, and Geist typography are inspired by [Saltfoss](https://www.saltfoss.com/). Its implementation is original; no Morana technical content or Saltfoss product claims have been imported.

## Content boundaries

The technical content is transcribed from `GFMR_ref.pdf`, the supplied model `.txt`, and the three original PNG figures. **Fuel Cycle is intentionally excluded**, including from search results. The original PDF remains local, outside `docs/`, and is ignored by Git because it contains the excluded section. Do not place it in `docs/` or add a public download link without preparing an edited publication copy first.

The complete model text is retained on the overview page. The disclaimer and generic-design notice are reproduced verbatim and appear on every page. The original PNGs are copied without modification into `docs/assets/images/`.

One terminology difference in the source is explicitly retained: the introduction calls the 350 cm dimension the reflector diameter, while the parameter table calls the corresponding 3.5 m dimension the core diameter. The site does not infer a correction.

The OpenMC listings preserve the source variables and values. Only PDF quotation marks and layout indentation have been normalized. They are excerpts, not runnable model implementations.

## Check the site

`mkdocs build --strict` validates the build. `scripts/check_site.py` checks local links and anchors, exact notices, completeness of the supplied text, unmodified images, and the absence of excluded content throughout the generated publication.

Optional browser checks:

```bash
.venv/bin/python -m pip install -r requirements-preview.txt
.venv/bin/python -m playwright install chromium
# With the preview server running in another terminal:
.venv/bin/python scripts/browser_check.py
```

These check all pages at desktop and mobile widths, search, navigation, image enlargement, and downloads. Screenshots and a report are written to `preview-artifacts/` (ignored by Git).


