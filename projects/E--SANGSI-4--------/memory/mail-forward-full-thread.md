---
name: mail-forward-full-thread
description: "메일 전달·답장 초안에는 원문 스레드 전체를 붙이고, 저장 후 초안을 다시 열어 확인한다"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-17T01:11:28.084Z
---

메일을 전달(FW)하거나 원문을 붙여 보고할 때는 원 메일 본문을 **스레드 전체(이전 -----Original Message----- 모두)** 그대로 붙인다. 손으로 일부만 옮겨 적지 않는다.

**Why:** 2026-11-17 철학과 설민 학과장 메일을 팀장님께 전달하는 초안에서, `w._fetch()` 결과(email.message 객체)를 dict처럼 `o['body']`로 읽다 None이 나오자 직전 메일 몇 줄만 하드코딩해 넣었다. 사용자가 "왜 이전 메일들 안 가져와져?"라고 지적하고 "실수 안 하도록 해줘"라고 함.

**How to apply:**
- `worksmail_imap._fetch(c, uid)` 는 email.message 객체 → `m.walk()` 에서 text/plain(없으면 text/html → `_html_to_text`)을 decode 해서 쓴다.
- 원문을 못 읽으면 대체 문구를 넣지 말고 멈춰서 원인을 고친다.
- 스크립트에 `assert '<가장 오래된 메일 날짜>' in orig` 같은 검사를 넣는다.
- save_draft 후 Drafts에서 초안을 다시 열어 'Original Message' 개수와 끝부분(첫 메일)을 확인한 뒤 보고한다.
- 관련 [[worksmail-mcp]] [[mail-follow-reference-html-format]]
