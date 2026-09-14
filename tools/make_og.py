"""허브 공유 이미지(og.png 1200x630)와 PNG 파비콘을 그린다.

실행: py -3 _hub/tools/make_og.py
문구·색을 바꾸면 index.html의 og:description·og:image ?v= 도 같이 올린다.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_R = r"C:\Windows\Fonts\malgun.ttf"
FONT_B = r"C:\Windows\Fonts\malgunbd.ttf"

PAPER = (246, 245, 240)
INK = (28, 31, 36)
MUTED = (95, 101, 112)
FAINT = (141, 147, 156)
LINE = (227, 225, 217)
GREEN = (5, 150, 105)
BLUE = (65, 107, 255)
PURPLE = (126, 68, 251)
ORANGE = (234, 88, 12)
TEAL = (13, 148, 136)

DESC_LINES = ["교육 서비스를 기획하며 직접 만든", "사내 도구 · 서비스 목업 · 공개 페이지 모음"]
BENCHES = [("사내 도구", ORANGE), ("서비스 Mock-up", BLUE), ("외부 공개 서비스", TEAL)]


def font(path, size, s):
    return ImageFont.truetype(path, int(size * s))


def flask_outline():
    return [(45, 8), (45, 44), (14, 108), (13, 114), (16, 120), (23, 124),
            (89, 124), (96, 120), (99, 114), (98, 108), (67, 44), (67, 8)]


def liquid_poly():
    return [(25.6, 84), (86.4, 84), (98, 108), (99, 114), (96, 120), (89, 124),
            (23, 124), (16, 120), (13, 114), (14, 108)]


def og(path):
    S = 2
    W, H = 1200 * S, 630 * S
    img = Image.new("RGB", (W, H), PAPER)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    step = 24 * S
    for x in range(0, W, step):
        g.line([(x, 0), (x, H)], fill=INK + (13,), width=S)
    for y in range(0, H, step):
        g.line([(0, y), (W, y)], fill=INK + (13,), width=S)
    img.paste(grid, (0, 0), grid)

    d = ImageDraw.Draw(img, "RGBA")
    L = 88 * S

    # eyebrow
    fb = font(FONT_B, 26, S)
    fr = font(FONT_R, 26, S)
    d.text((L, 120 * S), "OLIVIA LAB", font=fb, fill=INK)
    w = d.textlength("OLIVIA LAB", font=fb)
    d.text((L + w, 120 * S), "  ·  교육 AI 기획 실험 노트", font=fr, fill=MUTED)

    # title
    d.text((L, 168 * S), "올립의 실험실", font=font(FONT_B, 104, S), fill=INK)

    # description
    fd = font(FONT_R, 36, S)
    for i, line in enumerate(DESC_LINES):
        d.text((L, (318 + i * 52) * S), line, font=fd, fill=MUTED)

    # bench chips
    fc = font(FONT_B, 24, S)
    x = L
    y = 458 * S
    for label, color in BENCHES:
        tw = d.textlength(label, font=fc)
        cw = int(tw + 70 * S)
        ch = 52 * S
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=ch // 2, fill=(255, 255, 255), outline=LINE, width=2 * S)
        cx, cy = x + 26 * S, y + ch // 2
        r = 7 * S
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        d.text((x + 44 * S, y + 11 * S), label, font=fc, fill=INK)
        x += cw + 14 * S

    # bottom rule + url
    d.rectangle([L, 552 * S, W - L, 552 * S + 3 * S], fill=INK)
    d.text((L, 572 * S), "obkim-lgtm.github.io/hub", font=font(FONT_R, 22, S), fill=FAINT)

    # flask (header SVG, scaled)
    k = 2.7 * S
    ox, oy = 842 * S, 150 * S
    P = lambda pts: [(ox + px * k, oy + py * k) for px, py in pts]
    d.polygon(P(liquid_poly()), fill=GREEN + (41,))
    d.line(P([(25.6, 84), (86.4, 84)]), fill=GREEN, width=int(2.5 * k))
    for (bx, by, br, col) in [(50, 100, 4.5, BLUE), (62, 70, 3.4, PURPLE), (55, 38, 2.8, ORANGE), (60, 12, 2.2, BLUE), (52, -8, 1.8, PURPLE)]:
        cx, cy, rr = ox + bx * k, oy + by * k, br * k
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    d.line(P(flask_outline()), fill=INK, width=int(3 * k), joint="curve")
    d.line(P([(40, 8), (72, 8)]), fill=INK, width=int(3 * k))
    for (ax, ay, bx2, by2) in [(50, 22, 58, 22), (50, 34, 62, 34)]:
        d.line(P([(ax, ay), (bx2, by2)]), fill=INK + (90,), width=int(2 * k))
    for (ax, ay) in [(40, 8), (72, 8)]:
        cx, cy, rr = ox + ax * k, oy + ay * k, 1.5 * k
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=INK)

    img = img.resize((1200, 630), Image.LANCZOS)
    img.save(path, optimize=True)


def icon(size, path, background):
    """헤더 플라스크(viewBox -12 -2 136 136)를 정사각 아이콘으로."""
    S = 8
    W = size * S
    img = Image.new("RGBA", (W, W), PAPER + (255,) if background else (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    pad = 0.10 if background else 0.0
    k = W * (1 - 2 * pad) / 136
    off = W * pad
    P = lambda pts: [(off + (x + 12) * k, off + (y + 2) * k) for x, y in pts]
    d.polygon(P(liquid_poly()), fill=GREEN + (72,))
    d.line(P([(25.6, 84), (86.4, 84)]), fill=GREEN, width=max(1, int(5 * k)))
    for cx, cy, r, col in [(52, 64, 7, BLUE), (62, 102, 5.5, PURPLE)]:
        (x0, y0), (x1, y1) = P([(cx - r, cy - r), (cx + r, cy + r)])
        d.ellipse([x0, y0, x1, y1], fill=col + (217,))
    d.line(P(flask_outline()), fill=INK, width=max(1, int(7 * k)), joint="curve")
    d.line(P([(38, 8), (74, 8)]), fill=INK, width=max(1, int(7 * k)))
    for ax, ay in [(38, 8), (74, 8)]:
        (cx, cy), = P([(ax, ay)])
        rr = 3.5 * k
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=INK)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, optimize=True)


if __name__ == "__main__":
    og(os.path.join(HUB, "og.png"))
    icon(32, os.path.join(HUB, "favicon-lab-32.png"), background=False)
    icon(32, os.path.join(HUB, "favicon-32.png"), background=False)
    icon(180, os.path.join(HUB, "apple-touch-icon.png"), background=True)
    print("og.png · favicon-32.png · apple-touch-icon.png 생성")
