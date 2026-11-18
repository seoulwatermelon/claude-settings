---
name: mail-html-user-edits
description: "학과장송부메일 html은 사용자가 브라우저에서 편집·저장함 — 저장본(meta user-saved)은 재빌드 금지, 편집 중엔 빌드하지 말 것"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-06T07:52:52.478Z
---

학과장송부메일_*.html 은 사용자가 브라우저의 '편집'으로 직접 고친다. 2026-11-06 사용자가 편집 중일 때 내가 빌더로 파일을 다시 만들자
"지금 내가 편집 중인데 너가 고쳤다고?? … 저장이 되어야지" 라고 함. 그래서 html에 '저장'(Ctrl+S, 파일 덮어쓰기/다운로드)과
입력 자동 보관(localStorage, 새로고침 복원·이전 편집본 불러오기)을 넣었고, 빌더(write_page)는 meta user-saved 가 있는 파일을 덮어쓰지 않는다.

**Why:** 사용자 편집본이 내 재빌드로 사라지거나 내 수정이 사용자 화면에 안 보이는 혼선.
**How to apply:** 사용자가 html을 열어 편집 중이면 빌드하지 말고 고칠 문구(전→후)만 알려 준다. 저장본이 있으면 그 html을 문구 단위로 직접 고친다.
관련: [[user-hand-edited-final-hwpx]] [[dept-request-mail-template]]
