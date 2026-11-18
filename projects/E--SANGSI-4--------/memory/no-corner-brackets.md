---
name: no-corner-brackets
description: "메일·보고서에 「」 낫표 쓰지 말 것(AI스러움) — 인용·강조는 작은따옴표 ' ' 사용"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-06T07:41:05.724Z
---

메일·팀장 보고·한글 보고서 등 사용자에게 나가는 글에 「 」(낫표)를 쓰지 않는다. 인용 문구나 문서명은 작은따옴표 ' ' 로 쓴다.
예: '실적이 나오기 직전의 Fresh PhD를 타겟하여 채용후 관리', '이미 연구 기반이 있는 핵심 분야'.

**Why:** 2026-11-06 경제학과 팀장 보고에서 사용자 "「 이런 기호 쓰지마 AI 스러워. 차라리 ' 를 써".
**How to apply:** build_mail.py 같은 빌더 문자열에 넣을 때는 파이썬 작은따옴표 문자열 안이므로 \' 로 이스케이프. 담당자 메모(메일에 복사되지 않는 부분)는 예외지만 새로 쓸 때는 피한다. 관련: [[table-header-no-page-numbers]] [[copy-paste-plain-text]]
