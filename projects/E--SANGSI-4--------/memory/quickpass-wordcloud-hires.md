---
name: quickpass-wordcloud-hires
description: "퀵패스 Word Cloud는 IOU 그림(700x400, 흐림) 대신 SciVal Topic으로 직접 그린 고해상도 그림을 쓴다"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-21T08:28:37.108Z
---

퀵패스 Word Cloud는 IOU 결과본 그림을 그대로 쓰지 않는다. `02_연구력검증(IOU,퀵패스,GPR)\_scripts\make_wordcloud.py`로 실적 포함 논문의 SciVal Topic 이름을 2800x1600 px로 다시 그린다. 글자 크기는 논문 수로 정해서 IOU와 같은 내용이 되게 한다. B 경로 빌더(`build_pulled.py`)는 빌드할 때 이 그림을 자동으로 넣는다.

**Why:** 2026-10-21 사용자 지적("word cloud 해상도 왜이래?"). IOU 그림은 700x400이라 보고서 폭 15cm로 키우면 흐리다. 사용자가 새로 그리는 방식을 앞으로도 쓰라고 함.
**How to apply:** 새 배치는 빌드만 하면 된다. 예전 검증본은 make_wordcloud.py로 그림만 바꾸고 다시 렌더한다. A 경로(build_report, 통계학과 방식)는 아직 IOU 그림을 쓰니, 그 배치를 다시 만들 때는 바꿀지 사용자에게 묻는다. 관련: [[quickpass-pipeline-location]]
