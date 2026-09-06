# Document:    Night Watchman Compatibility Sync
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      0d71ef250b52b972c33037264ccf36fc160ed8072b88b1d4afc59bdeffa01206
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""Keep the inherited workflow download identical to the maintained template."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
shutil.copy2(ROOT / "projects/watchman/workflow.template.yml", ROOT / "courses/project-lab/level-02/assets/starter/watch.yml")
print("Updated the generated legacy Watchman workflow.")
