# Tally

**Do their numbers match?** An open, auditable dataset of the figures Nigerian leaders quote in national addresses, each one checked against the official release it refers to.

Apart Research AI x Epistemics Research Sprint, 13 to 15 November 2026. Track 4 (Open Track).

| | |
|---|---|
| Report | [`report/Tally-report.pdf`](report/Tally-report.pdf) |
| Dataset | [`data/claims.csv`](data/claims.csv) |
| Guide for judges | [`JUDGES.md`](JUDGES.md) |
| Slides | [`slides/Tally-slides.pdf`](slides/Tally-slides.pdf) |
| Presentation (about 3 minutes, narrated) | [`slides/Tally-presentation.mp4`](slides/Tally-presentation.mp4) |
| Second-check results | [`check/second_check.json`](check/second_check.json) |
| Checking log | [`notes.md`](notes.md) |

## Summary

Five national addresses were chosen before any checking: four by President Bola Tinubu and one by opposition candidate Atiku Abubakar. The figures in them were listed (59). 49 were checked against releases from Nigeria's statistics bureau, central bank, budget office and other official bodies, and 46 could be scored.

| Verdict | Count | Share of the 46 scored |
|---|---|---|
| Match | 37 | 80% |
| Close | 5 | 11% |
| Mismatch | 4 | 9% |

The dataset was then tested twice by means that do not depend on the first checker:

- A script with no AI in it downloaded every source and looked for the recorded official numbers on the page.
- A different AI model coded the scored rows blind, seeing only the claim and the source text.

The blind second coder found a match rate of 73% against 80%, and gave the same verdict on 32 of 45 rows. So the broad result holds under a second checker: most figures match. Individual verdicts near the category boundaries are less reliable, and the second coder disagreed on one of the two headline findings. The report says so.

The two most consequential errors are in the same speech and both attach the label "non-oil" to a figure that includes oil.

## How this fits Track 4 (deployment, adoption and impact)

Track 4 asks what it takes for epistemic tools to be deployed, adopted and useful in the real world. The track brief suggests this very project: pair quantitative claims with the statistical releases they cite, flag mismatches with links, and publish an auditable dataset.

- **Deployment.** Claim-checking tools are built and tested mostly where statistics are tidy. Tally is a test set from a setting where they are not, so a tool can be tried against it before anyone relies on it there.
- **A small deployment test is included.** The blind second coder is an off-the-shelf model given the right source for each claim. It agreed with most verdicts, but it missed one of the two "non-oil" label swaps: it read both revenue figures correctly and still called the claim a match. That is the kind of failure a deployed checker would make.
- **Adoption.** The work surfaced concrete things that get in the way of using such tools here: two official series for the same quantity, figures that exist only in government statements, official data published as PDF tables, and source sites that refuse automated readers (four did during the checks).
- **Impact.** The dataset can be used today by fact-checkers, journalists and tool builders. Every scored row links to its source, and the ten unchecked rows are open tasks.

What it does not claim: nobody has adopted the dataset yet, and no tool has been deployed with it. It is the groundwork.

## Why this matters

Political speeches lean on numbers. Growth is up, inflation is down, reserves are at a record. Each number comes from an official release, so in principle anyone can check it. In practice it is slow, and for Nigeria the author found no open dataset that puts the claims and the official figures side by side.

That gap matters for AI. Tools that check claims automatically are built and tested mostly on material from a few countries with tidy statistics. To know whether they work in Nigeria, someone first has to assemble real claims, the real figures behind them, and a verdict on each. The sprint brief asks for exactly this under Track 4: pair quantitative claims with the releases they cite, flag mismatches with links, and publish an auditable dataset. Tally is a first, small version.

## What was found

![Verdicts by speech](report/figure1.png)

**Headline figures were accurate.** Every specific quarterly growth rate and monthly inflation rate quoted in the five speeches matched the statistics bureau exactly.

**Nine figures did not match exactly.** Four mismatches and five close calls:

| Row | Claim | Official figure | Verdict | What went wrong |
|---|---|---|---|---|
| `T25-05` | Non-oil exports are 48% of exports | Crude 52.60%. Non-crude 47.40%, of which petroleum products and gas 34.21% and non-oil 13.39% | mismatch | A definition was swapped. The 48% is the non-crude share |
| `T25-16` | Non-oil revenue target met "by August with over N20 trillion" | Total collections N20.59 trillion, of which non-oil N15.69 trillion | mismatch (contested) | A definition was swapped. The N20 trillion is total revenue, oil included |
| `T25-07` | Oil output rose from "barely one million" barrels a day in May 2023 | 1,183,691 in May 2023. 998,602 was April | mismatch (contested) | The baseline belongs to the month before |
| `TB-06` | Over 418,000 students supported by the loan fund | 510,378 already reported in September | mismatch | Out of date |
| `TN-02` | The stock market gained 48.12% in 2025 | 51.19% for the full year | close | Out of date by ten days |
| `T25-13` | Tax-to-GDP rose "from less than 10 per cent" | 10.86% | close | Baseline understated |
| `T25-11` | Student upkeep allowance of N44.7 billion | N45.7 billion | close | Transcription |
| `A26-05` | A sliced loaf was "about N500" in April 2023 | N577.41 | close | Baseline understated |
| `A26-03` | N70,000 "buys just 50 litres" of petrol | 44 litres at the latest official price found; 48 to 50 at pump prices reported the month before | close | Official figure for the month not found |

**The errors ran both ways.** Eight of the nine have a clear direction. Five helped the speaker's argument and three hurt it. The two biggest errors, both "non-oil" definitions, helped. Eight cases are too few to say anything about intent, and the report does not.

**More checking did not find more errors.** The first 33 figures checked were the most prominent ones and 74% matched. The next 16 produced fourteen matches, one mismatch and one unverifiable figure.

**Two claims do not fit match or mismatch.**

- The President's foreign investment figure ($720 million) matches the central bank exactly. The statistics bureau reports $296 million for the same quarter. Both are official.
- The fall in the debt service to revenue ratio "from 97% to below 50%" appears only in government statements. No published series was found.

The two speakers should not be compared from these counts. One gave four speeches and the other gave one, and different shares were checked.

## How reliable is it

| Check | Who or what did it | Result |
|---|---|---|
| Speeches re-read from scratch | First checker | 8 missed figures added. Two verdicts revised |
| Every source re-opened | First checker | All verdicts held. 8 rows had a figure or link corrected |
| Numbers on the page | Script, no AI, clean GitHub machine | A source opened for 45 of 46 rows; one site refuses automated readers. Every recorded number found in 39. In 6 others the quoted figures were found; the missing items were the checker's own arithmetic, a number written in another form, or a non-numeric figure |
| Blind second coder | Different AI model (gpt-5.4-mini through SERV Reasoning) | Same verdict on 32 of 45 (71%, Cohen's kappa 0.26). Same on match versus not on 36 of 45 (80%) |
| Second round of checking | First checker | 16 more figures: 14 match, 1 mismatch, 1 unverifiable |

What the second coder changed:

- One verdict moved from mismatch to close (`TN-02`), because the first checker had not applied its own 10% threshold.
- Two April 2023 prices the first checker had failed to find were located (`A26-04`, `A26-05`).
- Two verdicts are contested. On `T25-07` the second coder read "barely one million" as fair for 1.18 million. On `T25-16` it recorded both revenue figures correctly and still returned a match. Both stay mismatches here and both rows say they are contested.

All thirteen disagreements are in Appendix B of the report, each with what was done about it.

What these checks do not cover: the second coder read the sources the first checker chose, so the choice of source was not tested. No person verified the rows.

## Method

1. **Speeches fixed first.** Five scripted addresses with published full texts, October 2025 to October 2026. The opposition address was given the same morning as the President's 2026 Independence Day address, so both sides go through one procedure.
2. **Figures listed.** Each statement with a number about the economy or public money. Proposals and targets were left out.
3. **Official figure looked up.** National Bureau of Statistics, Central Bank of Nigeria, Debt Management Office, the petroleum regulator, the student loan fund, the export council.
4. **Verdict given**, with a link.

| Verdict | Meaning |
|---|---|
| match | The official figure agrees with the claim |
| close | Within rounding, or within roughly 10 to 15 per cent |
| mismatch | Materially different, or a different quantity from the one named |
| unverifiable | Only the speaker's own side repeats the figure |
| forecast | A prediction when spoken. Recorded with its outcome, not scored |
| not checked | Listed, not reached |

## Check it yourself

**In two minutes.** Open `data/claims.csv`, pick any scored row, open its `source_url`, and compare. Good rows to start with: `T25-05` and `T25-16` (the two "non-oil" findings), `T25-07` (a contested one), `TN-03` (two official sources that disagree).

**Reproduce every number in the report.** Python 3, nothing to install:

```
python3 analyze.py
```

It prints the counts and the agreement figures and rewrites `data/summary.json`.

**Rerun the independent checks.** `second_check.py` downloads the sources and runs the number matching. It needs `pdfplumber`. With a `SERV_API_KEY` in the environment it also runs the blind second coder. In this repository it runs through GitHub Actions (`.github/workflows/second-check.yml`).

## What is in this repository

| Path | What it is |
|---|---|
| `data/claims.csv` | The dataset. One row per figure |
| `data/summary.json` | Every count used in the report |
| `analyze.py` | Computes the counts and the agreement figures |
| `second_check.py` | The two independent checks |
| `check/second_check.json`, `check/second_check_new_rows.json` | Their raw output, including the second coder's reason on every row |
| `figure.py` | Draws the chart from the dataset |
| `notes.md` | The checking log, including what each pass changed |
| `report/Tally-report.pdf` | The report |
| `report/report.tex` | Report source |
| `JUDGES.md` | Where to look, claim by claim, and the weakest points |
| `slides/` | Slides, the narrated presentation, and the narration script |

## Dataset columns

| Column | Meaning |
|---|---|
| `id` | Speech code plus number. `U` marks an unchecked figure |
| `speaker`, `role` | Who said it |
| `speech`, `speech_date`, `speech_url` | Where it was said, with a link to the full text |
| `claim` | The figure as stated. Sometimes an excerpt of the sentence |
| `period` | The period the figure refers to |
| `official_figure` | What the official release says |
| `official_source` | Which body published it |
| `source_type` | `primary document`, `press report of official release`, `independent secondary source`, or `government statement only` |
| `source_url` | Link used for the check |
| `verdict` | One of the six verdicts above |
| `error_type` | For close and mismatch rows |
| `direction` | `favourable` if the error helps the speaker's argument, `unfavourable` if it hurts |
| `note` | Anything needed to interpret the row, including second links and changes made after the checks |

## Limits

- **Small.** Five speeches, 46 scored figures, 10 unchecked.
- **Not a random sample.** The most prominent figures were checked first. The 80% applies to the checked figures only.
- **No human checker.** Both checkers are AI models. Their agreement was low (kappa 0.26). Eight of the thirteen disagreements sit on the edges of the close category. Read the nine rows that did not match exactly as one group.
- **Source choice was not independently tested.** The second coder read the sources the first checker picked.
- **Mostly secondary sources.** 3 scored figures were read from the statistics bureau's own document. 41 rely on press reports quoting the official release and 2 on independent secondary sources.
- **Some figures have one possible source.** For revenue, cash transfers and budget performance, the agency that produces the number is the only source. A match there means the speech agrees with the agency.
- **Two verdicts rest on arithmetic, not a quoted figure.** The 44.3% rise in the trade surplus was recomputed from the report's own numbers. "Over 4 per cent" growth in 2026 uses two official quarterly rates whose average is not an official figure.
- **The list may be incomplete.** The first pass missed eight figures.
- **Official figures are the reference, not the truth.** They can be wrong or revised, and several series were rebased during the period.

This is a starting dataset, not a fact-check of record. Re-check a row before relying on it.

## How to extend it

- Have a person verify each verdict.
- Check the 10 rows marked `not checked`.
- Replace press links with the primary release where one is online.
- Add speeches and speakers using the same procedure.

## AI assistance and prior work

An AI assistant (Claude, Anthropic) did the web research, checking, analysis and drafting, under the author's direction. A second model (gpt-5.4-mini) was used only as the blind second coder. The presentation is narrated with a synthetic voice (Kokoro). Nothing in this repository existed before the sprint.

## Author

Mia
