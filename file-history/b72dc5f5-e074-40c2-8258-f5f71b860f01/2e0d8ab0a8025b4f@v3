---
name: codex-review
description: "코드 리뷰 요청 시 사용. Reviews code for quality, security, performance."
context: fork
allowed-tools: mcp__codex-subagent__spawn_agent, Read, Grep, Glob
---

Codex에게 코드 리뷰를 위임하되:
1. 먼저 대상 파일을 Read로 확인
2. Codex에 리뷰 요청 (model: gpt-5, reasoningEffort: high)
3. 결과를 정리해서 [심각/주의/참고] 등급으로 분류
4. 3줄 이내 요약만 반환
