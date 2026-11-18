---
name: user-hand-edited-final-hwpx
description: "사용자가 한글에서 직접 고친 최종본은 빌더로 재생성 금지 — 해당 줄만 hwpx 안에서 바꾸고, 바꾸기 전 문구를 먼저 합의"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-19T08:10:21.010Z
---

무용학과 보고서 v5는 사용자가 2026-10-19 한글에서 직접 크게 고쳤다(제목 「무용학과 전임교원 채용 계획(안)」, 흐름표 ④ 상시채용 등).
이 파일로 팀장 보고를 마쳤고, `00_2026_초빙검토\무용학과 전임교원 채용 계획(안)_261015_v1.hwpx`로 이름을 바꿨으며 이전 판(향후 대응 v1~v4, 정상화 방안 v5)은 지웠다.
`_build_향후대응안_v5.py`는 이제 최종본과 내용이 다르다.

**Why:** 빌더로 다시 만들면 사용자의 수동 수정이 사라진다. 문구도 확정 전에 파일을 고치려다 사용자가 도구 실행을 거부했다(2026-10-19).
**How to apply:** 최종본 수정 요청은 먼저 문구안을 보여 주고 합의한 뒤, hwpx 안 해당 텍스트만 바꾸고 PDF만 다시 뽑는다. 빌더 재실행은 금지. 관련: [[report-at-a-glance-tables]] [[onetable-report-rules]]
