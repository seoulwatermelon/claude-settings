---
name: "rsa-docs"
description: "RSA(Rising-Fellowship/연구력 우수교원) 문서화 작업 전체 파이프라인. 로우데이터(Scopus + 업적평가 xlsx)에서 Top-tier 분류, 비고란 보강, 개인별 PDF 생성, 캠퍼스별 병합까지. \"RSA\", \"Rising-Fellowship\", \"연구력 문서화\", \"탑티어 분류\", \"개인별 PDF\" 등의 요청 시 사용."
---

# RSA 문서화 파이프라인

## 개요
성균관대학교 교원인사팀의 RSA(Rising-Fellowship) 연구력 문서화 작업 전체 파이프라인.
로우데이터(xlsx)로부터 Top-tier 분류 → 비고란 보강 → 개인별 PDF 생성 → 캠퍼스별 병합까지 수행.

---

## 1. 데이터 소스 구조

### RSA 엑셀 파일 시트 구성
- **최종정리 시트**: 교원별 요약 (사번, 소속, 성명, 직급, 논문수, FWCI, 순위, RSA대상 등)
- **SCOPUS(2023-2025) 시트**: Scopus 논문 원본 데이터
- **작업_연구업적다년도(23~25) 시트**: 업적평가 원본 데이터 (Top-tier 판별 대상)

### 최종정리 시트 주요 컬럼
| 인덱스 | 항목 |
|--------|------|
| [0] | 사번 |
| [2] | 행정관리소속 (학과) |
| [3] | 성명 |
| [4] | 직급 |
| [10] | 논문수 |
| [11] | FWCI 평균 |
| [12] | FWCI 합계 |
| [40] | 캠퍼스 |
| [47] | RSA대상 (RSA / RSA2) |

### SCOPUS 시트 주요 컬럼
| 인덱스 | 항목 |
|--------|------|
| [2] | 사번 |
| [13] | Publication type |
| [14] | CITATIONS |
| [15] | FWCI |
| [17] | Top 1% |
| [18] | Top 10% |
| [19] | International Collaboration |
| [20] | Title |
| [21] | Scopus Source title (저널명) |
| [24] | Full date |
| [25] | Number of Authors |

### 작업(업적평가) 시트 주요 컬럼
| 인덱스 | 항목 |
|--------|------|
| [4] | 개인번호 (사번) |
| [6] | 평가항목 |
| [8] | 제목 |
| [11] | 게재지명 |
| [13] | 발표일자 |
| [16] | 역할 |
| [25] | 분류A(%) |
| [27] | 분류B(%) |
| [28] | JCR년도 |
| [29] | 인정IF |
| [54] | Top tier 여부 (1=인정) |
| [55] | 비고 |
| [56] | 환산편수 |

---

## 2. Top-tier 분류 핵심 원칙

### 절대 규칙 (★★★)
1. **역할=책임저자만** Top-tier 대상 (22-24 기준)
2. **평가항목=국제A, 국제학술회의논문만** Top-tier 대상
3. **NSC = 본지 3종만** (Nature, Science, Cell) — 자매지(Nature Communications, PNAS, Science Advances 등)를 별도 열거한 경우에만 해당 학과 Top-tier에 포함
4. **JCR는 가장 유리한 카테고리 기준** 적용 (심리학과처럼 PDF에서 특정 카테고리 지정된 경우 제외)
5. **JCR IF 또는 JCI 둘 다 인정됨**
6. **JCR_%순위는 raw 데이터의 분류A(%)/분류B(%) — 둘 다 있으면 둘 다 표기**
7. **수식이 필요한 곳은 데이터값이 아닌 수식으로 남겨야 함**
8. **T1 학술대회는 main conference만** — workshop/poster/LBW/extended abstract 제외
9. **컨퍼런스 리스트는 학과별로 다르게 적용**
10. **22~24 때 탑티어로 넣은 사람들의 탑을 빼는 건 불가** — 기존 Top-tier 소급 삭제 불가
11. **확인 어려운 건은 빨간색 표시해서 수기확인으로 남김**
12. **임상교원은 Top-tier 포함 유지** (사용자 결정)

### 학과별 예외
- **화학공학부**: 2nd-tier는 I트랙에 "또는"으로 명시되어 있으므로 유지
- **통계학과**: 2nd-tier는 I트랙에 미포함이므로 Top-tier에서 제외
- **심리학과 등**: PDF에서 특정 JCR 카테고리를 지정한 학과는 해당 카테고리에서의 JCR%만 사용

### 5단계 매칭 파이프라인
1. **ISSN 정확 매칭** — 업적평가 저널 ISSN ↔ Top-tier 리스트 ISSN
2. **저널명 정규화 매칭** — 대소문자/공백/특수문자 제거 후 비교
3. **JCR 브릿지 매칭** — ISSN으로 JCR에서 찾아 정식 저널명 획득 후 재매칭
4. **컨퍼런스 별칭 매칭** — 학술대회 약칭/정식명 교차 비교
5. **수기 확인 대상** — 위 4단계 실패 시 빨간색 표시

### 환산편수 산출
- Top-tier만 대상 (2nd-tier, 3rd-tier 제외)
- 저자 수 기반 분배 (학과별 PDF 기준에 따름)

---

## 3. 비고란 보강 규칙

### 거대과학 FWCI 조정
- 저자 수 1,000명 초과 논문: FWCI의 5%만 반영
- 해당 분야: LIGO/Virgo/KAGRA(중력파), HAWC/IceCube(감마선/뉴트리노), ATLAS/CMS(입자물리) 등

### NSC 본지 주저자 검증
- Nature, Science, Cell 본지 게재 시 주저자 여부 웹 검색으로 확인
- 확인된 경우 비고에 기록 (예: "Science 본지 주저자")

### 기타 비고 항목
- 최근 수상 이력 (성균인상, 올해의 연구자 등)
- IBS/대형과제 참여 여부
- 외부 오퍼/리텐션 관련 (해당 시)
- 거대과학 소속 시 독립연구 FWCI 별도 표기

---

## 4. 개인별 PDF 생성 형식

### 공통 함수
```python
from datetime import datetime, date

def safe_str(val):
    """날짜 객체를 문자열로 변환"""
    if isinstance(val, datetime): return val.strftime('%Y-%m-%d')
    elif isinstance(val, date): return val.strftime('%Y-%m-%d')
    if val is None: return ''
    return str(val)

def calc_height(texts_widths):
    """한글/영문 혼합 텍스트의 행 높이 계산"""
    max_lines = 1
    for text, col_w in texts_widths:
        if not text: continue
        t = str(text)
        korean_count = sum(1 for c in t if 0xAC00 <= ord(c) <= 0xD7A3)
        total = len(t)
        if total == 0: continue
        effective_len = (total - korean_count) + korean_count * 1.8
        chars_per_line = max(1, col_w / 0.65)
        lines = max(1, int(-(-effective_len // chars_per_line)))
        max_lines = max(max_lines, lines)
    return max(14, max_lines * 12 + 4)
```

### Scopus PDF 형식
- **타이틀**: `SCOPUS 연구실적 (2023~2025) — {성명}` (가운데 정렬, 맑은 고딕 14pt 볼드)
- **부제**: `총 {N}건 | {학과}` (가운데 정렬, 9pt)
- **헤더**: 맑은 고딕 8pt 볼드, 배경 `#D6E4F0`, 테두리 `#B4C6E7`
- **데이터**: 맑은 고딕 7.5pt, 교대색상 `#EDF2F9` / `#FFFFFF`
- **컬럼**: `['연번', '성명', '문서타입', 'FWCI', 'Top\n1%', 'Top\n10%', '국제공동\n연구', 'Title', '저널명', '게재일', '저자수', '피인용']`
- **컬럼폭**: `[3.8, 5.5, 6.5, 5, 4, 4.5, 5.5, 46, 22, 9, 4.5, 5]`
- **Title/저널명은 좌측 정렬**, 나머지 가운데 정렬
- **페이지**: A4 가로, fitToWidth=1, 여백 좌우 0.15 / 상하 0.4

### Top-tier PDF 형식
- **★★★ TopTier=1인 행만 포함 (책임저자 필터 이미 적용된 결과)**
- **타이틀**: `Top-tier 연구실적 (2023~2025) — {성명}` (가운데 정렬, 맑은 고딕 14pt 볼드)
- **부제**: `총 {N}건 | {학과}` (가운데 정렬, 9pt)
- **헤더**: 맑은 고딕 8pt 볼드, 배경 `#D9E2C8`, 테두리 `#999999`
- **데이터**: 맑은 고딕 7.5pt, 배경 `#FFF2CC` (노란색, 전체 Top-tier이므로)
- **컬럼**: `['연번', '성명', '평가항목', '역할', '제목', '게재지명', '발표일자', 'JCR\n년도', 'IF', 'JCR상위\n%', 'Top\ntier여부', 'Top Tier\n환산편수', '비고']`
- **컬럼폭**: `[3.8, 5, 5.5, 4.5, 34, 20, 9, 5, 6, 5.5, 5, 6.5, 14]`
- **제목/게재지명/비고는 좌측 정렬**, 나머지 가운데 정렬
- **JCR상위%**: 분류A와 분류B 둘 다 있으면 `A / B` 형태로 표기
- **페이지**: A4 가로, fitToWidth=1, 여백 좌우 0.15 / 상하 0.4

### XLSX → PDF 변환
```bash
python scripts/office/soffice.py --headless --convert-to pdf output.xlsx
```
soffice.py 경로: docx 스킬의 `scripts/office/soffice.py` 사용

---

## 5. 캠퍼스별 병합 PDF

### 4종 병합 파일
1. 인사캠 Scopus — 인사캠 대상자 Scopus PDF 전체 병합
2. 인사캠 Top-tier — 인사캠 대상자 Top-tier PDF 전체 병합
3. 자과캠 Scopus — 자과캠 대상자 Scopus PDF 전체 병합
4. 자과캠 Top-tier — 자과캠 대상자 Top-tier PDF 전체 병합

### 병합 방법
```python
from PyPDF2 import PdfMerger
merger = PdfMerger()
for pdf_path in sorted_pdf_list:
    merger.append(pdf_path)
merger.write(output_path)
merger.close()
```

---

## 6. 기타 원칙

### 데이터 우선순위
- **PDF가 주(主), 엑셀이 보조** — 학과별 Top-tier 리스트 PDF가 primary source
- **raw 데이터에 없는 추가 열은 헤더 색상을 다르게**
- **RSA 대상은 사용자가 수동으로 채울 것이므로 빈칸 유지**
- **22-24 양식(57컬럼)을 그대로 따라야 함** — 임의 변경 금지

### PDF 저널명 매칭 주의
- **PDF 저널명 자체가 JCR 저널명과 안 맞을 수 있다는 것이 대전제**
- 영문명/중문명 불일치 (예: Taiwan Journal of East Asian Studies = 臺灣東亞文明研究學刊)
- 약칭/정식명 불일치 (예: MICRO = International Symposium on Microarchitecture)

### 부등호 통일
- `>` 는 `≥`(이상)으로 통일 처리

### 글로벌융합학부
- 사람별 개별 매핑 (H열에 반영)

### 제외 대상
- 학부대학, 산학협력단 제외
- 창작 실적은 수기 확인 필요, 비고에 기록

