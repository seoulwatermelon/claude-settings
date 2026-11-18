---
name: gyoinhyeop-conf-field-full-tables
description: 컨퍼런스 인정 학문분야는 연구역량·주요지표·생산성 표를 FULL 양식(우수국제학술회의)으로
metadata: 
  node_type: memory
  type: project
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

교인협 자료에서 **컨퍼런스 인정 학문분야**(회신현황표 F열='국제학술회의 논문 인정분야': 문헌정보·국어국문·통계·양자정보·응용AI)는 3개 표를 FULL 양식으로 만든다:
- **연구역량(표7)**·**후보자 주요지표(표13/22)**: 국제A(6열) + **우수국제학술회의(BK)**(FWCI·IF4급·IF3급·IF2급·IF1급) 추가
- **생산성(표14/24)**: 블록별 국제A(편수/IF합/FWCI) + **우수국제학술대회**(IF4~IF1 편수·전체편수) 행 추가

**데이터 소스**: 퀵패스 주요지표·생산성 표에 이미 있음 → config `주요지표`·`생산성` grid에 포함(추출기 변경 불필요). 우수국제학술회의 열은 주요지표 grid의 **마지막 6열**(FWCI,IF합,IF4~IF1급) — 학과우수학술지 유무로 grid 열수가 다름(통계 16·양자정보 14)이라 음수 인덱스로 접근. 우수 FWCI는 2자리 반올림.

**표 양식**: 팀장님이 편집한 `_FULL_template_통계.hwpx`(표7/13/14)를 **템플릿으로 고정, 값만 채움**(구조·서식·줄간격 절대 변경 금지). `_full_tables.py` `apply_full()`가 표7/13/14/22/24 교체. 빌더는 config `컨퍼런스인정`=True일 때 자동 적용(_build_field.py + 파일럿). [[gyoinhyeop-bigo-conf-toptier]]
