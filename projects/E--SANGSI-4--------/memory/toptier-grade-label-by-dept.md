---
name: toptier-grade-label-by-dept
description: "학과 Top-tier 등급 표기 — 통계학과·경제학과는 \"A0급\", 경영학과만 \"S급\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-21T05:54:44.409Z
---

원테이블·퀵패스·메일 등에서 학과 Top-tier 저널 등급을 쓸 때
- 통계학과, 경제학과: "학과S급" 대신 **"학과A0급"**으로 쓴다.
- 경영학과: "S급" 그대로 괜찮다.

**Why:** 2026-10-21 사용자 지시. 학과마다 등급 이름이 달라서, 통계·경제학과에는 S급이라는 이름이 맞지 않는다.
**How to apply:** onetable 문안의 `(IF n / JCR n% / ‘yy / 학과S급)` 표기와 특이사항에서 학과별로 바꿔 쓴다. 다른 학과는 그 학과 리스트의 등급 명칭을 확인한다. 관련: [[onetable-report-rules]]
