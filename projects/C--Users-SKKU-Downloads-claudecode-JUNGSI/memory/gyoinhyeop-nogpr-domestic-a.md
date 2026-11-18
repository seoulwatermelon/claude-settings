---
name: gyoinhyeop-nogpr-domestic-a
description: no_gpr 분야(건축·국어국문) 국내A 반영 — 주요지표·생산성 대분류=국제A/국내A
metadata: 
  node_type: memory
  type: project
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

GPR 미시행(no_gpr) 분야는 인문·건축 등으로 국제 지표만으론 실적이 빈약해, 주요지표·생산성 표에 국내A(KCI/성균학술목록)를 함께 반영한다. 해당 분야: 국어국문(노대원·단독), 건축 미래융합건축(박상희·성웅기), 건축 미래건축설계(이중호·김예리) = 정시 xlsx 퀵패스 기반 5명.

- **데이터 출처:** 정시 xlsx 퀵패스를 `_빌드작업/_xlsx_qp.py`가 파싱 → `국내A_지표`(전체/주저자: 편수·IF합·IF/논문), `국내A_생산성`(전체/주저자 편수·IF합, 연도별).
- **표 형태(회원님 확정):** 주요지표·생산성 모두 **대분류 = 국제A / 국내A**. 그 아래 전체(주+공)/주저자. 생산성은 3단(대분류→전체/주저자→편수/IF합/FWCI; 국내A는 편수/IF합만).
- **구현:** `_빌드작업/_add_domestic_a.py`의 `modify_jipyo`/`modify_saeng`. 같은 파일 셀 복제로 서식 유지([[hwpx-cross-file-font]]).
- **재발 방지:** `_build_field.py`의 `if _NO_GPR:` 블록에 통합되어, no_gpr 분야 재빌드 시 국내A가 자동 반영됨(더는 수동 스크립트 재실행 불필요). 과거 전체 재빌드로 이 반영분이 날아간 적 있음 → [[mistake-overbroad-rebuild]].
