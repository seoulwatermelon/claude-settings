---
name: risk-system
description: 03_위험도시스템 — 교원 이직 위험도 월간 자동 분석 Python 시스템의 구조와 실행법
metadata: 
  node_type: memory
  type: project
  originSessionId: ac4ba400-9501-46e3-bb5b-dfaac66a8d35
---

`03_위험도시스템\` 은 S급 교원의 이직 징후를 매월 자동 스코어링하는 Python 시스템. [[project-overview]]의 센싱 체계를 자동화한 것.

**진입점:** `monthly_run.py` (월 1회 실행 상정, Windows Task Scheduler cron)
- `python monthly_run.py` — `input\` 폴더 첫 .xlsx 명단 사용
- `python monthly_run.py --input path.xlsx`
- `python monthly_run.py --make-sample` — 샘플 명단 생성

**모듈:** `config.py`(임계값·기관ID·가중치 중앙관리), `scopus_client.py`(Elsevier/Scopus API), `analyzers.py`(공저자·본인 affiliation 변경·Q1 급증 분석 + 스코어링), `news_analyzer.py`(Google News RSS로 영입/수상/발표 신호), `db.py`(SQLite `data/retention.db`, upsert), `excel_io.py`(명단 로드·리포트 출력).

**스코어 가중치(config.py):** 신규 외부 공저자 +2, 본인 affiliation 변경 +2, Q1 급증 +1 / 뉴스 영입 +3, 수상 +1, 발표 +1. 임계값: 신규외부공저자 ≥3, Q1급증 비율 2.0배·최소 3편, CiteScore Q1 = 75퍼센타일.

**출력:** `output\risk_{날짜}.xlsx` + DB 저장 + 콘솔 요약표(합계 내림차순).

**기관 ID:** SKKU=60007511 / 경쟁대 힌트 = 서울대·연세대·고려대·KAIST·POSTECH.

**의존:** Elsevier API 키 필요(환경변수). Python 3.12(pyc 캐시 기준).
