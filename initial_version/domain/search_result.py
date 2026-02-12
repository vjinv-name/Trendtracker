from dataclasses import dataclass
from datetime import datetime
from typing import List
import pandas as pd
from domain.news_article import NewsArticle

@dataclass
class SearchResult:
    """검색 결과 및 AI 요약을 담는 데이터클래스"""
    search_key: str  # PK, "키워드-yyyymmddhhmm" 형식
    search_time: datetime
    keyword: str
    articles: List[NewsArticle]
    ai_summary: str

    def to_dataframe(self) -> pd.DataFrame:
        """CSV 저장을 위해 Long format(기사 1건=1행)으로 변환"""
        data = []
        for i, article in enumerate(self.articles, 1):
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "pub_date": article.pub_date,
                "ai_summary": self.ai_summary
            })
        
        # 검색 결과가 없는 경우에도 기본 구조를 가진 DataFrame 반환
        if not data:
            return pd.DataFrame(columns=[
                "search_key", "search_time", "keyword", "article_index",
                "title", "url", "snippet", "pub_date", "ai_summary"
            ])
            
        return pd.DataFrame(data)
