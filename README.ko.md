# AI-Assisted Java Code Generator (개발자 가이드)

자연어 비정형 설계서로부터 Gemini AI를 통해 구조화 데이터를 추출하고, Pydantic 검증 및 룰 기반 생성기를 거쳐 구문 에러 제로, 완전 규약 준수의 **Java 데이터 구조 및 도메인 모델 클래스를 자율 자동 생성하는 백엔드 개발 지원 엔진**입니다.

---

## 1. 개발 및 실행 환경

- OS: Windows 10/11
- Runtime: Python 3.14.8 (.venv)
- AI Model: Google Gemini API (`gemini-3.8-flash`, Free Tier)
- 핵심 라이브러리: `google-genai`, `pydantic`, `pytest`, `python-pptx`

---

## 2. 설치 및 실행 절차

```powershell
# 1. 가상환경 활성화
Set-ExecutionPolicy Unrestricted -Scope Process -Force
.\.venv\Scripts\activate

# 2. 20개 자동 테스트 실행 (회귀 테스트)
python -m pytest -v

# 3. AI 파이프라인 전체 실행 (설계서 ➔ AI ➔ 검증 ➔ Java 모델 클래스 생성)
python gemini_extraction_test.py

# 4. 제출용 아키텍처 슬라이드(PPTX) 자동 생성
python make_presentation.py
```

---

## 3. 핵심 아키텍처 및 안전장치

- **개념 확장**: DTO에 국한되지 않고 엔터프라이즈 백엔드의 기초가 되는 데이터 구조 및 도메인 모델 클래스(DTO/VO/Entity 골격) 생성으로 확장.
- **방탄 사니타이즈 (Bulletproof Parsing)**: AI 출력의 Markdown 백틱(```json) 및 주석 자동 정제.
- **자가 치유 (Self-Correction)**: Pydantic 검증 실패 시 오류 피드백을 프롬프트에 재주입하여 최대 3회 자동 복구.
- **무결성 보장**: 단위·통합·AI방어 테스트 20건 전원 통과 (`20 passed in 0.31s`).

---

## 4. 상세 문서 링크

- **한국어 실무 문서**: `docs/ko/` (진행상태, 아키텍처 결정, 요구사항, 테스트 결과, 인수인계서, 엔지니어링 가이드라인)
- **일본어 대외 문서**: `docs/ja/` (제출용 기술 사양서, ADR, 테스트 실적 보고서, 인수인계서)