"""HTCP "moment" clip renderer.

Makes one 8 to 10 second vertical video (1080x1920, H.264, 30 fps, silent
stereo AAC, faststart) from one or two stock clips with a single short phrase
on an HTCP cream card, plus the site name at the bottom.

Usage:
  python3 moment.py --phrase "Reminder to switch your laundry." \
      --kind funny --out moment-2026-10-21.mp4 clipA.mp4 [clipB.mp4 ...]

--kind funny   -> kicker "QUICK NUDGE"
--kind support -> kicker "A LITTLE SUPPORT"

Rules baked in (Disa's):
- Never freezes or holds a frame. If the first clip is 8.6s or longer it is
  used alone, trimmed to 9s. Otherwise clips are joined with a 0.6s crossfade
  until the total reaches at least 8s, capped at 10s. If all given clips
  together are still under 8s, it exits with NOT RENDERED (pass more clips).
- Phrase: at most 70 characters and 4 wrapped lines, else NOT RENDERED.
- No em or en dashes allowed in the phrase.
Prints OK <duration> on success.
"""
import argparse, json, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
TEAL = (31, 95, 91); CREAM = (251, 248, 243); MUST = (242, 165, 65)
FONTS = "/usr/share/fonts/truetype/google-fonts/"


def font(name, size):
    for n in (name, "Poppins-Bold.ttf", "DejaVuSans-Bold.ttf"):
        for d in (FONTS, "/usr/share/fonts/truetype/dejavu/"):
            try:
                return ImageFont.truetype(d + n, size)
            except OSError:
                pass
    return ImageFont.load_default()


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", p], capture_output=True, text=True).stdout
    return float(out.strip())


def card(phrase, kicker, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fb, fk, fu = font("Poppins-Bold.ttf", 78), font("Poppins-Medium.ttf", 36), font("Poppins-Medium.ttf", 34)
    lines = textwrap.wrap(phrase, 18); lh = 96
    bw = 880; bh = 110 + len(lines) * lh + 40; x0 = (W - bw) // 2; y0 = 560
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=44, fill=CREAM + (238,))
    kw = d.textlength(kicker, font=fk)
    d.rounded_rectangle([x0 + 60, y0 + 52, x0 + 60 + kw + 44, y0 + 104], radius=26, fill=MUST)
    d.text((x0 + 82, y0 + 56), kicker, font=fk, fill=TEAL)
    y = y0 + 130
    for l in lines:
        d.text((x0 + 60, y), l, font=fb, fill=TEAL); y += lh
    u = "howtocompleteaproject.com"; tw = d.textlength(u, font=fu)
    d.rounded_rectangle([(W - tw) // 2 - 28, 1640, (W + tw) // 2 + 28, 1704], radius=32, fill=CREAM + (225,))
    d.text(((W - tw) // 2, 1648), u, font=fu, fill=TEAL)
    im.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phrase", required=True)
    ap.add_argument("--kind", choices=["funny", "support"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("clips", nargs="+")
    a = ap.parse_args()
    ph = a.phrase.strip()
    if "—" in ph or "–" in ph:
        sys.exit("NOT RENDERED: phrase has a dash")
    if len(ph) > 70 or len(textwrap.wrap(ph, 18)) > 4:
        sys.exit("NOT RENDERED: phrase too long (max 70 characters, 4 lines)")

    XF = 0.6
    ds = [dur(c) for c in a.clips]
    use, total = [], 0.0
    if ds[0] >= 8.6:
        use, total = [(a.clips[0], 9.0)], 9.0
    else:
        for c, d in zip(a.clips, ds):
            add = d if not use else d - XF
            use.append((c, d)); total += add
            if total >= 8.0:
                break
        if total < 8.0:
            sys.exit(f"NOT RENDERED: clips only reach {total:.1f}s, pass another clip")
        if total > 10.0:  # trim the last clip so the result ends at 10s
            c, d = use[-1]; use[-1] = (c, d - (total - 10.0)); total = 10.0

    ov = a.out + ".overlay.png"
    card(ph, "QUICK NUDGE" if a.kind == "funny" else "A LITTLE SUPPORT", ov)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for c, _ in use:
        cmd += ["-i", c]
    n = len(use)
    cmd += ["-loop", "1", "-t", f"{total}", "-i", ov,
            "-f", "lavfi", "-t", f"{total}", "-i", "anullsrc=r=44100:cl=stereo"]
    fc = []
    for i, (_, d) in enumerate(use):
        fc.append(f"[{i}:v]trim=0:{d:.3f},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},fps=30,format=yuv420p[c{i}]")
    last, off = "c0", use[0][1]
    for i in range(1, n):
        fc.append(f"[{last}][c{i}]xfade=transition=fade:duration={XF}:offset={off - XF:.3f}[x{i}]")
        last = f"x{i}"; off += use[i][1] - XF
    fc.append(f"[{n}:v]format=rgba,fade=t=in:st=0.3:d=0.6:alpha=1[o]")
    fc.append(f"[{last}][o]overlay=0:0,format=yuv420p[out]")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[out]", "-map", f"{n + 1}:a",
            "-t", f"{total}", "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    subprocess.run(["rm", "-f", ov])
    print(f"OK {dur(a.out):.1f}")


if __name__ == "__main__":
    main()
