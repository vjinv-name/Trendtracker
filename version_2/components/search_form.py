import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    검색 폼을 렌더링하고 유효한 키워드가 입력되면 반환합니다.
    """
    with st.container():
        # 검색창과 버튼을 한 줄에 배치
        col1, col2 = st.columns([4, 1])
        
        with col1:
            keyword_input = st.text_input(
                "트렌드 분석 키워드",
                placeholder="예: AI 에이전트, 2026 경제 전망",
                key="keyword_input",
                label_visibility="collapsed" # 레이블 숨김 (공간 절약)
            )
        
        with col2:
            search_button = st.button("분석 시작", type="primary", use_container_width=True)
            
        # 검색 실행 조건: 버튼 클릭 OR 엔터키 입력 (입력값이 있고 이전 입력과 다를 때)
        search_triggered = search_button
        
        if keyword_input and not search_button:
            # 엔터키 감지 로직 (마지막 성공 검색어와 대조)
            if 'last_searched_keyword' not in st.session_state:
                st.session_state.last_searched_keyword = ""
            
            if keyword_input != st.session_state.last_searched_keyword:
                # 엔터키 입력으로 검색 트리거 (전처리 후)
                search_triggered = True

        if search_triggered:
            processed_keyword = preprocess_keyword(keyword_input)
            if not processed_keyword:
                if search_button: # 버튼 눌렀을 때만 경고
                    st.warning("분석할 키워드를 입력해주세요.")
                return None
            
            # 검색 시작 시 마지막 검색어 업데이트 (중복 방지)
            st.session_state.last_searched_keyword = processed_keyword
            return processed_keyword
            
    return None
