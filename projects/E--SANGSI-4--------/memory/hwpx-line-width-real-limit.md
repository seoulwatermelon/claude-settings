---
name: hwpx-line-width-real-limit
description: HWPX 보고서 작성 시 skku_report의 줄 폭 경고는 25% 관대하므로 믿지 말고 실측 기준으로 자동 줄바꿈할 것
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-09-08T02:56:36.571Z
---

hwpxskill로 한글 보고서를 만들 때 **문장을 여러 호출로 쪼개 수동 줄바꿈하지 말 것.**
**2026-11-05 갱신: 본문(l1·l2·dash·note)은 `flow()`로도 자르지 말고 한 문장을 한 호출에 통째로 넘긴다.**
`flow()`로 자른 이어지는 줄에는 앞 공백이 붙어, 한글에서 공백이 잔뜩 들어간 것처럼 보인다(사용자 지적 "배경 쓸 때 줄 넘어가니까 띄어쓰기가 엄청 많이").
둘째 줄 정렬은 skku_report 의 내어쓰기 문단모양이 해 준다 — 2026-11-05 skku_report.py 수정: 문단모양 id 를 기존 최대+1 부터 이어 매김(100번대면 한글이 무시), `left`=0·음수 `intent`만(left 를 주면 첫 줄까지 밀림). 표 셀은 `cellflow(text, w, hang=0)`([[hwpx-table-cell-format]]).

**실측 1줄 수용량** (A4 본문폭 169.98mm ÷ (글자크기pt × 0.3528mm)):

| 글자크기 | 실제 | skku_report 추정 |
|---|---|---|
| 15pt (본문1·2) | **32.1em** | 40.0 (과대) |
| 14pt (본문3·하위) | **34.4em** | 42.9 |
| 13pt (※ 참고) | **37.1em** | 46.2 |
| 12pt (표 셀) | **40.2em** | 50.0 |

표 셀은 `(열너비HWPUNIT − 282) ÷ 283.5 mm` 기준으로 별도 계산(cellflow가 처리).

**Why:** `skku_report.py`의 `C15 = 40.0` 상수가 실측보다 약 25% 관대해서
"[줄 폭 경고 없음]"이 거짓으로 뜬다. 이걸 믿고 40em까지 채웠다가 본문 105줄이
한글에서 자동 줄바꿈됐고, 거기에 수동 줄바꿈이 겹쳐 문서 전체가 깨졌다.
사용자가 "줄 깨지고 난리도 아니야"라고 지적해서야 발견했다.

**How to apply:** 빌드 후 반드시
`python C:/Users/SKKU/.claude/skills/hwpxskill/scripts/verify_layout.py <파일.hwpx>` 실행.
`validate.py`는 ZIP·XML 구조만 보고 레이아웃은 검사하지 않으며,
`page_guard.py`는 레퍼런스 복원용이라 신규 문서에는 부적합하다.
관련: [[hwpx-report-layout-checklist]]
