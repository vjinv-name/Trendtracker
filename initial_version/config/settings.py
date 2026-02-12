import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    """
    애플리케이션 환경 설정을 관리하는 클래스
    """
    
    # 필수 환경 변수 목록
    REQUIRED_VARS = [
        "TAVILY_API_KEY",
        "GEMINI_API_KEY",
        "CSV_PATH"
    ]
    
    def __init__(self):
        self._validate_required_vars()
        
        # API Keys
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        # Models
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Search Configuration
        domains_raw = os.getenv("SEARCH_DOMAINS", "")
        self.search_domains = [d.strip() for d in domains_raw.split(",") if d.strip()]
        
        # Data Storage
        # 기본값은 data/search_history.csv
        self.csv_path = Path(os.getenv("CSV_PATH", "data/search_history.csv"))
        
        # 데이터 디렉토리가 없으면 생성
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

    def _validate_required_vars(self):
        """
        필수 환경 변수가 설정되어 있는지 확인합니다.
        """
        missing_vars = []
        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            error_msg = f"""
❌ 환경변수가 설정되지 않았습니다.

누락된 변수: {', '.join(missing_vars)}

설정 방법
1. .env.example 파일을 .env로 복사하세요.
2. 각 API 키를 발급받아 입력하세요.

API 키 발급 안내:
- Tavily API: https://tavily.com/ (검색용)
- Google AI Studio: https://aistudio.google.com/ (Gemini 요약용)
"""
            raise EnvironmentError(error_msg)

# 싱글톤 인스턴스 제공
settings = Settings()
