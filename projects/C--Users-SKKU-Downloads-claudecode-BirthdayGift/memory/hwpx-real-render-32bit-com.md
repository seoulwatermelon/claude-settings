---
name: hwpx-real-render-32bit-com
description: hwpx 실제 렌더(PDF) 검증 — 32bit PowerShell로 한/글 COM(HWPFrame.HwpObject) 호출하면 됨
metadata:
  type: reference
---
한/글 2022 COM은 64bit Python에선 안 되지만 **32bit PowerShell**(`C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe`)에서 `New-Object -ComObject HWPFrame.HwpObject` → `RegisterModule('FilePathCheckDLL','FilePathCheckerModule')` → `Open(path,'HWPX','forceopen:true')` → `SaveAs(pdf,'PDF','')` → `Quit()` 로 PDF 생성 성공(2026-10-14, 대화상자 없이 수 초).
PDF는 PyMuPDF(fitz)로 쪽 이미지화해 고아 제목·표 쪽넘김을 눈으로 확인. 스크립트: `06_Hybrid_260918/_work/topdf.ps1`.

**Why:** verify_layout.py 는 skku 템플릿 charPr 번호를 가정해 팀장님 v9 양식(다른 charPr 번호)에선 오판. 실제 렌더가 최종 기준.
**How to apply:** hwpx 수술 후 항상 PDF 렌더로 쪽 배치 확인. 관련 [[hybrid-detail-user-edits]], [[skku-report-typesetting]]
