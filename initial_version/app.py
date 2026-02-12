import streamlit as st
from datetime import datetime
from config.settings import settings
from domain.search_result import SearchResult
from services.search_service import search_news
from services.ai_service import summarize_news
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
    num_results = render_settings()
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
    st.title("🚀 TrendTracker")
    st.markdown("최신 뉴스를 기반으로 실시간 트렌드를 분석하고 요약해드립니다.")
    st.markdown("---")

    # 검색 폼
    search_keyword = render_search_form()
    
    if search_keyword:
        # 새로운 검색 시작
        st.session_state.current_mode = "new_search"
        st.session_state.selected_key = None # 기록 선택 해제
        
        try:
            # 뉴스 검색
            with show_loading("🔍 뉴스를 검색하고 있습니다..."):
                articles = search_news(search_keyword, num_results)
            
            if not articles:
                st.info("검색 결과가 없습니다.")
                st.session_state.last_result = None
            else:
                # AI 요약
                with show_loading("🤖 AI가 내용을 요약하고 있습니다..."):
                    summary = summarize_news(articles)
                
                # 결과 객체 생성
                result = SearchResult(
                    search_key=generate_search_key(search_keyword),
                    search_time=datetime.now(),
                    keyword=search_keyword,
                    articles=articles,
                    ai_summary=summary
                )
                
                # 저장
                with show_loading("💾 결과를 저장하고 있습니다..."):
                    if repository.save(result):
                        st.session_state.last_result = result
                        st.success(f"'{search_keyword}' 분석 완료! {len(articles)}건의 뉴스를 찾았습니다.")
                    else:
                        st.error("결과 저장 중 오류가 발생했습니다.")
                        st.session_state.last_result = result
        
        except AppError as e:
            handle_error(e.error_type)
            st.session_state.last_result = None
        except Exception as e:
            st.error(f"알 수 없는 오류가 발생했습니다: {e}")
            st.session_state.last_result = None

    # 결과 표시 영역
    if st.session_state.current_mode == "new_search":
        if st.session_state.last_result:
            res = st.session_state.last_result
            render_summary(res.keyword, res.ai_summary)
            render_news_list(res.articles)
        elif not search_keyword:
            # 초기 화면 환영 메시지
            st.info("👋 환영합니다! 분석하고 싶은 키워드를 상단에 입력하고 버튼을 눌러보세요.")
            if not search_keys:
                st.caption("아직 검색 기록이 없습니다. 첫 번째 검색을 시작해보세요!")
        
    elif st.session_state.current_mode == "history" and st.session_state.selected_key:
        # 기록 모드에서 결과 불러오기
        history_result = repository.find_by_key(st.session_state.selected_key)
        if history_result:
            render_summary(history_result.keyword, history_result.ai_summary)
            render_news_list(history_result.articles)
        else:
            st.error("해당 기록을 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
