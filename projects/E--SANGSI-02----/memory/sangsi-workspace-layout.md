---
name: sangsi-workspace-layout
description: 상시채용 업무 작업 루트는 E:\SANGSI — 세션은 항상 이 루트에서 열 것(메모리 키가 cwd 기준이라 하위 폴더명은 무관)
metadata:
  node_type: memory
  type: project
  originSessionId: c826d76b-3760-4394-86eb-d3f49a0c4510
  modified: 2026-11-03T05:38:02.160Z
---

상시채용(비정시) 업무 전반의 작업 루트는 **`E:\SANGSI`** 다.
2026-09-18 에 기존 `E:\4_무용학과_상시` 를 이 아래로 옮기고 메모리를 새 키로 이전했다(2026-10-26 `00_특임\1_무용학과_상시` 로 다시 옮김).
퀵패스 배치 폴더 안은 `1_최초요청/2_IOU/3_퀵패스/4_GPR` 로 나눈다(quickpass 스킬 참고). 학과장·팀장 메일은 `04_학과소통\<정리번호_학과>`, 학과 발전계획은 `00_학과발전계획\<대학>\<정리번호_학과>`.
채용심의위원회 내부결재·일정표·회의자료는 `05_채용심의위원회\<NN차_YYMMDD>`(회의일 기준). 루트에는 트래커 xlsx 만 두고 백업은 `_backup`.
하위 폴더는 업무별로 계속 늘거나 **이름이 바뀔 수 있으므로 여기에 적지 않는다**
(현재 구성은 `E:\SANGSI` 를 직접 보면 된다).

## 세션은 항상 `E:\SANGSI` 에서 열 것

Claude Code 는 **세션을 연 디렉터리(cwd) 경로로 메모리 키를 만든다**
(`:` · `\` · 비ASCII 문자를 `-` 로 치환. 예: `E:\SANGSI` → `E--SANGSI`).
따라서

- 루트에서 열면 → 키 `E--SANGSI` → 메모리 정상. **하위 폴더 이름을 바꿔도 아무 영향 없다.**
- 하위 폴더에서 열면 → 그 경로의 새 키가 생기고 **메모리가 비어 있다**(조용히 안 읽힌다).
  게다가 폴더명을 바꾸면 키가 또 바뀌어 연결이 끊긴다.

그래서 **하위 폴더에서 세션을 열지 않는 것**이 유지보수가 0 인 방법이다.
부득이 하위 폴더에서 열어야 하면, 그 키의 `memory` 를 루트 메모리로 junction 하면 된다.

    mklink /J "C:\Users\SKKU\.claude\projects\<그_폴더의_키>\memory" ^
              "C:\Users\SKKU\.claude\projects\E--SANGSI\memory"

junction 이므로 사본이 갈라지지 않는다. **메모리 편집은 `E--SANGSI\memory` 한 곳만** 고친다.
`C:\Users\SKKU\.claude\scripts\link-sangsi-memory.ps1` 이 현재 경로에 맞춰 이걸 자동으로 해준다.

## 참고 (이전 이력)

| 항목 | 위치 |
|---|---|
| 메모리 실체 | `C:\Users\SKKU\.claude\projects\E--SANGSI\memory` |
| 이전 전 키(원본 보존) | `E--4--------` — `memory` 와 `memory_backup_20260918_135444` |
| 과거 세션 기록 사본 | `E--SANGSI\*.jsonl` (원본은 구 키에 그대로) |

**Why:** 폴더를 옮기거나 이름을 바꾸면 프로젝트 키가 바뀌어 메모리가 조용히 안 읽힌다.
경고도 없이 "기억이 없는" 상태가 되므로 원인을 찾기 어렵다.
**How to apply:** 상시 업무 세션은 `E:\SANGSI` 에서 열고, 하위 폴더 이름은 자유롭게 바꾼다.
관련: [[dance-dept-2026-recruitment-decisions]]
