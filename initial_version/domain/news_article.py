from dataclasses import dataclass
from typing import Optional

@dataclass
class NewsArticle:
    """뉴스 기사 정보를 담는 데이터클래스"""
    title: str
    url: str
    snippet: str
    pub_date: Optional[str] = None
