---
name: inplace-save-guard
description: 같은 파일을 읽고 그 자리에 저장하는 스크립트는 저장 직전에 _archive 로 날짜·시각 붙인 사본을 떠야 한다
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1882205a-801b-463f-9e26-3c69dde1fcc0
  modified: 2026-10-26T03:52:01.190Z
---

**같은 파일을 읽고 그 자리에 저장하는 스크립트는 저장 직전에 `_archive` 로
날짜·시각 붙인 사본을 떠라.** 본보기는 `01_교원확보율/_scripts/writer.py` 의
`_guard_and_backup`(①OUT 이 입력과 같으면 멈춤 ②이미 있으면 사본을 뜸)이다.

```python
_BAK = os.path.join(_ROOT, '<연도>', '<단계>', '_archive')
os.makedirs(_BAK, exist_ok=True)
_r, _e = os.path.splitext(os.path.basename(F))
shutil.copy2(F, os.path.join(
    _BAK, f'{_r}_수정전_{datetime.datetime.now():%y%m%d_%H%M%S}{_e}'))
```

**Why:** 담당자가 엑셀에서 손으로 고쳐 둔 것이 말없이 사라진다
([[mistake-output-overwrote-source]] 가 그 사고다). 더 나쁜 것은 **확정 산출물이
뒤쪽 단계의 입력**인 경우다 — 한 번 잘못 덮어쓰면 복구 경로가 없다.
2026-10-26 정리에서 실제로 그런 세 곳을 찾았다(평가자 지적).

```
01_초빙세부내역\02_산출물\…\성균관대_2027_정시채용_한영통합.xlsx
    ← fix_2200.py · fix_swap.py 가 읽고 제자리 저장
    → 02·03·05·08단계 스크립트가 읽는다
02_공고_모집요강\02_산출물\2027_교수초빙_회신체크리스트.xlsx
    ← create_competition_sheet.py 가 읽고 제자리 저장
    → 03·05·09단계 스크립트가 읽는다
09_면접일정조율\02_산출물\…일정표_260803_ver25.xlsx
    ← _rebuild_calendar_view.py 가 읽고 제자리 저장
```
네 곳 전부 가드를 붙였다. **`01_원본데이터`(받은 자료)를 제자리 덮어쓰는
스크립트는 0건**이다 — 학과 회신·추천서·시스템 조회 결과는 안전하다.

**How to apply:**
- 새 스크립트를 쓸 때 `wb.save(F)` 의 `F` 가 `load_workbook(F)` 의 것과 같은지 보라.
  같으면 가드를 붙이거나 **새 이름으로 저장**하라(후자가 더 낫다).
- 가드를 붙인 뒤 **실제로 백업이 생기는지 시험하라.** 구문 통과는 증거가 아니다.
  시험은 임시 폴더에 트리를 복제해서 하고, **가드 전체를 실제 루트로 돌리지 마라** —
  내가 그렇게 해서 진짜 `_archive` 에 백업 2개를 만들어 놓고 지웠다.
  대상을 알아낼 때는 `_SRC_FILE = …` 한 줄만 떼어 평가하면 된다.
- 검사 축으로 둘 때: `load_workbook`/`open` 의 인자와 `save` 의 인자가 같은 경로로
  해석되는데 그 사이에 `copy2`/`copy` 가 없는 곳.

[[mistake-output-overwrote-source]] [[path-rewrite-traps]] [[jungsi-folder-structure]]
[[excel-continuous-rows]]
