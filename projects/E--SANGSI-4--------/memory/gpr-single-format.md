---
name: gpr-single-format
description: "gpr_single.xlsx 작성 규칙 — 이번 요청 후보자 행만 남기고, 끝에 추천대학·추천학과 2열 추가"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-04T00:34:51.402Z
---

`E:\SANGSI\02_연구력검증(IOU,퀵패스,GPR)\gpr_single.xlsx`(GPR 요청용)는 매번 이번 배치 후보자 행만 남기고 이전 행은 지운다. 머리글 skku_id~Group(A~H) 뒤에 I「추천대학」, J「추천학과」를 붙여 후보자를 추천한 대학·학과를 적는다(예: 법학전문대학원 / 과학수사학과).

**Why:** 2026-10-28 사용자 — GPR 담당 쪽에 보낼 때 추천 대학/학과를 같이 보내기로 함.
**How to apply:** 퀵패스 후 gpr_single 작성 시. 고치기 전 `_scripts\_backup\gpr_single_<MMDD>_*.xlsx` 백업. Scopus ID가 여러 개면 쉼표로 함께.

**Affiliation·Country 는 영어, SciVal(=Scopus 저자 프로필 현재 소속) 값 그대로**(2026-11-04 사용자 지시). CV상 지금 소속과 달라도(박사 때 기관이 남아 있어도) 고치지 않는다. SciVal API에는 소속이 없으므로 Scopus `/content/author/author_id/<ID>?view=ENHANCED` 의 affiliation-current → ip-doc 에서 기관명(학과·스쿨이면 parent-preferred-name)과 address.country 를 가져온다.
