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
json.dump(out, open("data/summary.json", "w"), indent=1)
print(json.dumps(out, indent=1))
