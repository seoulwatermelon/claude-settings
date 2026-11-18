---
name: hwpx-direct-edit-lineseg-and-render
description: "HWPX section0.xml 직접 편집 시 낡은 linesegarray가 글자를 눌러 한 줄에 욱여넣는 문제와, 한글 COM으로 PDF 렌더해 눈으로 확인하는 절차"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 71add993-a020-4614-abd5-ccb65d5a6738
  modified: 2026-11-10T02:47:05.160Z
---

HWPX 문단의 글자를 바꾸거나 문단을 복제해 넣을 때는 그 문단의 `<hp:linesegarray>…</hp:linesegarray>`를 **지운다**. 그리고 완료 보고 전에 반드시 한글로 PDF를 뽑아 직접 본다.

**Why:** 2026-11-09 `_261109.hwpx`에서 문단을 복제하면서 원본의 줄배치(lineseg 1줄)를 그대로 뒀더니, 한글이 긴 문장을 그 한 줄 폭에 맞춰 자간을 눌러 그렸다(※주석이 거의 못 읽을 정도). 그때는 XML 파싱과 PageCount만 확인하고 "완료"라고 보고했고, 사용자가 다음 날 "주문이 적용이 잘 안 된 것 같다"고 지적했다. lineseg를 지우면 한글이 열 때 다시 조판한다(2026-11-10 확인).

**How to apply:**
- 편집 스크립트에 `LSEG = re.compile(r'<hp:linesegarray>.*?</hp:linesegarray>', re.S)`를 두고, 텍스트를 바꾼 문단·복제한 문단·새로 만든 표 셀·표를 감싼 문단에 모두 적용한다. 손대지 않은 문단은 그대로 둔다.
- 문단을 다른 문단의 틀로 쓸 거면, 원본을 지우는 편집보다 **먼저** 틀 문자열을 변수에 받아 둔다.
- 렌더: `hwp.Open(path,"HWPX","")` → `hwp.SaveAs(out,"PDF","")`가 이 PC에서 동작한다(`scratchpad/topdf.py`). `CreatePageImage`는 계속 실패하니 쓰지 않는다. PDF는 PyMuPDF(`fitz`)로 쪽별 PNG나 8쪽 한 장 모음을 만들어 Read로 본다(poppler 없음).
- `taskkill /IM Hwp.exe`를 무조건 돌리지 않는다. 사용자가 한글을 열어 두었을 수 있으니 먼저 `tasklist`로 확인하고, 내가 띄운 PID만 종료한다.
- 이 보고서 본문 폭은 48188 HWPUNIT: 14pt dash 줄 약 34자, 15pt `1.` 줄 약 32자, 13pt ※ 줄 약 37자(숫자·영문은 반 자). 사용자는 항목을 한 줄에 맞추는 편이라 넘치면 문장을 줄인다.
- 병합 머리글 표: 세로 병합 셀은 `cellSpan rowSpan="2"` + `cellSz height`를 2행분으로, 다음 행에서는 그 열의 `hp:tc`를 생략한다. 가로 병합은 `colSpan="2"` + 폭 합. 2단째 머리글은 본문 괘선(bf 6/7/8)에 굵은 글자.

- 사용자가 한글에서 저장한 뒤에는 문단 id가 0으로 바뀌는 것이 있다(2026-11-10 확인). 본문 문단은 `<hp:t>` 전체 텍스트로, 표는 표를 품은 문단 id로 찾는다. 매 작업 전에 사용자의 현재 파일을 새로 풀어 그 위에서 고친다.
- 좁은 열에 행을 복제해 넣을 때는 본문과 반대로 원본 셀의 lineseg를 **남긴다**(지우면 "중앙학술정보/관"처럼 꺾임).
- 표 편집 도구는 `scratchpad/build_G.py`의 `Table(pid)`(`get/put(r, colAddr)`, `insert_after`) + `build_J.py`의 `delete_row`. 이 절차는 hwpxskill SKILL.md "사용자가 손본 HWPX를 직접 편집할 때"에도 옮겨 둠.

관련: [[professor-lab-space-report]] · [[hwpx-native-charts]] · [[report-voice-team-lead]]
