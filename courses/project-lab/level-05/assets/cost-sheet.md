# Classroom Cost Sheet

```text
Document:    Classroom Cost Sheet
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      d02bb0f6ff89b61215faf44fccf7063b665229c72b8f20443e07fcb7a93511e4
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

This is a monthly operating estimate for a classroom project, not a Celaya Solutions Research quote, selling price, or promise of savings. No purchase is required. Use one currency throughout. Label each number measured, estimated, or hypothetical. Unknown is not zero.

## Fill your inputs

Copy this sheet into item 8 of the private worksheet. Do not screenshot your private bill for the room.

| Input | Your value and unit | Source and date or assumption |
| --- | --- | --- |
| Route and named model | Local / API / no model | Actual selected project |
| Tasks each month | count | Include repeat runs and failures |
| Model calls per task | count | Include retries if used |
| Input and output tokens per call | two counts | Include instructions and source passages |
| Input and output rates | currency per million tokens | Exact model/plan; official page and check date |
| Monthly host/platform bill | currency | Plan, minimum, usage, included credit; count once |
| Electricity | kWh times currency/kWh | Measured or stated assumption |
| Hardware share | currency/month | Optional allocation; explain an excluded existing laptop |
| Human review | hours times currency/hour | Include at least one hour |
| Other recurring costs | currency/month | Storage, network, domain, or subscriptions if used |
| One-time setup | hours/cost | Report separately from monthly cost |

Local models on your own computer have no provider token charge for those local requests. They still use hardware, power, and human time. A subscription you already pay for is not automatically the API bill. Record any allocated assistant subscription separately. For a no-model watcher, token charges are not applicable.

## Calculate

1. Monthly calls = tasks per month times model calls per task.
2. API amount = monthly calls times ((input tokens times input rate + output tokens times output rate) / 1,000,000).
3. Human review = review hours times hourly assumption. Use at least 1 hour even when API cost is zero.
4. Cost floor = API + host/platform bill + electricity + hardware share + human review + other recurring costs.
5. Three-times safety line = 3 times the cost floor. This is a classroom stress test, not an advised markup, margin, or selling price. If an important input is unknown, the total is provisional; if the base is zero, multiplying it does not resolve missing costs.

For hosting, copy the provider's total-bill rule. Do not add included usage credits twice or assume a plan minimum covers every possible usage charge. Separate one-time setup from monthly operation. Check taxes, currency conversion, and any excluded costs before treating an estimate as a real budget.

## Worked local example - hypothetical

A learner plans 100 workbench reminders per month using an already-owned laptop and the local named model. No API or cloud host is used. Power is assumed at $1/month, hardware share $2/month, and review is 1 hour at an assumed $20/hour. These are invented teaching inputs, not measurements or current service prices.

| Monthly line | Arithmetic | USD |
| --- | --- | ---: |
| API and hosting | Local requests; no host subscription | 0.00 |
| Electricity | Hypothetical monthly amount | 1.00 |
| Hardware share | Hypothetical allocation | 2.00 |
| Human review | 1 hour times $20/hour | 20.00 |
| Cost floor | 0 + 1 + 2 + 20 | 23.00 |
| Three-times safety line | 3 times 23 | 69.00 |

One-time setup is recorded separately as an assumed 30 minutes, not another recurring $10/month. The largest recurring assumption is human review. If review takes 2 hours, the floor becomes $43 and the safety line $129. Hardware/power must be measured or relabeled before this becomes a real budget.

## Worked API arithmetic - hypothetical rates

For calculator practice only: 1,000 tasks/month, one call/task, 2,000 input and 500 output tokens/call. Invented rates are $2/million input and $8/million output. API = 1,000 times ((2,000 times 2 + 500 times 8) / 1,000,000) = $8. Add a hypothetical total host bill $5, power $1, and 1 hour review at $20: floor $34; safety line $102. These are not any provider's quoted rates. Keep any excluded hardware allocation explicit.

## Official source card - checked 2026-09-06

- [Ollama pricing](https://ollama.com/pricing): local model use is available on the free offering; cloud pricing is a different route. This supports the local provider-fee assumption, not free electricity or labor.
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions): standard GitHub-hosted runner use in public repositories is free; private-repository quotas, larger runners, and storage need separate checks. Do not assume an entire account costs zero.
- [Railway pricing](https://railway.com/pricing): use the exact plan and total usage rule only if hosting is actually chosen.
- [Vercel pricing](https://vercel.com/pricing): verify the chosen plan, permitted use, and usage limits if that host is actually chosen.

For a selected API provider, open its official pricing link from your existing setup guide and record the exact model, date, units, and rates. Do not sign up just to complete this sheet. These source observations are dated; recheck before class. If offline, retain the date and use the hypothetical example rather than guessing a current price.

Your conclusion: record the monthly floor, currency, three-times line, largest assumption, unknown costs, separate setup cost, and next measurement in worksheet item 8.
