import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    검색 폼을 렌더링하고 유효한 키워드가 입력되면 반환합니다.
    """
    st.markdown("""
        <style>
        .search-area {
            background: #f0f2f5;
            padding: 20px;
            border-radius: 30px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s ease;
        }
        .search-area:focus-within {
            background: #ffffff;
            box-shadow: 0 0 0 2px #1a1a1a;
        }
        /* 스트림릿 입력창 배경 투명화 */
        div[data-testid="stTextInput"] input {
            background-color: transparent !important;
            border: none !important;
            font-size: 1.1rem !important;
            padding: 10px 0 !important;
        }
        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            border: none !important;
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        # 검색창과 버튼을 한 줄에 배치
        col1, col2 = st.columns([5, 1])
        
        with col1:
            keyword_input = st.text_input(
                "트렌드 분석 키워드",
                placeholder="궁금한 트렌드를 입력하세요 (예: AI 로봇, K-푸드)",
                key="keyword_input",
                label_visibility="collapsed"
            )
        
        with col2:
            search_button = st.button("분석", type="primary", use_container_width=True)
            
        # 검색 실행 조건
        search_triggered = search_button
        
        if keyword_input and not search_button:
            if 'last_searched_keyword' not in st.session_state:
                st.session_state.last_searched_keyword = ""
            
            if keyword_input != st.session_state.last_searched_keyword:
                search_triggered = True

        if search_triggered:
            processed_keyword = preprocess_keyword(keyword_input)
            if not processed_keyword:
                if search_button:
                    st.warning("분석할 키워드를 입력해주세요.")
                return None
            
            st.session_state.last_searched_keyword = processed_keyword
            return processed_keyword
            
    return None
