#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Run: python3 draw.py  -> writes entry.png next to this file.
All facts are the events reported on Tuesday 24 November 2026.
Deterministic: no randomness, no network, no timestamps in the image.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BG = (247, 243, 232)      # off-white newsprint
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 86, 78)
LIGHT = (255, 255, 255)
GREEN = (18, 110, 60)
DARK = (24, 28, 34)
PANEL = (238, 240, 236)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # 952 content width

    # ---------- Masthead ----------
    f_mast = font(FONTB, 56)
    title = "THE WORLD IN ONE PICTURE"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 22), title, font=f_mast, fill=INK)
    f_date = font(FONTB, 21)
    date = "Tuesday, 24 November 2026  •  ONE DAY, SEVEN STORIES"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 96), date, font=f_date, fill=RED)
    d.rectangle([mx, 132, W - mx, 137], fill=RED)
    d.rectangle([mx, 140, W - mx, 142], fill=INK)

    # ---------- Hero story ----------
    hy, hh = 156, 252
    d.rectangle([mx, hy, W - mx, hy + hh], fill=LIGHT, outline=INK, width=2)
    # left text column
    hx = mx + 20
    hw = 600
    y = hy + 14
    f_kick = font(FONTB, 16)
    d.text((hx, y), "TECH  •  LEAD STORY", font=f_kick, fill=RED)
    y += 26
    f_hero = font(FONTB, 50)
    y = text_block(d, hx, y, ["NVIDIA BRINGS", "BACK HUANG"], f_hero,
                   leading=52)
    y += 4
    f_sub = font(FONT, 19)
    sub = ("CEO reinstated days after saying he would retire, "
           "after reported intervention by President Trump.")
    y = text_block(d, hx, y, wrap(d, sub, f_sub, hw), f_sub, leading=24)
    y += 2
    f_sub2 = font(FONTB, 19)
    d.text((hx, y), "Shares soar 31% — a record $952bn jump.",
           font=f_sub2, fill=GREEN)
    y += 24
    d.text((hx, y), "Huang's wealth rose $33.7bn in a single day.",
           font=f_sub, fill=INK)

    # right graphic panel: rising chart
    gx, gw = mx + 640, 288
    gy, gh = hy + 14, hh - 28
    d.rectangle([gx, gy, gx + gw, gy + gh], fill=PANEL, outline=INK, width=1)
    f_big = font(FONTB, 46)
    s = "+31%"
    tw = d.textlength(s, font=f_big)
    d.text((gx + (gw - tw) / 2, gy + 12), s, font=f_big, fill=GREEN)
    f_cap = font(FONT, 16)
    cap = "Nvidia shares, 24 Nov"
    tw = d.textlength(cap, font=f_cap)
    d.text((gx + (gw - tw) / 2, gy + 66), cap, font=f_cap, fill=GREY)
    # chart axes + rising line
    ox, oy = gx + 24, gy + gh - 30
    d.line([(ox, oy - 92), (ox, oy)], fill=GREY, width=2)
    d.line([(ox, oy), (ox + gw - 48, oy)], fill=GREY, width=2)
    pts = [(ox + 6, oy - 14), (ox + 46, oy - 26), (ox + 86, oy - 20),
           (ox + 126, oy - 48), (ox + 166, oy - 44), (ox + 206, oy - 84)]
    d.line(pts, fill=GREEN, width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)
    # arrowhead at the top of the rise, pointing up and right
    d.polygon([(ox + 212, oy - 90), (ox + 196, oy - 82), (ox + 204, oy - 68)],
              fill=GREEN)
    f_rec = font(FONTB, 15)
    rec = "record $952bn surge"
    tw = d.textlength(rec, font=f_rec)
    d.text((gx + (gw - tw) / 2, gy + gh - 22), rec, font=f_rec, fill=INK)

    # ---------- Six more stories: 2 columns x 3 rows ----------
    stories = [
        ("MIDDLE EAST",
         "TANKERS BURN IN THE STRAIT OF HORMUZ",
         "Iran says three oil tankers hit mines and caught fire; "
         "the US has not confirmed it. Tehran sets seven conditions "
         "for any talks with Washington."),
        ("MIDDLE EAST",
         "HOUTHIS HIT RIYADH'S TALLEST TOWER AGAIN",
         "A strike on the capital's tallest skyscraper injures 11 — "
         "the second hit on the KAFD financial district in a week."),
        ("MIDDLE EAST",
         "GAZA STRIKE KILLS HAMAS SECURITY CHIEF",
         "An Israeli air strike kills Naeem Abu Nahal and two "
         "policemen in Gaza City, despite the ceasefire in place "
         "since last year."),
        ("EUROPE",
         "EU PLANS 22nd RUSSIA SANCTIONS PACKAGE",
         "The European Commission targets about 60 more banks and "
         "crypto networks used to evade earlier sanctions."),
        ("EUROPE",
         "RUSSIA 'MAY PUT A NUCLEAR WEAPON IN SPACE'",
         "Western intelligence warns of a launch within 60 days. "
         "Germany takes it seriously and NATO responds; the Kremlin "
         "dismisses the report."),
        ("WORLD",
         "14 NATIONS BACK ROHINGYA GENOCIDE RULING",
         "The UK, Spain, Canada, Australia and ten more recognise "
         "the ICJ decision establishing Myanmar's genocide of the "
         "Rohingyas."),
    ]
    f_tag = font(FONTB, 14)
    f_head = font(FONTB, 20)
    f_sum = font(FONT, 16)
    grid_y = 428
    row_h = 148
    col_w = (cw - 24) // 2
    for i, (tag, head, summ) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = mx + col * (col_w + 24)
        y = grid_y + row * row_h
        d.text((x, y), tag, font=f_tag, fill=RED)
        y += 22
        y = text_block(d, x, y, wrap(d, head, f_head, col_w), f_head,
                       leading=24)
        y += 2
        text_block(d, x, y, wrap(d, summ, f_sum, col_w), f_sum, leading=20)
        # divider under each cell except the last row
        if row < 2:
            d.line([(x, grid_y + (row + 1) * row_h - 12),
                    (x + col_w, grid_y + (row + 1) * row_h - 12)],
                   fill=(200, 194, 180), width=1)
    # vertical divider between columns
    d.line([(W // 2, grid_y + 4), (W // 2, grid_y + 3 * row_h - 16)],
           fill=(200, 194, 180), width=1)

    # ---------- Also today ----------
    ay = grid_y + 3 * row_h + 2
    f_also = font(FONT, 17)
    also = ("ALSO TODAY:  5.6-magnitude earthquake strikes Nepal near the "
            "Chinese border  •  USA, Mexico, Costa Rica and Jamaica to "
            "co-host the expanded 48-team 2031 Women's World Cup; "
            "the UK hosts 2035.")
    text_block(d, mx, ay, wrap(d, also, f_also, cw), f_also, leading=22)

    # ---------- Markets strip ----------
    my = 930
    d.rectangle([mx, my, W - mx, my + 56], fill=DARK)
    f_mk = font(FONTB, 18)
    mk1 = "MARKETS  •  S&P 500 +4.7%   Nasdaq +6.5%   Nikkei +3.9%   Hang Seng -0.6%"
    tw = d.textlength(mk1, font=f_mk)
    d.text(((W - tw) / 2, my + 6), mk1, font=f_mk, fill=(255, 255, 255))
    f_mk2 = font(FONT, 16)
    mk2 = ("Brent $86.7 (-3.0%)   Gold $3,620   Memory-chip stocks plunge "
           "as Goldman turns bearish on 2028 DRAM prices")
    tw = d.textlength(mk2, font=f_mk2)
    d.text(((W - tw) / 2, my + 30), mk2, font=f_mk2, fill=(210, 210, 210))

    # ---------- Footer ----------
    f_foot = font(FONT, 13)
    foot = "All events reported on Tuesday, 24 November 2026."
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, 996), foot, font=f_foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
