"""Real data for the portfolio, read from the four repositories' git history."""
import os
import re
from datetime import datetime

REPOS = ["research_paper", "hjtk", "korean_voice", "heok0308hth-glitch"]


def load(repo):
    out, cur = [], None
    for line in open(os.path.join(os.environ.get("LOG_DIR", "logs"), f"log_{repo}.txt"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("C|"):
            _, ts, msg = line.split("|", 2)
            cur = dict(repo=repo, t=datetime.fromisoformat(ts), msg=msg, ins=0, dele=0)
            out.append(cur)
        elif "changed" in line and cur is not None:
            m = re.search(r"(\d+) insertion", line)
            n = re.search(r"(\d+) deletion", line)
            cur["ins"] = int(m.group(1)) if m else 0
            cur["dele"] = int(n.group(1)) if n else 0
    return out


def kind(c):
    r, m = c["repo"], c["msg"]
    if r == "research_paper":
        if m.startswith(("Add paper", "Add papers", "논문 3편")):
            return "paper"
        if m.startswith("Update README to include"):
            return "doc"
        return "fix"
    if r == "hjtk":
        if re.match(r"^(\d\.\d\.\d|HJTK 1\.0\.0)", m):
            return "version"
        if m.startswith("fix"):
            return "fix"
        return "doc"
    if r == "korean_voice":
        if m.startswith("v2.1.4"):
            return "fix"
        if m.startswith("Add KoreanVoice"):
            return "release"
        return "doc"
    if re.search(r"correct|precise|align|fix|Simplify", m):
        return "fix"
    return "doc"


COMMITS = sorted((dict(c, kind=kind(c)) for r in REPOS for c in load(r)), key=lambda c: c["t"])
T0, T1 = COMMITS[0]["t"], COMMITS[-1]["t"]

PAPER_CLIPS = []  # (time, label)
for c in COMMITS:
    if c["kind"] != "paper":
        continue
    m = c["msg"]
    if m.startswith("논문 3편"):
        PAPER_CLIPS.append((c["t"], "01–03"))
    elif m.startswith("Add papers"):
        PAPER_CLIPS.append((c["t"], "08–10"))
    else:
        PAPER_CLIPS.append((c["t"], re.search(r"paper (\d+)", m).group(1)))

APP_CLIPS = []
for c in COMMITS:
    if c["kind"] == "version":
        v = re.match(r"^(?:HJTK )?(\d\.\d)", c["msg"]).group(1)
        APP_CLIPS.append((c["t"], "HJTK " + v if v == "1.0" else v, "hjtk"))
    if c["kind"] == "release":
        APP_CLIPS.append((c["t"], "KoreanVoice", "kv"))
    if c["repo"] == "korean_voice" and c["kind"] == "fix":
        APP_CLIPS.append((c["t"], "KV 2.1.4", "kv"))

FIXES = [c for c in COMMITS if c["kind"] == "fix"]

PAPERS = [  # number, short field, pages, figures (pages/figures counted from the PDFs and figures/ dirs)
    ("01", "그래프 연소", 19, 9), ("02", "거짓말 탐색", 16, 8), ("03", "램지 R(5,24)", 4, 0),
    ("04", "오케스트레이션", 14, 6), ("05", "콜라츠", 14, 6), ("06", "혁신의 역설", 19, 6),
    ("07", "시간과 공간", 15, 7), ("08", "자기수정", 16, 8), ("09", "사이클로토믹", 14, 6),
    ("10", "동결 랜덤망", 13, 7), ("11", "역방향 CoT", 15, 7), ("12", "면역 어텐션", 14, 8),
    ("13", "자기참조 검증", 16, 8), ("14", "메타게임", 16, 8), ("15", "기억 압축", 16, 9),
    ("16", "오더북 상전이", 18, 6),
]


def paper_fix_counts():
    cnt = {p[0]: 0 for p in PAPERS}
    for c in FIXES:
        if c["repo"] != "research_paper":
            continue
        for n in re.findall(r"[Pp]aper (\d{2})", c["msg"]):
            cnt[n] = cnt.get(n, 0) + 1
        for n in re.findall(r"[Pp]apers? (\d{1,2})\b", c["msg"]):
            k = f"{int(n):02d}"
            if k in cnt and f"aper {k}" not in c["msg"]:
                cnt[k] += 1
    return cnt


HJTK_VERSIONS = [  # (version, keyword) — keywords taken from each release commit
    ("1.0", "첫 공개"), ("1.1", "전송 크래시 수정"), ("1.2", "DeepSeek 응답"), ("1.3", "파이프라인"),
    ("2.0", "AI 다섯 종"), ("2.1", "빌드 통합"), ("3.0", "AI 전화"), ("3.1", "키 없는 로그인"),
    ("3.2", "계정 하나로"), ("3.3", "지휘자"), ("3.4", "합주"), ("3.5", "회사 모드"), ("3.6", "폰에서 APK"),
]

if __name__ == "__main__":
    print(len(COMMITS), "commits", T0, "→", T1, (T1 - T0))
    print("fixes", len(FIXES))
    print(PAPER_CLIPS)
    print(APP_CLIPS)
    print(paper_fix_counts())
    print("pages", sum(p[2] for p in PAPERS), "figs", sum(p[3] for p in PAPERS))
