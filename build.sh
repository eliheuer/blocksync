#!/bin/bash
# Keep the GF build entry point and its generated-font metadata.
set -euo pipefail
cd "$(dirname "$0")"
.venv/bin/fgtools build --compiler fontmake
.venv/bin/python scripts/fix_gf_metadata.py fonts/variable/*.ttf fonts/ttf/*.ttf
