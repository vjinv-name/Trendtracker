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

    def search_news(self, keyword: str, num_results: int = 5, category: str = "전체", time_range: str = None, include_all_sources: bool = False, language: str = "한국어") -> List[NewsArticle]:
        """
        Tavily API를 사용하여 최적화된 뉴스를 검색합니다.
        지원 언어에 따른 쿼리 힌트를 추가하여 정확도를 높입니다.
        """
        max_retries = 1
        attempt = 0
        
        # 언어별 검색 힌트 매핑
        lang_hints = {
            "한국어": "",
            "English": " news",
            "日本語": " ニュース",
            "Deutsch": " nachrichten"
        }
        query_hint = lang_hints.get(language, "")

        # 쿼리 구성 최적화
        search_query = keyword + query_hint
        if category and category != "전체":
            search_query = f"{category} {search_query}"
            
        # 시간 범위 설정
        days_map = {"day": 1, "week": 7, "month": 30}
        days_back = days_map.get(time_range) if time_range else None

        while attempt <= max_retries:
            try:
                include_domains = None if include_all_sources else settings.search_domains
                
                # 가속화를 위한 파라미터 튜닝
                # 성능 우선을 위해 search_depth를 'basic'으로 변경 (사용자 피드백 반영)
                search_params = {
                    "query": search_query,
                    "search_depth": "basic", 
                    "max_results": num_results,
                    "topic": "news",
                    "include_images": False # 이미지 수집 비활성화 (사용자 요청)
                }
                
                # Tavily API는 q=... 에 언어 필터를 넣거나 검색어 자체로 판단함.
                # 명시적인 search_language 파라미터가 없으면 쿼리에 언어를 힌트로 줄 수 있음
                # 하지만 Tavily는 보통 쿼리 언어에 따라 자동 조절함.
                # 여기서는 쿼리에 언어 힌트를 추가하거나 도메인 제한을 활용할 수 있으나, 일단 쿼리 자체는 유지함.
                
                if include_domains:
                    search_params["include_domains"] = include_domains
                
                if days_back:
                    search_params["days"] = days_back
                
                response = self.client.search(**search_params)
                results = response.get('results', [])
                images = response.get('images', []) # Tavily는 별도의 이미지 화일 리스트를 주기도 함
                
                if not results:
                    return []
                    
                # 최신순 정렬 (Tavily basic search는 정렬을 보장하지 않으므로 수동 정렬)
                results.sort(key=lambda x: x.get('published_date', ''), reverse=True)
                
                articles = []
                for i, item in enumerate(results[:num_results]):
                    # 도메인을 출처로 활용
                    url = item.get('url', '#')
                    source = url.split('//')[-1].split('/')[0].replace('www.', '')
                    
                    # 해당 기사와 관련된 이미지가 있다면 매칭 (tavily는 리스트 순서가 항상 보장되지는 않지만 최선)
                    img_url = images[i] if i < len(images) else None
                    
                    articles.append(NewsArticle(
                        title=item.get('title', '제목 정보 없음'),
                        url=url,
                        snippet=item.get('content', '요약된 내용이 없습니다.'),
                        pub_date=item.get('published_date'),
                        image_url=img_url,
                        category=category if category != "전체" else "News",
                        source=source
                    ))
                    
                return articles
                
            except Exception as e:
                attempt += 1
                error_str = str(e).lower()
                
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
                
                import time
                time.sleep(1)

# 싱글톤 패턴 또는 전역 함수 제공
_search_service = SearchService()

def search_news(keyword: str, num_results: int = 5, category: str = "전체", time_range: str = None, include_all_sources: bool = False, language: str = "한국어") -> List[NewsArticle]:
    return _search_service.search_news(keyword, num_results, category, time_range, include_all_sources, language)
