---
name: mail-draft-style
description: "사용자(교원인사팀 승주완) 업무 메일 초안은 보낸메일함의 본인 양식·서명을 그대로 쓰고, 첨부는 E:\\SANGSI 아래로 사본을 옮겨 붙인다"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7d620b3e-3c89-4885-8caf-4acc5644e29d
  modified: 2026-11-18T02:45:27.814Z
---

메일 초안을 쓸 때는 먼저 보낸메일함(Sent Messages)에서 최근 메일을 읽어 사용자 양식을 따른다.
- 시작: "안녕하세요. 저는 교원인사팀 승주완입니다."
- 끝: "이상입니다." → "그럼 오늘도 좋은 하루 보내세요." → "감사합니다." 뒤에 들여쓴 서명 블록(성명, 교원인사팀 / 책임, 주소, Tel·Mobile, Email)
- 제목은 "[교원인사팀] … 의 건" 형식을 자주 씀

worksmail save_draft 의 attach_files 는 허용 폴더(E:\SANGSI 등)만 받는다. E:\Daily 같은 곳의 파일은 E:\SANGSI\_메일첨부_<주제> 폴더로 사본을 만들어 붙인다(원본 그대로).

**Why:** 2026-11-18 공모전 제출 메일을 일반 형식·첨부 없이 만들었다가 "내 메일 서명이나 기존 양식 사용한 거 맞아?", "왜 첨부가 안 돼?" 지적을 받음.
**How to apply:** 메일 초안 요청 시 서명·양식 확인과 첨부 경로 처리를 처음부터 함께 한다. 관련: [[contest-skku-ai-challenge]]
