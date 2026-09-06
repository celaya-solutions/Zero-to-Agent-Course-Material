# Document:    Night Watchman Runtime
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      a28f5c6bdad46ae2601396ddee4919d0c41fc3052de9e9af6e924d473dff1758
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""Compatibility entry only. Maintained watcher: projects/watchman/watch.py."""
from pathlib import Path
import runpy
if __name__ == "__main__":
    for root in Path(__file__).resolve().parents:
        target = root / "projects/watchman/watch.py"
        if target.is_file():
            runpy.run_path(str(target), run_name="__main__")
            break
    else:
        raise SystemExit("Use the complete Level 2 clone and zta start watchman. This is not a standalone starter.")
