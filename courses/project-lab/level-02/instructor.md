# Instructor Run Sheet - Project Lab Level 2: The Night Watchman

## Outcome

Specify, run, and test a scheduled page watcher that records each round, alerts only on a meaningful change, and stops through a tested switch.

## Alignment

| Learning target | Practice | Evidence |
| --- | --- | --- |
| Define the job | Six-line watchman spec | Address, signal, rule, trigger, alert, never list |
| Distinguish states | Three controlled runs | Baseline, unchanged, changed receipts |
| Read operations evidence | Issue and log review | Old/new values and dated lines |
| Stop the system | Disable and attempted run | Named control and observed stopped state |

## Teaching stance

The watcher is intentionally small. Do not turn the level into a Python lesson. Beginners may paste the reviewed starter and work through browser controls. Builders may inspect and revise the parser after the same proof is complete.

## Prepare before learners arrive

- Create a clean practice repository from the starter assets.
- Run the watcher three times: baseline, unchanged, and after changing OPEN to PAUSED.
- Confirm issue permission and the location of the disable control.
- Capture a saved run and one useful failure log.
- Print the watchman spec and never-list card.
- Confirm GitHub's current scheduled-workflow behavior before stating timing.

## Safety boundary

Learners watch only the supplied page or a page they control. No scraping behind login, bypassing access controls, tracking people, or aggressive polling. The watcher can create a repository issue and update its state file. It cannot buy, reply, delete, post elsewhere, or spend.

## 90-minute schedule

| Block | Minutes |
| --- | ---: |
| Arrival, catch-up, and proof preview | 8 |
| Guard's rounds explanation and fence | 7 |
| Live baseline, unchanged, changed demo | 10 |
| Task 1: write and peer-check the spec | 12 |
| Starter orientation and repository setup | 12 |
| Task 2: baseline and unchanged runs | 10 |
| Task 2: controlled change and alert | 11 |
| Log review and error-reading pause | 4 |
| Task 3: disable and prove stop | 8 |
| Proof assembly, share, and exit | 8 |
| **Total** | **90** |

## Facilitation plan

### Opening

Ask which jobs are look, compare, tell jobs. Reject examples that require automatic purchase, reply, or deletion. Show the off switch before the first run.

### Demo

Read each log line aloud. Distinguish no change from failure. Change only the marked status so learners see why stable extraction matters.

### Practice

Check specs before repository setup. During runs, learners must predict the result first. If a red run appears, read the last ten lines and identify the first useful error before asking a coding tool.

### Close

Each learner points to the switch and reads one never item. Leave workflows disabled unless a learner has an approved page and schedule for homework.

## Passing proof

A complete watchman spec; baseline, unchanged, and changed runs; one useful alert and log trail; a never list; and proof that the learner used the off switch.

## Grading guide

| Check | Meets | Return for revision when |
| --- | --- | --- |
| Spec | A stranger can predict alert behavior | The signal or meaningful-change rule is vague |
| Runs | Baseline, unchanged, and changed states are distinct | A failed run is called no change |
| Alert | One controlled change names old and new | A moving footer creates noise |
| Log | Each round has time, observed value, and decision | Only the alert is shown |
| Switch | Disable action was used and observed | Learner only names where it is |

## Access and support

- Phone-only learners own the spec, predictions, and log review.
- Keep one instructor repository for a whole-room fallback.
- Give builders parser or Railway-contract extensions after proof.
- Keep UI labels visible because GitHub can move controls.
- Use the shared helper stop rule after two failed setup attempts.

## Fallbacks

- GitHub down: use assets/fallback-three-runs.md.
- Workflow hidden: use the instructor repository while recording the local path issue.
- Issue permission blocked: the changed log is partial proof; repair the permission before pass.
- Email missing: do not delay. Repository issue plus log are the assessed alert.
- Fifteen minutes behind: paste the starter from the instructor repository; protect the three runs and switch test.

## After class

Record successful baseline, unchanged, changed, and disabled proofs separately. Note noisy signals, permission failures, and learners who left a schedule enabled. Turn off any instructor-owned practice workflow.
