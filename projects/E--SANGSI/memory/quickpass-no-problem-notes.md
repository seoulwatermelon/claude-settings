---
name: quickpass-no-problem-notes
description: "퀵패스 결과물(논문 상세표 비고 등)에 \"Scopus 미색인(Citations·FWCI 미산출)\"처럼 문제 있어 보이는 문구 금지"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-22T08:18:34.222Z
---

퀵패스 검증본 hwpx/pdf의 비고·표에 "Scopus 미색인", "Citations·FWCI 미산출" 같은 문구를 쓰지 않는다.
2026-10-22 추가: "(문헌유형 제외)", "CV 미기재"도 쓰지 않는다. 제외 여부는 '실적 포함 여부' 열(X)이 보여 주고, CV 대조 결과는 사용자에게 말로만 보고한다(엑셀은 CV_확인 열에만 남김).
2026-11-04 추가: "JCR 미수록"도 금지(이상해 보임). build_pulled.to_item 이 `_사유`를 비고로 내보내지 않게 고침.
비고는 `Article,국제A`처럼 유형·등급 태그만 쓴다. 값이 없으면 칸을 `-`로 둔다.

**Why:** 2026-10-21 사용자 지시. 이런 문구가 있으면 논문이나 후보자에게 문제가 있는 것처럼 보인다. 실제로는 Scopus 등록이 늦었을 뿐인 정식 논문이었다(강복경 CEJ 2026).
**How to apply:** 수기 추가 논문(cands.py EXTRA, build_pulled 수기 건)의 근거는 스크립트 주석·`_출처`·`_사유`에만 남기고, 결과물에 나가는 `_비고추가`는 비운다. 값이 비는 이유는 사용자에게 보고할 때 따로 설명한다. 관련: [[quickpass-report-header]] [[quickpass-conference-mode]]
