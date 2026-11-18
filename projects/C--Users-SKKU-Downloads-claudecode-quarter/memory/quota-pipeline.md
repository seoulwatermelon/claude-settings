---
name: quota-pipeline
description: 임용쿼터 산정 업무의 기준·규칙과 quarter 폴더 파이프라인 구조
metadata:
  type: project
---

임용쿼터(교원인사규정 제12조제2항, 특정대학 학사 60% 미만 원칙) 산정 업무.
판정 규칙: 총인원<=3 제외 → T/O 0이면 해당없음 → (최다+1)/(총+TO)>=60% 이면 "쿼터대상"
→ (최다+TO)/(총+TO)>=60% 이면 "조건부". 이 규칙은 2026.3 확정본 81건을 100% 재현함(회귀테스트).

산정 대상: 교직원구분=교원 AND 직종코드=전임교원 (외국인교육전담=(외)전임교원, 총장 제외),
정년예정일자<=퇴직기준일 제외, 다음 학기 임용예정자 포함. 그룹 단위는 T/O 배정 학문단위(채용분야).

`C:\Users\SKKU\Downloads\claudecode\quarter` 에 파이프라인 구축:
`python _scripts/run_all.py` 한 줄로 회귀검증→워크북 생성→Excel COM 재계산→결과 대조까지 실행.
새 회차는 `_scripts/config.py` 의 파일명·기준일 3개만 고치면 됨.
업무 절차는 `임용쿼터 산출 매뉴얼.txt`, 코드 구조는 `_scripts/README.md`.

관련: [[excel-formula-traceability]]
