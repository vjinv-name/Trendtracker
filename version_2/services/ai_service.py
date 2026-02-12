from typing import List
from google import genai
from config.settings import settings
from domain.news_article import NewsArticle
from utils.exceptions import AppError

class AIService:
    """Gemini API를 사용하여 뉴스 요약 기능을 제공하는 서비스 클래스"""
    def __init__(self):
        """Gemini 클라이언트를 초기화합니다."""
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_id = settings.gemini_model

    def summarize_news(self, articles: List[NewsArticle]) -> str:
        """
        Gemini API를 사용하여 뉴스 기사들을 요약합니다.
        네트워크 오류 시 1회 재시도합니다.
        """
        if not articles:
            return "요약할 기사가 없습니다."

        context = ""
        for i, article in enumerate(articles, 1):
            context += f"{i}. 제목: {article.title}\n   내용: {article.snippet}\n\n"

        prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{context}
        """.strip()

        max_retries = 1
        attempt = 0
        
        while attempt <= max_retries:
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                
                if not response or not response.text:
                    raise AppError("ai_error")
                    
                return response.text.strip()
                
            except Exception as e:
                attempt += 1
                error_str = str(e).lower()
                
                if attempt > max_retries or "401" in error_str or "400" in error_str:
                    if "401" in error_str or "invalid" in error_str:
                        raise AppError("api_key_invalid")
                    elif "429" in error_str or "limit" in error_str:
                        raise AppError("rate_limit_exceeded")
                    elif "400" in error_str:
                        raise AppError("bad_request")
                    else:
                        raise AppError("ai_error")
                
                import time
                time.sleep(1)

    def expand_query(self, keyword: str) -> str:
        """
        Gemini API를 사용하여 검색어를 확장하고 최적화합니다.
        연관 키워드, 영문 변환 등을 포함한 최적의 검색 쿼리를 생성합니다.
        """
        prompt = f"""
당신은 뉴스 검색 전문가입니다. 사용자가 입력한 트렌드 분석 키워드를 바탕으로, 
가장 정확하고 풍부한 뉴스 검색 결과를 얻을 수 있는 최적화된 검색어(Search Query) 1개를 만들어주세요.

[입력 키워드]: {keyword}

[지침]:
- 관련 핵심 단어나 동의어를 조합하세요.
- 만약 글로벌 트렌드라면 검색어 뒤에 영문 키워드도 같이 포함하세요 (예: "AI 반도체 기술 NVIDIA").
- 검색어는 쉼표 없이 한 줄의 문자열로만 답하세요.
- 특수문자보다는 핵심 명사 위주로 구성하세요.

최적화된 검색어:""".strip()

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
            return keyword
        except Exception:
            # 실패 시 원본 검색어 반환 (중단 방지)
            return keyword

# 싱글톤 인스턴스 또는 전역 함수 제공
_ai_service = AIService()

def summarize_news(articles: List[NewsArticle]) -> str:
    return _ai_service.summarize_news(articles)

def expand_query(keyword: str) -> str:
    """검색어를 AI로 최적화합니다."""
    return _ai_service.expand_query(keyword)
