# Guide for judges

## One-minute summary

Tally lists every figure in five Nigerian national addresses (four by the President, one by the main opposition candidate) and checks each against the official release. 51 figures listed, 31 checked, 29 scored: 20 match, 5 close, 4 mismatch. The output is an open dataset with a source link on every scored row.

Track 4. The sprint brief suggests pairing quantitative claims with the statistical releases they cite, flagging mismatches with links, and publishing an auditable dataset. This is that, for a country current resources do not cover.

## Where things are

| You want | Open |
|---|---|
| The report | `report/Tally-report.pdf` |
| The data | `data/claims.csv` |
| The numbers in the report | `data/summary.json`, made by `python3 analyze.py` |
| The working log | `notes.md` |

## Check a claim in the report yourself

| Claim in the report | Row in `data/claims.csv` |
|---|---|
| "Non-oil" exports of 48% are mostly petroleum products and gas | `T25-05` |
| Oil baseline of "barely one million" belongs to April, not May 2023 | `T25-07` |
| Stock market gain was ten days out of date | `TN-02` |
| Student loan figure lower than the one cited eleven weeks earlier | `TB-06`, compare `T25-08` |
| Two official sources disagree on foreign direct investment | `TN-03` |
| Debt service ratio cannot be verified | `T25-14` |
| Opposition petrol claim understated its own point | `A26-03` |
| 20 match, 5 close, 4 mismatch | `verdicts` in `data/summary.json` |
| Five errors favourable, four unfavourable | `direction_of_errors` in `data/summary.json` |

Each row has a `source_url`. Open it and compare.

## Against the criteria

**Impact and innovation.** A reusable ground-truth set for claim verification in a low-resource statistical setting, sampled by listing every figure in a fixed set of speeches, so the denominator is visible. Two findings go beyond a tally: errors ran in both directions, and two cases (conflicting official sources, no release at all) break a simple match or mismatch scheme.

**Execution quality.** Speeches were fixed before checking. Government and opposition went through one procedure. Unchecked figures are listed, not dropped. Every count comes from one script over one file.

**Presentation and clarity.** Report is six pages, body within the limit. Limitations and dual-use appendix included.

## Weakest points, stated plainly

1. Small sample: 29 scored figures.
2. One AI checker, no second checker, no human verification of every row.
3. 26 of 29 scored figures rest on press reports of the official release or an agency statement, not the primary document.
4. Checked figures were prioritised by prominence, not sampled at random.
5. The 20 unchecked rows carry no source link. Two of them (`A26-06`, `A26-07`) were searched for and not found.
6. Claim wording is sometimes an excerpt of the sentence, not the full sentence.

## Questions you might ask

**Is this a comparison of the President and the opposition?** No. Four speeches against one, with different shares checked. The report says so.

**Why count "48% non-oil" as a mismatch when crude really was 52%?** Because the claim is about non-oil exports, and most of the 48% is oil and gas products. The row explains the reasoning so you can disagree with it.

**Why is the foreign investment claim a match?** It matches the central bank exactly. The conflict with the statistics bureau is recorded in the note.

**Was anything built before the sprint?** No.
