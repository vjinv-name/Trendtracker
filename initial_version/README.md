# TrendTracker 🚀

키워드로 뉴스를 검색하고 Gemini AI를 사용하여 핵심 내용을 요약해주는 실시간 트렌드 분석 앱입니다.

## 주요 기능

- **실시간 뉴스 검색**: Tavily API를 사용하여 신뢰할 수 있는 뉴스 소스에서 정보를 가져옵니다.
- **AI 요약**: Google Gemini API를 사용하여 검색된 기사들을 불릿 포인트 형식으로 깔끔하게 요약합니다.
- **검색 기록 관리**: 과거 검색 결과를 로컬 CSV 파일에 저장하고 언제든지 다시 불러올 수 있습니다.
- **데이터 백업**: 저장된 모든 검색 데이터를 CSV 파일로 다운로드할 수 있습니다.

## 설치 및 실행 방법

### 1. uv 설치 (없는 경우)

본 프로젝트는 파이썬 패키지 관리를 위해 `uv`를 사용합니다.

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 프로젝트 설정

```bash
# 의존성 설치
uv sync

# 환경변수 설정
cp .env.example .env
```

### 3. API 키 설정

`.env` 파일을 열어 다음 키들을 입력하세요:

- `TAVILY_API_KEY`: [Tavily](https://tavily.com/)에서 발급 가능 (무료 플랜 제공)
- `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)에서 발급 가능

### 4. 앱 실행

```bash
uv run streamlit run app.py
```

## 폴더 구조

- `app.py`: 메인 애플리케이션 파일
- `config/`: 환경변수 및 설정 관리
- `domain/`: 비즈니스 데이터 모델 (NewsArticle, SearchResult)
- `services/`: 외부 API 연동 서비스 (Tavily, Gemini)
- `repositories/`: 데이터 저장 및 로드 관리 (CSV)
- `components/`: UI 구성 요소 (검색 폼, 사이드바, 결과 섹션 등)
- `utils/`: 공통 유틸리티 (입력 처리, 에러 핸들링 등)
- `data/`: 검색 기록 CSV가 저장되는 폴더

## API 한도 안내

- **Tavily**: 무료 플랜 기준 월 1,000건 검색 가능
- **Gemini**: 무료 플랜(Flash 모델) 기준 분당 15회 요청 가능

## 기술 스택

- **언어**: Python 3.11+
- **UI**: Streamlit
- **데이터 분석**: Pandas
- **AI**: Google GenAI (Gemini 2.5 Flash)
- **검색**: Tavily Search API
