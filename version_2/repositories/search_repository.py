import os
import pandas as pd
import logging
from typing import List, Optional
from datetime import datetime
from config.settings import settings
from domain.search_result import SearchResult
from domain.news_article import NewsArticle

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchRepository:
    """CSV 파일을 사용하여 검색 기록 데이터를 관리하는 리포지토리 클래스"""
    def __init__(self, csv_path: str):
        """
        리포지토리 초기화 및 데이터 저장 경로 설정
        :param csv_path: CSV 파일 저장 경로
        """
        self.csv_path = csv_path
        # 데이터 디렉토리 생성
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        
        # 기본 컬럼 정의
        self.columns = [
            "search_key", "search_time", "keyword", "article_index",
            "title", "url", "snippet", "pub_date", "ai_summary"
        ]

    def load(self) -> pd.DataFrame:
        """
        CSV 파일을 로드하여 DataFrame으로 반환합니다.
        파일이 없으면 기본 컬럼 구조를 가진 빈 DataFrame을 반환합니다.
        """
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=self.columns)
        
        try:
            df = pd.read_csv(self.csv_path)
            # 저장된 데이터의 컬럼이 일치하는지 확인 (필요시 보정)
            for col in self.columns:
                if col not in df.columns:
                    df[col] = None
            return df
        except Exception as e:
            logger.warning(f"CSV 로드 실패: {e}")
            return pd.DataFrame(columns=self.columns)

    def save(self, search_result: SearchResult) -> bool:
        """
        SearchResult 객체를 CSV 파일에 추가(Append) 저장합니다.
        :param search_result: 저장할 검색 결과 객체
        :return: 저장 성공 여부
        """
        try:
            new_df = search_result.to_dataframe()
            
            if os.path.exists(self.csv_path):
                # 기존 데이터가 있으면 불러와서 합침
                existing_df = self.load()
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                final_df = new_df
                
            final_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            logger.error(f"CSV 저장 실패: {e}")
            return False

    def get_all_keys(self) -> List[str]:
        """
        저장된 모든 search_key 고유값 리스트를 검색 시간 기준 최신순으로 반환합니다.
        """
        df = self.load()
        if df.empty:
            return []
            
        try:
            df['search_time'] = pd.to_datetime(df['search_time'])
            unique_keys = df.sort_values(by='search_time', ascending=False)['search_key'].unique().tolist()
            return unique_keys
        except Exception as e:
            logger.error(f"키 목록 추출 실패: {e}")
            return df['search_key'].unique().tolist()

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """
        특정 search_key에 해당하는 검색 데이터를 찾아 SearchResult 객체로 반환합니다.
        :param search_key: 찾을 검색 키
        :return: SearchResult 객체 또는 None
        """
        df = self.load()
        if df.empty:
            return None
            
        result_df = df[df['search_key'] == search_key]
        if result_df.empty:
            return None
            
        first_row = result_df.iloc[0]
        
        articles = []
        for _, row in result_df.sort_values(by='article_index').iterrows():
            articles.append(NewsArticle(
                title=str(row['title']),
                url=str(row['url']),
                snippet=str(row['snippet']),
                pub_date=str(row.get('pub_date', ''))
            ))
            
        return SearchResult(
            search_key=str(first_row['search_key']),
            search_time=pd.to_datetime(first_row['search_time']),
            keyword=str(first_row['keyword']),
            articles=articles,
            ai_summary=str(first_row['ai_summary'])
        )

    def get_all_as_csv(self) -> str:
        """
        전체 데이터를 CSV 형식의 문자열로 반환합니다. (다운로드용)
        """
        df = self.load()
        return df.to_csv(index=False, encoding='utf-8-sig')
