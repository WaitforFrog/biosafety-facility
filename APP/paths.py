# APP/paths.py
# Provides path constants for the app.
# Reads Setting.md directly to avoid circular import with Setting.py.

import sys
import re
from pathlib import Path

_CODE_ROOT = Path(__file__).resolve().parent.parent

_md_path = _CODE_ROOT / "Setting.md"
_pattern = re.compile(r'^(\w+)\s*=\s*(.+)$', re.MULTILINE)
_g = {"Path": Path}

for match in _pattern.finditer(_md_path.read_text(encoding="utf-8")):
    key, raw_value = match.group(1), match.group(2).strip()
    if key.startswith("#") or key in (
        "Source", "root", "How", "Note", "active", "currently",
    ):
        continue
    try:
        value = eval(raw_value, {}, _g)
    except Exception:
        continue
    _g[key] = value

PRODUCE_DIR = _g.get("PRODUCE_DIR", _CODE_ROOT / "Produce")

# Make sure Code/ is on sys.path so 'from Setting import ...' works in child scripts
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

CODE_ROOT = _CODE_ROOT
APP_DIR   = _CODE_ROOT / "APP"

__all__ = ["CODE_ROOT", "APP_DIR", "PRODUCE_DIR"]

