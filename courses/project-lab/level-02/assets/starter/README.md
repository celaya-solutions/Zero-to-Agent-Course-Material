# Night Watchman Starter Map

Use a new practice repository. Do not put these files into an employer or production repository.

## Put each file here

| Course file | Practice repository location |
| --- | --- |
| watch.py | /watch.py |
| test_watch.py | /test_watch.py |
| ../practice-page.html | /practice-page.html |
| watch.yml | /.github/workflows/watch.yml |

## Before the first hosted run

1. Run python -m unittest test_watch.py locally or use the instructor's tested copy.
2. Commit all four files.
3. Replace WATCH_URL in the workflow. A simple route is the raw public address of your practice page: https://raw.githubusercontent.com/ACCOUNT/REPOSITORY/main/practice-page.html.
4. Open repository Settings, Actions, General, Workflow permissions. The class starter needs read and write permission to save its state and create its practice issue.
5. Run the workflow by hand. The first run saves OPEN as the baseline.

The workflow uses the temporary repository token supplied by GitHub Actions. Do not create or paste a personal token.

## Class test

1. Run once: baseline, no issue.
2. Run unchanged: no change, no issue.
3. Change only OPEN to PAUSED in practice-page.html.
4. Run again: one issue and one changed log line.
5. Disable the workflow and record the stopped state.

## Schedule note

GitHub schedules use UTC and can be delayed. The sample 13:00 UTC schedule is about 6 a.m. MST and 7 a.m. MDT in El Paso. Review the schedule when daylight-saving time changes. Do not promise an exact alert minute.
