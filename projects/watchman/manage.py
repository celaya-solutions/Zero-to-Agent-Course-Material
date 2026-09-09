# Document:    Night Watchman Local Setup
# Version:     v1.0.0
# Author:      Celaya Solutions
# Contact:     hello@celayasolutions.com
# Date:        2026-09-06
# SHA256:      dbeec29392f8c2e179505e862316b9e17b28031c3e56ff920ef4d51cc7aaac2f
# Chain:       n/a
# Tx:          [not anchored]
# License:     All Rights Reserved / Celaya Solutions

"""Install the reviewed workflow and private worksheet without enabling anything."""
import argparse
import shutil

from zta import storage

ROOT = storage.root()


def prepare(root=ROOT):
    files = [(root / "projects/watchman/workflow.template.yml", root / ".github/workflows/watchman.yml"),
             (root / "courses/project-lab/level-02/worksheet.md", root / ".zta/PROJECT-LAB-02.md")]
    for source, target in files:
        if target.exists():
            print(f"Kept existing {target.relative_to(root)}; no overwrite.")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        print(f"Created {target.relative_to(root)}")
    print("Nothing enabled or published. Follow the Level 2 preparation guide before any hosted run.")


def doctor(root=ROOT):
    for name in ["projects/watchman/watch.py", "projects/watchman/workflow.template.yml", "courses/project-lab/level-02/assets/practice-page.html"]:
        if not (root / name).is_file():
            raise SystemExit(f"Missing {name}. Use the instructor's Level 2 candidate checkout.")
    print("PASS: local watcher files found. No model, API key, or network needed for rehearsal.")
    print("Hosted readiness still requires your public fork, default branch, Issues, Actions policy, and explicit enable step.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["prepare", "doctor"])
    args = parser.parse_args()
    {"prepare": prepare, "doctor": doctor}[args.command]()
