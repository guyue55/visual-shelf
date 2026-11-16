#!/usr/bin/env bash
# Stable entry point; lifecycle and ownership checks live in service.py.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "${VISUAL_SHELF_PYTHON:-python3}" "$SCRIPT_DIR/service.py" "$@"
