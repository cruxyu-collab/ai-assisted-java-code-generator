# HANDOFF.ko.md (프로젝트 인수인계 및 맥락 보존 문서)

## 1. 프로젝트 정체성
- **프로젝트명**: JavaGen (AI-Assisted Java Code Generator)
- **목적**: 일본 IT 기업(메이텍, 테크노프로 등) 제출용 엔터프라이즈급 AI/Java 융합 기술 자산 증명
- **핵심 특징**: AI에게 Java 문법 생성을 맡기지 않고, '의미 해석(LLM) ➔ 데이터 계약 검증(Pydantic) ➔ 결정론적 소스 렌더링(Python)'으로 이원화한 견고한 아키텍처

## 2. 개발 및 실행 환경
- **OS**: Windows PC
- **Runtime**: Python 3.14.8 (`.venv`)
- **AI Model**: Google Gemini API (`gemini-3.8-flash`, Free Tier 유지)
- **핵심 패키지**: `google-genai`, `pydantic`, `pytest`, `python-pptx`

## 3. 핵심 실행 명령어 (Cheat Sheet)
```powershell
# 1. 가상환경 활성화
.\.venv\Scripts\activate

# 2. 20개 단위/통합/방어 자동 테스트 실행
python -m pytest -v

# 3. AI 연동 및 Java 생성 파이프라인 전체 실행
python gemini_extraction_test.py

# 4. 제출용 PPTX 슬라이드 자동 생성
python make_presentation.py
```

## 4. 문서 운영 규칙
- **대외용 문서 (`README.md`, `docs/ja/*`)**: 취업/포트폴리오/면접 흔적(就活臭)을 배제하고 상용 오픈소스 기술 백서 톤앤매너 유지.
- **실무용 문서 (`README.ko.md`, `docs/ko/*.ko.md`)**: 개발자-AI 간의 진실의 원천(SSOT)으로 솔직한 기술 제약 및 실무 로그 관리.