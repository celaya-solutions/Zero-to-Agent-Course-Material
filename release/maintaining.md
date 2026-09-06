# Maintaining and Releasing the Course

```text
Document:    Maintaining and Releasing the Course
Version:     v1.1.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      c9ca1a6e6e362a5cd18ce148a0aa61bfb431c465aab7da7bc1449a7e1ebac963
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

The course source lives in [this repository](https://github.com/celaya-solutions/Zero-to-Agent-Course-Material). `courses/project-lab/` contains exactly five levels of 90 minutes each. Application code lives under `projects/`; the existing alternative-project catalog stays on the website. The website and private Rails platform are generated consumers.

## Build a reviewed candidate

Run these commands from the repository root after the matching preparation guide. Build tools are locked in `uv.lock`; Ruby is only a maintainer dependency, available from [ruby-lang.org](https://www.ruby-lang.org/en/downloads/). Learners do not need Ruby.

| Where | Action | Why | Expected result | Recovery if it fails |
| --- | --- | --- | --- | --- |
| GitHub Desktop | Create a `codex/` branch and an isolated checkout before edits. | Protect current work. | Changes appear only in the chosen checkout. | Review branch and local folder before continuing. |
| Terminal | Run `uv sync --frozen`. | Install the course's locked environment. | No lockfile changes. | Use the OS recovery guide. |
| Editor | Edit the canonical Markdown, manifests, app, or slide source. | Avoid hand-edited generated copies. | One source change explains the intended behavior. | Check the five-level map and source location. |
| Terminal | Run `uv run --frozen python scripts/sync_watchman_starter.py`, then `uv run --frozen python scripts/update_headers.py`. | Refresh document body hashes. | Headers match canonical bodies. | Fix malformed header fields and rerun. |
| Terminal | Run `ruby scripts/build_project_lab_slides.rb`. | Generate every 20-slide deck from the manifest and slide source. | Five `slides.html` files. | Run `ruby --version` and install Ruby if absent. |
| Terminal | Run `uv run --frozen python scripts/build_pdfs.py`. | Generate portable handouts from Markdown. | PDFs beside their source files. | Fix the reported source or layout error. |
| Terminal | Run `uv run --frozen zta test documents` and `uv run --frozen zta test watchman` and `uv run --frozen zta test local-models`. | Check app behavior without paid calls. | Every deterministic check passes. | Read the failing test; fix the behavior before release. |
| Terminal | Run `LANG=en_US.UTF-8 ruby scripts/validate_project_lab.rb`, then `uv run --frozen python scripts/validate_materials.py`. | Check alignment, timing, links, PDFs, and privacy boundaries. | Both validators pass. | Repair the named source and rebuild. |
| Browser/PDF viewer | Open all lesson routes and representative PDFs, resize, page through the deck, test downloads. | Catch clipping and navigation problems. | Content and controls remain readable. | Correct the renderer or source and rebuild. |
| Pilot computers | Follow `release/verification.md` and `release/level-02-verification.md` and `release/level-03-verification.md` from a fresh learner fork. | Prove real setup, generation, editing, and submission. | Evidence for every release gate. | Label the candidate prerelease while gates remain open. |
| GitHub Desktop | Review and commit only intended source/generated files. | Save a reproducible candidate. | No `.zta`, keys, personal files, or learner exports. | Remove accidental files from staging, not from the learner's disk. |
| Terminal | Run `uv run --frozen python scripts/package_release.py`. | Build downloads from an allowlist. | Two ZIPs and SHA256SUMS in `dist/`. | Fix a missing source/build output and rebuild. |
| GitHub release page | Tag the reviewed commit and attach both ZIPs and SHA256SUMS. Mark **pre-release** if any gate is open. | Give downloads an exact version. | Tag, files, and status identify the same candidate. | Check assets before sharing links. |

## Generate the website copy

Clone the website repository using GitHub Desktop into a separate checkout, then create an isolated branch/worktree. From this canonical repository run:

```sh
uv run --frozen python scripts/export_course.py ../open-hub-learning-platform
uv run --frozen python scripts/export_course.py ../open-hub-learning-platform --check
```

The argument is the actual website checkout path. Replace it with the path shown in GitHub Desktop; quote it if it contains spaces. The exporter refuses folders without `course/landing.html`. It copies the course, preparation, linked Watchman and local-model project resources, project README handouts, release notes, validation/build helpers, and a version/hash manifest. Review and commit that generated diff in the website checkout. It does not merge or deploy. Website maintainers continue running their repository's checks before any separately approved release.

## Generate the private platform copy

Use a separate private-platform worktree with its existing development dependencies. Never copy the Rails source or database into this public repository. In the private worktree, run its guarded task with the absolute canonical checkout path:

```sh
bundle exec rake 'zta:sync_content[/absolute/path/to/Zero-to-Agent-Course-Material]'
bundle exec rake 'zta:check_content[/absolute/path/to/Zero-to-Agent-Course-Material]'
```

Replace the example path with the folder shown by GitHub Desktop before running it. `ZTA_COURSE_MATERIAL_REPO` provides the same source path; `ZTA_HOME_REPO` remains a compatibility fallback. The task validates and copies the five-level content into `lib/project_lab/content` and stores its source commit/hash. It does not seed, reset, migrate, delete submissions, or change the running service. Review and commit that generated bundle separately. Student evidence and existing submissions must remain intact.

## Licenses and artifacts

The original MIT notice is retained in `LICENSE` for inherited course code/material. New teaching documents carry the Celaya Solutions header. Third-party applications and models keep their own terms. Release packages include the license and attribution notes. No cloud credentials, private platform source, old retired curricula, or student data belong in the public release.
