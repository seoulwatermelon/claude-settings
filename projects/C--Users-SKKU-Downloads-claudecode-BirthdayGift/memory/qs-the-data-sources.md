---
name: qs-the-data-sources
description: QS·THE 대학평가 원데이터 1차 출처 주소와 판번 식별법 — nid 오인 사고 재발 방지
metadata:
  type: reference
---

QS·THE 순위 수치를 인용할 때는 **반드시 아래 1차 출처에서 직접 받고, 판번을 종합순위로 검증**한다. 2차 기사·검색 결과를 그대로 옮기지 말 것.

## QS World University Rankings

```
https://www.topuniversities.com/rankings/endpoint?nid=<NID>&page=0&items_per_page=50&tab=indicators&countries=kr&sort_by=rank&order_by=asc
```

| 판 | nid |
|---|---|
| 2027 | `4153156` |
| 2026 | `4061771` |
| 2025 | `3990755` |

- `countries=kr` 빼고 `page=0,1,2`로 돌리면 세계 순위(진입선 산출용).
- **접근 조건**: 브라우저 User-Agent + `Referer: https://www.topuniversities.com/world-university-rankings` 헤더 필수. 없으면 403.
- 지표명 주의: 지속가능성의 실제 키는 `Sustainability`가 아니라 **`Sustainability Score`**. 파싱 시 누락되면 가중손실 검산이 약 0.87점 어긋난다.
- nid는 `https://www.topuniversities.com/world-university-rankings?countries=kr` HTML에서 추출.

## THE World University Rankings

```
https://www.timeshighereducation.com/cms-academic/sites/default/files/ranking-dataset/world-university-rankings/<판>/world-ranking/ranking-dataset.json
```
`<판>` 에 edition year 를 넣는다. **`latest` 는 404 다**(2026-10-06 확인). 2026 은 200, 2024·2027 은 404 — 즉 **미발표 판은 조회할 수 없다**.
2,191개 기관 전량. 헤더 없이 열린다. 응답은 `{total,count,institutions:[...]}` 이고 기관 한 건의 실제 수치는
`r['results'][0]['level1']` 의 `overall_rank_number` · `overall_score_display` 이며 pillar 5개는 `level2s`.
국가는 `r['country']`(`South Korea`). pillar 단위까지만 공개되며 18개 metric 개별 점수는 **구조적으로 취득 불가**.

### THE 성균관대 실측 (2026-10-06 조회)

| 판(edition) | 발표 | 세계 | 점수 | 국내 | 사립 |
|---|---|---|---|---|---|
| 2025 | '24.10. | **145위** | 62.5 | 4위 | 2위 |
| 2026 | '25.10. | **87위** | 68.3 | 4위 | 2위 |
| **2027** | **'26.9.30. 발표** | **68위** | — | **3위** | **1위** |

- 2026판 국내 서열 — 서울대 58 · KAIST 70 · **연세대 86** · 성균관대 87 · POSTECH 141 · 고려대 156.
  **2025·2026판은 국내 4위·사립 2위**(연세대가 앞)이고, **2027판에서 국내 3위·사립 1위**가 된다. 수식어를 쓸 때 판을 반드시 밝힐 것.
- **2027판은 데이터셋 엔드포인트가 404 여도 이미 공표된 것이다**(발표 '26.9.30., 2,297개 기관, 전년 87위에서 19계단 상승, 4년 연속 상승).
  데이터셋은 2025·2026판만 서비스되므로 **404 를 미발표로 단정하지 말고 보도자료·언론을 교차 확인**할 것.
- THE 는 edition year 와 발표연도가 1년 어긋난다(2025판 = 2024년 10월 발표). **한 문장 안에서 두 규약을 섞지 말 것.**

## ★ 판번 식별 (QS) — 성균관대 종합순위 한 개로 판별

| 종합순위 | 판 |
|---|---|
| **108위 / 67.3점** | 2027 |
| =126위 / 65.2점 | 2026 |
| =123위 / 55.5점 | 2025 |

이 표는 **QS** 기준이다(THE 와 혼동 주의 — THE 는 위 실측표를 쓴다).

**Why:** 2026.9.11. 보고서가 `nid=3990755`(2025판)를 "2027판"으로 표기해 인용한 사고가 있었다. QS 2027 발표(2026.6.18.) 이후에도 구 엔드포인트가 살아 있어 겉으로는 정상 응답했다. 순위 6개와 지표 9개가 소수점까지 2025판과 일치해 판명되었다.

**How to apply:** 수치를 쓰기 전 ① 위 표로 판번을 확인하고 ② **가중손실 합 = Σ 배점×(100−점수)÷100 으로 역산해 공표 종합점수와 0.1점 이내인지 검산**한다. 세 판 모두 이 검산이 성립하므로, 어긋나면 파싱이 틀린 것이다.

관련: [[project-overview]] · [[report-format]]
