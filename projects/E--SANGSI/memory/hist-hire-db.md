---
name: hist-hire-db
description: 과거 합격자 연구력 DB(2019.8~2024) 위치·재생성 절차·가림 원칙 — 25~26년 자료 추가 시 참고
metadata:
  node_type: memory
  type: project
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-27T05:24:55.177Z
---

과거 합격자 연구력 DB: E:\SANGSI\02_연구력검증(IOU,퀵패스,GPR)\과거합격자_연구력DB_2019-2024.xlsx (140명, 2026-10-27 마감).
빌더·자료: _scripts\hist_db\ (json\ 1인 1파일 → build_hist_db.py, txt\ 는 redact_txt.py <스크래치 원문 txt 폴더>로 생성).
문서별 실명·문구 가림 목록 redact_terms.json 은 DB 폴더 밖(세션 스크래치 hist\)에 둠 — 새 세션에서는 다시 만들어야 할 수 있음.

**Why:** 팀장님 지시 — 상시채용 후보를 과거 합격자와 비교. 평가자 루프(r20~r69)로 정확성 A축은 r60 이후 대부분 40/40, 전체 최고 99점에서 사용자가 마무리 지시.
**How to apply:** 25~26년 자료가 오면 같은 json 형식으로 넣고 build_hist_db.py 재실행. 가림 원칙(경쟁 후보·교원·지도교수·외부위원 소속·특정 가능한 수식어)은 작성기준 시트와 [[user-hand-edited-final-hwpx]] 처럼 재생성 금지 대상 아님. 열 번호 하드코딩 금지(머리글 이름으로).
