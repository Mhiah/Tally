"""Draws report/figure1 from data/claims.csv. Needs matplotlib."""
import csv, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in fm.findSystemFonts():
    if "Inter" in os.path.basename(f): fm.fontManager.addfont(f)
if any("Inter" == f.name for f in fm.fontManager.ttflist): plt.rcParams["font.family"] = "Inter"
rows = list(csv.DictReader(open("data/claims.csv")))
speeches = [("Bola Tinubu", "2025-10-01", "President: Independence Day, Oct 2025"), ("Bola Tinubu", "2025-12-19", "President: Budget speech, Dec 2025"), ("Bola Tinubu", "2026-01-01", "President: New Year message, Jan 2026"), ("Bola Tinubu", "2026-10-01", "President: Independence Day, Oct 2026"), ("Atiku Abubakar", "2026-10-01", "Opposition: Independence Day, Oct 2026")]
V = [("match", "Match", "#2a78d6", "white"), ("close", "Close", "#9ec5f4", "#0b0b0b"), ("mismatch", "Mismatch", "#0b0b0b", "white")]
n_scored = sum(r["verdict"] in ("match", "close", "mismatch") for r in rows)
fig, ax = plt.subplots(figsize=(7.6, 3.3), dpi=200); fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
for i, (sp, d, label) in enumerate(speeches):
    y = len(speeches) - 1 - i; x = 0
    for v, name, col, ink in V:
        n = sum(1 for r in rows if r["speaker"] == sp and r["speech_date"] == d and r["verdict"] == v)
        if n:
            ax.barh(y, n - 0.06, left=x + 0.03, height=0.56, color=col)
            ax.text(x + n / 2, y, str(n), ha="center", va="center", color=ink, fontsize=9, fontweight="bold"); x += n
    ax.text(-0.25, y, label, ha="right", va="center", fontsize=8.5, color="#0b0b0b")
for j, (v, name, col, ink) in enumerate(V):
    ax.barh(-1.05, 0.7, left=j * 5.0, height=0.3, color=col); ax.text(j * 5.0 + 0.95, -1.05, name, va="center", fontsize=8.5, color="#0b0b0b")
ax.text(0, len(speeches) - 0.35, f"Figures checked against official releases, by speech ({n_scored} scored)", fontsize=9.5, fontweight="bold", color="#0b0b0b")
ax.set_xlim(-0.2, 27); ax.set_ylim(-1.5, len(speeches)); ax.axis("off")
fig.subplots_adjust(left=0.36, right=0.99, top=0.98, bottom=0.02)
fig.savefig("report/figure1.png", facecolor=fig.get_facecolor()); fig.savefig("report/figure1.pdf", facecolor=fig.get_facecolor())
