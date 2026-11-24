"""Builds the profile's SVG set (light + dark) from real repository data.
Concept: the profile is an edit timeline. Everything published between
2026-11-22 23:46 and 2026-11-24 22:13 sits on its tracks at the minute it
was committed; every commit that corrected something is marked in the one
accent colour."""
import os
from datetime import datetime, timedelta
from textpath import Glyphs
from data import COMMITS, T0, T1, PAPER_CLIPS, APP_CLIPS, FIXES, PAPERS, HJTK_VERSIONS, paper_fix_counts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0E0E0E", panel="#151515", lane="#1B1B1B", line="#2A2A2A", ink="#EDEBE6",
                 mid="#A3A09A", dim="#5E5C58", clip="#3A3936", clip2="#575550", lit="#D9D6CF",
                 litink="#111111", accent="#E44D2E"),
    "light": dict(bg="#F4F2EE", panel="#FFFFFF", lane="#ECE9E3", line="#DAD6CE", ink="#151515",
                  mid="#5F5C57", dim="#9E9A92", clip="#CFCBC3", clip2="#B5B0A6", lit="#2A2927",
                  litink="#F4F2EE", accent="#D2401F"),
}

W = 1200


def svg(w, h, body, g, css, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{g.defs_svg()}<style>{css}</style>{body}</svg>')


def dur(td):
    s = int(td.total_seconds())
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:00"


# ───────────────────────────── header timeline ─────────────────────────────
def header(theme):
    c = THEMES[theme]
    g = Glyphs("h")
    H = 588
    LX, RX = 132, W - 28            # timeline content span
    start = T0.replace(minute=0) - timedelta(minutes=30)
    end = T1.replace(minute=0) + timedelta(hours=1)
    span = (end - start).total_seconds()

    def X(t):
        return LX + (t - start).total_seconds() / span * (RX - LX)

    DUR = 9.0  # seconds of playhead sweep; then hold
    SWEEP = 0.78  # fraction of the loop spent sweeping

    def pct(x):
        return (x - LX) / (RX - LX) * SWEEP * 100

    b = [f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>']
    css = [f"""
.ph{{animation:sweep {DUR / SWEEP:.2f}s linear infinite}}
@keyframes sweep{{0%{{transform:translateX(0)}}{SWEEP * 100:.1f}%{{transform:translateX({RX - LX}px)}}100%{{transform:translateX({RX - LX}px)}}}}
@media (prefers-reduced-motion:reduce){{.ph{{animation:none;transform:translateX({RX - LX}px)}}.k{{animation:none!important;opacity:1!important}}}}
"""]
    kf = []

    def lightup(name, x):
        p = pct(x)
        kf.append(f"@keyframes {name}{{0%,{p:.2f}%{{opacity:0}}{min(p + 0.6, 99):.2f}%,96%{{opacity:1}}100%{{opacity:0}}}}"
                  f".{name}{{animation:{name} {DUR / SWEEP:.2f}s linear infinite}}")
        return f"k {name}"

    # ── chrome bar
    b.append(f'<rect x="0" y="0" width="{W}" height="36" fill="{c["panel"]}"/>'
             f'<rect x="0" y="36" width="{W}" height="1" fill="{c["line"]}"/>')
    b.append(g.text("SEQUENCE 01", 24, 23, "mono-m", 12, c["mid"], track=0.08))
    b.append(g.text("2026.11.22 — 11.24", 136, 23, "mono", 12, c["dim"], track=0.04))
    b.append(g.text("github.com/heok0308hth-glitch", W - 24, 23, "mono", 12, c["dim"], anchor="end", track=0.02))

    # ── monitor: name block
    b.append(g.text("허태혁", 44, 168, "sans-b", 96, c["ink"], track=-0.02))
    nw = g.width("허태혁", "sans-b", 96, -0.02)
    b.append(g.text("Taehyeok Heo", 48, 206, "sans-m", 22, c["mid"]))
    b.append(f'<rect x="{44 + nw + 22}" y="100" width="2" height="72" fill="{c["line"]}"/>')
    b.append(g.text("학생", 44 + nw + 46, 168, "sans-sb", 44, c["ink"]))

    # ── monitor: timecode readout (right)
    papers_n, apps_n = 16, 2
    rows = [("IN", T0.strftime("%m.%d  %H:%M")), ("OUT", T1.strftime("%m.%d  %H:%M")), ("DUR", dur(T1 - T0))]
    ry = 92
    for k, v in rows:
        b.append(g.text(k, W - 290, ry, "mono-m", 13, c["dim"], track=0.1))
        b.append(g.text(v, W - 36, ry, "mono", 22, c["ink"], anchor="end"))
        ry += 34
    stats = [(str(papers_n), "논문"), (str(apps_n), "앱"), (str(len(COMMITS)), "커밋"), (str(len(FIXES)), "고친 커밋")]
    sx = W - 290
    b.append(f'<rect x="{sx}" y="{ry - 12}" width="{W - 36 - sx}" height="1" fill="{c["line"]}"/>')
    sy = ry + 26
    colw = (W - 36 - sx) / 4
    for i, (n, lab) in enumerate(stats):
        col = c["accent"] if lab == "고친 커밋" else c["ink"]
        b.append(g.text(n, sx + i * colw, sy, "mono-m", 22, col))
        b.append(g.text(lab, sx + i * colw, sy + 22, "sans-m", 13, c["mid"]))

    # ── timeline panel
    TY = 262
    b.append(f'<rect x="0" y="{TY}" width="{W}" height="{H - TY}" fill="{c["panel"]}"/>'
             f'<rect x="0" y="{TY}" width="{W}" height="1" fill="{c["line"]}"/>')
    # ruler
    RY = TY + 18
    t = start.replace(minute=0)
    while t <= end:
        x = X(t)
        if LX - 1 <= x <= RX + 1:
            major = t.hour % 6 == 0
            hgt = 10 if major else 5
            b.append(f'<rect x="{x:.1f}" y="{RY + 22 - hgt}" width="1" height="{hgt}" fill="{c["dim"] if major else c["line"]}"/>')
            if major:
                lab = t.strftime("%m.%d") if t.hour == 0 else t.strftime("%H:00")
                b.append(g.text(lab, x + 4, RY + 8, "mono-m" if t.hour == 0 else "mono", 11,
                                c["ink"] if t.hour == 0 else c["dim"]))
        t += timedelta(hours=1)
    b.append(f'<rect x="{LX}" y="{RY + 22}" width="{RX - LX}" height="1" fill="{c["line"]}"/>')

    # tracks
    tracks = [("V3", "HJTK"), ("V2", "KoreanVoice"), ("V1", "논문 16편"), ("A1", "고친 것")]
    lane_y0 = RY + 36
    LH, GAP = 50, 8
    for i, (tag, name) in enumerate(tracks):
        y = lane_y0 + i * (LH + GAP)
        b.append(f'<rect x="{LX}" y="{y}" width="{RX - LX}" height="{LH}" fill="{c["lane"]}"/>')
        b.append(g.text(tag, 24, y + 27, "mono-m", 13, c["accent"] if tag == "A1" else c["dim"], track=0.06))
        b.append(g.text(name, 24, y + 43, "sans-sb", 14 if len(name) > 6 else 16, c["ink"]))

    def clips(items, row, label_fn, key):
        y = lane_y0 + row * (LH + GAP) + 8
        hgt = LH - 16
        for j, it in enumerate(items):
            x0 = X(it[0])
            x1 = X(items[j + 1][0]) if j + 1 < len(items) else X(T1) + 6
            x1 = max(x1 - 2, x0 + 5)
            w = x1 - x0
            label = label_fn(it)
            name = f"{key}{j}"
            cls = lightup(name, x0)
            b.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{hgt}" rx="2" fill="{c["clip"]}"/>')
            inner = [f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{hgt}" rx="2" fill="{c["lit"]}"/>']
            fits = g.width(label, "mono-m", 12) + 10 <= w
            if fits:
                b.append(g.text(label, x0 + 5, y + hgt / 2 + 4.5, "mono-m", 12, c["mid"]))
                inner.append(g.text(label, x0 + 5, y + hgt / 2 + 4.5, "mono-m", 12, c["litink"]))
            b.append(f'<g class="{cls}" opacity="0">' + "".join(inner) + "</g>")
            # in-point marker (accent when the clip itself is a repair release)
            col = c["accent"] if label in ("2.1.4",) else c["clip2"]
            b.append(f'<rect x="{x0:.1f}" y="{y}" width="{3 if col == c["accent"] else 1.5}" height="{hgt}" fill="{col}"/>')

    apps = sorted(APP_CLIPS, key=lambda a: a[0])
    hj = [a for a in apps if a[2] == "hjtk"]
    clips(hj, 0, lambda a: a[1], "a")
    kv = [a for a in apps if a[2] == "kv"]
    clips(kv, 1, lambda a: "KoreanVoice" if a[1] == "KoreanVoice" else "2.1.4", "v")
    clips(sorted(PAPER_CLIPS), 2, lambda p: p[1], "p")

    # A1: one peak per commit. Height ~ log of lines changed. Fixes in accent.
    import math
    ay = lane_y0 + 3 * (LH + GAP) + LH / 2
    b.append(f'<rect x="{LX}" y="{ay:.1f}" width="{RX - LX}" height="1" fill="{c["line"]}"/>')
    for k, cm in enumerate(COMMITS):
        x = X(cm["t"])
        n = cm["ins"] + cm["dele"]
        h = min(21, 3 + 2.6 * math.log10(1 + n) * 2)
        col = c["accent"] if cm["kind"] == "fix" else c["clip2"]
        wbar = 3 if cm["kind"] == "fix" else 2
        b.append(f'<rect x="{x - wbar / 2:.1f}" y="{ay - h:.1f}" width="{wbar}" height="{2 * h:.1f}" rx="1" fill="{col}"/>')

    # playhead
    py0, py1 = RY - 4, lane_y0 + 4 * (LH + GAP) - GAP
    b.append(f'<g class="ph"><rect x="{LX - 0.75}" y="{py0}" width="1.5" height="{py1 - py0}" fill="{c["accent"]}"/>'
             f'<path d="M{LX - 7} {py0 - 8}h14v6l-7 7l-7-7z" fill="{c["accent"]}"/></g>')

    css.append("".join(kf))
    title = "허태혁 — 학생. 2026년 11월 22일부터 24일까지 올린 논문 16편, 앱 2개, 커밋 74개를 편집 타임라인으로 표시"
    return svg(W, H, "".join(b), g, "".join(css), title)


if __name__ == "__main__":
    for th in THEMES:
        open(f"{OUT}/timeline-{th}.svg", "w").write(header(th))
    print("ok")


# ───────────────────────────── project strips ─────────────────────────────
def strip_frame(c, g, h, tag, name, lines, meta):
    b = [f'<rect width="{W}" height="{h}" fill="{c["panel"]}"/>',
         f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" fill="none" stroke="{c["line"]}"/>',
         f'<rect x="300" y="24" width="1" height="{h - 48}" fill="{c["line"]}"/>']
    code, word = tag.split(" · ")
    b.append(g.text(code, 32, 50, "mono-m", 13, c["dim"], track=0.08))
    b.append(g.text(word, 32 + g.width(code, "mono-m", 13, 0.08) + 10, 50, "sans-m", 13, c["dim"]))
    b.append(g.text(name, 32, 92, "sans-b", 30, c["ink"], track=-0.01))
    y = 128
    for ln in lines:
        b.append(g.text(ln, 32, y, "sans", 16, c["mid"]))
        y += 25
    b.append(g.text(meta, 32, h - 32, "mono", 12, c["dim"], track=0.02))
    return b


def strip_papers(theme):
    c = THEMES[theme]; g = Glyphs("p"); h = 340
    b = strip_frame(c, g, h, "V1 · 논문", "Research_paper",
                    ["단독 저자 논문 16편.", "PDF · 원고 · 재현 인증서."], "Python · Markdown · SAT/MILP")
    fx = paper_fix_counts()
    for k in ("05", "13", "15", "16"):  # 2026-11-24 22:13 commit: one fix each (subject line names none)
        fx[k] += 1
    x0, x1, base, top = 336, W - 40, h - 64, 44
    colw = (x1 - x0) / 16
    maxp = max(p[2] for p in PAPERS)
    for i, (num, field, pages, figs) in enumerate(PAPERS):
        x = x0 + i * colw + 4; w = colw - 8
        bh = (base - top - 30) * pages / maxp
        b.append(f'<rect x="{x:.1f}" y="{base - bh:.1f}" width="{w:.1f}" height="{bh:.1f}" fill="{c["clip"]}"/>')
        # field label, rotated, reading upward from the base
        lw = g.width(field, "sans-m", 13)
        inside = lw + 16 <= bh
        lx, ly = x + w / 2 + 4.5, (base - 8) if inside else (base - bh - 8)
        b.append(f'<g transform="rotate(-90 {lx:.1f} {ly:.1f})">' +
                 g.text(field, lx, ly, "sans-m", 13, c["ink"] if inside else c["mid"]) + "</g>")
        b.append(g.text(num, x + w / 2, base + 22, "mono-m", 12, c["mid"], anchor="middle"))
        b.append(g.text(f"{pages}p", x + w / 2, base + 38, "mono", 10, c["dim"], anchor="middle"))
        for k in range(fx.get(num, 0)):
            b.append(f'<rect x="{x:.1f}" y="{base - bh - 6 - k * 6 - (0 if inside else lw + 16):.1f}" width="{w:.1f}" height="3" fill="{c["accent"]}"/>')
    b.append(f'<rect x="{x0}" y="{base}" width="{x1 - x0}" height="1" fill="{c["line"]}"/>')
    b.append(g.text("막대 높이 = 쪽수", x1, top + 4, "sans", 12, c["dim"], anchor="end"))
    lw2 = g.width("막대 높이 = 쪽수", "sans", 12)
    b.append(f'<rect x="{x1 - lw2 - 108:.1f}" y="{top - 4}" width="14" height="3" fill="{c["accent"]}"/>')
    b.append(g.text("고친 커밋 1개", x1 - lw2 - 88, top + 4, "sans", 12, c["dim"]))
    tot = f"{sum(p[2] for p in PAPERS)}쪽 · 그림 {sum(p[3] for p in PAPERS)}장"
    b.append(g.text(tot, 32, 198, "sans-sb", 16, c["ink"]))
    return svg(W, h, "".join(b), g, "", "Research_paper: 논문 16편의 쪽수와 고친 커밋 수")


def strip_hjtk(theme):
    c = THEMES[theme]; g = Glyphs("j"); h = 340
    b = strip_frame(c, g, h, "V3 · 앱", "HJTK",
                    ["AI 모델을 넣지 않은 안드로이드 앱.", "이미 쓰는 웹 AI들을 한 팀으로 지휘."],
                    "Kotlin · Jetpack Compose · CI")
    stats = [("13", "릴리스"), ("131", "테스트"), ("0", "앱 안의 AI 모델")]
    sx = 32
    for n, lab in stats:
        b.append(g.text(n, sx, 210, "mono-m", 22, c["ink"]))
        b.append(g.text(lab, sx, 232, "sans", 12, c["mid"]))
        sx += max(g.width(n, "mono-m", 22), g.width(lab, "sans", 12)) + 22
    x0, x1, y0, y1 = 340, W - 150, h - 46, 58
    n = len(HJTK_VERSIONS)
    dx = (x1 - x0) / (n - 1); dy = (y0 - y1) / (n - 1)
    pts = [(x0 + i * dx, y0 - i * dy) for i in range(n)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f"V{y:.1f}H{x:.1f}" for x, y in pts[1:])
    b.append(f'<path d="{d}" fill="none" stroke="{c["clip2"]}" stroke-width="1.5"/>')
    major = {"2.0", "3.0"}
    for (v, kw), (x, y) in zip(HJTK_VERSIONS, pts):
        is_major = v in major or v == "1.0"
        r = 5 if is_major else 3.5
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c["ink"] if is_major else c["panel"]}" stroke="{c["ink"]}" stroke-width="1.5"/>')
        b.append(g.text(v, x + 10, y + 4.5, "mono-m", 13, c["ink"]))
        b.append(g.text(kw, x + 10 + g.width(v, "mono-m", 13) + 7, y + 4.5, "sans", 13, c["mid"]))
    # time anchors under first and last
    b.append(g.text("11.23 01:59", x0, h - 22, "mono", 11, c["dim"]))
    b.append(g.text("11.24 18:43", pts[-1][0], h - 22, "mono", 11, c["dim"], anchor="middle"))
    return svg(W, h, "".join(b), g, "", "HJTK: 1.0부터 3.6까지 13번의 릴리스")


def strip_voice(theme):
    c = THEMES[theme]; g = Glyphs("v"); h = 340
    b = strip_frame(c, g, h, "V2 · 앱", "Korean_voice",
                    ["폰 안에서만 도는 한국어 음성 합성", "· 목소리 복제. 모델은 한 번만 받는다."],
                    "Kotlin · ONNX Runtime · 4-bit")
    rows = [  # label, value text, fraction of meter, ghost fraction (before), note
        ("글자 오류율", "1.1%", 0.011 / 0.10, None, "Whisper로 받아쓰기, 화자 5명 × 문장 4개"),
        ("학습 중 메모리", "1.9 → 0.8 GB", 0.8 / 2.0, 1.9 / 2.0, "쓰지 않는 모델을 미리 올리던 것을 걷어냄"),
        ("PyTorch 원본과 일치", "186 / 186", 1.0, None, "음성 토큰, fp16 저장 후에도 동일"),
        ("APK", "16 MB", 16 / 1200, None, "모델 약 1.2 GB는 첫 실행 때 한 번만"),
    ]
    x0, mx1 = 340, 860
    seg, gap = 6, 2
    y = 70
    for lab, val, frac, ghost, note in rows:
        b.append(g.text(lab, x0, y - 12, "sans-sb", 14, c["ink"]))
        b.append(g.text(note, x0 + g.width(lab, "sans-sb", 14) + 12, y - 12, "sans", 12, c["dim"]))
        nseg = int((mx1 - x0) / (seg + gap))
        for k in range(nseg):
            f = (k + 0.5) / nseg
            col = c["lane"]
            if ghost and f <= ghost:
                col = c["clip"]
            if f <= max(frac, 0.6 / nseg):
                col = c["ink"]
            b.append(f'<rect x="{x0 + k * (seg + gap)}" y="{y}" width="{seg}" height="16" fill="{col}"/>')
        b.append(g.text(val, W - 40, y + 14, "mono-m", 20, c["ink"], anchor="end"))
        y += 66
    return svg(W, h, "".join(b), g, "", "Korean_voice: 측정값 네 가지")


def end_slate(theme):
    c = THEMES[theme]; g = Glyphs("e"); h = 96
    b = [f'<rect width="{W}" height="{h}" fill="{c["bg"]}"/>',
         f'<rect x="0" y="0" width="{W}" height="1" fill="{c["line"]}"/>']
    b.append(g.text("END", 32, 56, "mono-m", 13, c["accent"], track=0.12))
    b.append(g.text("Don't make tool, make innovation.", 96, 57, "sans-sb", 22, c["ink"]))
    b.append(g.text(dur(T1 - T0), W - 32, 56, "mono", 14, c["dim"], anchor="end"))
    return svg(W, h, "".join(b), g, "", "END — Don't make tool, make innovation.")


if __name__ == "__main__":
    for th in THEMES:
        for nm, fn in [("papers", strip_papers), ("hjtk", strip_hjtk), ("voice", strip_voice), ("end", end_slate)]:
            open(f"{OUT}/{nm}-{th}.svg", "w").write(fn(th))
    print("strips ok")
