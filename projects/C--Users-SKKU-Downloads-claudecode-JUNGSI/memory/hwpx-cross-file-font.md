---
name: hwpx-cross-file-font
description: HWPX 표를 다른 파일에서 복사하면 글자체가 깨짐 — 같은 파일에서 복제할 것
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

HWPX 표를 다른 hwpx 파일에서 복사해 넣으면 표 안 글자체(charPr)가 원본과 달라진다. 실제로 정보학 박유진 영향성 표를 재빌드본에서 복사했더니 안용수 표와 글자체가 안 맞아 회원님이 지적함.

**Why:** 셀의 charPrIDRef/borderFill 등은 그 파일 `Contents/header.xml`의 스타일 ID를 참조한다. 파일마다 header.xml이 달라, 다른 파일의 표를 넣으면 같은 ID가 다른 글꼴로 해석된다.

**How to apply:**
- 표를 보충할 땐 **같은 파일 안**의 동일 구조 표(예: 다른 후보자 표)를 deepcopy해서 글자체를 자동 일치시키고, 데이터 값만 run 단위로 교체한다.
- 교체 시 id 충돌 방지를 위해 복제 서브트리의 숫자 id를 재매핑한다.
- 삭제/이동 전엔 정상 파일(예: 안용수 섹션, 정상 빌드된 통계)과 표 역할을 대조해 오진을 막는다. 관련 실수: [[mistake-overbroad-rebuild]].
