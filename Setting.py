# Setting.py — Unified configuration module
# Reads human-editable values from Setting.md at import time.
#
# Downstream files use `from Setting import ...` — no changes needed.
# Re-exports from APP/paths.py and api_config.py are maintained.

import re
from pathlib import Path

# ============================================================
# Base path (always hardcoded — Setting.md cannot provide __file__)
# ============================================================

CODE_ROOT    = Path(__file__).resolve().parent
PROJECT_ROOT = CODE_ROOT

# ============================================================
# Load all other config from Setting.md
# ============================================================

def _load_md_settings():
    md_path = CODE_ROOT / "Setting.md"
    pattern = re.compile(r'^(\w+)\s*=\s*(.+)$', re.MULTILINE)

    # Make PROJECT_ROOT available inside eval() so MD can use e.g. PROJECT_ROOT / "Produce"
    # Accumulate loaded keys in g so later entries can reference earlier ones
    g = {"PROJECT_ROOT": PROJECT_ROOT, "Path": Path}

    for match in pattern.finditer(md_path.read_text(encoding="utf-8")):
        key, raw_value = match.group(1), match.group(2).strip()
        if key.startswith("#") or key in (
            "Source", "root", "How", "Note", "active", "currently",
        ):
            continue
        try:
            value = eval(raw_value, {}, g)
        except Exception:
            continue
        globals()[key] = value
        g[key] = value  # allow subsequent lines to reference this key

_load_md_settings()
del _load_md_settings
