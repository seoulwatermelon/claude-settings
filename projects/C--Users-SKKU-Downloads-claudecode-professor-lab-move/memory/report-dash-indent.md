---
name: report-dash-indent
description: "SKKU 보고서 들여쓰기 하우스룰 — '- ' 소항목은 '1.'보다 2칸만 깊게(과들여쓰기 금지)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 71add993-a020-4614-abd5-ccb65d5a6738
  modified: 2026-11-05T06:31:21.231Z
---

HWPX 보고서에서 `1.`(l1) 다음 줄 `-`(dash) 소항목이 **너무 오른쪽으로 밀려** 있으면 안 된다. 사용자(교무처)가 "두 칸 앞으로 당기라"고 지적.

**규칙**: `S_DASH` 들여쓰기 = **4칸**(이전 6칸에서 −2). `1.`(S_L1)이 2칸이므로 dash는 그보다 2칸 깊은 4칸이 맞다. `skku_report.py`의 `S_DASH = (16, 14, 14.0, 4)`.

**Why**: 6칸이면 부모 "1. " 본문 시작(5열)보다 3칸이나 더 들어가 계층이 과장되고 읽기 흐름이 뒤로 처진다. 2칸 차이가 적정.

**How to apply**: `-` 항목만 해당. `※`(S_NOTE, 4칸)는 건드리지 말 것. skku_report는 공유 빌더라 이 값은 전 SKKU 보고서 공통 하우스룰. 관련 [[professor-lab-space-report]] · [[hwpx-native-charts]].
