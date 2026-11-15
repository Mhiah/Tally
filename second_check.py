"""Second, independent check of every scored row in data/claims.csv.

Two checks, both run from GitHub Actions so they do not depend on the first checker's tools:

1. Mechanical check (no AI). Download each row's source and test whether the numbers recorded as the
   official figure are literally present in the page text.
2. Blind second coder (a different AI model, through SERV Reasoning). The model is shown the claim and
   the downloaded source text only. It is not shown the first checker's verdict, official figure or notes.
   It returns its own verdict.

Without SERV_API_KEY only the mechanical check runs. Output: check/second_check.json.
Needs Python 3 and pdfplumber (for the statistics bureau's PDF files).
"""
import csv, io, json, os, re, sys, time, html, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
BASE = os.environ.get("SERV_BASE_URL", "https://inference-api.openserv.ai/v1")
MODEL = os.environ.get("SERV_MODEL", "gpt-5.4-mini")
KEY = os.environ.get("SERV_API_KEY", "").strip()
SCORED = ("match", "close", "mismatch")

# Full sentence for rows whose `claim` cell is only a fragment. Taken from the speech texts.
CONTEXT = {
    "T25-07": "Oil production rebounded to 1.68 million barrels per day from barely one million in May 2023.",
    "T25-09": "Approximately 510,000 students have benefited from the student loan fund, covering 228 higher institutions.",
    "T25-10": "As of September 10, the total [student] loan disbursed was N99.5 billion.",
    "T25-11": "As of September 10, the [student loan] upkeep allowance stood at N44.7 billion.",
    "T25-12": "Our tax-to-GDP ratio has risen to 13.5 per cent from less than 10 per cent. (Check the 13.5 per cent.)",
    "T25-13": "Our tax-to-GDP ratio has risen to 13.5 per cent from less than 10 per cent. (Check the starting point, 'less than 10 per cent'.)",
    "TB-03": "Headline inflation declined to 14.45% in November 2025 from 24.23% in March 2025. (Check the March 2025 figure.)",
    "TB-05": "External reserves of about US$47 billion as at 14 November 2025 provide more than 10 months of import cover.",
    "TN-02": "The Nigerian stock market posted a robust 48.12 per cent gain in 2025. (Said on 1 January 2026.)",
    "A26-04": "The average price of one egg was about N88 in April 2023.",
}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/pdf,*/*", "Accept-Language": "en"})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read(8_000_000); ctype = r.headers.get("Content-Type", "")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"[:200]
    if raw[:4] == b"%PDF" or "pdf" in ctype:
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                return "\n".join((p.extract_text() or "") for p in pdf.pages[:25]), "pdf"
        except Exception as e:
            return None, f"pdf error: {e}"[:200]
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|form).*?</\1>", " ", t)
    t = re.sub(r"(?i)<(br|/p|/div|/li|/h\d|/tr)[^>]*>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = "\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in t.splitlines())
    return re.sub(r"\n{2,}", "\n", t).strip(), "html"

def numbers(s):
    """Numbers with at least three significant characters, e.g. 4.23, 52.60, 1,183,691, 510,378."""
    out = []
    for n in re.findall(r"\d[\d,]*\.?\d*", s):
        n = n.rstrip(".,")
        if len(n.replace(",", "").replace(".", "")) >= 3 and not re.fullmatch(r"20[12]\d", n): out.append(n)
    return list(dict.fromkeys(out))

def present(n, text):
    flat = text.replace(",", "")
    variants = {n, n.replace(",", "")}
    if "." in n: variants.add(n.replace(",", "").rstrip("0").rstrip("."))
    return any(re.search(r"(?<![\d.])" + re.escape(v) + r"(?!\d)", flat if "," not in v else text) for v in variants)

def digest(text, cap=9000):
    """Keep the title area and every line that contains a digit, in order, up to a cap."""
    lines = [l for l in text.splitlines() if l]
    keep = lines[:3] + [l for l in lines[3:] if re.search(r"\d", l) and len(l) > 25]
    return "\n".join(keep)[:cap]

SYSTEM = """You are checking a statistical claim made in a political speech against source material.
You are given the claim and text downloaded from one or more sources. Use ONLY the source text. Do not use prior knowledge.
Decide what the source says about the quantity in the claim, then give one verdict:
- "match": the source figure agrees with the claim (a claim hedged with "about", "over", "approximately" matches if the source figure fits the hedge).
- "close": the claim is within rounding, or within roughly 10 to 15 per cent, of the source figure, but does not agree.
- "mismatch": the source figure differs materially, or the claim describes a different quantity from the one it names, or the claim was out of date by a material amount when spoken.
- "not_in_source": the source text does not contain what is needed to judge.
Reply with JSON only: {"source_figure": "<what the source says, with numbers>", "verdict": "<one of the four>", "reason": "<one or two sentences>"}"""

def ask(user):
    body = json.dumps({"model": MODEL, "temperature": 0, "max_completion_tokens": 2000, "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]}).encode()
    last = ""
    for attempt in range(4):
        try:
            req = urllib.request.Request(BASE + "/chat/completions", data=body, headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r: res = json.load(r)
            msg = res["choices"][0]["message"]; txt = msg.get("content") or ""
            out = json.loads(re.search(r"\{.*\}", txt, re.S).group(0))
            if out.get("verdict") in ("match", "close", "mismatch", "not_in_source"):
                out["model"] = res.get("model", MODEL); return out
            last = "bad verdict: " + txt[:200]
        except Exception as e:
            last = f"{type(e).__name__}: {e}"[:300]
            if hasattr(e, "read"):
                try: last += " | " + e.read().decode()[:300]
                except Exception: pass
        time.sleep(3 * (attempt + 1))
    return {"verdict": "error", "reason": last}

def main():
    rows = [r for r in csv.DictReader(open("data/claims.csv")) if r["verdict"] in SCORED]
    only = set(sys.argv[1:])
    cache, results = {}, []
    for r in rows:
        if only and r["id"] not in only: continue
        urls = list(dict.fromkeys([r["source_url"]] + re.findall(r"https?://\S+", r["note"])))
        urls = [u.rstrip(").,") for u in urls if u]
        srcs = []
        for u in urls:
            if u not in cache: cache[u] = fetch(u); time.sleep(1)
            text, kind = cache[u]
            srcs.append({"url": u, "ok": text is not None and len(text) > 400, "kind": kind, "chars": len(text or "")})
        alltext = "\n".join(cache[u][0] or "" for u in urls)
        nums = numbers(r["official_figure"])
        mech = {n: present(n, alltext) for n in nums}
        res = {"id": r["id"], "speaker": r["speaker"], "first_verdict": r["verdict"], "sources": srcs,
               "official_numbers": mech, "all_numbers_in_source": bool(nums) and all(mech.values()), "any_source_ok": any(s["ok"] for s in srcs)}
        if KEY and res["any_source_ok"]:
            claim = CONTEXT.get(r["id"], r["claim"])
            parts = [f"SOURCE {i+1} ({u}):\n{digest(cache[u][0])}" for i, u in enumerate(urls) if cache[u][0]]
            user = (f"Speaker: {r['speaker']} ({r['role']})\nSpeech: {r['speech']}, {r['speech_date']}\nClaim: {claim}\n"
                    f"Period the claim refers to: {r['period']}\n\n" + "\n\n".join(parts))[:24000]
            res["second"] = ask(user)
        results.append(res); print(res["id"], res["first_verdict"], "| numbers in source:", res["all_numbers_in_source"], "| second:", res.get("second", {}).get("verdict"), flush=True)
    os.makedirs("check", exist_ok=True)
    json.dump({"model": MODEL if KEY else None, "rows": results}, open("check/second_check.json", "w"), indent=1)

if __name__ == "__main__":
    main()
