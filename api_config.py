# api_config.py
# Backward-compatibility wrapper — re-exports API config from Setting
import sys as _sys
from pathlib import Path as _Path

_CODE_ROOT = _Path(__file__).resolve().parent

if str(_CODE_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_CODE_ROOT))

from Setting import OPENAI_API_KEY, API_BASE_URL, MODEL_NAME

__all__ = ["OPENAI_API_KEY", "API_BASE_URL", "MODEL_NAME"]
