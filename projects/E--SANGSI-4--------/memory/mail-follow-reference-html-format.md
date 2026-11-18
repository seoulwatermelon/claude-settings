---
name: mail-follow-reference-html-format
description: 참고 메일을 주고 메일 초안을 요청하면 원문 HTML 서식(글씨 크기·색·형광펜·굵게·밑줄·hr)을 그대로 따라야 함 — 일반 텍스트 초안 반려(2026-11-03)
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-11T06:32:28.575Z
---

**재발(2026-11-11, 교원인사협의회 면접 안내 강복경·마틴겔만): 또 일반 텍스트로 쓰고 영문은 항목(오프라인 선택지·회신 요청)까지 바꿔 "양식은 참조한 대로 해줘야지. 이거 계속 실수하네" 지적.** 참고 메일이 있으면 첫 초안부터 HTML 원문을 받아 이름·일시·연락처·서명만 바꾼다. 구성·문구·선택지는 바꾸지 않는다(후보자 사정에 맞춘다는 이유로도 X — 바꾸고 싶으면 초안은 원본대로 두고 제안만). 원 발신자 readReceipt 이미지는 제거. 예시 스크립트: 스크래치 coun\make.py.

참고 메일(예: 정우현 책임 FW 메일)을 따라 메일을 쓰라고 하면 문구뿐 아니라 **디자인·글씨 크기·색상 서식도 그대로** 따른다. 일반 텍스트 초안은 반려됐다(2026-11-03, 통계·유학동양 추천서류 요청/채용심의위 참석 요청).

**Why:** 학과장·학장에게 가는 공식 안내 메일은 마감일(빨강·형광 16px), 서류명(형광 굵게) 등 강조 서식이 핵심 전달 수단이다.

**How to apply:** 참고 메일 HTML을 IMAP으로 받아(worksmail_imap._fetch → get_body('html')) 문구만 치환하고, 서명은 사용자 보낸메일 HTML에서 승주완 서명 블록을 가져온다. 저장은 save_draft 의 html_body 인자(2026-11-03 추가, MCP 재시작 전에는 스크립트에서 worksmail_imap.save_draft 직접 호출). 예시 스크립트: 스크래치 build_html_drafts.py. **수신자 주소는 찾기 어려우면 빈칸으로 두고 넘어간다**(사용자 지시 2026-11-03 "수신자 넣기 힘들면 안넣어도 돼 기억해" — 주소 찾느라 느린 한글 검색 반복 금지, 이미 아는 주소만 넣음). to="" 가능. 로컬 파일 첨부는 attach_files(E:\SANGSI 등 허용 폴더, 합계 25MB). GPR 요청 메일(박희태 hita3@skku.edu)은 gpr_single_<YYMMDD>_<학과 n>.xlsx + CV·요청서 zip 을 배치 4_GPR 에 만들어 첨부. 참고 메일의 첨부 양식도 그대로 붙인다: save_draft 의 attach_from_uid/attach_from_folder/attach_names(서버), 스크립트에서는 attach_uid/attach_folder/attach_names. 관련: [[worksmail-mcp]] [[copy-paste-plain-text]] — 톡 복붙용은 여전히 일반 텍스트.
