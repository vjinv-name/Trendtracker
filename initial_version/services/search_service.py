from typing import List
from tavily import TavilyClient
from config.settings import settings
from domain.news_article import NewsArticle
from utils.exceptions import AppError

class SearchService:
    """Tavily API를 사용하여 뉴스 검색 기능을 제공하는 서비스 클래스"""
    def __init__(self):
        """TavilyClient를 초기화합니다."""
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search_news(self, keyword: str, num_results: int = 5) -> List[NewsArticle]:
        """
        Tavily API를 사용하여 뉴스를 검색하고 최신순으로 정렬하여 반환합니다.
        네트워크 오류 시 1회 재시도합니다.
        """
        max_retries = 1
        attempt = 0
        
        while attempt <= max_retries:
            try:
                # 설정에서 도메인 제한 리스트 가져오기
                include_domains = settings.search_domains
                
                # 충분한 기사를 확보한 뒤 최신순으로 필터링하기 위해 더 많이 가져옴
                max_results_to_fetch = max(num_results * 3, 20)
                
                # search 호출 (내부적으로 타임아웃이 발생할 수 있음)
                response = self.client.search(
                    query=keyword,
                    search_depth="advanced",
                    include_domains=include_domains,
                    max_results=max_results_to_fetch,
                    topic="news"
                )
                
                results = response.get('results', [])
                if not results:
                    return []
                    
                # published_date 기준 내림차순(최신순) 정렬
                results.sort(
                    key=lambda x: x.get('published_date') if x.get('published_date') else "", 
                    reverse=True
                )
                
                top_results = results[:num_results]
                
                articles = []
                for item in top_results:
                    articles.append(NewsArticle(
                        title=item.get('title', '제목 없음'),
                        url=item.get('url', ''),
                        snippet=item.get('content', ''),
                        pub_date=item.get('published_date')
                    ))
                    
                return articles
                
            except Exception as e:
                attempt += 1
                error_str = str(e).lower()
                
                # 마지막 시도에서도 실패한 경우 또는 치명적인 오류인 경우 raise
                if attempt > max_retries or "401" in error_str or "400" in error_str:
                    if "401" in error_str or ("invalid" in error_str and "api" in error_str):
                        raise AppError("api_key_invalid")
                    elif "429" in error_str or "limit" in error_str:
                        raise AppError("rate_limit_exceeded")
                    elif "400" in error_str:
                        raise AppError("bad_request")
                    elif any(err in error_str for err in ["500", "502", "503"]):
                        raise AppError("server_error")
                    else:
                        raise AppError("network_error")
                
                # 재시도 전 짧은 대기 (선택 사항)
                import time
                time.sleep(1)

# 싱글톤 패턴 또는 전역 함수 제공
_search_service = SearchService()

def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    return _search_service.search_news(keyword, num_results)
