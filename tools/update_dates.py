"""허브 카드의 data-updated 값을 실제 소스의 마지막 수정일로 맞춘다.

카드의 data-src="<작업 디렉토리 기준 폴더>:<그 안의 경로>" 를 읽어서
- git repo면  `git log -1 -- <경로>` 의 커밋 날짜
- git이 아니면 파일(폴더면 하위 전체) 최종 수정 시각
으로 data-updated="YYYY-MM-DD" 를 덮어쓴다.

실행 (작업 디렉토리 어디서든):
    py -3 _hub/tools/update_dates.py
"""
import datetime as dt
import os
import re
import subprocess
import sys

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(HUB)  # 내 드라이브/Claude
INDEX = os.path.join(HUB, "index.html")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}

CARD_TAG = re.compile(r'<a class="card"[^>]*>')
SRC_ATTR = re.compile(r'data-src="([^"]+)"')
UPD_ATTR = re.compile(r'data-updated="[^"]*"')


def git_date(repo, path):
    try:
        out = subprocess.run(
            ["git", "-C", repo, "log", "-1", "--format=%cs", "--", path],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout.strip() or None if out.returncode == 0 else None


def mtime_date(target):
    latest = 0.0
    if os.path.isfile(target):
        latest = os.path.getmtime(target)
    else:
        for base, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                latest = max(latest, os.path.getmtime(os.path.join(base, f)))
    return dt.date.fromtimestamp(latest).isoformat() if latest else None


def resolve(src):
    folder, _, path = src.partition(":")
    repo = os.path.join(ROOT, folder)
    target = os.path.join(repo, path or ".")
    if not os.path.exists(target):
        return None, "경로 없음"
    if os.path.isdir(os.path.join(repo, ".git")):
        d = git_date(repo, path or ".")
        if d:
            return d, "git"
    return mtime_date(target), "mtime"


def main():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()

    cache, report = {}, []

    def patch(match):
        tag = match.group(0)
        m = SRC_ATTR.search(tag)
        if not m:
            return tag
        src = m.group(1)
        if src not in cache:
            cache[src] = resolve(src)
        date, how = cache[src]
        if not date:
            report.append(f"  건너뜀  {src} ({how})")
            return tag
        old = UPD_ATTR.search(tag)
        report.append(f"  {date}  {src} ({how})")
        if old:
            return UPD_ATTR.sub(f'data-updated="{date}"', tag, count=1)
        return tag[:-1] + f' data-updated="{date}">'

    new = CARD_TAG.sub(patch, html)
    today = dt.date.today().isoformat()
    new = re.sub(r'(<span id="built-at">)[^<]*(</span>)', rf"\g<1>{today}\g<2>", new)

    if new != html:
        with open(INDEX, "w", encoding="utf-8", newline="") as f:
            f.write(new)
    print("\n".join(report))
    print("index.html 갱신됨" if new != html else "변경 없음")


if __name__ == "__main__":
    sys.exit(main())
