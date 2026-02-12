import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    검색 폼을 렌더링하고 유효한 키워드가 입력되면 반환합니다.
    """
    with st.container():
        keyword_input = st.text_input(
            "트렌드 분석 키워드",
            placeholder="예: AI 에이전트, 2026 경제 전망",
            key="keyword_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            search_button = st.button("트렌드 분석 시작", type="primary", use_container_width=True)
            
        if search_button:
            if not keyword_input:
                st.warning("검색어를 입력해주세요.")
                return None
                
            processed_keyword = preprocess_keyword(keyword_input)
            if not processed_keyword:
                st.warning("유효한 검색어를 입력해주세요.")
                return None
                
            return processed_keyword
            
    return None
