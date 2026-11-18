---
name: hwpx-table-cell-format
description: 보고서 표는 행·열 제목(첫 행·첫 열) 항상 굵게, 셀 안 줄바꿈은 들여쓰기 없이 — skku_report 기본값이 둘 다 어긋남
metadata:
  type: feedback
---

표를 만들 때는 **첫 행(열 제목)과 첫 열(행 제목)을 항상 굵게** 한다. 셀 안에서 다음 줄로 넘어갈 때 **앞에 공백을 넣지 않는다**(2026-11-05 사용자 지시: "셀별로 문장 쓸 때 다음줄로 넘어가면 3칸 띄어쓰기가 되서 부자연스럽다", "표 만들땐 항상 행,열 제목 줄은 볼드체").

**Why:** `cellflow()` 기본 hang=2 가 이어지는 줄 앞에 공백 2칸을 넣고 양쪽정렬로 3칸처럼 보였다. skku_report 양식에는 12pt 굵은 글자 모양이 없어 머리글이 보통 글씨로 나왔다.
**How to apply:** `cellflow(text, width, hang=0)` 로 나누고, 저장 뒤 `E:\SANGSI\00_특임\2_경영학과_전략_상시\_hwpx_bold.py` 의 `bold_table_headers(path)`(charPr 복제 + `<hh:bold/>`)를 호출한다. 무용학과 보고서 빌더 등 기존 빌더를 다시 돌릴 때도 적용. 관련: [[hwpx-report-layout-checklist]] [[report-at-a-glance-tables]]

**2026-11-05 추가(무용 면담 시나리오, 사용자 재지적 "띄어쓰기 3칸 하지 말고 shift+enter로 맞춰")**: 셀 글을 cellflow 로 자르지도 말고,
`r.table(..., hang_left=True)` 로 넘긴다 — 좌측정렬 셀에서 '- '·'1. '·'① ' 로 시작하는 줄은 한 문단 + 내어쓰기(표지 뒤 정렬),
정렬 LEFT, 한글 어절 단위 줄바꿈(breakNonLatinWord=BREAK_WORD; 양식 기본 KEEP_WORD 는 **글자** 단위라 "최종/안"처럼 끊김).
본문 l1 도 flow() 없이 한 문장 통째로. 규정 인용("세칙 제○조")이 있으면 붙임에 그 조 전체(항·호·목)를 싣고 인용한 항만 굵게.

