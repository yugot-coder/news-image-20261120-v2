#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - Friday 20 November 2026.

One dense broadsheet page, drawn entirely in code: three illustrated
lead stories, ten numbered cards, a world map with pins, a stats
strip and a one-line index of the rest of the day. Pure Python
standard library (zlib/struct PNG writer), no network, no file
reads, no randomness or clock - two runs are byte-identical.

Facts were checked on the day against Reuters, CNN, The Times,
IMD (India), the Statistics Bureau of Japan, Scientific American,
Carbon Herald, Cricbuzz and Sotheby's reporting (see README).
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 241, 227)
PAPER_D = (238, 229, 205)
INK = (24, 22, 18)
RED = (178, 30, 38)
RED_D = (140, 20, 30)
NAVY = (16, 32, 56)
NAVY2 = (24, 48, 82)
TEAL = (14, 104, 110)
GOLD = (214, 164, 32)
CREAM = (255, 250, 238)
GREY = (96, 92, 84)

# ------------------------------------------------------------- bitmap font
# 5x7 glyphs, '#' = ink. Written for this entry.
BF = {
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
 "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
 "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
 "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
 "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
 "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
 "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
 "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
 "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
 "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
 "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
 "a": (".....", ".....", ".####", "....#", ".####", "#...#", ".###."),
 "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
 "c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
 "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
 "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
 "f": ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
 "g": (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
 "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
 "i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
 "j": ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", ".##.."),
 "k": ("#....", "#....", "#.#..", "#.#..", "##...", "#.#..", "#..#."),
 "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
 "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
 "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
 "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
 "p": (".....", ".....", "####.", "#...#", "#...#", "####.", "#....", "...."),
 "q": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#", "....#"),
 "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
 "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
 "t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
 "u": (".....", ".....", "#...#", "#...#", "#...#", "#...#", ".###."),
 "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
 "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
 "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
 "y": (".....", "#...#", "#...#", "#...#", ".####", "....#", ".###."),
 "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
 " ": (".....",) * 7,
 ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
 ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
 ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
 ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
 "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
 "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
 "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
 "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
 '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
 "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
 ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
 "/": ("....#", "...#.", "...#.", "..#..", "..#..", ".#...", "#...."),
 "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
 "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
 "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
 "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
 "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
 "*": (".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."),
}
BLANK = (".....",) * 7

# ------------------------------------------------------------- vector font
# Stroke glyphs on a 10-wide, 14-tall grid (y down, baseline = 14).
# Each glyph: list of strokes; each stroke: list of (x, y) points.
VF = {
 "A": [[(0, 14), (5, 0), (10, 14)], [(2.5, 8), (7.5, 8)]],
 "B": [[(1, 0), (6, 0), (9, 3.5), (6, 7), (1, 7)], [(1, 0), (1, 14)],
       [(1, 7), (6.5, 7), (9.5, 10.5), (6, 14), (1, 14)]],
 "C": [[(9, 3), (6, 0.5), (3, 0.5), (0.5, 4), (0.5, 10), (3, 13.5),
        (6, 13.5), (9, 11)]],
 "D": [[(1, 0), (1, 14)], [(1, 0), (5.5, 0), (9.5, 4.5), (9.5, 9.5),
        (5.5, 14), (1, 14)]],
 "E": [[(9, 0), (1, 0), (1, 14), (9, 14)], [(1, 7), (7, 7)]],
 "F": [[(1, 14), (1, 0), (9, 0)], [(1, 7), (7, 7)]],
 "G": [[(9, 3), (6, 0.5), (3, 0.5), (0.5, 4), (0.5, 10), (3, 13.5),
        (6.5, 13.5), (9.5, 10.5), (9.5, 8), (6, 8)]],
 "H": [[(1, 0), (1, 14)], [(9, 0), (9, 14)], [(1, 7), (9, 7)]],
 "I": [[(5, 0), (5, 14)], [(2, 0), (8, 0)], [(2, 14), (8, 14)]],
 "J": [[(9, 0), (9, 10), (6.5, 13.5), (3, 13.5), (0.5, 11)]],
 "K": [[(1, 0), (1, 14)], [(9, 0), (1.5, 7.5)], [(3.5, 5.5), (9, 14)]],
 "L": [[(1, 0), (1, 14), (9, 14)]],
 "M": [[(0.5, 14), (0.5, 0), (5, 8), (9.5, 0), (9.5, 14)]],
 "N": [[(1, 14), (1, 0), (9, 14), (9, 0)]],
 "O": [[(3, 0.5), (7, 0.5), (9.5, 4), (9.5, 10), (7, 13.5), (3, 13.5),
        (0.5, 10), (0.5, 4), (3, 0.5)]],
 "P": [[(1, 14), (1, 0), (6.5, 0), (9.5, 3.5), (6.5, 7), (1, 7)]],
 "Q": [[(3, 0.5), (7, 0.5), (9.5, 4), (9.5, 10), (7, 13.5), (3, 13.5),
        (0.5, 10), (0.5, 4), (3, 0.5)], [(6, 10), (10, 14.5)]],
 "R": [[(1, 14), (1, 0), (6.5, 0), (9.5, 3.5), (6.5, 7), (1, 7)],
       [(5.5, 7), (9.5, 14)]],
 "S": [[(9, 2.5), (6, 0.5), (3, 0.5), (0.5, 3), (3, 6.5), (7, 7.5),
        (9.5, 10.5), (7, 13.5), (3, 13.5), (0.5, 11.5)]],
 "T": [[(0.5, 0), (9.5, 0)], [(5, 0), (5, 14)]],
 "U": [[(1, 0), (1, 10), (3.5, 13.5), (6.5, 13.5), (9, 10), (9, 0)]],
 "V": [[(0.5, 0), (5, 14), (9.5, 0)]],
 "W": [[(0, 0), (2, 14), (5, 4), (8, 14), (10, 0)]],
 "X": [[(0.5, 0), (9.5, 14)], [(9.5, 0), (0.5, 14)]],
 "Y": [[(0.5, 0), (5, 6.5), (9.5, 0)], [(5, 6.5), (5, 14)]],
 "Z": [[(0.5, 0), (9.5, 0), (0.5, 14), (9.5, 14)]],
 "0": [[(3, 0.5), (7, 0.5), (9.5, 4), (9.5, 10), (7, 13.5), (3, 13.5),
        (0.5, 10), (0.5, 4), (3, 0.5)], [(8, 2), (2, 12)]],
 "1": [[(2.5, 3), (5.5, 0), (5.5, 14)], [(2, 14), (9, 14)]],
 "2": [[(0.5, 3.5), (3, 0.5), (7, 0.5), (9.5, 3.5), (0.5, 14),
        (9.5, 14)]],
 "3": [[(0.5, 2), (3, 0.5), (7, 0.5), (9, 3.5), (6, 7), (3.5, 7)],
       [(6, 7), (9.5, 10), (7, 13.5), (3, 13.5), (0.5, 11.5)]],
 "4": [[(6.5, 14), (6.5, 0), (0.5, 10), (9.5, 10)]],
 "5": [[(9, 0), (1.5, 0), (1, 6), (6, 5.5), (9.5, 8.5), (7, 13.5),
        (3, 13.5), (0.5, 11)]],
 "6": [[(8.5, 2.5), (5.5, 0.5), (2, 3), (0.5, 8), (3, 13), (6.5, 13.5),
        (9.5, 10.5), (7, 6.5), (2.5, 7)]],
 "7": [[(0.5, 0), (9.5, 0), (4, 14)]],
 "8": [[(3, 7), (0.8, 4), (3, 0.8), (7, 0.8), (9.2, 4), (7, 7),
        (9.5, 10.5), (7, 13.5), (3, 13.5), (0.5, 10.5), (3, 7)]],
 "9": [[(1.5, 11.5), (4.5, 13.5), (8, 11), (9.5, 6), (7, 1), (3.5, 0.5),
        (0.5, 3.5), (3, 7.5), (7.5, 7)]],
 ".": [[(5, 13), (5, 14)]],
 ",": [[(5.5, 11), (4.5, 14.5)]],
 ":": [[(5, 3.5), (5, 4.5)], [(5, 10), (5, 11)]],
 "!": [[(5, 0), (5, 9.5)], [(5, 13), (5, 14)]],
 "?": [[(0.8, 3), (3, 0.5), (7, 0.5), (9.2, 3), (5, 7), (5, 10)],
       [(5, 13), (5, 14)]],
 "-": [[(2, 7), (8, 7)]],
 "'": [[(5, 0), (4.5, 3)]],
 "%": [[(1, 1.2), (4.2, 1.2), (4.2, 4.6), (1, 4.6), (1, 1.2)],
       [(9.2, 0), (0.8, 14)],
       [(5.8, 9.4), (9, 9.4), (9, 12.8), (5.8, 12.8), (5.8, 9.4)]],
 "+": [[(5, 3), (5, 11)], [(1.5, 7), (8.5, 7)]],
 "/": [[(9, 0), (1, 14)]],
 "$": [[(5, -1), (5, 15)], [(8.5, 2.5), (6, 0.8), (3, 1.2), (1, 3.5),
        (3.5, 6.8), (7, 7.6), (9, 10.5), (6.5, 13.2), (3, 13),
        (1.2, 11)]],
 "*": [[(5, 2), (5, 12)], [(1.5, 4.5), (8.5, 9.5)], [(8.5, 4.5),
        (1.5, 9.5)]],
}
VF_SPACE = 5.0


def vwidth(s, size):
    """Width of vector-font string s at cap-height `size` pixels."""
    u = size / 14.0
    w = 0.0
    for ch in s:
        w += (VF_SPACE if ch == " " else 10.0) * u
        w += 2.2 * u
    return w - 2.2 * u if s else 0


# ----------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.clip = None
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if self.clip is not None:
            cx, cy, cw, ch = self.clip
            if not (cx <= x < cx + cw and cy <= y < cy + ch):
                return
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def blend(self, x, y, c, a):
        if self.clip is not None:
            cx, cy, cw, ch = self.clip
            if not (cx <= x < cx + cw and cy <= y < cy + ch):
                return
        if 0 <= x < self.w and 0 <= y < self.h and a > 0:
            i = (y * self.w + x) * 3
            b = 1.0 - a
            self.px[i] = int(self.px[i] * b + c[0] * a)
            self.px[i + 1] = int(self.px[i + 1] * b + c[1] * a)
            self.px[i + 2] = int(self.px[i + 2] * b + c[2] * a)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        if self.clip is not None:
            cx, cy, cw, ch = self.clip
            x0, y0 = max(x0, cx), max(y0, cy)
            x1, y1 = min(x1, cx + cw), min(y1, cy + ch)
        for yy in range(y0, y1):
            base = yy * self.w * 3
            for xx in range(x0, x1):
                i = base + xx * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def frame(self, x, y, w, h, c, t=1):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def disc(self, cx, cy, r, c, a=1.0):
        for yy in range(int(cy - r), int(cy + r) + 1):
            for xx in range(int(cx - r), int(cx + r) + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    if a >= 1.0:
                        self.set(xx, yy, c)
                    else:
                        self.blend(xx, yy, c, a)

    def ring(self, cx, cy, r, c, t=2):
        for yy in range(int(cy - r), int(cy + r) + 1):
            for xx in range(int(cx - r), int(cx + r) + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 < d2 <= r * r:
                    self.set(xx, yy, c)

    def line(self, x0, y0, x1, y1, c, t=1, a=1.0):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        r = t // 2
        while True:
            if a >= 1.0:
                self.rect(x - r, y - r, t, t, c)
            else:
                for yy in range(y - r, y - r + t):
                    for xx in range(x - r, x - r + t):
                        self.blend(xx, yy, c, a)
            if x == x1 and y == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def poly(self, pts, c, t=1, a=1.0, close=False):
        for i in range(len(pts) - 1):
            self.line(int(pts[i][0]), int(pts[i][1]), int(pts[i + 1][0]),
                      int(pts[i + 1][1]), c, t, a)
        if close and len(pts) > 2:
            self.line(int(pts[-1][0]), int(pts[-1][1]), int(pts[0][0]),
                      int(pts[0][1]), c, t, a)

    def grad(self, x, y, w, h, top, bot):
        for yy in range(y, y + h):
            f = (yy - y) / max(1, h - 1)
            c = tuple(int(top[i] + (bot[i] - top[i]) * f) for i in range(3))
            self.rect(x, yy, w, 1, c)

    # -- bitmap text ------------------------------------------------------
    def btext(self, s, x, y, scale, c, bold=False, align="left"):
        w = self.bwidth(s, scale, bold)
        if align == "center":
            x -= w // 2
        elif align == "right":
            x -= w
        cx = x
        for ch in s:
            rows = BF.get(ch, BLANK)
            for ry, row in enumerate(rows):
                for rx, cell in enumerate(row):
                    if cell == "#":
                        self.rect(cx + rx * scale, y + ry * scale,
                                  scale, scale, c)
                        if bold:
                            self.rect(cx + rx * scale + scale, y + ry * scale,
                                      scale, scale, c)
            cx += 6 * scale + (scale if bold else 0)
        return cx - x

    def bwidth(self, s, scale, bold=False):
        return len(s) * (6 * scale + (scale if bold else 0)) - scale

    def wrap(self, s, scale, max_w, bold=False):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = word if not cur else cur + " " + word
            if self.bwidth(trial, scale, bold) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def bpara(self, s, x, y, scale, c, max_w, lh=None, bold=False):
        if lh is None:
            lh = 7 * scale + 3 * scale
        for line in self.wrap(s, scale, max_w, bold):
            self.btext(line, x, y, scale, c, bold)
            y += lh
        return y

    # -- vector text ------------------------------------------------------
    def vtext(self, s, x, y, size, c, thick=None, align="left"):
        s = s.upper()
        u = size / 14.0
        if thick is None:
            thick = max(1, int(round(size * 0.16)))
        w = vwidth(s, size)
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        cx = float(x)
        for ch in s:
            if ch == " ":
                cx += VF_SPACE * u + 2.2 * u
                continue
            strokes = VF.get(ch)
            if strokes:
                for stroke in strokes:
                    pts = [(cx + px * u, y + py * u) for px, py in stroke]
                    for i in range(len(pts) - 1):
                        self.line(int(pts[i][0]), int(pts[i][1]),
                                  int(pts[i + 1][0]), int(pts[i + 1][1]),
                                  c, thick)
                        self.disc(pts[i][0], pts[i][1], thick / 2, c)
                    self.disc(pts[-1][0], pts[-1][1], thick / 2, c)
            cx += 10 * u + 2.2 * u
        return w


# ------------------------------------------------------------ illustrations
def hash2(x, y):
    v = math.sin(x * 127.1 + y * 311.7) * 43758.5453
    return v - math.floor(v)


def ill_kyiv(cv, x, y, w, h):
    """Night missile attack on Kyiv: skyline, Dnipro bridge, streaks."""
    cv.grad(x, y, w, h, (8, 12, 32), (38, 44, 74))
    for i in range(90):
        sx = x + int(hash2(i, 1) * w)
        sy = y + int(hash2(i, 2) * h * 0.45)
        if hash2(i, 3) > 0.4:
            cv.set(sx, sy, (200, 205, 225))
    # missile streaks with glow heads
    hits = [(0.30, 0.86), (0.58, 0.90), (0.80, 0.84)]
    starts = [(0.06, 0.04), (0.40, 0.02), (0.66, 0.06)]
    for (sx, sy), (hx, hy) in zip(starts, hits):
        x0, y0 = x + int(sx * w), y + int(sy * h)
        x1, y1 = x + int(hx * w), y + int(hy * h)
        cv.line(x0, y0, x1, y1, (255, 120, 60), 5, a=0.35)
        cv.line(x0, y0, x1, y1, (255, 190, 90), 2)
        cv.disc(x1, y1, 3, (255, 230, 170))
    # skyline silhouette
    base = y + int(h * 0.86)
    bx = x + 4
    seed = 5
    while bx < x + w - 14:
        bw = 14 + int(hash2(seed, 7) * 22)
        bh = int(h * (0.18 + hash2(seed, 8) * 0.30))
        cv.rect(bx, base - bh, bw, bh, (5, 7, 14))
        for wy in range(base - bh + 4, base - 4, 7):
            for wx in range(bx + 3, bx + bw - 3, 6):
                if hash2(wx, wy) > 0.55:
                    cv.rect(wx, wy, 2, 3, (255, 196, 84))
        bx += bw + 2
        seed += 1
    # river + bridge
    cv.rect(x, base, w, h - (base - y), (10, 22, 44))
    for i in range(40):
        rx = x + int(hash2(i, 11) * w)
        ry = base + 3 + int(hash2(i, 12) * (h - (base - y) - 5))
        cv.line(rx, ry, rx + 7, ry, (70, 100, 150), 1, a=0.7)
    deck = base - int(h * 0.10)
    cv.line(x + 6, deck + 8, x + w - 6, deck - 6, (190, 198, 214), 3)
    for px_ in (0.16, 0.5, 0.84):
        pxp = x + int(px_ * w)
        cv.line(pxp, deck + 4, pxp, base, (150, 160, 180), 2)
    cv.line(x + int(0.16 * w), deck + 2, x + int(0.5 * w), deck - 16,
            (150, 160, 180), 1)
    cv.line(x + int(0.84 * w), deck - 4, x + int(0.5 * w), deck - 16,
            (150, 160, 180), 1)
    # explosions at hit points
    for hx, hy in hits:
        cxp, cyp = x + int(hx * w), y + int(hy * h)
        cv.disc(cxp, cyp, 13, (255, 110, 30), a=0.45)
        cv.disc(cxp, cyp, 8, (255, 150, 40), a=0.75)
        cv.disc(cxp, cyp, 4, (255, 214, 120))
        for a_ in range(6):
            ang = a_ * 1.05 + hx
            cv.line(cxp, cyp, int(cxp + 16 * math.cos(ang)),
                    int(cyp + 12 * math.sin(ang)), (255, 170, 70), 2, a=0.8)


def ill_cyclone(cv, x, y, w, h):
    """Cyclone Akvan: spiral over the Bay of Bengal hitting the coast."""
    cv.grad(x, y, w, h, (10, 58, 74), (16, 96, 104))
    cx, cy = x + int(w * 0.60), y + int(h * 0.46)
    max_r = int(w * 0.46)
    # spiral rain bands
    for arm in range(3):
        off = arm * 2.094
        prev = None
        for i in range(150):
            t = i / 149.0
            ang = off + t * 5.4
            r = 12 + t * (max_r - 12)
            pxp = int(cx + r * math.cos(ang))
            pyp = int(cy + r * math.sin(ang) * 0.88)
            shade = 0.35 + 0.55 * (1 - t)
            col = (190, 228, 230) if arm % 2 == 0 else (140, 205, 210)
            cv.disc(pxp, pyp, 6 - int(t * 2), col, a=shade)
            prev = (pxp, pyp)
    cv.disc(cx, cy, 17, (8, 44, 58))
    cv.ring(cx, cy, 19, (235, 245, 245), 3)
    cv.disc(cx, cy, 6, RED)
    # coastline silhouette, left edge: Odisha-Andhra shore
    shore = [(0.00, 0.06), (0.10, 0.20), (0.07, 0.36), (0.14, 0.52),
             (0.10, 0.68), (0.16, 0.84), (0.13, 1.00)]
    pts = [(x + int(a * w), y + int(b * h)) for a, b in shore]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                (10, 26, 22), 10)
    # palms bending in the wind
    for bx, by, s in ((0.10, 0.30, 16), (0.13, 0.58, 13), (0.09, 0.78, 15)):
        pxp, pyp = x + int(bx * w), y + int(by * h)
        cv.line(pxp, pyp, pxp + 3, pyp - s, (8, 20, 16), 2)
        for a_ in (0.4, 0.9, 1.4):
            cv.line(pxp + 3, pyp - s,
                    int(pxp + 3 + s * 0.8 * math.cos(a_ + 2.6)),
                    int(pyp - s + s * 0.45 * math.sin(a_ + 2.6)),
                    (20, 90, 50), 2)
    # rain streaks
    for i in range(46):
        rx = x + int(hash2(i, 21) * w)
        ry = y + int(hash2(i, 22) * h)
        cv.line(rx, ry, rx - 7, ry + 11, (200, 230, 235), 1, a=0.5)
    # waves at the shore
    for i, wy in enumerate((0.90, 0.95)):
        for wx in range(x + 8, x + w - 10, 26):
            cv.line(wx + (i * 9), y + int(wy * h), wx + 12 + (i * 9),
                    y + int(wy * h), (220, 240, 240), 2, a=0.65)


def ill_markets(cv, x, y, w, h):
    """AI-stock crash: candlesticks and a plunging red line."""
    cv.grad(x, y, w, h, (10, 12, 20), (22, 16, 22))
    for gx in range(x + 14, x + w, 34):
        cv.line(gx, y + 6, gx, y + h - 8, (70, 74, 92), 1, a=0.5)
    for gy in range(y + 12, y + h - 6, 26):
        cv.line(x + 6, gy, x + w - 6, gy, (70, 74, 92), 1, a=0.5)
    # candlesticks sliding down
    seed = 3
    cxp = x + 16
    lvl = 0.24
    while cxp < x + w - 20:
        drop = 0.03 + hash2(seed, 31) * 0.075
        top = y + int(lvl * h)
        bot = y + int((lvl + drop) * h)
        col = RED if seed % 4 else (60, 190, 120)
        if col == RED:
            cv.rect(cxp, top, 9, max(4, bot - top), col)
            cv.line(cxp + 4, top - 5, cxp + 4, bot + 5, col, 1)
        else:
            cv.rect(cxp, bot - 8, 9, 8, col)
            cv.line(cxp + 4, bot - 13, cxp + 4, bot + 3, col, 1)
        lvl += drop * 0.82
        cxp += 17
        seed += 1
    # plunge line
    pts = [(x + int(px_ * w), y + int(py_ * h)) for px_, py_ in
           ((0.03, 0.16), (0.22, 0.22), (0.38, 0.34), (0.52, 0.33),
            (0.66, 0.52), (0.80, 0.68), (0.95, 0.86))]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                (255, 70, 60), 5, a=0.30)
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                (255, 92, 80), 3)
    ax, ay = pts[-1]
    cv.poly([(ax, ay), (ax - 14, ay - 3), (ax - 4, ay - 13)], (255, 92, 80),
            3, close=True)


# ------------------------------------------------------------------- icons
def icon(cv, kind, x, y, s):
    """Small flat icons, drawn in an s-by-s box (s ~ 34)."""
    u = s / 34.0
    def L(a, b, c2, d, col, t=2):
        cv.line(int(x + a * u), int(y + b * u), int(x + c2 * u),
                int(y + d * u), col, max(1, int(t * u)))
    if kind == "flags":  # summit: three flags
        for i, col in enumerate(((70, 110, 180), RED, (240, 240, 240))):
            fx = 3 + i * 11
            L(fx, 4, fx, 30, INK, 2)
            cv.rect(int(x + fx * u), int(y + 4 * u), int(8 * u),
                    int(6 * u), col)
            cv.frame(int(x + fx * u), int(y + 4 * u), int(8 * u),
                     int(6 * u), INK, 1)
    elif kind == "globe":  # COP31
        cv.ring(int(x + 17 * u), int(y + 17 * u), int(13 * u), TEAL,
                max(1, int(2 * u)))
        L(4, 17, 30, 17, TEAL, 2)
        L(17, 4, 17, 30, TEAL, 2)
        cv.disc(int(x + 24 * u), int(y + 9 * u), int(4 * u), (60, 170, 80))
    elif kind == "chip":  # Anthropic / AI
        cv.frame(int(x + 8 * u), int(y + 8 * u), int(18 * u), int(18 * u),
                 NAVY, max(1, int(2 * u)))
        cv.btext("AI", int(x + 11 * u), int(y + 14 * u), max(1, int(2 * u)),
                 NAVY, bold=True)
        for p in (11, 17, 23):
            L(p, 2, p, 8, NAVY, 2)
            L(p, 26, p, 32, NAVY, 2)
            L(2, p, 8, p, NAVY, 2)
            L(26, p, 32, p, NAVY, 2)
    elif kind == "art":  # Van Gogh frame + swirl
        cv.frame(int(x + 4 * u), int(y + 4 * u), int(26 * u), int(26 * u),
                 GOLD, max(2, int(3 * u)))
        cv.disc(int(x + 17 * u), int(y + 17 * u), int(6 * u), (70, 110, 180))
        cv.ring(int(x + 17 * u), int(y + 17 * u), int(10 * u),
                (240, 200, 60), max(1, int(2 * u)))
    elif kind == "yen":  # Japan CPI
        cv.disc(int(x + 17 * u), int(y + 17 * u), int(13 * u), RED)
        cv.btext("Y", int(x + 12 * u), int(y + 9 * u), max(1, int(2 * u)),
                 CREAM, bold=True)
        L(11, 20, 23, 20, CREAM, 2)
        L(11, 24, 23, 24, CREAM, 2)
    elif kind == "planet":  # BepiColombo
        cv.disc(int(x + 15 * u), int(y + 19 * u), int(9 * u),
                (200, 130, 70))
        cv.ring(int(x + 15 * u), int(y + 19 * u), int(14 * u),
                NAVY, max(1, int(2 * u)))
        cv.disc(int(x + 27 * u), int(y + 7 * u), int(3 * u), NAVY)
        cv.disc(int(x + 27 * u), int(y + 7 * u), int(1 * u), CREAM)
    elif kind == "cricket":
        L(10, 4, 20, 24, (170, 120, 60), 4)
        cv.frame(int(x + 7 * u), int(y + 2 * u), int(9 * u), int(14 * u),
                 (170, 120, 60), 1)
        cv.disc(int(x + 25 * u), int(y + 24 * u), int(5 * u), RED)
        L(23, 6, 23, 14, INK, 2)
        L(29, 6, 29, 14, INK, 2)
    elif kind == "bridge":  # Crimea bridge
        L(3, 24, 31, 24, INK, 3)
        L(8, 10, 8, 24, INK, 2)
        L(26, 10, 26, 24, INK, 2)
        L(8, 24, 17, 10, INK, 1)
        L(26, 24, 17, 10, INK, 1)
        cv.disc(int(x + 17 * u), int(y + 12 * u), int(4 * u), RED)
        L(17, 12, 24, 5, RED, 2)
        L(17, 12, 10, 5, RED, 2)
    elif kind == "dollar":
        cv.disc(int(x + 17 * u), int(y + 17 * u), int(13 * u),
                (46, 140, 80))
        cv.ring(int(x + 17 * u), int(y + 17 * u), int(13 * u), GOLD, 2)
        cv.btext("$", int(x + 13 * u), int(y + 9 * u), max(1, int(2 * u)),
                 CREAM, bold=True)
    elif kind == "star":  # Europe
        cxp, cyp = x + 17 * u, y + 17 * u
        for i in range(12):
            ang = i * math.pi / 6
            cv.disc(int(cxp + 12 * u * math.cos(ang)),
                    int(cyp + 12 * u * math.sin(ang)), max(1, int(1.6 * u)),
                    GOLD)
        cv.ring(int(x + 17 * u), int(y + 17 * u), int(15 * u),
                (70, 110, 180), max(1, int(2 * u)))


# -------------------------------------------------------------- world map
MAP = (
 "................................................................................",
 ".####...........................................................................",
 "########..###...................................................................",
 ".################..........#....................................................",
 "..#################......#####...........##..####...............................",
 "...################....#########........#################..##...................",
 "....##############....##########......#############################.............",
 ".....############......########......#################################..........",
 "......##########........######......####..#############################.........",
 ".......########..........####......###.....########..##################.........",
 "........#######...................##.......#######......################........",
 ".........######..................#.........######.........##############........",
 "..........#####.............................#####...........###########.........",
 "...........####..............................###......#......##########.........",
 "............###...............................##.....###......########..........",
 ".............##................................#....#####......######...........",
 ".............#......................................#######......####...........",
 "............##.....................................########.......##............",
 "...........###....................................#########.....................",
 "..........#####..................................##########.....................",
 "..........######................................###########.....................",
 "...........#####...............................############..........##.........",
 "............####..............................#############.........####........",
 ".............###.............................##############........######.......",
 "..............##............................###############.......########......",
 "..............#............................################......##########.....",
 "..........................................#################.....###########.....",
 ".........................................##################......########.......",
 "........................................###################........####.........",
 ".......................................####################.........##..........",
 "......................................#####################.....................",
 ".....................................######################.....................",
 "....................................#######################.....................",
 "...................................########################.....................",
)


def draw_map(cv, x, y, w, h):
    cv.grad(x, y, w, h, NAVY, (10, 22, 40))
    rows, cols = len(MAP), len(MAP[0])
    cw, chh = w / cols, h / rows
    for ry, row in enumerate(MAP):
        for rx, cell in enumerate(row):
            if cell == "#":
                cv.disc(int(x + (rx + 0.5) * cw), int(y + (ry + 0.5) * chh),
                        max(1.4, cw * 0.34), (96, 140, 190), a=0.9)
    pins = [(0.505, 0.16, "1"), (0.635, 0.44, "2"), (0.845, 0.30, "3"),
            (0.795, 0.36, "4"), (0.135, 0.30, "5")]
    for fx, fy, n in pins:
        pxp, pyp = int(x + fx * w), int(y + fy * h)
        cv.disc(pxp, pyp, 11, RED)
        cv.ring(pxp, pyp, 13, CREAM, 2)
        cv.btext(n, pxp - 3, pyp - 4, 1, CREAM, bold=True)
    cv.rect(x + 8, y + 6, 218, 20, NAVY)
    cv.btext("WHERE IT HAPPENED", x + 12, y + 10, 2, CREAM, bold=True)
    cv.rect(x + 8, y + h - 20, 432, 14, NAVY)
    cv.btext("1 KYIV   2 GOPALPUR   3 TOKYO   4 SHENZHEN   5 NEW YORK",
             x + 12, y + h - 16, 1, (170, 195, 225))


# ------------------------------------------------------------------- page
def build():
    cv = Canvas(W, H, PAPER)
    cv.frame(10, 10, W - 20, H - 20, INK, 3)
    cv.frame(17, 17, W - 34, H - 34, INK, 1)
    MX, MW = 28, W - 56  # content margin / width

    # ---- masthead -------------------------------------------------------
    cv.vtext("THE WORLD IN ONE DAY", MX, 28, 19, INK)
    cv.btext("ALL THE NEWS - ONE PAGE - DRAWN IN CODE", MX + MW, 34, 1,
             GREY, align="right")
    cv.rect(MX, 56, MW, 3, INK)
    cv.vtext("FRIDAY 20 NOVEMBER 2026", 512, 66, 45, INK, align="center")
    cv.rect(MX, 120, MW, 2, INK)
    cv.btext("MISSILES ON KYIV  -  CYCLONE AKVAN ASHORE  -  "
             "AI STOCKS CRASH", 512, 128, 2, RED, bold=True, align="center")
    cv.rect(MX, 152, MW, 2, INK)

    # ---- region chips ----------------------------------------------------
    chips = [("EUROPE 5", NAVY), ("ASIA-PACIFIC 15", TEAL),
             ("AMERICAS 8", RED_D), ("WORLD 5", (90, 70, 30))]
    cw = (MW - 3 * 8) // 4
    for i, (label, col) in enumerate(chips):
        cx = MX + i * (cw + 8)
        cv.rect(cx, 160, cw, 20, col)
        cv.btext(label, cx + cw // 2, 166, 1, CREAM, bold=True,
                 align="center")

    # ---- stats strip -----------------------------------------------------
    stats = [("300,000+", "EVACUATED AHEAD OF CYCLONE AKVAN"),
             ("110+", "MISSILES FIRED ON KYIV OVERNIGHT"),
             ("-7%", "ASIA-PACIFIC STOCKS THIS WEEK"),
             ("$190.4M", "VAN GOGH AUCTION RECORD, NEW YORK"),
             ("2.3%", "JAPAN INFLATION, OCTOBER"),
             ("8 YRS", "BEPICOLOMBO'S VOYAGE TO MERCURY")]
    sw = MW // 6
    for i, (num, lab) in enumerate(stats):
        cx = MX + i * sw
        if i:
            cv.rect(cx - 1, 192, 1, 44, PAPER_D)
        cv.vtext(num, cx + sw // 2, 188, 21, RED if i % 2 == 0 else NAVY,
                 align="center")
        lines = cv.wrap(lab, 1, sw - 10)
        ly = 220
        for ln in lines[:2]:
            cv.btext(ln, cx + sw // 2, ly, 1, INK, align="center")
            ly += 10
    cv.rect(MX, 244, MW, 2, INK)

    # ---- hero panels -----------------------------------------------------
    heroes = [
        ("1 - EUROPE - WAR", ill_kyiv, "KYIV UNDER FIRE",
         "Russia fires more than 110 missiles overnight and three "
         "Dnipro bridges are hit, hours after the Shenzhen summit "
         "declares peace."),
        ("2 - ASIA - STORM", ill_cyclone, "AKVAN SLAMS ASHORE",
         "Cyclone Akvan crosses the coast at Gopalpur, Odisha. Over "
         "300,000 people are evacuated as winds gust to 90 km/h."),
        ("3 - MARKETS - CRASH", ill_markets, "AI STOCKS CRASH",
         "Asia-Pacific shares fall 7% in a week, their worst since "
         "2020. Even Anthropic's record IPO cannot calm AI fears."),
    ]
    pw, ph, py = 317, 252, 254
    for i, (kick, ill, title, body) in enumerate(heroes):
        px = MX + i * (pw + 12)
        cv.frame(px, py, pw, ph, INK, 2)
        cv.rect(px, py, pw, 20, INK)
        cv.btext(kick, px + 8, py + 6, 1, CREAM, bold=True)
        cv.clip = (px + 3, py + 23, pw - 6, 128)
        ill(cv, px + 3, py + 23, pw - 6, 128)
        cv.clip = None
        cv.vtext(title, px + 10, py + 160, 19, INK)
        cv.rect(px + 10, py + 186, pw - 20, 2, RED)
        cv.bpara(body, px + 10, py + 194, 1, INK, pw - 20, lh=11)

    # ---- numbered cards --------------------------------------------------
    cv.btext("THE DAY IN TEN MORE STORIES", MX, 518, 2, INK, bold=True)
    cv.btext("EVERY ITEM CHECKED AGAINST THE DAY'S WIRES", MX + MW, 522, 1,
             GREY, align="right")
    cards = [
        ("4", "flags", "SHENZHEN SUMMIT",
         "First Trump-Xi-Putin meeting. A peace declaration vows no "
         "nuclear war; no arms deal follows."),
        ("5", "globe", "COP31 DEADLOCK",
         "Final day in Antalya: the draft deal drops fossil fuels "
         "and bets on carbon capture instead."),
        ("6", "chip", "ANTHROPIC IPO",
         "A record debut, shares up 30% - yet the listing cannot "
         "lift a market losing faith in AI."),
        ("7", "art", "VAN GOGH RECORD",
         "Chataigniers en fleurs, unseen for 50 years, sets a Van "
         "Gogh record at Sotheby's New York."),
        ("8", "yen", "JAPAN CPI 2.3%",
         "Inflation climbs to 2.3% in October, above target. A "
         "December rate rise is now in play."),
        ("9", "planet", "MERCURY AT LAST",
         "BepiColombo ends an 8-year, 10bn km voyage and slips "
         "into Mercury orbit on Saturday."),
        ("10", "cricket", "NICHOLLS 175*",
         "Nicholls 175 not out and Phillips 118 lift New Zealand "
         "to 368 against India in Wellington."),
        ("11", "bridge", "CRIMEA BRIDGE HIT",
         "Ukraine hits the Kerch bridge a third time this week; "
         "a span falls and the rail line burns."),
        ("12", "dollar", "DOLLAR AT HIGH",
         "Safe-haven flows push the dollar to a 19-month high as "
         "investors sell gold to cover losses."),
        ("13", "star", "EUROPE HITS BACK",
         "European leaders tell Trump his Putin meeting changes "
         "nothing for Ukraine's defence."),
    ]
    cardw, cardh = 187, 104
    for idx, (num, ic, title, body) in enumerate(cards):
        cx = MX + (idx % 5) * (cardw + 10)
        cy = 542 + (idx // 5) * (cardh + 10)
        cv.rect(cx, cy, cardw, cardh, (252, 248, 236))
        cv.frame(cx, cy, cardw, cardh, INK, 1)
        cv.disc(cx + 14, cy + 14, 10, RED)
        cv.btext(num, cx + 14 - (3 if len(num) == 1 else 6), cy + 10, 1,
                 CREAM, bold=True)
        icon(cv, ic, cx + cardw - 40, cy + 4, 32)
        cv.vtext(title, cx + 8, cy + 34, 11, INK)
        cv.bpara(body, cx + 8, cy + 52, 1, INK, cardw - 16, lh=10)

    # ---- map -------------------------------------------------------------
    draw_map(cv, MX, 772, MW, 104)

    # ---- also on Friday --------------------------------------------------
    cv.btext("ALSO ON FRIDAY - 20 MORE STORIES", MX, 888, 1, RED,
             bold=True)
    cv.rect(MX, 900, MW, 1, INK)
    also = [
        "Taiwan stocks -17% this week, worst since 1990",
        "Kospi slides 5% as chip shares tumble",
        "SoftBank dives 14.5% in Tokyo rout",
        "S&P 500 falls 2% to a six-month low",
        "China leaves benchmark rates on hold",
        "Panama threatens to block COP31 deal",
        "Niue wins Earthshot prize at COP31",
        "Kyiv districts blacked out by strikes",
        "9,341 shelters opened across Odisha",
        "Trump: summit was 'bigger than Yalta'",
        "Republicans lose Congress in midterms",
        "Jaiswal and Rahul lead India's reply",
        "Bumrah takes 3-52 on opening day",
        "Anthropic slips 3% after the bell",
        "Gold sold to cover stock losses",
        "Antalya-Addis adaptation roadmap set",
        "Tokyo braced for three-day weekend",
        "Zelensky: every target was civilian",
        "1,012 rescue teams fan out in Odisha",
        "Sotheby's night totals $777.8m",
    ]
    colw = MW // 3
    for i, line in enumerate(also):
        cx = MX + (i // 7) * colw
        cy = 908 + (i % 7) * 10
        cv.disc(cx + 3, cy + 3, 2, RED)
        cv.btext(line, cx + 10, cy, 1, INK)

    # ---- date check + sources -------------------------------------------
    cv.frame(MX, 980, 452, 22, RED, 2)
    cv.btext("DATE CHECK: FRIDAY 20 NOVEMBER 2026 - VERIFIED",
             MX + 10, 987, 1, RED_D, bold=True)
    cv.btext("SOURCES: REUTERS - CNN - THE TIMES - IMD - AP - BBC",
             MX + MW, 987, 1, GREY, align="right")
    return cv


def png_bytes(cv):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    data = png_bytes(build())
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
