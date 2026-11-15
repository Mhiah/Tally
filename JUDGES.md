# Guide for judges

## One-minute summary

Tally lists every figure in five Nigerian national addresses (four by the President, one by the main opposition candidate) and checks each against the official release. 59 figures listed, 33 checked, 31 scored: 23 match, 4 close, 4 mismatch. The output is an open dataset with a source link on every scored row.

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
| Opposition petrol claim: official month not found, pump prices agree | `A26-03` |
| Tax-to-GDP figure predates the GDP rebasing | `T25-12`, `T25-13` |
| 23 match, 4 close, 4 mismatch | `verdicts` in `data/summary.json` |
| Four errors favourable, three unfavourable | `direction_of_errors` in `data/summary.json` |

Each row has a `source_url`. Open it and compare.

## Against the criteria

**Impact and innovation.** A reusable ground-truth set for claim verification in a low-resource statistical setting, sampled by listing the figures in a fixed set of speeches, so the denominator is visible. Beyond the tally: the types of error, and two cases (conflicting official sources, no release at all) break a simple match or mismatch scheme.

**Execution quality.** Speeches were fixed before checking. Government and opposition went through one procedure. Unchecked figures are listed, not dropped. Every count comes from one script over one file. The work was then checked three times. Each speech was re-read, which added eight missed figures and revised two verdicts. The source on every scored row was re-opened; all verdicts held and eight rows had a figure or link corrected. Unsupported statements in the report were cut. The report and `notes.md` say what changed. A separate script with no AI in it (`second_check.py`, run in GitHub Actions) downloaded every source and found the recorded official numbers on the page for all 31 scored rows, apart from numbers the checker derived by arithmetic.

**Presentation and clarity.** Report is seven pages; the body ends on page six. Limitations and dual-use appendix included.

## Weakest points, stated plainly

1. Small sample: 31 scored figures. Seven errors with a direction is too few to say anything about intent.
2. One AI checker, no second checker, no human verification of every row.
3. 28 of 31 scored figures rest on press reports of the official release or other secondary sources, not the primary document.
4. Checked figures were prioritised by prominence, not sampled at random.
5. The 26 unchecked rows carry no source link. The first extraction missed eight figures, so the list may still be incomplete. Two of them (`A26-06`, `A26-07`) were searched for and not found.
6. Claim wording is sometimes an excerpt of the sentence, not the full sentence.
7. Two verdicts rest on the checker's arithmetic from published figures (`T25-04`, `T26-01`). The rows say so.
8. Two food-price rows (`A26-04`, `A26-05`) are bracketed by the months either side because the April 2023 table was not located.

## Questions you might ask

**Is this a comparison of the President and the opposition?** No. Four speeches against one, with different shares checked. The report says so.

**Why count "48% non-oil" as a mismatch when crude really was 52%?** Because the claim is about non-oil exports, and most of the 48% is oil and gas products. The row explains the reasoning so you can disagree with it.

**Why is the foreign investment claim a match?** It matches the central bank exactly. The conflict with the statistics bureau is recorded in the note.

**Was anything built before the sprint?** No.
