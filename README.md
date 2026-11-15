# Tally

**Do their numbers match?** An open, auditable dataset of the figures Nigerian leaders quote in national addresses, each one checked against the official release it refers to.

Apart Research AI x Epistemics Research Sprint, 13 to 15 November 2026. Track 4 (Open Track).

| | |
|---|---|
| Report | [`report/Tally-report.pdf`](report/Tally-report.pdf) |
| Dataset | [`data/claims.csv`](data/claims.csv) |
| Guide for judges | [`JUDGES.md`](JUDGES.md) |
| Checking log | [`notes.md`](notes.md) |

## In one paragraph

Five national addresses were chosen before any checking: four by President Bola Tinubu and one by opposition candidate Atiku Abubakar. The figures in them were listed (59), and 33 were checked against releases from Nigeria's statistics bureau, central bank, debt office and other official bodies. 31 could be scored. 23 matched, 4 were close and 4 did not match. Every scored row carries a link so the verdict can be checked.

## Why this matters

Political speeches lean on numbers. Growth is up, inflation is down, reserves are at a record. Each number comes from an official release, so in principle anyone can check it. In practice it is slow, and for Nigeria the author found no open dataset that puts the claims and the official figures side by side.

That gap matters for AI. Tools that check claims automatically are built and tested mostly on material from a few countries with tidy statistics. To know whether they work in Nigeria, someone first has to assemble real claims, the real figures behind them, and a verdict on each. The sprint brief asks for exactly this under Track 4: pair quantitative claims with the releases they cite, flag mismatches with links, and publish an auditable dataset. Tally is a first, small version.

## Results

| Verdict | Count | Share of the 31 scored |
|---|---|---|
| Match | 23 | 74% |
| Close | 4 | 13% |
| Mismatch | 4 | 13% |

One further figure was unverifiable, one was a forecast, and 26 were listed but not checked.

![Verdicts by speech](report/figure1.png)

**What matched.** Every specific quarterly growth rate and monthly inflation rate quoted in the five speeches matched the statistics bureau exactly.

**What did not match.**

| Claim | Official figure | What went wrong |
|---|---|---|
| Non-oil exports are 48% of exports | Crude 52.60%. Non-crude 47.40%, of which petroleum products and gas 34.21% and non-oil 13.39% | A definition was swapped. The 48% is the non-crude share |
| Oil output rose from "barely one million" barrels a day in May 2023 | 1,183,691 in May 2023. 998,602 was April | The baseline belongs to a different month |
| The stock market gained 48.12% in 2025 | 51.19% for the full year | Out of date. 48.12% was the figure on 22 December |
| Over 418,000 students supported by the loan fund | 510,378 already reported in September | Out of date, and lower than the President's own earlier figure |

**Which way the errors ran.** Seven of the eight errors have a clear direction. Four helped the speaker's argument and three hurt it. The four that helped were the larger ones. Seven cases are too few to say anything about intent, and the report does not.

**Two cases that do not fit match or mismatch.**

- The President's foreign investment figure ($720 million) matches the central bank exactly. The statistics bureau reports $296 million for the same quarter. Both are official.
- The fall in the debt service to revenue ratio "from 97% to below 50%" appears only in government statements. No published series was found.

The two speakers should not be compared from these counts. One gave four speeches and the other gave one, and different shares were checked.

## How the checking was done

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

Then the work was checked three times, and the report says what each pass changed:

- **Audit pass.** Each speech was read again from scratch. Eight missed figures were added. One verdict was changed from close to match, and one lost its direction label.
- **Verification pass.** The source link on every scored row was opened again and the figure read a second time. All 30 existing verdicts held. Eight rows had the recorded figure or the link corrected. One unchecked figure was confirmed and added.
- **Claims pass.** Statements in the report that the evidence did not support were cut or toned down.
- **Mechanical check, no AI.** `second_check.py` runs on a clean GitHub machine, downloads every source and tests by plain text matching whether the recorded official numbers are on the page. All 31 scored rows had a source that opened. In 26 every number was found. In the other 5 the quoted numbers were found and the missing item was the checker's own arithmetic, a number written in another form, or a non-numeric figure. Output: `check/second_check.json`.

## Check it yourself in two minutes

Open `data/claims.csv`, pick any scored row, open its `source_url`, and compare. Good rows to start with:

| Row | Why |
|---|---|
| `T25-05` | The non-oil exports claim. The most consequential finding |
| `T25-07` | The oil baseline. One number, one month |
| `TN-03` | Two official sources that disagree |
| `TN-02` | A figure that was ten days out of date |

To reproduce every count in the report:

```
python3 analyze.py
```

Python 3 only. It prints the counts and rewrites `data/summary.json`. `python3 figure.py` redraws the chart and needs matplotlib.

## What is in this repository

| Path | What it is |
|---|---|
| `data/claims.csv` | The dataset. One row per figure |
| `data/summary.json` | Every count used in the report |
| `analyze.py` | Computes the counts from the dataset |
| `figure.py` | Draws the chart from the dataset |
| `notes.md` | The checking log, including what each pass changed |
| `second_check.py` | The independent check: source download, number matching, and an optional blind second coder |
| `check/second_check.json` | Its output |
| `report/Tally-report.pdf` | The report |
| `report/report.tex` | Report source |
| `JUDGES.md` | Where to look, claim by claim, and the weakest points |

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
| `note` | Anything needed to interpret the row, including second links |

## Limits

- **Small.** Five speeches, 31 scored figures, 26 unchecked.
- **Not a random sample.** The most prominent figures were checked first. The 74% applies to the checked figures only.
- **One checker.** An AI assistant did the extraction and checking. The three passes above were also done by it. No second person verified the rows.
- **Mostly secondary sources.** 3 scored figures were read from the statistics bureau's own document. 26 rely on press reports quoting the official release and 2 on independent secondary sources.
- **Two verdicts rest on arithmetic, not a quoted figure.** The 44.3% rise in the trade surplus was recomputed from the report's own numbers. "Over 4 per cent" growth in 2026 uses two official quarterly rates whose average is not an official figure.
- **The list may be incomplete.** The first pass missed eight figures.
- **Official figures are the reference, not the truth.** They can be wrong or revised, and several series were rebased during the period.

This is a starting dataset, not a fact-check of record. Re-check a row before relying on it.

## How to extend it

- Check the 26 rows marked `not checked`.
- Replace press links with the primary release where one is online.
- Add speeches and speakers using the same procedure.
- Have a second person verify each verdict.

## AI assistance and prior work

An AI assistant (Claude, Anthropic) did the web research, checking, analysis script and drafting, under the author's direction. Nothing in this repository existed before the sprint.

## Author

Mia
