---
name: quickpass-pipeline-location
description: 퀵패스 스크립트는 E:\SANGSI\02_연구력검증(IOU,퀵패스,GPR)\_scripts 에 둔다 — 스크래치패드(%TEMP%)는 저장소 센스가 지운다. 같은 Elsevier 키로 SciVal API 도 열린다
metadata:
  node_type: memory
  type: project
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-10-01T07:56:22.370Z
---

퀵패스 파이프라인(수집·빌드 스크립트와 중간 json)은 `E:\SANGSI\02_연구력검증(IOU,퀵패스,GPR)\_scripts` 에 있다.
사용법은 그 폴더의 `README.md`.

**Why:** 2026-09-30 스크래치패드(`%LOCALAPPDATA%\Temp\claude\…\scratchpad`)의 9/29 이전 파일이
모두 사라졌다. 이 PC 는 Windows 저장소 센스(임시 파일 삭제)가 켜져 있고, Claude Code 의
`cleanupPeriodDays: 3650`(사용자가 '10년 보관'으로 기억)은 대화 기록 .jsonl 만 지킨다.
대화 기록에서 Write/Edit/heredoc 패치를 재생해 복원했다(`_scripts\_recovery\replay.py`,
살아남은 11개 중 10개 바이트 일치로 검증).

**How to apply:**
- 여러 번 다시 쓸 스크립트·데이터는 처음부터 E: 에 만든다. 스크래치패드는 일회용만.
- 윈도우 경로처럼 역슬래시가 든 문자열은 Bash heredoc 대신 Edit 도구로 고친다
  (heredoc 에서 `\\` 가 변형돼 `\20`→제어문자, 널 바이트 등으로 파일이 깨졌다).
- 같은 Elsevier 키로 SciVal API 가 열린다: 논문별 FWCI·Topic Cluster·인용 상위% 를
  수기 SciVal export 없이 받을 수 있다(수기 export 15편과 대조: Topic Cluster 15/15 일치,
  FWCI 차이는 데이터 갱신 시점 차이). IF·JCR·HCP 는 여전히 불가.

- GPR 요청서의 SCOPUS ID 칸과 SCOPUS link 칸의 authorId 가 다를 수 있다(우상은: 36810597600 /
  60538394600 — 동일인 분리 프로필, 사용자 확인 2026-09-30). 두 값을 대조하고 다르면
  cfg 의 `ScopusID_추가` 에 넣어 합쳐 수집한다(`pull_batch.py` 가 EID 로 중복 제거).
  링크 칸도 다 잡지 못한다 — 우상은은 IOU 대조로 3번째 ID(60201904800, 논문 1편)가 나왔다.
  IOU 결과본이 오면 논문 목록부터 대조할 것.
- IOU 결과본에서 받는 것은 Word Cloud·HCP·논문 누락 확인뿐. IF·JCR(이전 연도판)·Top-tier(전 학과
  매칭)·생년(학력 역산이 더 정확)은 우리 값 유지 — 2026-10-01 사용자 확인.

관련: [[quickpass-report-header]]

**스킬:** 실행 절차 전체는 `E:\SANGSI\.claude\skills\quickpass\SKILL.md` (2026-10-19). 이 메모리는 배경 사실만.
