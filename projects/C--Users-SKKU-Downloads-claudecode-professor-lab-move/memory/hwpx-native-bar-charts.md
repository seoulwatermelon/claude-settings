---
name: hwpx-native-bar-charts
description: SKKU HWPX 보고서에 한글 네이티브 막대그래프·도식을 표-셀 음영으로 넣는 법과 렌더 필수조건
metadata:
  node_type: memory
  type: reference
  originSessionId: 71add993-a020-4614-abd5-ccb65d5a6738
  modified: 2026-11-04T05:27:23.847Z
---

SKKU 회의자료 HWPX(`skku_report.Report`)에 **한글에서 편집 가능한 막대그래프·도식**을 PNG 없이 표-셀 음영으로 그린다. 2026-11-04 사용자 한글에서 렌더 확인 완료.

**도구 (`C:/Users/SKKU/.claude/skills/hwpxskill/scripts/skku_report.py`)**
- `r.add_fill(face, bw='0.1 mm', bc='#000000', alpha='0')` → 색 채움 borderFill 등록, id 반환.
- `r.table(..., cell_fills={(행,열): fid})` → 셀 단위 음영(막대·배지).
- 헬퍼 `viz.py`(스크래치패드): `diverging_bar`(발산형), `grouped_bar`(묶은막대), `hbar`(가로단일+기준선 mark), `timeline2`(2단계 박스·화살표 도식).

**렌더 필수조건 (이거 틀리면 "색/막대 하나도 안 보임"으로 무음 실패)**
1. **커스텀 borderFill id는 기존 최대 id 바로 다음부터 연속**이어야 한다. 28 뒤 50처럼 공백을 두면 한글이 참조를 순번으로 해석해 빈자리로 빠져 **채움이 통째로 안 보인다.** `_inject_borderfills`가 max_id+1로 재번호 + section0.xml 참조 remap.
2. borderFill 요소 순서: slash·backSlash·4borders·**`<hh:diagonal>`**·`<hc:fillBrush>`. diagonal 빠지면 한글이 fillBrush를 무시.
3. `alpha="0"` = **불투명(색 보임)**. hatchColor `#FF000000`. (양식 원본 id 13·25·26과 동일 구조로 맞춘 것.)
4. 검증은 `validate.py`(well-formed)만으로 부족 — 위 3개는 한글에서 실제로 열어 확인해야 드러난다.

**경험칙**: 색이 안 보인다고 할 때 추측으로 fillBrush 형식만 바꾸지 말 것. 양식 `_reference.hwpx`의 **실제 색칠된 셀(id 13 등)을 바이트 단위로 복제**하고, 2~4칸짜리 테스트 파일(색/alpha 변형)을 사용자가 열어 어떤 칸이 보이는지로 원인을 못박는 게 최단경로였다.

관련: [[professor-lab-space-report]]
