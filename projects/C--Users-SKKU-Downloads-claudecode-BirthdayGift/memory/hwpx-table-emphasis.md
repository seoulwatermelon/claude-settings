---
name: hwpx-table-emphasis
description: hwpx 표에서 특정 행만 크게 쓰려면 skku_report.table(char_rows=...) — 2026.9.29. 내가 추가한 기능
metadata:
  type: reference
---

`skku_report.Report.table()` 에 **`char_rows={행index: charPrIDRef}`** 를 넘기면 그 행만 글자크기가 달라진다. 2026.9.29. 내가 추가했고, 인자를 안 주면 기존과 동일하게 동작한다(하위 호환 확인됨).

```python
T([...], [5.9, 2.2, 5.9], header_rows=3, char_rows={0: 9, 1: 14})
```

charPrIDRef ↔ 크기 : **8=16pt · 9=15pt · 14=14pt · 17=13pt · 31=12pt(표 기본)**

행 높이도 해당 행의 실제 크기로 다시 계산되므로 글자가 잘리지 않는다. 폭 검사(`_check`)도 그 행 크기 기준으로 돈다.

## 표에서 한 행을 부각하는 방법 (효과 順)

1. **글자크기** — `char_rows` 로 12pt → 15pt. 가장 확실하다.
2. **머리행 음영** — `header_rows` 를 늘리면 그 행까지 음영이 들어간다. 목표 행을 맨 위에 두고 `header_rows=3` 처럼 잡으면 제목부 전체가 한 덩어리로 보인다.
3. **줄 수** — 셀 텍스트에 `
` 을 넣으면 행이 그만큼 높아진다. 15pt 2줄이면 12pt 1줄의 약 2.5배 높이가 된다.
4. **글자 사이 공백** — 「목    표」처럼 자간을 벌리면 표제처럼 읽힌다. 한글 공문서 관행.

색·굵기는 템플릿의 charPr/borderFill 에 묶여 있어 이 경로로는 못 바꾼다. 필요하면 `templates/skku/` 의 header.xml 에 charPr 를 추가해야 한다.

관련: [[skku-report-typesetting]] · [[report-format]]
