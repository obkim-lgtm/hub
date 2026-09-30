"""허브 카드 대상 페이지의 공유 이미지(1200x630 PNG) + og 태그 묶음을 만든다.

허브(`_hub/index.html`) 자체의 og.png는 make_og.py 담당. 이 스크립트는 **카드가 가리키는 각 페이지**용.
Chrome 헤드리스로 HTML 한 장을 찍는다(폰트 = Pretendard jsdelivr, 네트워크 필요).

실행 예:
    py -3 _hub/tools/make_page_og.py --theme pink --eyebrow "🎀 연수 노트" \
        --title "CLIPO 연수<br>강사 현황" --desc "연수가 가입·사용·매출로<br>이어졌는지 강사별로" \
        --art _hub/tools/og_art/training.svg --out clipo_analytics/og_training.png \
        --url https://internal-tool.pages.ddapp.io/clipo-analytics/training.html \
        --img-url https://internal-tool.pages.ddapp.io/clipo-analytics/og_training.png

- 출력: PNG 파일 + 표준출력에 <head>에 붙일 태그 묶음(description·og:*·twitter:*)
- --title/--desc 의 <br>은 이미지 줄바꿈용. 태그 문구에서는 공백으로 바뀐다
- --art 는 오른쪽 그림(SVG 파일, 400~420px 정사각 권장). 없으면 그림 없이 글자만
- 테마는 그 페이지 화면 톤과 맞춘다. 새 톤이 필요하면 THEMES에 한 줄 추가
"""
import argparse, html, os, re, subprocess, sys, tempfile

THEMES = {
    # 이름: (바탕 CSS, 머리말 뱃지 CSS, 제목색, 설명색)
    'sky':   ("background:linear-gradient(180deg,#BFE3FF 0%,#DDF0FF 55%,#F3FAFF 100%)",
              "background:#fff;color:#0B5CAD;border:3px solid #B5D6F0", "#16324F", "#3E5A77"),   # 근태 캘린더
    'note':  ("background-color:#F6F5F0;background-image:linear-gradient(rgba(28,31,36,.06) 1px,transparent 1px),"
              "linear-gradient(90deg,rgba(28,31,36,.06) 1px,transparent 1px);background-size:30px 30px",
              "background:#FFF1E6;color:#C2410C;border:3px solid #F6C9A6", "#1C1F24", "#5F6570"),  # 팀 캘린더·허브 톤
    'cream': ("background:#FFF9F0",
              "background:#FFE9CF;color:#8A4A12;border:3px solid #F2C98F", "#3A2A18", "#7A6048"),  # 주요 지표 대시보드
    'pink':  ("background-color:#FFF0F6;background-image:radial-gradient(#F9D3E3 3px,transparent 3.5px);background-size:44px 44px",
              "background:#fff;color:#A8325F;border:3px solid #F7C6DA", "#3B2433", "#654657"),   # 연수 강사 현황
    'clipo': ("background:linear-gradient(180deg,#EEF3FF 0%,#FFFFFF 100%)",
              "background:#fff;color:#2F55E0;border:3px solid #C7D5FF", "#1B2F66", "#4A5E8C"),   # CLIPO 공개 페이지
    'hiai':  ("background:linear-gradient(180deg,#E8F0FA 0%,#FFFFFF 100%)",
              "background:#fff;color:#0950A0;border:3px solid #BCD3EE", "#0B2E57", "#46607F"),   # HIAI 톤
}

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:Pretendard,sans-serif;position:relative;{bg}}}
.box{{position:absolute;left:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;width:{box}px}}
.eb{{display:inline-flex;align-self:flex-start;align-items:center;line-height:1;font-size:26px;font-weight:700;padding:12px 22px;border-radius:999px;margin-bottom:26px;{eb}}}
h1{{font-size:84px;font-weight:800;letter-spacing:-.03em;line-height:1.1;color:{h1}}}
p{{font-size:34px;font-weight:500;margin-top:22px;line-height:1.45;word-break:keep-all;color:{p}}}
.art{{position:absolute;right:70px;top:50%;transform:translateY(-50%)}}
</style></head><body><div class="box">{eyebrow_html}<h1>{title}</h1><p>{desc}</p></div><div class="art">{art}</div></body></html>"""

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def plain(s):
    return html.escape(re.sub(r'\s+', ' ', re.sub(r'<br\s*/?>', ' ', s)).strip(), quote=True)


def main():
    for st in (sys.stdout, sys.stderr):
        st.reconfigure(encoding='utf-8')  # Windows 콘솔(cp949)에서 태그 한글이 깨지지 않게
    ap = argparse.ArgumentParser()
    ap.add_argument('--theme', required=True, choices=sorted(THEMES))
    ap.add_argument('--title', required=True)
    ap.add_argument('--desc', required=True)
    ap.add_argument('--eyebrow', default='')
    ap.add_argument('--art', help='오른쪽 그림 SVG 파일')
    ap.add_argument('--out', required=True, help='PNG 저장 경로')
    ap.add_argument('--url', required=True, help='페이지 주소(og:url)')
    ap.add_argument('--img-url', required=True, help='PNG가 배포될 절대 주소(og:image)')
    ap.add_argument('--alt', default='', help='og:image:alt (없으면 제목)')
    ap.add_argument('--site', default='데이터드리븐 사내 도구', help='og:site_name')
    a = ap.parse_args()

    bg, eb, h1, p = THEMES[a.theme]
    art = open(a.art, encoding='utf-8').read() if a.art else ''
    doc = PAGE.format(bg=bg, eb=eb, h1=h1, p=p, box=640 if art else 1000, title=a.title, desc=a.desc, art=art,
                      eyebrow_html=f'<div class="eb">{a.eyebrow}</div>' if a.eyebrow else '')
    chrome = next((c for c in CHROME_CANDIDATES if os.path.exists(c)), None)
    if not chrome:
        sys.exit('Chrome을 찾지 못했습니다 — CHROME_CANDIDATES에 경로를 추가하세요.')
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, 'og.html')
        open(src, 'w', encoding='utf-8').write(doc)
        out = os.path.abspath(a.out)
        subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1200,630', '--virtual-time-budget=4000', '--screenshot=' + out,
                        'file:///' + src.replace('\\', '/')], check=True, capture_output=True)
    print('이미지:', out, file=sys.stderr)

    t, d = plain(a.title), plain(a.desc)
    alt = html.escape(a.alt, quote=True) if a.alt else t
    print(f'''<meta name="description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{html.escape(a.site, quote=True)}">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{a.url}">
<meta property="og:image" content="{a.img_url}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{a.img_url}">''')


if __name__ == '__main__':
    main()
