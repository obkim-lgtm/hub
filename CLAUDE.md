# Hub Page — 올립의 실험실 (OLIVIA LAB)

작업 디렉토리에 만든 프로젝트들의 카드 모음. 2026-09-14부터 **다른 사람에게 보여주는 "실험실" 컨셉**으로 개편했다. **새 프로젝트 만들거나 배포할 때마다 카드 추가 필수.**

## 배포 정보

> 경로는 작업 디렉토리(`내 드라이브\Claude`) 기준 상대경로로 적는다. 드라이브 문자는 PC마다 다름.

| 항목 | 값 |
|------|-----|
| 소스 | `_hub\index.html` |
| 날짜 동기화 스크립트 | `_hub\tools\update_dates.py` |
| GitHub repo | `obkim-lgtm/hub` (public) |
| 호스팅 | GitHub Pages |
| 배포 URL | https://obkim-lgtm.github.io/hub/ |
| 배포 브랜치 | `main` (push하면 자동 배포, ~30초) |

## 외부 공개 페이지라서 지킬 것

- 노출 문구에 **HIAI·하이러닝을 쓰지 않는다** → 공식명 `AI 서·논술형 평가지원시스템` (섹션명·카드명·설명 모두).
- **동료 이름·내부 사정(예: "루카스 제안", "BS 채널")을 카드 설명에 쓰지 않는다.**
- 내부 용어(까망이 등)는 URL에만 남고 문구엔 쓰지 않는다.

## 페이지 구조

단일 HTML 파일. 인라인 CSS·JS. 외부 의존성은 Pretendard(jsdelivr) + JetBrains Mono(Google Fonts)뿐.
배경은 모눈종이, 섹션은 "실험대(BENCH)", 카드는 "실험 표본" 컨셉.

### 섹션 (순서 고정)

| 코드 | 섹션 제목 | class | 컬러 | 용도 |
|------|-----------|-------|------|------|
| BENCH A | 사내 도구 | `.internal` | `#EA580C` | 사내 Gitea·dd-mac 앱 |
| BENCH B | 서비스 Mock-up | `.mockups` | 카드별 `.hiai`/`.clipo` | 서비스별 **인덱스 카드 1장씩(총 2장)**. 목업은 카드 안 `.sub-link` 줄로 추가 |
| STORAGE | 보관함 (접힘) | `.archive` | `#6B7280` | 끝났거나 반영 못 하는 실험(구 '추후' 목업 포함) |
| SIDE | 업무 밖 실험 (접힘) | `.personal` | `#059669` | 개인 프로젝트 — 항상 맨 마지막 |

## 카드 추가 방법

해당 섹션 `.cards` 안 아무 곳에 넣으면 된다. **순서는 JS가 최근 업데이트 순으로 자동 정렬**하므로 신경 쓰지 않는다.

```html
<a class="card" href="URL" target="_blank" rel="noopener" data-src="clipo_mockup:output/foo.html" data-created="YYYY-MM-DD" data-updated="YYYY-MM-DD">
  <div class="card-top"><span class="exp-no"></span><span class="status"></span></div>
  <div class="card-head"><div class="card-icon">🌸</div><div class="card-name">카드 제목</div></div>
  <ul class="card-desc"><li>무엇인지 한 줄</li><li>핵심 흐름·기능 한 줄</li></ul>
  <div class="card-meta"><span class="updated"></span><span class="access"></span></div>
</a>
```

빈 `span`(`exp-no`·`status`·`updated`·`access`)은 JS가 채운다. 직접 쓰지 않는다.

**서비스 Mock-up 벤치는 새 카드를 만들지 않는다.** 해당 서비스 인덱스 카드(`div.card.index-card`) 안 `.sub-list`에 한 줄 추가:

```html
<a class="sub-link" href="URL" target="_blank" rel="noopener" data-src="clipo_mockup:output/foo.html" data-updated="YYYY-MM-DD"><span class="sub-icon">🌸</span><span class="sub-name">화면 이름</span><span class="sub-date"></span><svg class="sub-arrow" …/></a>
```

- 카드의 최근 업데이트 = 하위 줄 중 가장 최근 날짜(JS 계산)
- HIAI 줄은 인덱스 페이지 섹션을 옮긴 것이라 날짜 대신 `sub-note`(일정)를 쓴다

### 문구 규칙 (2026-09-14)

- **개조식 2~3줄**, 한 줄은 짧게. 문단 금지.
- 처음 보는 사람 기준 — 사내 약어(OCR·세특 단독 등)·사람 이름·케이스용 가짜 학생 이름 금지. 필요하면 풀어 쓴다.
- 흐름은 `A → B → C` 한 줄로.

### 속성 규칙

| 속성 | 뜻 | 비고 |
|------|----|------|
| `data-src` | `<작업 디렉토리 기준 폴더>:<그 안 경로>` | 날짜 스크립트가 이걸로 마지막 수정일을 찾는다. 폴더 전체면 `:.` |
| `data-created` | 카드(실험)를 처음 만든 날 | `EXP-001` 번호가 이 순서로 매겨진다 |
| `data-updated` | 소스 마지막 수정일 | **손으로 쓰지 말고 스크립트로 갱신** |
| `data-live="매일 자동 갱신"` | 스케줄로 계속 도는 서비스 | 날짜 대신 이 문구 + `가동 중` 상태. 자동 갱신이 실제로 있을 때만 붙인다 |
| `data-local` | 내 PC에서만 열리는 링크 | 배포 환경(localhost 외)에선 클릭이 막힌다 |

### 자동으로 계산되는 표시

- **상태**: 보관함=`보관 중` · `data-live`=`가동 중` · 14일 이내=`실험 중` · 60일 이내=`관찰 중` · 그 외=`휴면 중`
- **열람 범위**: `ddapp.io`·`192.168.*`=`사내망 전용`, `localhost`·`data-local`=`내 PC 전용`, 나머지=`누구나 열람`
- **GitHub Pages 목업**(`obkim-lgtm.github.io/<repo>/<path>`)은 방문 시 GitHub API로 그 파일의 최신 커밋 날짜를 가져와 더 최근이면 덮어쓴다(1시간 캐시). 그래서 목업만 고치고 허브를 재배포하지 않아도 날짜가 산다.
- 사내 도구는 외부에서 조회가 안 되므로 **허브를 배포할 때마다 스크립트로 날짜를 갱신**해야 한다.

## 배포 명령

```bash
py -3 _hub/tools/update_dates.py
cd _hub
git add -A
git -c user.name="obkim-lgtm" -c user.email="ob.kim@datadriven.kr" commit -m "허브: <변경 내용>"
git push
```

GitHub Pages가 push 후 자동 배포. 약 30초 후 https://obkim-lgtm.github.io/hub/ 에 반영.

## 카드 수정/삭제

- 프로젝트가 사라지면 카드 삭제, 끝난 실험은 보관함(`.archive`)으로 이동
- URL 변경 시 `href`와 `data-src`를 같이 고친다

## 관련 지침

루트 `CLAUDE.md`에도 짧은 요약 있음:
- 새 프로젝트 시 hub 카드 추가
- HIAI/CLIPO 목업은 추가 전에 사용자에게 먼저 확인
