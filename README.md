# Tally

**Do their numbers match?** An open, auditable dataset of the figures Nigerian leaders quote in national addresses, each one checked against the official release it refers to.

Built for the Apart Research AI x Epistemics Research Sprint (13 to 15 November 2026), Track 4.

- Report: [`report/Tally-report.pdf`](report/Tally-report.pdf)
- Dataset: [`data/claims.csv`](data/claims.csv)
- Judge guide: [`JUDGES.md`](JUDGES.md)

## The idea

Political speeches lean on numbers. Growth is up, inflation is down, reserves are at a record. Each of those numbers comes from somewhere: the statistics bureau, the central bank, the debt office. So in principle anyone can check them. In practice almost nobody does it systematically, and for Nigeria nobody has put the claims and the official figures side by side in one place that others can inspect and reuse.

That gap matters for AI. Tools that check claims automatically are built and tested mostly on material from a handful of countries with tidy statistics. If we want those tools to work in Nigeria, we first need a record of real claims, the real figures behind them, and a verdict on each. Tally is a first, small version of that record.

## What was done

1. **Picked the speeches first.** Five scripted national addresses with published full texts, from October 2025 to October 2026. Four are by President Bola Tinubu. One is by opposition candidate Atiku Abubakar, given the same morning as the President's 2026 Independence Day address, so that government and opposition go through the same check.
2. **Listed the figures.** Each statement with a number about the economy or public money. Each speech was then read a second time to catch anything missed, which added eight. That gave 59 figures.
3. **Looked up the official figure.** National Bureau of Statistics, Central Bank of Nigeria, Debt Management Office, the petroleum regulator, the student loan fund, the export council, the tax authority.
4. **Gave each one a verdict**, with a link to the source.

| Verdict | Meaning |
|---|---|
| match | The official figure agrees with the claim |
| close | Within rounding, or within roughly 10 to 15 per cent |
| mismatch | Materially different, or describes a different quantity from the one named |
| unverifiable | Only the speaker's own side repeats the figure; no release found |
| forecast | A prediction when spoken; recorded with its outcome, not scored |
| not checked | Listed, but not reached in the time available |

## What was found

32 of the 59 figures were checked. 30 could be scored.

| | Count | Share of scored |
|---|---|---|
| Match | 22 | 73% |
| Close | 4 | 13% |
| Mismatch | 4 | 13% |

![Verdicts by speech](report/figure1.png)

- **Headline figures were accurate.** Every specific quarterly growth rate and monthly inflation rate quoted in the five speeches matched the statistics bureau exactly.
- **The biggest error was a swapped definition.** The President said non-oil exports were 48 per cent of the total. The trade release shows crude oil at 52.6 per cent, but another 34.2 per cent was other petroleum products and gas. Exports outside oil and gas were about 13 per cent.
- **Some figures were out of date.** The New Year message quoted a 48.12 per cent stock market gain. That was the figure on 22 December. The full-year gain was 51.19 per cent.
- **Some baselines were off.** Oil output was said to have risen from "barely one million" barrels a day in May 2023. The regulator's May 2023 figure was about 1.18 million. The figure near one million was April.
- **Errors ran both ways.** Of seven errors with a clear direction, four helped the speaker's argument and three hurt it. The ones that helped were the bigger ones. Seven is too few to say anything about intent.
- **Two official sources can disagree.** The President's foreign investment figure ($720 million) matches the central bank. The statistics bureau reports $296 million for the same quarter. Both are official.
- **One claim cannot be checked at all.** The fall in the debt service to revenue ratio "from 97% to below 50%" appears only in government statements.

The two speakers should not be compared from these counts. One gave four speeches and the other one, and different shares were checked.

## What is in this repository

| Path | What it is |
|---|---|
| `data/claims.csv` | The dataset. One row per figure |
| `data/summary.json` | Every count used in the report, produced by `analyze.py` |
| `analyze.py` | Computes the counts from the dataset |
| `figure.py` | Draws the chart from the dataset (needs matplotlib) |
| `notes.md` | The working log kept while checking |
| `report/Tally-report.pdf` | The report |
| `report/report.tex` | Report source |
| `report/figure1.png` | The chart above |
| `JUDGES.md` | A short guide for reviewers |

## The dataset columns

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
| `error_type` | For close and mismatch rows: definition, baseline, stale figure, transcription, official month not located |
| `direction` | `favourable` if the error helps the speaker's argument, `unfavourable` if it hurts |
| `note` | Anything a reader needs to interpret the row |

## Reproduce the numbers

You need Python 3 and nothing else.

```
python3 analyze.py
```

This prints the counts and rewrites `data/summary.json`.

## Limits

- It is small: five speeches, 30 scored figures. 27 listed figures are unchecked.
- The first pass missed eight figures. A second read found them. Others may still be missing.
- The checked figures were the most prominent ones, not a random sample. The 73 per cent applies to them only.
- An AI assistant did the extraction and checking. There was no second checker and no human check of every row.
- Only 3 scored figures were checked against the primary document. The others rely on press reports that quote the official release.
- Official figures are the reference point here. They can be wrong or revised too.

This is a starting dataset, not a fact-check of record. Please re-check a row before you rely on it. The link is on the row for that purpose.

## How to extend it

- Check the 27 rows marked `not checked`.
- Replace press report links with the primary release where one is online.
- Add more speeches and more speakers, using the same procedure.
- Have a second person verify each verdict.

## AI assistance

An AI assistant (Claude, Anthropic) did the web research, checking, analysis script and drafting, under the author's direction. Nothing in this repository existed before the sprint.

## Author

Mia
