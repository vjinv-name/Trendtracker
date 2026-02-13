import streamlit as st
import html
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str, keywords: str = ""):
    """AI 요약 결과를 렌더링합니다."""
    st.markdown("---")
    st.subheader(f"'{title}' 트렌드 분석")
    
    if keywords:
        # 키워드를 태그 형태로 표시
        kw_list = [k.strip() for k in keywords.split(',') if k.strip()]
        kw_html = " ".join([f"<span style='background:#f0f2f6; padding:4px 12px; border-radius:100px; font-size:12px; color:#4a5568; margin-right:8px; display:inline-block; margin-bottom:8px;'>#{kw}</span>" for kw in kw_list])
        st.markdown(f"<div style='margin-bottom: 20px;'>{kw_html}</div>", unsafe_allow_html=True)
        
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """뉴스 기사 리스트를 실제 UI 레이아웃으로 렌더링합니다."""
    st.markdown("---")
    st.subheader("관련 트랜드 뉴스")
    
    if not articles:
        st.info("관련 뉴스 기사가 없습니다.")
        return

    # 1. CSS 디자인 정의 (사용자 커스텀 디자인 반영)
    st.markdown("""
        <style>
        .news-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin-top: 20px;
        }
        .news-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
            position: relative;
        }
        .news-card:hover {
            border-color: #111111;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transform: translateY(-2px);
        }
        .news-category {
            font-size: 0.75rem;
            color: #666666;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 10px;
            letter-spacing: 0.05em;
        }
        .news-title-link {
            font-size: 1.4rem;
            font-weight: 700;
            color: #111111;
            line-height: 1.4;
            margin-bottom: 15px;
            text-decoration: none;
            display: block;
        }
        .news-title-link:hover {
            color: #333333;
            text-decoration: underline;
        }
        .news-snippet {
            font-size: 0.95rem;
            color: #444444;
            line-height: 1.6;
            margin-bottom: 20px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .news-footer {
            font-size: 0.85rem;
            color: #888888;
            border-top: 1px solid #f0f0f0;
            padding-top: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .news-meta {
            display: flex;
            gap: 15px;
        }
        .read-more-btn {
            background-color: #111111;
            color: #ffffff !important;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
            text-decoration: none;
            transition: background 0.2s;
        }
        .read-more-btn:hover {
            background-color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. 뉴스 목록을 HTML 문자열로 구축
    html_content = '<div class="news-container">'
    
    # 반복문을 사용하여 각 뉴스를 카드로 생성
    for article in articles:
        # 데이터 가공 및 보안(Escape) 처리
        title = html.escape(article.title)
        snippet = html.escape(article.snippet)
        url = article.url
        date = html.escape(article.pub_date.split('T')[0] if article.pub_date and 'T' in article.pub_date else (article.pub_date or "최신"))
        source = html.escape(article.source or "뉴스 피드")
        category = html.escape(article.category or "NEWS")
        
        # 개별 뉴스 카드 HTML 생성
        card_html = f"""
        <div class="news-card">
            <div class="news-category">{category}</div>
            <a href="{url}" target="_blank" class="news-title-link">{title}</a>
            <div class="news-snippet">{snippet}</div>
            <div class="news-footer">
                <div class="news-meta">
                    <span>📅 {date}</span>
                    <span>출처: <b>{source}</b></span>
                </div>
                <a href="{url}" target="_blank" class="read-more-btn">원문 보기 ↗</a>
            </div>
        </div>
        """
        html_content += card_html
    
    html_content += '</div>'

    # 3. st.markdown을 사용하여 실제 UI로 렌더링
    st.markdown(html_content, unsafe_allow_html=True)
