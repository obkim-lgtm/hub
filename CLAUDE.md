# Hub Page (프로젝트 바로가기)

작업 디렉토리에 만든 프로젝트들의 카드 모음. **새 프로젝트 만들거나 배포할 때마다 카드 추가 필수.**

## 배포 정보

> 경로는 작업 디렉토리(`내 드라이브\Claude`) 기준 상대경로로 적는다. 드라이브 문자는 PC마다 다름 (현재 PC: `F:`).

| 항목 | 값 |
|------|-----|
| 소스 | `_hub\index.html` |
| GitHub repo | `obkim-lgtm/hub` (public) |
| 호스팅 | GitHub Pages |
| 배포 URL | https://obkim-lgtm.github.io/hub/ |
| 배포 브랜치 | `main` (push하면 자동 배포, ~30초) |

## 페이지 구조

단일 HTML 파일. 인라인 CSS, 외부 의존성은 Pretendard CDN뿐.

### 섹션 4개 (고정)

| 섹션 | class | 컬러 (--accent) | 배경 (--accent-bg) | 용도 |
|------|-------|-----------------|---------------------|------|
| Internal App | `.internal` | `#EA580C` (주황) | `#FFF7ED` | 사내 Gitea 배포 앱 |
| HIAI 목업 | `.hiai` | `#7E44FB` (보라) | `#F3EEFF` | HIAI 서비스 UI 목업 |
| CLIPO 목업 | `.clipo` | `#416BFF` (파랑) | `#EEF2FF` | CLIPO 서비스 UI 목업 |
| Personal | `.personal` | `#059669` (초록) | `#ECFDF5` | 개인 프로젝트 |

## 카드 추가 방법

각 섹션의 `.cards` 안에 다음 패턴으로 카드 추가:

```html
<a class="card" href="URL" target="_blank">
  <div class="card-top">
    <div class="card-icon">🌸</div>
    <span class="card-date">YYYY-MM-DD</span>
  </div>
  <div class="card-name">카드 제목</div>
  <div class="card-desc">한두 줄 설명. 너무 길지 않게.</div>
  <div class="card-arrow"><svg fill="none" viewBox="0 0 14 14" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M2 7h10M7 2l5 5-5 5"/></svg></div>
</a>
```

### 작성 규칙

- **`href`**:
  - 배포 URL이 있으면 절대 URL (예: `https://training.clipo.ai/event/`)
  - 로컬 파일 경로면 상대경로 (예: `clipo_mockup/output/foo.html`) → `data-local` 속성 추가 필수
- **`data-local` 속성**: 파일 시스템 경로를 가리키는 카드는 GitHub Pages에선 안 열리므로, 배포 환경에선 자동 비활성화 처리되도록 이 속성을 붙임
- **`card-icon`**: 이모지 1개. 카드 성격에 맞게 선택
- **`card-date`**: 카드 추가일 (작업 시점 날짜) `YYYY-MM-DD` 형식
- **`card-name`**: 짧고 명료하게 (15자 이내 권장)
- **`card-desc`**: 1~2줄. 무슨 프로젝트인지, 어떤 흐름인지 핵심만

### 카드 위치

같은 섹션 안에서는 **최근 순**으로 (가장 최근 카드가 맨 위). 새 카드는 해당 섹션 `.cards` 맨 앞에 추가. 섹션 자체 순서는 고정.

## 배포 명령

```bash
cd _hub
git add index.html
git -c user.name="obkim-lgtm" -c user.email="ob.kim@datadriven.kr" \
  commit -m "허브: <카드명> 추가"
git push
```

GitHub Pages가 push 후 자동 배포. 약 30초 후 https://obkim-lgtm.github.io/hub/ 에 반영.

## 카드 수정/삭제

- 프로젝트가 사라지면 해당 카드도 삭제
- 프로젝트 URL 변경 시 `href` 업데이트
- 설명이 부정확해지면 `card-desc` 수정

## `data-local` 동작

`index.html` 하단 `<script>`에서 `window.location.protocol`이 `http:`/`https:`이면(=배포 환경) `data-local` 카드를 비활성화/숨김 처리. 로컬에서 직접 파일을 열면 정상 동작.

## 관련 지침

루트 `CLAUDE.md`에도 짧은 요약 있음:
- 새 프로젝트 시 hub 카드 추가
- HIAI/CLIPO 목업은 추가 전에 사용자에게 먼저 확인
