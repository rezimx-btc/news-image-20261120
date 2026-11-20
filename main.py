#!/usr/bin/env python3
"""The World Today -- Friday, 20 November 2026.

A dense one-page broadsheet newspaper front page rendered as a
1024x1024 PNG. Pure Python 3.13 standard library only (zlib + struct).
Deterministic: running it twice produces a byte-identical entry.png.

The program writes entry.png ONLY into the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (default '/output'). It never
writes beside main.py or anywhere inside the repository at run time.
"""

import os
import struct
import zlib

W = 1024
H = 1024

# 5x7 pixel font. '#' = ink, '.' = blank.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
}

FONT.update({
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "%": ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    "&": (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    "~": (".....", ".....", ".##.#", "#.##.", ".....", ".....", "....."),
})


PAPER = (250, 248, 240)
INK = (18, 18, 18)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (110, 110, 108)
LIGHT = (214, 212, 204)
SEA = (198, 210, 214)
RED = (168, 30, 30)


def new_canvas():
    return bytearray(bytes(PAPER) * (W * H))


def fill_rect(img, x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(c) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        img[i:i + (x1 - x0) * 3] = row


def fill_ellipse(img, cx, cy, rx, ry, c):
    for yy in range(cy - ry, cy + ry + 1):
        dy = (yy - cy) / float(ry)
        inside = 1.0 - dy * dy
        if inside < 0:
            continue
        dx = int(rx * (inside ** 0.5))
        fill_rect(img, cx - dx, yy, 2 * dx + 1, 1, c)


def hline(img, x, y, w, c, t=1):
    fill_rect(img, x, y, w, t, c)


def vline(img, x, y, h, c, t=1):
    fill_rect(img, x, y, t, h, c)


def text_w(s, scale):
    if not s:
        return 0
    return len(s) * 6 * scale - scale


def draw_text(img, x, y, s, scale, c):
    for ci, ch in enumerate(s):
        g = FONT.get(ch, FONT[" "])
        ox = x + ci * 6 * scale
        for r in range(7):
            row = g[r]
            for col in range(5):
                if row[col] == "#":
                    fill_rect(img, ox + col * scale, y + r * scale,
                              scale, scale, c)


def draw_center(img, cx, y, s, scale, c):
    draw_text(img, cx - text_w(s, scale) // 2, y, s, scale, c)


def wrap(s, scale, max_w):
    lines = []
    cur = ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def marker(img, x, y, n):
    fill_ellipse(img, x, y, 10, 10, BLACK)
    label = str(n)
    draw_text(img, x - text_w(label, 1) // 2, y - 3, label, 1, WHITE)


def headline_item(img, x, y, num, text, width, detail=""):
    fill_rect(img, x, y, 16, 16, BLACK)
    label = str(num)
    draw_text(img, x + (16 - text_w(label, 1)) // 2, y + 4, label, 1, WHITE)
    lines = wrap(text, 1, width - 24)
    for i, line in enumerate(lines):
        draw_text(img, x + 24, y + i * 10, line, 1, INK)
    yy = y + max(1, len(lines)) * 10 + 2
    if detail:
        for line in wrap(detail, 1, width - 24):
            draw_text(img, x + 24, yy, line, 1, GREY)
            yy += 10
    return yy + 8


# Story numbers double as the numbered markers on the world map.
COLUMNS = [
    ("AMERICAS", [
        (2, "TRUMP PUSHES ANY IRAN WAR DECISION TO 2027"),
        (5, "GTA 6 SALES PASS THE ODYSSEY'S $1.80BN GLOBAL RUN"),
        (7, "ANTHROPIC SHARES CLOSE 17% HIGHER ON FIRST DAY OF TRADING"),
        (3, "NASA CONFIRMS VOYAGER 1 PASSES A LIGHT-DAY MILESTONE"),
    ]),
    ("EUROPE", [
        (8, "EUROPE READY FOR TALKS WITH RUSSIA ON ENDING UKRAINE WAR"),
        (11, "EU-UK SUMMIT TAKES PLACE IN BRUSSELS TODAY"),
        (9, "ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA"),
        (12, "TODAY IS WORLD CHILDREN'S DAY, 20 NOVEMBER"),
    ]),
    ("ASIA-PACIFIC", [
        (4, "ENGINE TROUBLE FORCES HAYABUSA2 TO ABANDON ASTEROID LANDING"),
        (6, "CYCLONE AKVAN: 300,000 EVACUATED AS STORM NEARS ODISHA COAST"),
        (13, "SOUTH KOREA TOP COURT OVERTURNS EX-PM HAN DUCK-SOO CONVICTION"),
        (14, "FIJI DECLARES NATIONAL STATE OF DISASTER OVER SEVERE DROUGHT"),
        (10, "CRICKET: NICHOLLS 113 NOT OUT AS NZ FACE INDIA IN WELLINGTON"),
    ]),
]

MARKERS = [
    (1, 762, 338), (2, 598, 368), (3, 948, 296), (4, 838, 330),
    (5, 196, 362), (6, 700, 382), (7, 138, 330), (8, 540, 308),
    (9, 742, 396), (10, 928, 448), (11, 492, 318), (12, 60, 452),
    (13, 800, 322), (14, 952, 428),
]


def draw_masthead(img):
    fill_rect(img, 14, 14, W - 28, H - 28, PAPER)
    hline(img, 14, 14, W - 28, BLACK, 3)
    hline(img, 14, H - 15, W - 28, BLACK, 3)
    vline(img, 14, 14, H - 28, BLACK, 3)
    vline(img, W - 15, 14, H - 28, BLACK, 3)
    draw_center(img, W // 2, 30, "THE WORLD TODAY", 7, INK)
    hline(img, 30, 92, W - 60, BLACK, 2)
    draw_text(img, 30, 102, "VOL. CCLXXIV - NO. 324", 1, GREY)
    draw_center(img, W // 2, 100, "FRIDAY, 20 NOVEMBER 2026", 2, RED)
    draw_text(img, W - 30 - text_w("PRICE $2.50", 1), 102, "PRICE $2.50", 1, GREY)
    hline(img, 30, 122, W - 60, BLACK, 4)


def draw_lead(img):
    draw_center(img, W // 2, 134, "APEC SUMMIT - SHENZHEN, CHINA", 1, RED)
    lines = wrap("TRUMP, XI AND PUTIN HOLD HISTORIC FIRST THREE-WAY MEETING", 3, W - 80)
    y = 152
    for line in lines:
        draw_center(img, W // 2, y, line, 3, INK)
        y += 28
    deck = wrap("LEADERS TO DISCUSS GLOBAL SECURITY AND NUCLEAR ARMS CONTROL "
                "IN LANDMARK SUMMIT - THE FIRST TIME THE THREE HAVE MET TOGETHER", 1, W - 160)
    for line in deck:
        draw_center(img, W // 2, y, line, 1, GREY)
        y += 11
    hline(img, 30, y + 6, W - 60, BLACK, 2)
    return y + 14


def draw_map(img, top):
    draw_center(img, W // 2, top, "THE WORLD TODAY - WHERE THE NEWS IS", 1, INK)
    my = top + 18
    fill_rect(img, 30, my, W - 60, 210, SEA)
    hline(img, 30, my, W - 60, BLACK, 2)
    hline(img, 30, my + 210, W - 60, BLACK, 2)
    vline(img, 30, my, 210, BLACK, 2)
    vline(img, W - 31, my, 210, BLACK, 2)
    # Simplified continents.
    fill_ellipse(img, 170, my + 62, 108, 44, LIGHT)
    fill_ellipse(img, 120, my + 40, 55, 30, LIGHT)
    fill_ellipse(img, 330, my + 28, 30, 16, LIGHT)
    fill_ellipse(img, 280, my + 140, 44, 44, LIGHT)
    fill_ellipse(img, 500, my + 48, 46, 24, LIGHT)
    fill_ellipse(img, 520, my + 118, 54, 52, LIGHT)
    fill_ellipse(img, 700, my + 58, 148, 48, LIGHT)
    fill_ellipse(img, 800, my + 132, 58, 16, LIGHT)
    fill_ellipse(img, 862, my + 156, 54, 24, LIGHT)
    for n, x, y in MARKERS:
        marker(img, x, my + y - 282, n)
    return my + 210 + 12


def draw_columns(img, top):
    col_w = 312
    xs = [24, 356, 688]
    bottom = top
    for (title, stories), x in zip(COLUMNS, xs):
        fill_rect(img, x, top, col_w, 22, BLACK)
        draw_center(img, x + col_w // 2, top + 7, title, 1, WHITE)
        y = top + 32
        for num, text in stories:
            y = headline_item(img, x, y, num, text, col_w,
                              DETAILS.get(num, ""))
            hline(img, x, y - 2, col_w, LIGHT, 1)
        bottom = max(bottom, y)
    return bottom


def draw_footer(img):
    fill_rect(img, 24, 902, W - 48, 44, BLACK)
    draw_center(img, W // 2, 912,
                "MARKETS - ANTHROPIC +17% ON DEBUT - VALUATION $1.5 TRILLION", 1, WHITE)
    draw_center(img, W // 2, 928,
                "GTA 6 PASSES $1.80BN - CYCLONE AKVAN EVACUATIONS UNDER WAY", 1, WHITE)
    hline(img, 30, 960, W - 60, BLACK, 2)
    draw_center(img, W // 2, 970,
                "WORLD CHILDREN'S DAY - 20 NOVEMBER 2026", 1, RED)
    draw_center(img, W // 2, 988,
                "PRINTED IN LONDON - NEW YORK - SINGAPORE", 1, GREY)


DETAILS = {
    2: "NO DECISION BEFORE 2027, SAYS THE PRESIDENT",
    5: "ROCKSTAR'S BLOCKBUSTER ALREADY AHEAD OF THE FILM'S GLOBAL RUN",
    7: "VALUATION REPORTED AT $1.5 TRILLION AFTER DAY-ONE SURGE",
    3: "THE PROBE IS NOW MORE THAN A LIGHT-DAY FROM EARTH",
    8: "LEADERS SAY THEY ARE READY TO TALK TO MOSCOW",
    11: "LEADERS MEET IN BRUSSELS AS TIES ARE RESET",
    9: "THE HAGUE COURT FINDS MYANMAR GUILTY OVER THE ROHINGYA",
    12: "CHILDREN'S RIGHTS MARKED AROUND THE WORLD TODAY",
    4: "JAXA DROPS THE LANDING PLAN AFTER ENGINE TROUBLE",
    6: "THE STORM IS HEADING FOR THE ODISHA COAST",
    13: "THE FORMER PM'S CONVICTION IS QUASHED",
    14: "THE PACIFIC NATION FACES ITS WORST DROUGHT IN YEARS",
    10: "FIRST TEST, WELLINGTON - NEW ZEALAND V INDIA",
}

BRIEFS = [
    "THE SUMMIT: FIRST MEETING OF ITS KIND - SECURITY AND ARMS CONTROL ON THE TABLE",
    "IRAN: NO DECISION BEFORE 2027, TRUMP SAYS - SEE WHAT HAPPENS",
    "SPACE: VOYAGER 1 PASSES A LIGHT-DAY - HAYABUSA2 LANDING ABANDONED",
    "CLIMATE: 300,000 EVACUATED AHEAD OF CYCLONE AKVAN - FIJI IN DROUGHT EMERGENCY",
    "MARKETS: ANTHROPIC +17% ON DEBUT - GTA 6 BEATS $1.80BN",
    "SPORT: NICHOLLS 113 NOT OUT - NEW ZEALAND V INDIA, FIRST TEST, WELLINGTON",
]


def draw_briefs(img, top, bottom):
    hline(img, 30, top, W - 60, BLACK, 2)
    draw_center(img, W // 2, top + 8, "ALSO IN THE NEWS", 1, INK)
    y = top + 28
    col_w = (W - 60) // 2 - 12
    for i, text in enumerate(BRIEFS):
        bx = 30 if i % 2 == 0 else 30 + col_w + 24
        by = y + (i // 2) * 26
        draw_text(img, bx, by, "-", 1, RED)
        for j, line in enumerate(wrap(text, 1, col_w - 14)):
            draw_text(img, bx + 12, by + j * 10, line, 1, INK)
    hline(img, 30, bottom - 8, W - 60, BLACK, 2)


def render():
    img = new_canvas()
    draw_masthead(img)
    after_lead = draw_lead(img)
    after_map = draw_map(img, after_lead)
    after_cols = draw_columns(img, after_map)
    draw_briefs(img, after_cols + 8, 892)
    draw_footer(img)
    return img


def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(img):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw += img[yy * W * 3:(yy + 1) * W * 3]
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", ihdr)
    data += png_chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    data += png_chunk(b"IEND", b"")
    return data


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    data = encode_png(render())
    with open(os.path.join(outdir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
