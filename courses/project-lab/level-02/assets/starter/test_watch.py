# Document:    Night Watchman Legacy Test Entry
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      17d93788144b1a4b68ea00df905c4e65d59dd1ce84a7a8e08165552b4e502944
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""Compatibility entry only. Use zta test watchman from the complete clone."""
from pathlib import Path
import subprocess
import sys
if __name__ == "__main__":
    for root in Path(__file__).resolve().parents:
        target = root / "projects/watchman/tests"
        if target.is_dir():
            raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", str(target), "-q"], cwd=root))
    raise SystemExit("Use the complete Level 2 clone and zta test watchman; this file has no separate tests.")
