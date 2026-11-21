#!/usr/bin/env python3
# Deterministic 1024x1024 world-news poster for Saturday 21 November 2026.
# No randomness, no network. Writes entry.png next to this file.
# Headlines compiled from BBC World, Straits Times, NDTV and Times of India
# coverage of 20-21 November 2026.
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 251, 247)
INK = (26, 26, 26)
RED = (179, 38, 30)
MUTE = (105, 105, 105)
RULE = (70, 70, 70)
WHITE = (255, 255, 255)

FDIR = r"C:\Windows\Fonts"


def F(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_MAST = F("arialbd.ttf", 64)
F_DATELINE = F("arial.ttf", 25)
F_TAG = F("arialbd.ttf", 18)
F_HEAD = F("arialbd.ttf", 26)
F_SUM = F("arial.ttf", 18)
F_ALSO = F("arialbd.ttf", 19)
F_ALSO_BODY = F("arial.ttf", 18)
F_FOOT = F("arial.ttf", 16)

CAT_COLORS = {
    "DIPLOMACY": (31, 78, 121),
    "PEACE": (31, 78, 121),
    "MARKETS": (15, 107, 60),
    "SCIENCE": (107, 45, 139),
    "HUMANITY": (179, 38, 30),
    "JUSTICE": (122, 59, 18),
    "CLIMATE": (14, 110, 140),
    "SPORT": (192, 86, 33),
}


def wrap(draw, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(d, x, y, w, tag, head, summ):
    c = CAT_COLORS.get(tag, (60, 60, 60))
    tw = d.textlength(tag, font=F_TAG) + 26
    d.rounded_rectangle([x, y, x + tw, y + 30], radius=15, fill=c)
    d.text((x + 13, y + 5), tag, font=F_TAG, fill=WHITE)
    yy = y + 42
    for ln in wrap(d, head, F_HEAD, w):
        d.text((x, yy), ln, font=F_HEAD, fill=INK)
        yy += F_HEAD.size + 5
    yy += 5
    for ln in wrap(d, summ, F_SUM, w):
        d.text((x, yy), ln, font=F_SUM, fill=MUTE)
        yy += F_SUM.size + 4
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle([10, 10, W - 11, H - 11], outline=RULE, width=2)
    d.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=1)

    # masthead
    mast = "WORLD NEWS DISPATCH"
    mw = d.textlength(mast, font=F_MAST)
    d.text(((W - mw) / 2, 44), mast, font=F_MAST, fill=INK)
    # red underline accent
    d.rectangle([(W - 340) / 2, 128, (W + 340) / 2, 134], fill=RED)

    # dateline
    dl = "SATURDAY  ·  21 NOVEMBER 2026  ·  THE WORLD IN ONE IMAGE"
    dw = d.textlength(dl, font=F_DATELINE)
    d.text(((W - dw) / 2, 148), dl, font=F_DATELINE, fill=INK)

    # columns
    margin = 44
    gap = 30
    colw = (W - 2 * margin - gap) // 2
    x1, x2 = margin, margin + colw + gap
    top = 208
    rowh = 158

    blocks = [
        ("DIPLOMACY", "Trump and Xi agree: humans stay in the loop on military AI",
         "Shenzhen summit deal on 'super intelligence' safeguards, says Bessent"),
        ("PEACE", "Trump hails 'very good' Putin talks on Ukraine",
         "President says a deal has 'a real good chance' after APEC meeting"),
        ("MARKETS", "Wall Street rout deepens into correction",
         "Dow and S&P 500 fall over 10% from records as Anthropic debut flops"),
        ("SCIENCE", "Claude chatbot used to prove Riemann Hypothesis",
         "Anthropic researcher claims 160-year-old maths riddle solved with AI"),
        ("HUMANITY", "UN warns global hunger is growing",
         "WFP funding shortfall threatens food aid for 91 million people"),
        ("JUSTICE", "Rights groups demand action on Myanmar",
         "Calls for reparations after ICJ's landmark Rohingya genocide ruling"),
        ("CLIMATE", "Cyclone Akvan weakens after landfall",
         "Deep depression crosses Odisha and Andhra coasts; alert continues"),
        ("SPORT", "F1 to return to V8 engines from 2030",
         "FIA, teams and manufacturers agree framework for louder racing"),
    ]

    maxy = top
    for i, (tag, head, summ) in enumerate(blocks):
        col = i % 2
        row = i // 2
        x = x1 if col == 0 else x2
        y = top + row * rowh
        end = draw_block(d, x, y, colw, tag, head, summ)
        maxy = max(maxy, end)

    # ALSO TODAY strip
    ay = maxy + 26
    d.rectangle([margin, ay, W - margin, ay + 2], fill=RULE)
    d.text((margin, ay + 14), "ALSO TODAY", font=F_ALSO, fill=RED)
    also = [
        "Trump attacks 'political' Fed, demands lowest rates for 15-20% GDP",
        "Modi opens first SCO Civilisational Dialogue Forum in New Delhi",
        "FIIs pour record Rs 1.01 lakh crore into Indian equities in November",
    ]
    by = ay + 46
    for line in also:
        d.ellipse([margin + 2, by + 7, margin + 10, by + 15], fill=RED)
        d.text((margin + 22, by), line, font=F_ALSO_BODY, fill=INK)
        by += F_ALSO_BODY.size + 6

    # footer
    foot = "Compiled from BBC World  ·  Straits Times  ·  NDTV  ·  Times of India   —   Saturday, 21 November 2026"
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((W - fw) / 2, H - 36), foot, font=F_FOOT, fill=MUTE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()