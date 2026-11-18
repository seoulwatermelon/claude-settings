---
name: gyoinhyeop-reviewer-dept-classification
description: 교인협 심사위원 내외구분은 학과별로 조회해야 함(같은 이름이 학과마다 내부/외부 다름)
metadata: 
  node_type: memory
  type: project
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

교인협 자료에서 심사위원 내외구분(내부/외부)·추천구분·학교는 심사위원명단_v3에서 조회하는데, **같은 이름의 교수가 학과마다 내부/외부가 다를 수 있음**(자기 학과=내부, 타 학과 외부심사=외부).

예: 이명재는 물리학과 소속 교수 → 물리학과 심사에선 **내부**지만, 타 학과 외부위원으로도 등재돼 전역 조회 시 외부로 잘못 나옴. 이 때문에 물리학과가 내부1+외부4로 표(내부2·외부3)와 안 맞았음.

**해결**: WM을 `(학과, 이름)` 키로 만들고 `look(nm)`은 `WM.get((FIELD['학과'], nm))` 우선, 없으면 전역. `_extract_config.py`에 반영됨.

2단계표·외부의견표 위원 정렬: 내부 = 전공적합 내외='내부'(config 순서), 외부 = 내외='외부'를 **학과추천 먼저** 정렬 후 상위 3명(=설문 응답자와 일치해야 함). [[gyoinhyeop-eval-table-2baesu]]
