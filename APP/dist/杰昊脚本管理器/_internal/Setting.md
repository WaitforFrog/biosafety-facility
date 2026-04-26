# Setting.md — Unified configuration (human-editable)

## How this works
- Edit the values in this file directly (no Python needed).
- `Setting.py` reads this file at import time and exposes all values as module-level variables.
- All `from Setting import ...` statements in other files need **no changes**.

## API Configuration
## Note: Uncomment only ONE block at a time (小象api or 万象api).

# ---- 小象api (currently active) ----
OPENAI_API_KEY = "sk-j4kGaMBeZYyma78n"
API_BASE_URL  = "https://acloudvip.top/v1"
MODEL_NAME    = "claude-opus-4-6-a"

# ---- 万象api (comment out the above and uncomment below to switch) ----
# OPENAI_API_KEY = "sk-RQADwtfxQ8BDx9cE"
# API_BASE_URL   = "https://mix88.top/v1"
# MODEL_NAME     = "claude-sonnet-4-6"
