# Agent Instructions — Subtext

Cross-client rules for this repo. The hub contract lives in
[WalksWithASwagger/kk-agents](https://github.com/WalksWithASwagger/kk-agents)
(`AGENT-SURFACE-STANDARD.md`). This file is the repo-specific operating
sheet. Read `README.md` for the method and the UI.

## Purpose and Authority

Subtext is a local chat instrument. It streams Jacobian-lens readouts from a
Hugging Face decoder (default `Qwen/Qwen3.5-4B`) while the model reads a
prompt and while it generates a reply. The browser draws those silent words
as a sea chart (`index.html`); the older cloud view stays at `/classic`.

**Stack (from `requirements.txt` and `server.py`):** Python 3.11+,
PyTorch ≥ 2.5, Hugging Face `transformers` / `huggingface_hub`, FastAPI +
Uvicorn + WebSockets, `jlens` from `git+https://github.com/anthropics/jacobian-lens`.
The viewers are vanilla HTML/JS. There is no `package.json`, Makefile, or
bundler.

This checkout is `WalksWithASwagger/Subtext`. The README still documents
clone/setup against `ninjahawk/Subtext`. Apache-2.0; independent of Anthropic.
TODO for KK: say whether this fork is the working original or a tracking
copy, and whether it should keep pointing people at the ninjahawk clone URL.

## Capability Ownership

This repo has no `.agents/skills/`, no `CLAUDE.md`, and no `REVIEW.md`.
Portable skills stay in the kk-agents hub. Do not invent a project skill
tree here.

| Path | Role |
|---|---|
| `server.py` | FastAPI app: static files + `/ws` lens stream. Binds `127.0.0.1:8765`. |
| `index.html` | Sea-chart viewer (default `/`). |
| `classic.html` | Original cloud view (`/classic`). |
| `verify_accuracy.py` | Offline audit vs `jlens.JacobianLens.apply()`. |
| `test_client.py`, `test_multiturn.py` | Websocket smokes; need a running server. |
| `record_session.py` | Writes `docs/demo_session.json` for the Pages replay. |
| `start.sh`, `start.bat` | Launchers. `start.sh` prefers `.venv/bin/python` when present. |
| `requirements.txt` | Python deps. |
| `docs/` | GitHub Pages replay (`index.html` + `demo_session.json`). |
| `media/` | Demo stills, gif/mp4, star-history SVGs. |
| `.github/workflows/star-history.yml` | Daily star-history SVG update. |
| `.github/scripts/star_chart.py` | Chart generator used by that workflow. |

`.gitignore` covers `__pycache__/`, `*.pyc`, `token_mask*.pt`, and `.venv/`.

TODO for KK: add a root `REVIEW.md` with `## Automation Writeback` if you
want this repo under the full hub contract.

## Routing and Context Loading

Load this file plus `README.md`. Then open the file you are changing.

- Live path and lens math: `server.py`.
- Chart UI: `index.html`. Classic UI: `classic.html`.
- Pages-only replay: `docs/index.html` (not the live app).
- Accuracy vs Anthropic's reference: `verify_accuracy.py`.
- Star-history CI: `.github/workflows/star-history.yml` and
  `.github/scripts/star_chart.py`.

**Conventions that are actually in the tree**

- One Python process, no package layout, no app factory.
- Port `8765` is hardcoded. Device is CUDA, else MPS, else CPU.
- Keep the explanatory comments in `server.py`; they are the in-file method
  notes.
- Do not add a JS build step. Edit the HTML files in place.
- Do not treat `docs/index.html` as a second source for the sea chart; the
  live chart is root `index.html`.
- Open work on `codex/*` (PRs #7–#12) is out of scope unless a task names
  that PR. Do not rebase, retarget, or land those branches as a side effect.

## Verification

Only commands that exist in this repo's files. There is no test runner
config and no `make` target.

**Install**

```sh
pip install -r requirements.txt
```

Needs an NVIDIA GPU with ~10 GB VRAM (CUDA PyTorch) or Apple Silicon with
16 GB+ (PyTorch ≥ 2.3, macOS 14+, `mps`). Otherwise CPU — usable for smoke
tests, slow. First launch downloads the model and lens (~10 GB for the
default; `Qwen/Qwen3.5-0.8B` is ~1.8 GB) and builds a display-token mask.

**Run**

```sh
python server.py
# → http://localhost:8765
```

macOS/Linux: `./start.sh` (uses `.venv/bin/python` if that binary exists,
else `python3`, then opens the browser). Windows: `python -u -X utf8 server.py`
or `start.bat`. Laptop-sized model:

```sh
SUBTEXT_MODEL=Qwen/Qwen3.5-0.8B python server.py
```

**Test**

Stop the server first (both want the GPU), then:

```sh
python verify_accuracy.py
```

With the server up:

```sh
python test_client.py
python test_multiturn.py
```

To refresh the Pages replay fixture (server up):

```sh
python record_session.py
```

There is no `pytest`, `npm test`, or lint script in this repo.

## Safety and Human Gates

### Secrets

There is no `.env.schema` and no `.env.example`. Env vars are names only.
Do not commit values. Load them with Varlock (`varlock run`) when you have
a schema, or with Cursor Cloud secrets. Never write a real key into a file,
issue, log, or PR body.

**Names this repo actually reads**

| Name | Where | What |
|---|---|---|
| `SUBTEXT_MODEL` | `server.py` | Hugging Face model id. Default `Qwen/Qwen3.5-4B`. |
| `SUBTEXT_LENS_FILE` | `server.py` | Path inside `neuronpedia/jacobian-lens` when the model is not one of the three built-in ids. |
| `GITHUB_TOKEN` | `.github/scripts/star_chart.py` | GitHub API token for stargazer timestamps. |
| `REPO` | `.github/scripts/star_chart.py` | `owner/name`. Required. |
| `OUT_DIR` | `.github/scripts/star_chart.py` | Chart output dir. Default `media`. |

GitHub Actions maps repo secret `STARGAZER_TOKEN` (or `github.token`) onto
`GITHUB_TOKEN` in `.github/workflows/star-history.yml`. That secret is
CI-only; do not invent a local `.env` for it.

The Python files do not read `HF_TOKEN`. TODO for KK: if gated Hugging Face
downloads ever need a token, add a `.env.schema` and name it there.

### Do not

- Change code, CI, or dependencies as a drive-by while doing docs.
- Touch open PRs #7–#12 or their `codex/*` branches unless the task is
  that PR.
- Push to `main`, merge, or enable auto-merge without a separate human ask.
- Run `verify_accuracy.py` while `server.py` is up (they contend for the
  same GPU).
- Commit `token_mask*.pt`, `.venv/`, or downloaded model weights.

## Delivery

Live chat is local only (`127.0.0.1:8765`). There is no deploy script, Docker
file, or Vercel/Fly config.

The GPU-free hosted replay documented in the README is
https://ninjahawk.github.io/Subtext/ — `docs/` plus `?replay=` (or
`demo_session.json` when the host ends with `github.io`). This repo's only
automation is the star-history workflow; there is no Pages workflow here.
TODO for KK: confirm whether `WalksWithASwagger/Subtext` publishes Pages
itself or only tracks the upstream demo.

Land your own branch as a draft PR. Stage only the files you changed.
Agent-surface work for this repo is tracked from
[kk-agents#107](https://github.com/WalksWithASwagger/kk-agents/issues/107).
