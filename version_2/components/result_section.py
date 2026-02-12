import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.markdown("---")
    st.subheader(f"🤖 '{title}' 트렌드 요약")
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 리스트를 핀터레스트 스타일 그리드로 렌더링합니다."""
    st.markdown("---")
    st.subheader("📰 관련 트렌드 뉴스")
    
    if not articles:
        st.info("관련 뉴스 기사가 없습니다.")
        return

    # 핀터레스트 스타일 카드 디자인을 위한 커스텀 CSS
    st.markdown("""
        <style>
        /* 카드 컨테이너 */
        .news-card-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: space-between;
        }
        /* 개별 카드 */
        .st-emotion-cache-12w0qpk { /* 스트림릿 컬럼 여백 조정 */
            padding: 0 !important;
        }
        div[data-testid="column"] {
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #e1e4e8;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 20px;
        }
        div[data-testid="column"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            border-color: #0366d6;
        }
        .date-tag {
            color: #888;
            font-size: 0.75rem;
            margin-bottom: 5px;
            display: block;
        }
        .article-title {
            font-weight: bold;
            font-size: 1.1rem;
            margin-bottom: 10px;
            color: #1f2328;
            text-decoration: none;
            line-height: 1.3;
        }
        .article-snippet {
            font-size: 0.9rem;
            color: #444;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-top: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3열 그리드 생성
    cols = st.columns(3)
    
    for i, article in enumerate(articles):
        with cols[i % 3]:
            # 발행 날짜
            if article.pub_date:
                date_str = article.pub_date.split('T')[0] if 'T' in article.pub_date else article.pub_date
                st.markdown(f"<span class='date-tag'>📅 {date_str}</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='date-tag'>📅 날짜 정보 없음</span>", unsafe_allow_html=True)
            
            # 제목
            st.markdown(f"<a href='{article.url}' target='_blank' style='text-decoration: none;'><div class='article-title'>{article.title}</div></a>", unsafe_allow_html=True)
            
            # 썸네일 (이미지 기능 추가 시 활성화할 자리)
            if article.image_url:
                st.image(article.image_url, use_column_width=True)
            
            # 스니펫 (내용 요약)
            st.markdown(f"<div class='article-snippet'>{article.snippet}</div>", unsafe_allow_html=True)
            
            # 바로가기 링크 (이미 제목에 링크가 있지만 접근성을 위해 추가)
            st.markdown(f"[기사 읽기]({article.url})")
