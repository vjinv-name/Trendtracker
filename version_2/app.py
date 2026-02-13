import streamlit as st
from datetime import datetime
from config.settings import settings
from domain.search_result import SearchResult
from services.search_service import search_news
from services.ai_service import summarize_news, expand_query, correct_spelling, extract_keywords
from repositories.search_repository import SearchRepository
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, 
    render_settings, 
    render_info, 
    render_history_list, 
    render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key

def main():
    """
    TrendTracker 메인 애플리케이션 함수.
    전체 레이아웃 및 검색/조회 흐름을 관리합니다.
    """
    # 1. 페이지 설정
    st.set_page_config(page_title="TrendTracker", layout="wide")

    # 2. 초기화 (리포지토리 및 세션 상태)
    repository = SearchRepository(str(settings.csv_path))
    
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # 3. 사이드바 렌더링
    render_sidebar_header()
    num_results, category, time_range, use_ai_expansion, use_all_sources, language, spell_check = render_settings()
    render_info()
    
    # 검색 기록 목록 준비
    search_keys = repository.get_all_keys()
    keywords_map = {}
    for sk in search_keys:
        # search_key 형식: "키워드-yyyymmddhhmm"
        parts = sk.split('-')
        keyword = "-".join(parts[:-1]) if len(parts) > 1 else sk
        keywords_map[sk] = keyword
    
    # 기록 선택 시 세션 상태 업데이트 및 모드 전환
    history_selected_key = render_history_list(search_keys, keywords_map)
    if history_selected_key and history_selected_key != st.session_state.selected_key:
        st.session_state.selected_key = history_selected_key
        st.session_state.current_mode = "history"
        # 기록 선택 시 기존 검색 결과 초기화
        st.session_state.last_result = None
        st.rerun()

    # 다운로드 버튼
    csv_data = repository.get_all_as_csv()
    render_download_button(csv_data, len(search_keys) == 0)

    # 4. 메인 영역 렌더링
    st.markdown("""
        <style>
        /* 배경 그라데이션 및 전체 폰트 설정 */
        .stApp {
            background: linear-gradient(180deg, #FFFFFF 0%, #F0F2F6 100%);
            font-family: 'Pretendard', -apple-system, sans-serif;
        }

        /* 메인 타이틀 및 텍스트 시인성 */
        .main-title {
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -2px;
            color: #111111;
            margin-bottom: 0.5rem;
            text-align: left;
        }
        
        .main-subtitle {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 3rem;
        }

        /* 버튼 스타일 최적화 (사용자 요청: 직각 블랙 버튼) */
        div.stButton > button {
            background-color: #000000 !important;
            color: white !important;
            border-radius: 0px !important;
            border: none !important;
            padding: 0.6rem 2rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            background-color: #333333 !important;
            transform: translateY(-1px);
        }

        /* 입력창 디자인 */
        .stTextInput > div > div > input {
            border-radius: 0px !important;
            border: 1px solid #E0E0E0 !important;
            padding: 0.75rem 1rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-title">TrendTracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">전 세계 실시간 브레이킹 뉴스 및 트렌드 인사이트 분석기</div>', unsafe_allow_html=True)

    # 5. 검색창 영역 (Enter 키 지원을 위해 st.form 사용)
    with st.form("search_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])
        with col1:
            search_keyword = st.text_input(
                "트렌드 키워드를 입력하세요", 
                placeholder="예: 생성형 AI, 뉴욕 증시, 비건 요리",
                label_visibility="collapsed"
            )
        with col2:
            start_search = st.form_submit_button("분석 시작")

    st.markdown("---")

    # 6. 검색 정기 로직
    if start_search and search_keyword:
        st.session_state.current_mode = "new_search"
        st.session_state.selected_key = None # 기록 선택 해제
        
        try:
            # 오타 수정 로직 (사용 옵션 확인)
            actual_query = search_keyword
            if spell_check:
                with show_loading("검색어 교정 중..."):
                    corrected = correct_spelling(search_keyword)
                    if corrected.lower() != search_keyword.lower():
                        st.info(f"💡 '{corrected}'로 검색어를 교정하여 분석을 진행합니다.")
                        actual_query = corrected

            # AI 검색어 확장
            if use_ai_expansion:
                with show_loading("검색어 최적화 중..."):
                    actual_query = expand_query(actual_query)
                    st.toast(f"검색 최적화: {actual_query}")

            # 뉴스 검색
            with show_loading("데이터 수집 중..."):
                articles = search_news(
                    keyword=actual_query, 
                    num_results=num_results, 
                    category=category, 
                    time_range=time_range,
                    include_all_sources=use_all_sources,
                    language=language
                )
            
            if not articles:
                st.warning("일치하는 검색 결과가 없습니다.")
                st.session_state.last_result = None
            else:
                # AI 트렌드 분석 및 키워드 추출
                with show_loading("AI 종합 분석 보고서 생성 중..."):
                    summary = summarize_news(articles)
                    keywords = extract_keywords(articles)
                
                # 결과 객체 생성 및 저장
                result = SearchResult(
                    search_key=generate_search_key(search_keyword),
                    search_time=datetime.now(),
                    keyword=search_keyword,
                    articles=articles,
                    ai_summary=summary,
                    ai_keywords=keywords
                )
                
                if repository.save(result):
                    st.session_state.last_result = result
                    st.success(f"분석 완료: {len(articles)}건의 트렌드를 포착했습니다.")
                else:
                    st.error("결과 저장 중 오류가 발생했습니다.")
                    st.session_state.last_result = result
        
        except AppError as e:
            handle_error(e.error_type)
            st.session_state.last_result = None
        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.session_state.last_result = None

    # 7. 결과 표시 영역
    if st.session_state.current_mode == "new_search":
        if st.session_state.last_result:
            res = st.session_state.last_result
            render_summary(res.keyword, res.ai_summary, res.ai_keywords)
            render_news_list(res.articles)
        elif not search_keyword:
            render_info() # 초기 환영/가이드 메시지
        
    elif st.session_state.current_mode == "history" and st.session_state.selected_key:
        # 기록 모드에서 결과 불러오기
        history_result = repository.find_by_key(st.session_state.selected_key)
        if history_result:
            render_summary(history_result.keyword, history_result.ai_summary, history_result.ai_keywords)
            render_news_list(history_result.articles)
        else:
            st.error("해당 기록을 불러올 수 없습니다.")

if __name__ == "__main__":
    main()