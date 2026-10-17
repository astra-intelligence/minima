#!/usr/bin/env python3
"""Generate a 1200x630 OG image for jekyll/minima demo site.

Pillow-only, byte-reproducible. Clean card matching Minima theme:
white ground, #828282 minima header grey accent, dark title,
feature pills + domain chip, subtle Jekyll gem motif.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (255, 255, 255)          # white ground
GREY = (130, 130, 130)        # #828282 minima header grey
DARK = (34, 34, 34)           # #222222 minima text
WHITE = (255, 255, 255)

FONT_DIR = os.environ.get("FONT_DIR", "/usr/share/fonts/truetype/dejavu")


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    p = os.path.join(FONT_DIR, name)
    if not os.path.exists(p):
        p = os.path.join(FONT_DIR, "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf")
    return ImageFont.truetype(p, size)


def rounded(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # top accent bar (minima header grey)
    d.rectangle([0, 0, W, 10], fill=GREY)

    f_title = font(76, bold=True)
    f_sub = font(34)
    f_pill = font(30, bold=True)
    f_domain = font(30, bold=True)

    # title + subtitle
    d.text((70, 70), "Minima", font=f_title, fill=DARK)
    d.text((70, 180), "A beautiful, minimal Jekyll theme", font=f_sub, fill=GREY)
    d.text((70, 222), "for your personal site", font=f_sub, fill=GREY)

    # separator
    d.line([70, 300, W - 70, 300], fill=(225, 228, 232), width=2)

    # feature pills
    pills = ["Responsive layout", "Built-in search", "GitHub Pages ready", "Easy customization"]
    x = 70
    y = 340
    for p_ in pills:
        w = d.textlength(p_, font=f_pill) + 44
        if x + w > 1130:  # wrap to next row before overflow
            x = 70
            y += 82
        rounded(d, [x, y, x + w, y + 62], 31, GREY)
        d.text((x + 22, y + 13), p_, font=f_pill, fill=WHITE)
        x += w + 18

    # footer domain chip
    d.rounded_rectangle([70, H - 92, 560, H - 44], 24, fill=DARK)
    d.text((108, H - 84), "jekyll.github.io/minima", font=f_domain, fill=WHITE)

    # subtle Jekyll gem motif in the top-right
    cx, cy = W - 200, 150
    pts = [(cx, cy - 60), (cx + 52, cy - 30), (cx + 52, cy + 30),
           (cx, cy + 60), (cx - 52, cy + 30), (cx - 52, cy - 30)]
    d.polygon(pts, outline=GREY, width=5)
    d.line([cx, cy - 60, cx, cy + 60], fill=GREY, width=3)
    d.line([cx - 52, cy - 30, cx + 52, cy - 30], fill=GREY, width=3)
    d.line([cx - 52, cy + 30, cx + 52, cy + 30], fill=GREY, width=3)

    out = "og-image.png"
    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
