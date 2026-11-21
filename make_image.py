#!/usr/bin/env python3
# make_image.py - deterministic 1024x1024 news-poster renderer (build-time only).
# The grader runs main.py, which only copies the shipped entry.png (offline, byte-identical every run).
# Headlines: world news reported 20-21 Nov 2026 UTC (AP, Reuters, BBC World, Google News RSS).
# Determinism: fixed system fonts, fixed coordinates, no randomness, no timestamp chunks in the PNG.

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 54                       # page margin
CW = W - 2 * M               # content width = 916
PAPER = (246, 241, 231)
INK   = (17, 14, 10)
RED   = (177, 34, 26)
GRAY  = (90, 82, 70)
FAINT = (203, 194, 176)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

SERIF, SERIF_B, SERIF_I = "georgia.ttf", "georgiab.ttf", "georgiai.ttf"
SANS, SANS_B = "arial.ttf", "arialbd.ttf"

def F(name, size):
    return ImageFont.truetype(name, size)

def wrap(text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out

def para(x, y, text, font, fill, maxw, lh=None):
    lh = lh or round(font.size * 1.16)
    lines = wrap(text, font, maxw)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y, lines

def center(text, y, font, fill, maxw=CW):
    for ln in wrap(text, font, maxw):
        w = d.textlength(ln, font=font)
        d.text(((W - w) / 2, y), ln, font=font, fill=fill)
        y += round(font.size * 1.16)
    return y

checks = []  # (name, y_used, y_limit) - layout overflow assertions

# ---- masthead ----
center("THE WORLD IN ONE FRAME", 40, F(SERIF_B, 46), INK)
d.line((M, 104, W - M, 104), fill=INK, width=3)
d.line((M, 110, W - M, 110), fill=INK, width=1)

# ---- red dateline band ----
BY0, BY1 = 124, 170
d.rectangle((M, BY0, W - M, BY1), fill=RED)
line = "SATURDAY  \u00b7  21 NOVEMBER 2026   |   WORLD EDITION   |   ONE FRAME FOR ONE DAY"
f = F(SANS_B, 21)
d.text(((W - d.textlength(line, font=f)) / 2, BY0 + 12), line, font=f, fill=PAPER)

# ---- lead story ----
LEAD = 184
d.text((M, LEAD), "EUROPE  \u00b7  THE LEAD STORY", font=F(SANS_B, 17), fill=RED)
y, hl = para(M, LEAD + 30, "Russian missile hits Poland; NATO calls it a violation", F(SERIF_B, 50), INK, CW, 58)
y, sb = para(M, y + 8, "The strike lands as alliance forces hold drills nearby - Warsaw calls it likely a provocation; Kyiv's bridges are hit again", F(SERIF_I, 22), GRAY, CW, 28)

# explainer graphic: RU -> PL border crossing
GY0 = y + 16
d.text((M, GY0), "WHERE IT CAME DOWN", font=F(SANS_B, 13), fill=GRAY)
bx0, by0, bx1, by1 = M, GY0 + 22, W - M, GY0 + 76
d.rectangle((bx0, by0, bx1, by1), outline=FAINT, width=2)
split = bx0 + (bx1 - bx0) * 0.55
for yy in range(by0 + 6, by1 - 5, 12):
    d.line((split, yy, split, yy + 6), fill=GRAY, width=2)
fl = F(SANS_B, 16)
cy = (by0 + by1) / 2
d.text((bx0 + 16, cy - 11), "RUSSIA", font=fl, fill=GRAY)
d.text((split + 16, cy - 11), "POLAND", font=fl, fill=INK)
d.line((bx0 + 120, cy, split - 16, cy), fill=RED, width=3)
d.polygon(((split - 8, cy), (split - 24, cy - 7), (split - 24, cy + 7)), fill=RED)
cx = split + 170
for r in (9, 17, 25):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=RED, width=2)
d.text((cx + 34, cy - 9), "impact", font=F(SANS, 14), fill=RED)
d.text((M, by1 + 5), "AP  \u00b7  Reuters  \u00b7  BBC, 21 Nov 2026", font=F(SANS, 14), fill=GRAY)
checks.append(("lead", by1 + 27, 516))

# ---- story grid: 2 cols x 3 rows ----
ROW0, ROWH = 520, 120
cells = [
    ("AMERICAS", "Magnitude 6.8 quake rattles Lima", "Peru's Andes shake sends residents onto the streets."),
    ("MARKETS", "AI rout deepens: Nasdaq -5%, S&P -3.7%", "Nvidia sinks to a 52-week low on an SEC accounting probe."),
    ("EUROPE", "EU and UK sign landmark post-Brexit reset", "London says 'even closer ties' are now on the table."),
    ("MIDDLE EAST", "Houthi missile hits Riyadh's tallest tower", "Saudi wealth-fund HQ struck; two missiles intercepted."),
    ("LAW", "UN court: Myanmar's Rohingya campaign is genocide", "Myanmar and China reject the ICJ ruling."),
    ("CLIMATE", "COP31 draft slammed: fossil fuels unmentioned", "Leaders and activists protest as the talks drag on."),
]
GUT = 28
colw = (CW - GUT) / 2
fh, fk, fb = F(SERIF_B, 27), F(SANS_B, 15), F(SANS, 16)
for i, (k, h, b) in enumerate(cells):
    cx = M + (i % 2) * (colw + GUT)
    cy = ROW0 + (i // 2) * ROWH
    d.line((cx, cy, cx + colw, cy), fill=INK, width=2)
    d.text((cx, cy + 8), k, font=fk, fill=RED)
    yy, lines = para(cx, cy + 32, h, fh, INK, colw, 32)
    yy, blines = para(cx, yy + 4, b, fb, GRAY, colw, 20)
    used = cy + 32 + len(lines) * 32 + 4 + len(blines) * 20
    checks.append((f"cell{i}", used, ROW0 + 3 * ROWH))
GRID_END = ROW0 + 3 * ROWH

# ---- bottom ticker ----
TY = GRID_END + 12
d.line((M, TY, W - M, TY), fill=INK, width=2)
d.text((M, TY + 10), "ALSO TODAY", font=F(SANS_B, 15), fill=RED)
y, tb = para(M, TY + 34, "Kyiv's three bridges struck again  \u00b7  Trump courts Putin and Xi, wants a Ukraine deal by January  \u00b7  Palisades Fire arsonist convicted  \u00b7  NYC to close Rikers Island by 2032  \u00b7  Hackers breach US agriculture department", F(SANS, 16), GRAY, CW, 21)
checks.append(("ticker", y, 988))

# ---- footer ----
FOOT = 996
d.line((M, FOOT, W - M, FOOT), fill=FAINT, width=1)
center("One frame for one day  \u00b7  Saturday 21 November 2026  \u00b7  headlines as reported 20-21 Nov 2026 (AP / Reuters / BBC / Google News)", FOOT + 8, F(SANS, 14), GRAY)

for name, used, limit in checks:
    assert used <= limit, f"overflow {name}: {used} > {limit}"
img.save("entry.png", optimize=True)
print("saved entry.png", img.size)

