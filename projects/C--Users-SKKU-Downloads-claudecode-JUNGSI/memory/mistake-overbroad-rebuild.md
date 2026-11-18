---
name: mistake-overbroad-rebuild
description: 표적 수정 후 전체 재빌드로 수동/특수 작업을 날리는 반복 실수
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

한 분야만 고치면 되는데 `_build_field` 전체를 재빌드해서, config에 없는 수동/특수 작업분을 덮어써 날린 실수를 여러 번 반복함. 실제 피해: 정보학 수동 서식(선두 공백), 국어국문·건축의 국내A 반영분이 사라짐.

**Why:** 빌더는 config만으로 재생성하므로, config에 담기지 않은 결과물(수동 편집, 별도 스크립트로 넣은 표)은 재빌드 시 전부 사라진다. 특히 no_gpr 분야의 [[gyoinhyeop-nogpr-domestic-a]] 국내A, 파일럿(정보학) 수동 서식이 위험.

**How to apply:**
- 버그 수정이 실제로 영향을 주는 분야만 재빌드한다(예: apply_full/영향성 버그는 컨퍼런스 인정 분야만 해당).
- 재빌드/덮어쓰기 전, 대상 파일에 config에 없는 특수 내용(국내A, 수동 서식)이 있는지 먼저 확인한다.
- 파괴적 덮어쓰기 전 스크래치패드에 백업을 만든다(이 프로젝트는 git 없음).
- 특수 작업은 가능하면 빌더에 통합해 재빌드가 자동 반영하도록 만든다.
