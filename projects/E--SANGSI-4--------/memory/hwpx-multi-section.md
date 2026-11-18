---
name: hwpx-multi-section
description: HWPX에 구역을 추가할 때(세로 본문+가로 표 등) 한글이 조용히 무시하는 4가지 — secCnt가 가장 흔한 원인
metadata: 
  node_type: memory
  type: reference
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-09-10T06:01:12.542Z
---

세로 본문 + 가로 표처럼 용지 방향이 다른 쪽을 만들려면 구역(section)을 나눠야 하고,
`Contents/section1.xml`, `section2.xml` … 을 직접 만들어 넣게 된다.
이때 **아래 4가지를 전부** 맞춰야 한글이 읽는다. 하나라도 틀리면
**그 구역이 통째로 안 보이는데 오류 메시지가 전혀 없다.**

1. **`Contents/header.xml` 루트의 `secCnt` 를 실제 구역 수로 고칠 것** ← 가장 먼저 확인
   `<hh:head version="1.5" secCnt="1">` 이면 한글은 section0 만 읽고 나머지를 버린다.
   2026-09 무용학과 문서에서 이것 하나 때문에 여러 판을 헤맸다.
2. **`META-INF/container.rdf`** 에 구역마다 두 쌍을 등록할 것
   (`<rdf:Description rdf:about=""><pkg:hasPart rdf:resource="Contents/section1.xml"/>` 와
   `<rdf:Description rdf:about="Contents/section1.xml"><rdf:type …#SectionFile/>`).
3. **`Contents/content.hpf`** 의 manifest/spine 에서 **section 항목이 연속**이어야 한다.
   `settings` 뒤에 덧붙이면 안 된다(참조 파일은 header→section0→section1→settings 순).
4. 새 구역 루트 `hs:sec` 의 **네임스페이스 선언은 section0 의 nsmap 을 그대로 복사**할 것
   (hp/hs 두 개만 선언하지 말 것).

문단·표 `id` 는 문서 전체에서 고유하게 맞춰 두는 편이 좋지만, **원인은 아니다**
(한글이 만든 실제 다중구역 파일에도 섹션 간 중복 id 가 있었다).

## 가로 용지는 width/height 를 맞바꾸지 않는다

hwpx 2,094개를 전수 조사한 결과, 한글이 만든 **가로 구역 9건이 전부**
용지 치수를 **A4 세로(width=59528, height=84188) 그대로** 두고
`landscape="NARROWLY"` 플래그로만 방향을 뒤집고 있었다(표 폭은 240~275mm).

    pp.set('landscape', 'NARROWLY')      # 치수는 건드리지 않는다
    margin left/right 5669               → 렌더 본문 폭  = 297 - 20 - 20 = 257mm
    margin top 5668 / bottom 4252        → 렌더 본문 높이 = 210 - 20 - 15 = 175mm

즉 렌더링 시 **본문 폭 = height - left - right, 높이 = width - top - bottom** 으로 뒤집힌다.
`WIDELY`/`NARROWLY` 는 이름과 달리 세로 문서에도 NARROWLY 가 62건 있었으므로,
값 이름만 보고 판단하지 말고 **표 폭 같은 실제 내용 폭으로 판정**할 것.

## 검증

`C:\Users\SKKU\.claude\skills\hwpxskill\scripts\validate.py` 의 `check_sections()` 가
위 1~3번을 점검한다. 구역을 추가했으면 반드시 통과시킬 것.
구현 유틸은 세션 스크래치의 `hwpxsec.py`(read_zip/write_zip/get_secpr/build_section/
register_section/register_section_rdf/set_sec_count/renumber).

관련: [[hwpx-report-layout-checklist]] [[trust-your-validator-last]]
