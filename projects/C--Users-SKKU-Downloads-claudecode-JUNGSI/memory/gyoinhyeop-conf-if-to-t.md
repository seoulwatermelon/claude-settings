---
name: gyoinhyeop-conf-if-to-t
description: 컨퍼런스 인정 분야 표 라벨 IF4급~IF1급 → T1~T4 (상위 IF가 T1)
metadata: 
  node_type: memory
  type: project
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

컨퍼런스 인정 분야(2027_학과추천_회신현황표_260618 F열=국제학술회의)의 결과자료에서 우수국제학술회의 IF 등급 라벨을 T 등급으로 표기한다. 대상 4개 분야: 정보학(문헌정보), 양자정보공학과(반도체), 양자정보공학과_광집적, 통계학과.

**매핑(상위 IF가 T1 — 역순):** IF4급→T1, IF3급→T2, IF2급→T3, IF1급→T4.
- 연구역량·주요지표 표: `IF4급`~`IF1급` → `T1`~`T4`
- 연구 생산성 표: `IF4 편수`~`IF1 편수` → `T1 편수`~`T4 편수`
- 논문 상세 정보 표 IF열 값: `BK 인정IF 4`~`1` → `T1`~`T4` (단, **열 제목 'IF'는 그대로 유지**)
- 주요논문 산문 목록('▮주요 논문' ▸줄글)의 'IF BK 인정IF N'도 동일 치환(사용자 확인: 산문도 바꾸는 게 맞음 → 'IF T4' 형태).
- 일반(비컨퍼런스) 분야 논문상세엔 'BK 인정IF' 값 자체가 없어(숫자/'-'만) 변환 대상 없음. 즉 IF→T는 컨퍼런스 4개 분야에만 적용.

**구현:** `_빌드작업/_relabel_if_to_t.py`의 `relabel_root(root)`(표 셀 정확일치 + 산문 부분문자열 치환). 라벨은 FULL 템플릿(_FULL_template_통계.hwpx)에 하드코딩돼 있어 재빌드 시 원복되므로, 빌더에 통합함 — `_build_field.py`(if 컨퍼런스인정)와 `_build_pilot_interim.py`(정보학) 모두 tree.write 직전 호출. 재빌드 시 자동 반영됨. 관련 [[gyoinhyeop-conf-field-full-tables]], [[mistake-overbroad-rebuild]].
