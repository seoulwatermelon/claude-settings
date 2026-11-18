---
name: skku-report-hwpx-format
description: "SKKU 행정보고서 HWPX는 「[양식] 회의자료 작성 양식」 — 반드시 skku_report.Report 사용"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7fd623ec-17c6-444d-807f-64ecb2ebd2e4
  modified: 2026-09-07T06:09:50.469Z
---

SKKU 행정보고서를 HWPX로 만들 때는 **「[양식] 회의자료 작성 양식」**(= `hwpxskill` 의 `skku` 템플릿)을 쓰고, 반드시 `scripts/skku_report.py` 의 `Report` 클래스로 생성한다. section0.xml을 손으로 쓰지 말 것.

```python
import sys; sys.path.insert(0, r'C:/Users/SKKU/.claude/skills/hwpxskill/scripts')
from skku_report import Report
r = Report(head='교원인사팀 2026. 9. 7.(월)', title='보고서 제목')
r.h1('Ⅰ. 배  경'); r.l1('1. 항목'); r.l2('1) 세목')
r.l3('① 상세'); r.dash('- 하위'); r.note('※ 참고')
r.table(rows, widths, aligns); r.blank(); r.save('결과.hwpx')
```

**Why:** 사용자가 두 번 지적한 실수 — ① 양식 파일을 그대로 빌드해 안내문("창업지원단행정실 2018. 11. 25(금)", "→ 중고딕, 14P", "가가가가…", "※ 표 양식", "※ 여 백: …")이 제출물에 남은 것, ② 다른 양식(양식참고.hwpx)으로 작성해 서식이 완전히 달라진 것. 정답 양식은 **「[양식] 회의자료 작성 양식」** 하나다.

**계층 구조 (양식 안내문 그대로):**
`Ⅰ.` 헤드라인M 16P(0칸) → `1.` 휴먼명조 15P(2칸) → `1)` 15P(3칸) → `①` 14P(4칸) → `-` 14P(6칸), 참고 `※` 중고딕 13P(4칸). 머리말 중고딕 14P, 제목은 글상자(헤드라인M 22P, 테두리 0.3mm), 표는 휴먼명조 12P **개방형 괘선**(헤더 상단 0.4mm·마지막 행 하단 0.4mm·좌우 바깥선 없음).

**How to apply:**
- 상세 스타일 맵·borderFill 배치·표 규격은 `templates/skku/README.md` 참조
- 들여쓰기는 **문자열 앞 공백**(paraPr 여백 아님), 번호는 **수동 입력**(paraPr 5~11은 OUTLINE 자동번호라 `I. Ⅰ.` 중복)
- 줄 폭 한도 실측: 본문폭 48190에서 **15pt 40em/줄**(14pt 42.9 / 13pt 46.2 / 12pt 50). `Report`가 초과 시 경고
- 빌드 후 `validate.py` + `BK/_work/{audit,pagefit}.py` 로 안내문 잔재·표 병합 정합성·쪽 배치 확인
- 한/글 COM(HWPFrame.HwpObject)은 **64bit Python에서 호출 불가**(Hancom 32bit) → PDF 렌더 검증 대신 추정 스크립트 사용

**보고서 구성 취향(사용자 지시):** 개요·인원현황 章은 넣지 말 것. **일반교원 지원 / 외국인교원 전용 지원**으로 구분하고, 항목마다 **근거 공문번호와 시행 시점**을 명시하며 최대한 상세히 쓸 것.

관련: [[bk-foreign-faculty-support-methodology]]
