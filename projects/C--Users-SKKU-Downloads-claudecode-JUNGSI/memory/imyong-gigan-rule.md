---
name: imyong-gigan-rule
description: 전임교원 임용기간 만료일 = (임용일 + 4년 - 1일)이 속한 학기의 말일. SKK GSB는 2년 트랙으로 규칙이 다름
metadata:
  node_type: memory
  type: reference
  originSessionId: 1882205a-801b-463f-9e26-3c69dde1fcc0
  modified: 2026-10-29T05:00:19.405Z
---

**전임교원 신규임용 임용기간 만료일 = (임용일 + 4년 − 1일)이 속한 학기의 말일**
(1학기 3.1~8.31 → **8.31**, 2학기 9.1~2월말 → **2월 말일**). 직급과 무관하다 —
조교수·부교수·교수 모두 4년이다.

```python
def term_end(start, years=4):
    anniv = start.replace(year=start.year + years) - datetime.timedelta(days=1)
    if (3, 1) <= (anniv.month, anniv.day) <= (8, 31):
        return datetime.date(anniv.year, 8, 31)
    yr = anniv.year if anniv.month <= 2 else anniv.year + 1
    return datetime.date(yr, 2, 29 if yr % 4 == 0 and yr % 100 != 0 else 28)
```

**예외: 경영전문대학원(SKK GSB)은 2년 트랙이고 기념일 −1일을 그대로 쓴다.**
26.8.15 임용 → 28.8.14. 학기말로 맞추지 않는다.

**Why:** 이사회자료·임용조건동의서 어디에도 임용기간이 안 적혀 있어서 직접
산정해야 한다. 규칙을 모르면 '+4년' 으로 계산해 3.1 이 아닌 날짜에 임용되는
사람(상시채용은 1.1·7.1 같은 날도 있다)을 틀린다.

**How to apply:**
- 근거는 `11_발령장수여식\26.2학기 신임교원 발령장 수여식 명단_v7.hwp` 의
  일반교원 30행이다. 26.3.1→30.2.28 / 26.7.1→30.8.31 / 26.8.31→30.8.31 /
  26.9.1→30.8.31 네 가지 시작일 모두 이 규칙으로 재현된다.
- **v1·v3 이 아니라 v7 을 보라.** v1·v3 에는 GSB 를 30.8.14 로 적은 값과
  현동진 43.8.31 이 남아 있다(현동진은 v7 에서 아예 빠졌다 — 33명→32명).
- 새로 산정했으면 같은 방식으로 과거 명단을 역검증해라. 값 하나를 맞춰 보는
  것으로는 규칙이 맞는지 알 수 없다 ([[verification-two-axes]]).

[[balryeongjang-myeongdan]] [[jungsi-folder-structure]]
