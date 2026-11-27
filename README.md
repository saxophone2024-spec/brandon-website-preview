# 브랜든 최 웹사이트 v4 — White / Pretendard / Cobalt

`brandonjinwoochoi.com` 전면 개편 v4. 사용자 피드백(히어로 축소·672만 뷰 제거·문구 축약·공식 프로필 반영) 반영. **순백색(#FFFFFF) + Pretendard 단일 산세리프 + 코발트(#1F3BFF) 포인트**의 아티스트·에이전시 스타일 정적 사이트.

```
index.html                 메인 (KR/EN, 프로필·섭외·EPK·미디어·문의)
epk.html                   5쪽 EPK (A4 인쇄용, 같은 톤)
assets/css/style.css       디자인 시스템
assets/js/main.js          언어·내비·모바일 메뉴·리빌·EPK 탭·복사·문의 폼
assets/img/                사진·음반 커버
assets/downloads/          EPK PDF · 프레스 사진 · 무대 도면
deploy.sh                  GitHub Pages push
render.py / test_cta.py    검증 스크립트
shots/                     렌더 검수 이미지
```

## 디자인 기준 (레퍼런스 조사 반영)

- **레퍼런스**: `pieplans.kr`(Pretendard 사용 확인 — 실제 소스에서 `pretendardvariable-dynamic-subset` 로드), `raychenviolin.com`(큰 앨범 히어로·짧은 문장·날짜 리스트), `seongjin-cho.com`(Nunito 단일 산세리프·화이트·13~60px 타입 스케일), `olafurarnalds.com`(단어 단위 초미니멀 내비).
- **컬러**: `#FFFFFF` 본문 / `#F7F7F8` 보조 패널 / `#111111` 텍스트 / `#1F3BFF` 단일 포인트.
- **타이포**: `Pretendard Variable` 단일 패밀리. H1 `clamp(3rem, 7.4vw, 6.9rem)`·800·자간 `-0.05em`, H2 `clamp(2.05rem, 4.2vw, 3.7rem)`, 본문 17px/1.62, 라벨 12px·700·대문자.
- **그리드**: 최대 1280px, 24~56px 거터, 22~40px 라운드 패널, 1px 헤어라인, 카드 `#F7F7F8` → hover 시 흰색 + 그림자.
- **카피**: 문학적 문장 없이 사실·숫자·행동 중심. “클래식 색소폰, 브랜든 최.” / 히어로 서브 한 줄 “호흡으로 클래식의 경계를 넓히는 색소포니스트.” / “Expanding the boundaries of classical music.” / “섭외 프로그램” / “섭외 문의”. (2026-11-27 사용자 요청으로 히어로 서브·마퀴·메타에서 링컨센터·조수미 언급 제거 — 프로필 본문 서술은 유지.)

## 구성

1. **Hero** — 좌: 800 웨이트 타이포 + 실적 한 줄 + `[공연·강연 섭외]` `[▶ 672만 뷰]`, 우: 흑백 포트레이트 카드, 하단 블랙 마퀴
2. **숫자** — 음반 7 · 오케스트라 14+ · 유튜브 51K · 쇼츠 6.7M
3. **01 Profile** — 인물 사진 + 2문단 + 학력/수상/현직/악기 표
4. **이미지 밴드** — 부산시립교향악단 무대 (풀블리드)
5. **02 Booking** — 프로그램 카드 6종, 3단계 진행(블랙 패널)
6. **03 EPK** — Biography(숏·풀 복사), Repertoire, Discography, Press, Media & Stage + PDF
7. **04 Media** — 블랙 섹션, 라흐마니노프 〈첼로 소나타〉(예술의전당 IBK홀) 메인 + 크레스턴 협주곡(예술의전당 콘서트홀) 서브 카드
8. **05 Contact** — 매니지먼트 정보 + 문의 폼(메일 앱 연결)
9. **Footer** + 모바일 하단 고정 CTA

## 검수

- 1440 / 834 / 390 / 320px 렌더 — 가로 스크롤 0, 겹침 없음, Pretendard 적용 확인
- 언어 전환·유지, EPK 탭, 바이오 복사, 프로그램→폼 자동 선택, 모바일 메뉴, 플로팅 CTA(문의 섹션에서 숨김) 동작 확인
- EPK PDF 5쪽 A4, 같은 톤(화이트·Pretendard·코발트)

## 남은 확인

- **연락처**: 브리프의 `010-8143-1214` 사용. 기존 기록(v1 사이트·USER.md)은 서지안 매니저 `010-8068-7678`이므로 공개 전 확인 필요.
- GitHub Pages 설정(저장소 Settings → Pages → main / root)은 Pickle GitHub 앱 권한 밖이라 사용자 1회 설정 필요.
- 도메인(`www.brandonjinwoochoi.com`)은 Wix DNS → GitHub Pages 전환 작업 별도.
