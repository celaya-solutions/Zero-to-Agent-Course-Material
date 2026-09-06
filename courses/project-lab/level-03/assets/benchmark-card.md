# Local Model Benchmark Card

```text
Document:    Local Model Benchmark Card
Version:     v1.0.0
Author:      Celaya Solutions
Contact:     hello@celayasolutions.com
Date:        2026-09-06
SHA256:      f89b68062b48af3db4c7d0e637725acdfa86745d6d3fff27e6d32fad2c789377
Chain:       n/a
Tx:          [not anchored]
License:     All Rights Reserved / Celaya Solutions
```

Use the supplied `prompts.json`; the lab loads it and inserts the full dated public source into prompt 2. Do not silently shorten a prompt for the larger model. Record predictions before seeing results.

## Three tests

1. **Writing:** rewrite the supplied workbench reminder. Keep 4 p.m., the request for a reply, polite/firm tone, fewer than 70 words, and no new threat or policy.
2. **Source:** state the lab's location and work using only [Public Identity and Work](../../level-01/assets/public-identity-and-work.md). Name both headings, **Where the lab is based** and **Work and systems the lab builds**. Open that source yourself before scoring.
3. **Arithmetic:** choose among 84, 109, and 97 dollars; add 8.25 percent synthetic training tax with no tip. Independent key: 84 x 1.0825 = 90.93 dollars. This is invented classroom arithmetic, not tax advice.

## Fair timing and quality

Run both models on the same computer, with the same three prompts and no competing model jobs. The lab unloads the selected model before its first request and after each request. It records total request time including loading, not time to first word. Options: temperature 0.2, seed 42, context 4096, maximum output 256 tokens. Equal settings help a comparison; they do not guarantee identical replies across devices or versions.

| Score | Meaning | Evidence needed |
| --- | --- | --- |
| 1 | Wrong or unusable | Name the wrong fact, arithmetic, missing requirement, or invented policy |
| 2 | Useful with a correction | Name the exact correction; no uncorrected false core fact |
| 3 | Meets every test requirement | Show the deadline/reply, source headings, or arithmetic check |

A token-limit/truncated answer is incomplete even if the request completed. A failed request has no quality score or invented completion time. Preserve partial rows. Your ratings and source verdicts stay blank in generated receipts until you write them in the worksheet.

Use the missing-price/date prompt only for the named helper before/after test. It is not a fourth benchmark prompt. Good behavior names the absent quote/schedule and asks a person to confirm; it does not invent a range.
