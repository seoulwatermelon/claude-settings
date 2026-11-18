---
name: openpyxl-column-width-trap
description: "openpyxl 미설정 열의 width는 None이 아니라 13.0 — max(dim.width or 0, w) 패턴이 좁은 열을 전부 13으로 뭉갠다"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1882205a-801b-463f-9e26-3c69dde1fcc0
  modified: 2026-08-24T04:18:50.638Z
---

openpyxl에서 `ws.column_dimensions['A'].width` 는 아직 지정한 적 없는 열이라도 **`None` 이 아니라 기본값 `13.0`** 을 돌려준다.

그래서 아래 패턴은 13보다 좁은 열을 전부 13으로 밀어버린다:

```python
# 틀림 — 5, 6, 8, 9 같은 좁은 폭이 전부 13이 된다
ws.column_dimensions[gl(i)].width = max(ws.column_dimensions[gl(i)].width or 0, w)
```

실제로 직급산정 53열 워크북에서 **41열의 폭이 깨졌고**, 화면상 표는 멀쩡해 보여서 한참 못 알아챘다.

**How to apply:**
- 폭은 **의도한 값끼리만** 비교해 한 번에 지정한다. 시트에서 현재 폭을 읽어와 비교하지 말 것.
  ```python
  want = {i: float(w) for i, (_k, _h, _g, w) in enumerate(COLS, 1)}
  for i, (_h, w) in enumerate(DASH, 1):
      want[i] = max(want.get(i, 0.0), float(w))   # 의도값끼리 비교
  for i, w in want.items():
      ws.column_dimensions[gl(i)].width = w        # 마지막에 한 번만 지정
  ```
- 헤더 그리는 함수 여러 곳에서 폭을 건드리지 말고 `apply_widths(ws)` 한 곳으로 모은다.
- 검증할 때는 저장된 xlsx의 `xl/worksheets/sheet1.xml` `<cols>` 를 직접 파싱해 의도값과 대조한다.
  (openpyxl로 다시 읽으면 연속 열이 범위로 병합돼 있어 열 단위 확인이 어긋난다)

[[excel-self-verification]]
