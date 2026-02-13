import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """사이드바 헤더 영역을 렌더링합니다."""
    st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E0E0E0;
            padding-top: 1rem;
        }
        .sidebar-brand {
            font-size: 2.2rem;
            font-weight: 800;
            color: #111;
            margin-bottom: 0px;
            letter-spacing: -1px;
            text-align: left;
        }
        </style>
        <div class="sidebar-brand">Antigravity</div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")

def render_settings() -> tuple:
    """검색 건수, 카테고리 및 언어 설정을 수행하고 선택된 값을 반환합니다."""
    # 언어 모드 설정 (Stage 2.1)
    language = st.sidebar.radio("검색 언어 설정 (Language)", ["한국어 (KR)", "English (US)"])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("엔진 옵션")
    use_ai_expansion = st.sidebar.checkbox("AI 검색어 최적화", value=True)
    spell_check = st.sidebar.checkbox("오타 자동 수정 기능", value=True)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("상세 필터")
    
    with st.sidebar.container():
        count = st.slider("가져올 뉴스 수", min_value=3, max_value=30, value=12)
        
        categories = [
            "전체", "과학/기술", "의학/바이오", "IT/공학", "사회", 
            "문화/예술", "스포츠", "경제/금융", "정치", "기타"
        ]
        category = st.selectbox("카테고리 필터", options=categories, index=0)

        time_ranges = {
            "모든 시간": None,
            "최근 24시간": "day",
            "최근 1주일": "week",
            "최근 1개월": "month"
        }
        time_range_label = st.selectbox("업데이트 기준", options=list(time_ranges.keys()), index=0)
        time_range = time_ranges[time_range_label]

        use_all_sources = st.checkbox("뉴스 데이터 다양화", value=True)
        
    return count, category, time_range, use_ai_expansion, use_all_sources, language, spell_check

def render_history_list(search_keys: List[str], keywords_map: dict) -> Optional[str]:
    """과거 검색 기록 목록을 렌더링하고 선택된 search_key를 반환합니다."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("히스토리")
    
    if not search_keys:
        st.sidebar.info("검색 기록이 없습니다.")
        return None
        
    options = []
    for key in search_keys:
        keyword = keywords_map.get(key, "키워드")
        try:
            timestamp_str = key.split('-')[-1]
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M")
            display_time = dt.strftime("%m/%d %H:%M")
        except:
            display_time = "Unk"
            
        options.append(f"{keyword} ({display_time})")
    
    selected_option = st.sidebar.selectbox(
        "기록 불러오기",
        options=options,
        index=None,
        placeholder="과거 기록 선택",
        key="history_selectbox"
    )
    
    if selected_option:
        idx = options.index(selected_option)
        return search_keys[idx]
        
    return None

def render_download_button(csv_data: str, is_empty: bool):
    """CSV 전체 데이터를 다운로드하는 버튼을 렌더링합니다."""
    if not is_empty:
        st.sidebar.markdown("---")
        now = datetime.now().strftime("%Y%m%d")
        st.sidebar.download_button(
            label="전체 데이터 내보내기",
            data=csv_data,
            file_name=f"antigravity_{now}.csv",
            mime="text/csv",
            use_container_width=True
        )

def render_info():
    """사이드바 하단에 이용 가이드북 섹션을 렌더링합니다."""
    st.sidebar.markdown("---")
    with st.sidebar.expander("📘 TrendTracker 이용 가이드북", expanded=False):
        st.write("""
        1. **키워드 입력**: 분석하고 싶은 트렌드 키워드를 입력창에 넣으세요.
        2. **언어 설정**: 사이드바에서 한국어 또는 영어 뉴스를 선택할 수 있습니다.
        3. **카드 클릭**: 제목을 클릭하면 해당 뉴스의 상세 원문으로 이동합니다.
        """)
        
    st.sidebar.markdown("<br><br><p style='text-align: center; color: #aaa; font-size: 0.7rem;'>Antigravity AI<br>v2.6.0 Stable</p>", unsafe_allow_html=True)
