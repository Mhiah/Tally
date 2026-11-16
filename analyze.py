"""Counts every number used in the report from data/claims.csv. Needs only Python 3."""
import csv, json, collections
rows = list(csv.DictReader(open("data/claims.csv")))
scored = [r for r in rows if r["verdict"] in ("match", "close", "mismatch")]
out = {
    "figures_listed": len(rows),
    "verdicts": dict(collections.Counter(r["verdict"] for r in rows)),
    "scored": len(scored),
    "scored_share": {v: round(100 * sum(r["verdict"] == v for r in scored) / len(scored), 1) for v in ("match", "close", "mismatch")},
    "by_speaker": {s: dict(collections.Counter(r["verdict"] for r in rows if r["speaker"] == s)) for s in sorted(set(r["speaker"] for r in rows))},
    "by_speech": {f'{r["speaker"]} | {r["speech"]} | {r["speech_date"]}': None for r in rows},
    "error_types": dict(collections.Counter(r["error_type"] for r in rows if r["error_type"])),
    "direction_of_errors": dict(collections.Counter(r["direction"] for r in rows if r["direction"])),
    "direction_by_speaker": {s: dict(collections.Counter(r["direction"] for r in rows if r["speaker"] == s and r["direction"])) for s in sorted(set(r["speaker"] for r in rows))},
    "source_types_for_scored": dict(collections.Counter(r["source_type"] for r in scored)),
}
for k in out["by_speech"]:
    sp, speech, date = k.split(" | ")
    out["by_speech"][k] = dict(collections.Counter(r["verdict"] for r in rows if r["speaker"] == sp and r["speech"] == speech and r["speech_date"] == date))
# Agreement with the blind second coder (check/second_check.json), using the verdicts as they stood when it ran.
import os
if os.path.exists("check/second_check.json"):
    allrows = json.load(open("check/second_check.json"))["rows"]
    if os.path.exists("check/second_check_new_rows.json"):
        allrows += json.load(open("check/second_check_new_rows.json"))["rows"]
    sc = [r for r in allrows if "second" in r]
    pairs = [(r["first_verdict"], r["second"]["verdict"]) for r in sc]
    n = len(pairs); agree = sum(a == b for a, b in pairs)
    cats = sorted(set(x for p in pairs for x in p))
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    binary = sum((a == "match") == (b == "match") for a, b in pairs)
    out["second_coder"] = {"model": sc[0]["second"].get("model"), "rows": n, "same_verdict": agree, "same_verdict_share": round(100 * agree / n, 1),
        "cohens_kappa": round((agree / n - pe) / (1 - pe), 2), "same_on_match_vs_not": binary, "same_on_match_vs_not_share": round(100 * binary / n, 1),
        "disagreements": {r["id"]: [r["first_verdict"], r["second"]["verdict"]] for r in sc if r["first_verdict"] != r["second"]["verdict"]},
        "second_coder_counts": dict(collections.Counter(b for _, b in pairs))}
    mech = allrows
    out["mechanical_check"] = {"rows": len(mech), "a_source_opened": sum(r["any_source_ok"] for r in mech), "all_recorded_numbers_found": sum(r["all_numbers_in_source"] for r in mech)}
json.dump(out, open("data/summary.json", "w"), indent=1)
print(json.dumps(out, indent=1))
