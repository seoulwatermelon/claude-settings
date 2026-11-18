---
name: hwpx-native-charts
description: HWPX 네이티브 차트(선 그래프=축정렬 rect 체인, 막대/도식) + 고딕 라벨 글자모양 주입 + 한글 COM 렌더 자가확인 + dataviz 평가자 루프
metadata:
  node_type: memory
  type: reference
  originSessionId: 71add993-a020-4614-abd5-ccb65d5a6738
  modified: 2026-11-05T08:49:16.413Z
---

사용자는 "PNG처럼 보이는 차트를 한글 기능으로" 원한다(이미지 삽입 거부, 진짜 편집가능 네이티브 요구). 2026-11-04 확립.

**무엇이 되고 안 되는가 (렌더 검증으로 확정)**
- **한글 "차트 개체"(hp:chart)**: OLE2 복합 바이너리(1MB)로 저장 → 외부 코드로 생성 불가.
- **COM 자동화 삽입(ChartInsert)**: 모달 대화상자를 띄워 헤드리스 자동화 막힘. 포기.
- **✅ 축정렬 hp:rect만 안정적으로 렌더**: 한 run(_emit)에 수백 개 넣어도 전부 나온다.
- **❌ hp:line(대각선)·hp:ellipse·회전된 hp:rect**: 한 run 안에서 **조용히 누락**(렌더 안 됨, XML은 유효). 수평/수직 선만 얇은 rect로 OK. 2026-11-05 확정. (hp:line은 `<hp:startPt>/<hp:endPt>`로 가끔 나오나 위치가 불안정 → 쓰지 말 것.)
- **✅ 선 그래프 = 축정렬 rect 체인(벡터 계단)**: 각 선분을 아주 짧게 겹치는 축정렬 사각형들로 그려 매끈한 선처럼. 마커 = 가로 슬라이스 원(disc) + 흰색 헤일로. 전부 네이티브·편집가능. **대각선의 정답.** → `linechart.py`.
  - **품질 파라미터(렌더 확대 확인)**: `_seg step=95`(계단 안 보임), `lw=140`(~3px), 마커 `rad=205`, `_disc rows=23`(촘촘→매끈한 원), 흰 헤일로 `rad+72`. 이 값이면 matplotlib에 근접. 막대(rect)는 원래 또렷.
  - **네이티브 vs 이미지 교환**: 손도형이라 품질 천장 있음. 1차엔 네이티브 선택했으나, "구리다" 재지적 + 경영진 보고라는 목적상 **최종 이미지(matplotlib) 전환**(2026-11-05). 결정 논리: 차트를 설득 필수 소수(3개)로 줄이니 편집성 부담↓ + 이미지가 품질 천장 돌파. `mpl_charts.py`가 개별 PNG(fig_IV/V1/V2) 출력 → `r.image(png, width_mm=150)`로 삽입(캡션 【그림】이 제목 담으므로 PNG 안엔 제목 넣지 않음). **교훈: 경영진 문서는 '편집가능 네이티브'보다 '출판품질 이미지'가 맞다.**
  - **차트 규율(경영진 설득)**: 도식/그래프/표는 "설득에 기여할 때만". 표를 그대로 복창하는 장식 차트(예: 1행 누적막대)는 삭제. 각 차트가 다른 메시지를 지도록: 단기긴급(세로막대)·결과(발산막대 누적과부족)·원인(선 수요vs공급, 부족구간 음영). [[professor-lab-space-report]]
- **표-셀 음영**: 가로 막대·박스 도식엔 OK(로드맵 등). 세로 컬럼엔 부적합.

**형태는 데이터 역할에 맞춘다(한 종류로 통일 금지)** — dataviz choosing-a-form:
- 시계열 추이·다계열 비교 → **선**. 범주형 크기 비교(이산 시나리오) → **세로 막대**. 0선 기준 여유/부족 극성 → **발산형 막대**. 부분-전체 → **가로 누적막대(파이는 anti-pattern)**. 로드맵/도식 → 표(viz.timeline2).
- `linechart.py`가 **차트킷**: 모든 형태가 `_frame()`(배경·격자·뮤트고딕축·y눈금·x라벨·기준선) 공유 → 한 보고서 안에서 한 식구처럼 보임.

**도구 (스크래치패드 `linechart.py`=차트킷, `shapechart.py`, `skku_report` 확장)**
- `_frame(r,n,xlabels,ymin,ymax,yticks,yfmt,legend,reflines,zero_emphasis,band)` — 공통 프레임. band=True면 밴드중앙 정렬(막대), False면 양끝(선). (shapes,X,Y,ch,geom) 반환.
- `line_chart(r, series, ...)` — 선. series=[{name,data,color,fmt,ann}]. annotate='key'/'all'/'none'/[인덱스]/계열별 'ann'. 2계열 legend=True(프레임 위 짧은 선키).
- `bar_chart(r, data, xlabels, ymin, ymax, yticks, color, reflines, barfrac=0.42, lfmt)` — 세로 막대(밑변서 자람, 값은 캡 위). reflines 'side':'left'로 라벨 위치.
- `diverging_bar(r, data, ..., pos_color=BLUE, neg_color=RED, fmt)` — 0선 발산 막대(위/아래 색). zero_emphasis 내장.
- `stacked_bar_h(r, segments=[(label,value,color)], unit)` — 가로 누적막대. 조각 안 값=흰색 글자, 아래 이름=보조잉크, 2px 표면간격.
- `shapechart.single/diverging/grouped/roadmap` — 구형 막대(미사용, _rect/_emit만 재사용).
- `_rect(...)`: 양식 제목 글상자(hp:rect) 복제. 한 run에 도형들, **첫 도형 treat='1'로 H 공간확보**, 나머지 treat='0' 떠있게 vertOffset/horzOffset(vertRelTo/horzRelTo=PARA). 배경은 fill='#ffffff'(페이지색, 안 보이게).
- **차트 라벨 글자모양**: 본문은 명조(구식). `r.add_char(size_pt, color, bold=False, base=17)`로 **고딕 색상 글자모양** 주입(`_inject_chars`가 borderfill처럼 기존 최대 id 뒤로 **연속 재번호**+section 참조 remap). 축=뮤트회색 #898781, 값=잉크 #1a1a19 bold, 범례/범주=#52514e.
- **dataviz 검증 팔레트**: BLUE #2a78d6, ORANGE #eb6834, RED #d03b3b, 격자 #e1e0d9, 기준축 #c3c2b7. 값/축 글자는 잉크 토큰(계열색 금지). y눈금 숫자는 맨숫자(단위는 제목 '(단위: …)'에 한 번).
- 값 라벨 겹침: 위 라벨 cy−740, 아래 cy+360(마커 링 clear), 양끝은 안쪽으로 ±1150 밀기, 눈금 headroom.
- **도형 차트는 페이지 경계에서 잘린다** → 앞에 `r.pagebreak()`.
- 로드맵 도식은 `viz.timeline2`(표+셀음영).

**디자인 평가자 루프 (사용자 요구: "100점까지")**: dataviz 레퍼런스(marks-and-anatomy/choosing-a-form/anti-patterns)를 읽는 subagent에 렌더 PNG를 Read시켜 0~100 채점+구체 수정안 받고 반영 반복. 63→91→100 달성. 정적 인쇄물이므로 hover/다크모드/table-view는 감점 제외하라고 명시.

**한글 COM 렌더 자가확인 (블라인드 탈출 — 매우 중요)**
- **gen_py 캐시 손상 회피**: 그냥 `Dispatch`도 캐시가 있으면 깨진 gen_py 클래스를 집어 `com_error(-2147023170 RPC 실패)`를 낸다. → **`%TEMP%\gen_py` 삭제 + `from win32com.client import dynamic; hwp=dynamic.Dispatch("HWPFrame.HwpObject")`(late-binding)로 확실히 우회**. (2026-11-05 확인)
- 열기 전 `hwp.SetMessageBoxMode(0x00020000)` — 복구/알림 대화상자 자동응답(강제종료 후 복구팝업이 Open을 블로킹함).
- `hwp.Open(abspath, "HWPX", "")` (포맷은 "HWP" 아님 "HWPX"), `hwp.CreatePageImage(bmp, pg, 150, 24, "BMP")` → PIL로 PNG 변환해 Read로 눈으로 확인.
- 매 실행 후 `taskkill /F /IM Hwp.exe` — **Hwp 프로세스가 쌓이면 충돌로 Open이 멈춘다.**
- **CreatePageImage가 page 0만 렌더되고 1+는 실패하면**: 열자마자 전 페이지 레이아웃이 안 된 것. `hwp.Run("MoveDocEnd"); sleep; hwp.Run("MoveDocBegin"); sleep` 로 **전체 페이지 강제 레이아웃** 후 `hwp.PageCount`로 루프, 페이지별 2~3회 재시도. (2026-11-05 확인)
- **반복 강제종료로 COM이 오염되면 정상 파일도 CreatePageImage가 hang** 한다(파일 탓 아님). 이럴 땐 한글 없이 검증: zip 열어 section0.xml을 `ET.fromstring`(well-formed) + 핵심 문자열/표 수 확인으로 대체. 사용자가 한글 UI로 직접 열면 정상.
- 스크래치패드 `render.py`가 이 루프를 담음.
- **본문/노트에 em-dash `—`(U+2014) 쓰지 말 것**: Windows cp949 콘솔이 못 찍어 skku_report save()의 경고 출력에서 `UnicodeEncodeError` → 빌드가 이미지 주입 전 중단 → 한글에서 깨진 이미지로 보임. 쉼표/`·`/`→`로 대체(또는 `PYTHONIOENCODING=utf-8`). 2026-11-05 확인.

관련: [[hwpx-native-bar-charts]], [[professor-lab-space-report]]
