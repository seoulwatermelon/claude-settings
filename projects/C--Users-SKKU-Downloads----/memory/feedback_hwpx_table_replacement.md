---
name: HWPX 표 셀 값 교체는 lxml 위치 기반 필수
description: HWPX 표 내 셀 값을 교체할 때 str.replace/find 순차 방식 금지 — 동일 값 충돌으로 잘못된 셀 교체 버그 발생
type: feedback
originSessionId: 74c29b9e-c67c-4d61-b6b5-61325995c9ae
---
HWPX 표(hp:tbl) 셀 값 교체 시 `str.replace()`, `xml.find()` 등 텍스트 순차 탐색을 사용하면 안 된다. 반드시 lxml로 파싱하여 `trs[row].tcs[col]` 인덱스로 직접 접근할 것.

**Why:** 2026-04-16 김경아 기초분석 작성 중, 카테고리별 저널 테이블과 연도별 논문실적 테이블에서 `xml.find(old_value, pos)` 순차 교체 방식이 동일 값 충돌을 일으켜 2024년, 2026년 편수 및 上位50%~ 값이 잘못 교체됨. 교체 후 새 값(new_v)이 뒤쪽 셀의 교체 전 값(old_v)과 동일할 때 이미 변환된 셀을 재매칭하는 구조적 버그.

**How to apply:** HWPX 표 셀 값 교체가 필요할 때마다 lxml 위치 기반 패턴을 사용. 단, lxml write 사이클은 1회로 제한하고, 표 이외의 고유 텍스트는 str.replace() 사용 가능.
