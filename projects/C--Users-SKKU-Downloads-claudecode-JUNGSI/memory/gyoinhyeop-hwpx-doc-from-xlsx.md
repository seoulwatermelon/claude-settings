---
name: gyoinhyeop-hwpx-doc-from-xlsx
description: 결재문서(수기결재) 붙임2 표는 확정 엑셀 ver01 을 그대로 읽어 만든다 — 파이썬 재계산본을 쓰면 담당자 확정값과 어긋난다
metadata:
  type: project
---

교인협 직급산정 결재문서(`(수기결재)…임용직급 부여 및 재직경력 인정.hwpx`)의 붙임2 표는
**`신임교원 직급산정_…_ver01.xlsx` 를 유일한 근거로** 만든다(`_scripts/doc_source.py`).
파이썬 산정 파이프라인(rank_rules/confirmed.py) 재계산본을 쓰면 담당자가 엑셀에서 직접 손본
확정 직급·확정 연차·승진심사 시기가 반영되지 않아 결재본과 갈린다(김의겸 4년→1년,
전용현 4년→5년, 조제윤 종료일 등이 실제로 어긋났음).

hwpx 표 갱신 시 지켜야 할 양식 사항:
- 마지막 행은 굵은 바깥선용 borderFill `12/13×8/10` (중간 행은 `14/9×8/11`)
- lineseg 는 문단당 1개, vertpos 는 접힘 줄 수 누적. 줄 간격은 칸마다 다름
  — 0~4열 900, 5열(주요경력) 1200, 6~9열 1100
- 대학명과 학과명이 같으면 소속칸은 1문단 (원본에 같은 값 반복은 없음)
- zip 은 원본의 엔트리 순서·compress_type 그대로, mimetype 은 첫 항목·무압축
- `<hp:lineBreak/>` 는 넣지 않는다. 원본의 수동 줄바꿈은 공백 없는 긴 영문 토큰 때문이었고,
  현재 표는 모든 줄에 공백이 있어 한/글 자동 접힘으로 충분

관련: [[hwpx-cross-file-font]] [[hwpx-text-extraction-pitfall]] [[verification-two-axes]]
