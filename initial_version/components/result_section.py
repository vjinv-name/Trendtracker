import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.markdown("---")
    st.subheader(f"🤖 '{title}' 트렌드 요약")
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 리스트를 렌더링합니다."""
    st.markdown("---")
    st.subheader("📰 최신 관련 뉴스")
    
    if not articles:
        st.write("관련 뉴스 기사가 없습니다.")
        return

    for article in articles:
        # expander 제목: 기사 제목 + (발행일)
        expander_title = article.title
        if article.pub_date:
            expander_title += f" ({article.pub_date})"
            
        with st.expander(expander_title):
            if article.pub_date:
                st.caption(f"📅 발행일: {article.pub_date}")
            
            st.markdown(article.snippet)
            st.markdown(f"[🔗 기사 보기]({article.url})")
