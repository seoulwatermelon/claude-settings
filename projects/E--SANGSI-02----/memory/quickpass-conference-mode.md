---
name: quickpass-conference-mode
description: 우수 학술대회 실적이 있으면 퀵패스에 항상 같이 보여줌(손용석 양식) — 국제A 0편이면 컨퍼런스형, 있으면 병행형; 학과 Top-tier 컨퍼런스 + SW컨퍼런스목록 T1~T4 둘 다
metadata:
  type: feedback
---

국제A(Article) 논문이 0편이고 학술대회 논문만 있는 후보자(예: 과학수사학과 이유찬, 2026-11-04)는 퀵패스를 컨퍼런스형으로 만든다. 참고 양식: `E:\SANGSI\00_참고\2026-11-02_손용석_후보자_연구력_기초분석_20261103.docx`(우수 국제학술대회 지표 → 주요 논문 → 논문 상세(국제학술대회)).

등급은 두 기준을 같이 쓴다: ①`★학문단위별 Top-tier 리스트` 학과별 탑티어 시트의 '컨퍼런스' 행(Top-tier/2nd-tier) ②같은 파일 'SW컨퍼런스목록'(T1~T4). 과학수사학과처럼 학과 목록에 컨퍼런스가 따로 있어도 SW 목록을 무시하지 않는다(사용자 지시).

**Why:** 보안·SW 분야는 최상위 학회(S&P, CCS, USENIX Security) 논문이 핵심 실적인데 국제A 표만 쓰면 전부 0으로 보인다.
**How to apply:** `_scripts\build_pulled.py` 가 `build_conf.applies()`(국제A 0편+학술대회 있음)면 자동으로 `build_conf.convert()` 적용, 등급 판정은 `conf_tier.py`(Scopus 학회명 ↔ 목록 정식명·약칭). 2026-11-04 사용자 지시 "학술대회 실적 있을 땐 같이 보여주자": 국제A가 있어도 우수 학술대회(두 목록 중 하나라도 등재)가 1편이라도 있으면 병행형(build_conf.add_conf) — 1쪽에 학술대회 주요지표·주요 논문, 국제A는 다음 쪽부터, 상세표는 국제학술대회/학술지 둘로 나눔(예: 김영준). Word Cloud 에도 우수 학술대회 Topic 포함. 관련: [[quickpass-no-problem-notes]] [[quickpass-pipeline-location]]
