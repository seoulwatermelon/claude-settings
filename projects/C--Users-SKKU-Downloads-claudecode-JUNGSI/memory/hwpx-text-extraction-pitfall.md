---
name: hwpx-text-extraction-pitfall
description: HWPX 문서 대조·검증 시 lineBreak 꼬리와 charPr 강조를 안 읽으면 거짓 차이/거짓 일치가 난다
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 09227373-c0e6-4afa-899c-8abfb901ae26
---

HWPX 텍스트를 뽑을 때 `''.join(t.text for t in p.findall('.//hp:t'))` 만 쓰면 **두 가지를 놓친다**:

1. **`lineBreak` 꼬리 텍스트** — `<t>4.33 / 5<lineBreak/>[보통]</t>` 구조에서 `[보통]`은 `lineBreak.tail`에 있다. `t.text`만 읽으면 사라져서 "라벨이 없다"는 **거짓 차이**가 난다.
2. **강조 서식** — 볼드밑줄은 `charPrIDRef='36'` 런이다. 텍스트만 비교하면 강조 유무 차이를 **못 잡는다**(거짓 일치).

올바른 추출:
```python
def rich(p):
    o = ''
    for rn in p.findall('hp:run', NS):
        s = ''.join((t.text or '') + ''.join(c.tail or '' for c in t)
                    for t in rn.findall('hp:t', NS))
        if s:
            o += ('«%s»' % s) if rn.get('charPrIDRef') == '36' else s
    return o
```

**Why:** 이 실수를 두 번 반복했다. 교인협 빌더 검증에서 `[보통]` 라벨과 학과추천의견 2인분이 "누락됐다"고 잘못 보고했고, 사용자가 "너가 최종파일 확인해봐"라고 지적해서야 발견했다. 강조는 반대로 놓쳐서 골든 3개 파일(no_gpr)에 강조가 빠진 걸 늦게 알았다.

**How to apply:** HWPX 문서를 비교·검증하는 스크립트를 쓸 때는 처음부터 꼬리 + charPr를 읽는 추출 함수를 쓴다. 차이가 "이상하게 많다/적다"면 추출 함수부터 의심한다. 빈 셀·빈 문단은 `hp:t`가 아예 없다는 점도 함께 기억([[mistake-overbroad-rebuild]] 참고).
