# Which model Subtext runs, and the pre-fitted Jacobian lens that goes with it.
# Only the standard library, so the accuracy audit can resolve the model the
# same way as server.py without importing server.py (which loads the model).

import os
import re

# Pick the model with SUBTEXT_MODEL. These three have a pre-fitted lens in
# LENS_REPO; for any other model, also point SUBTEXT_LENS_FILE at its lens
# (a path inside LENS_REPO).
LENS_FILES = {
    "Qwen/Qwen3.5-0.8B": "qwen3.5-0.8b/jlens/Salesforce-wikitext/Qwen3.5-0.8B_jacobian_lens.pt",
    "Qwen/Qwen3.5-4B": "qwen3.5-4b/jlens/Salesforce-wikitext/Qwen3.5-4B_jacobian_lens_n1000.pt",
    "Qwen/Qwen3.5-27B": "qwen3.5-27b/jlens/Salesforce-wikitext/Qwen3.5-27B_jacobian_lens.pt",
}
DEFAULT_MODEL = "Qwen/Qwen3.5-4B"
# SUBTEXT_MODEL set but empty counts as unset.
MODEL_NAME = os.environ.get("SUBTEXT_MODEL", "").strip() or DEFAULT_MODEL
# The model's short name, safe in a file name: names the mask cache, and the viewer shows it.
MODEL_SHORT = (
    re.sub(r"[^\w.-]+", "_", MODEL_NAME.rstrip("/\\").replace("\\", "/").rsplit("/", 1)[-1])
    or "model"
)
LENS_REPO = "neuronpedia/jacobian-lens"
LENS_REVISION = "qwen-n1000"
LENS_FILE = os.environ.get("SUBTEXT_LENS_FILE") or LENS_FILES.get(MODEL_NAME)
if not LENS_FILE:
    raise SystemExit(
        f"[subtext] no pre-fitted lens known for {MODEL_NAME}. Set SUBTEXT_LENS_FILE "
        f"to its path inside {LENS_REPO}, or pick one of: {', '.join(LENS_FILES)}"
    )


def pick_layers(source_layers, n_layers, fracs):
    """The lens's source layers nearest to each fraction of the network's depth, deduplicated and sorted."""
    wanted = [round(f * (n_layers - 1)) for f in fracs]
    return sorted({min(source_layers, key=lambda s, w=w: abs(s - w)) for w in wanted})
