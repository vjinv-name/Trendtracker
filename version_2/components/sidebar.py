import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """사이드바 헤더 영역을 렌더링합니다."""
    st.sidebar.title("💠 TrendTracker")
    st.sidebar.markdown("키워드로 뉴스를 검색하고 AI가 요약해드립니다")
    st.sidebar.markdown("---")

def render_settings() -> tuple:
    """검색 건수 및 카테고리 설정을 위한 렌더링을 수행하고 선택된 값을 반환합니다."""
    with st.sidebar.expander("⚙️ 검색 설정", expanded=True):
        count = st.slider("검색 뉴스 건수", min_value=1, max_value=20, value=5)
        
        categories = [
            "전체", "과학", "의학", "공학", "사회", 
            "문화", "예술", "스포츠", "경제", "정치", "기타"
        ]
        category = st.selectbox("뉴스 카테고리", options=categories, index=0)

        # 날짜 시간 관련 설정 추가
        time_ranges = {
            "전체 기간": None,
            "최근 1일": "day",
            "최근 1주일": "week",
            "최근 1개월": "month"
        }
        time_range_label = st.selectbox("검색 기간", options=list(time_ranges.keys()), index=0)
        time_range = time_ranges[time_range_label]

        # Stage 4: 고급 옵션
        st.markdown("---")
        st.markdown("**🚀 알고리즘 고도화**")
        use_ai_expansion = st.checkbox("AI 검색어 최적화", value=True, help="Gemini가 검색어를 분석하여 더 나은 결과를 찾도록 쿼리를 확장합니다.")
        use_all_sources = st.checkbox("모든 언론사 검색(다양성)", value=False, help="체크 시 지정된 주요 언론사 외의 모든 신뢰할 수 있는 매체를 검색합니다.")
        
    return count, category, time_range, use_ai_expansion, use_all_sources

def render_history_list(search_keys: List[str], keywords_map: dict) -> Optional[str]:
    """과거 검색 기록 목록을 렌더링하고 선택된 search_key를 반환합니다."""
    st.sidebar.subheader("📜 검색 기록")
    
    if not search_keys:
        st.sidebar.info("저장된 검색 기록이 없습니다")
        return None
        
    # 표시 형식: "키워드 (yyyy-mm-dd HH:MM)"
    options = []
    for key in search_keys:
        keyword = keywords_map.get(key, "알 수 없는 키워드")
        try:
            # key 형식: "키워드-yyyymmddhhmm"
            timestamp_str = key.split('-')[-1]
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
            display_time = dt.strftime("%Y-%m-%d %H:%M")
        except:
            display_time = "시간 정보 없음"
            
        options.append(f"{keyword} ({display_time})")
    
    selected_option = st.sidebar.selectbox(
        "다시 볼 기록 선택",
        options=options,
        index=None,
        placeholder="기록을 선택하세요",
        key="history_selectbox"
    )
    
    if selected_option:
        # 선택된 옵션의 인덱스로 search_key 찾기
        idx = options.index(selected_option)
        return search_keys[idx]
        
    return None

def render_download_button(csv_data: str, is_empty: bool):
    """CSV 전체 데이터를 다운로드하는 버튼을 렌더링합니다."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 데이터 백업")
    
    if is_empty:
        st.sidebar.info("다운로드할 데이터가 없습니다")
    else:
        now = datetime.now().strftime("%Y%m%d")
        st.sidebar.download_button(
            label="전체 기록 다운로드 (CSV)",
            data=csv_data,
            file_name=f"trendtracker_export_{now}.csv",
            mime="text/csv",
            use_container_width=True
        )

def render_info():
    """사이드바 하단에 사용 안내 및 정보 섹션을 렌더링합니다."""
    st.sidebar.markdown("---")
    with st.sidebar.expander("ℹ️ 사용법", expanded=False):
        st.markdown("""
        1. 검색어를 입력하고 **'트렌드 분석 시작'** 버튼을 누르세요.
        2. 최신 뉴스를 검색하고 AI가 핵심 내용을 요약합니다.
        3. 과거 검색 기록은 사이드바에서 다시 선택하여 조회할 수 있습니다.
        """)
        
    with st.sidebar.expander("📊 API 한도", expanded=False):
        st.markdown("""
        - **Tavily**: 무료 플랜 기준 월 1,000건 검색 가능
        - **Gemini**: 무료 플랜 기준 분당 15회 요청 가능
        """)
        
    with st.sidebar.expander("💾 데이터 저장 안내", expanded=False):
        st.markdown("""
        - 검색 기록은 로컬 CSV 파일(`data/search_history.csv`)에 저장됩니다.
        - 중요한 기록은 다운로드 기능을 통해 주기적으로 백업하세요.
        """)
        
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 TrendTracker AI")
