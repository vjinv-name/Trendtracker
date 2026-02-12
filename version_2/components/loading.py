import streamlit as st
from contextlib import contextmanager

@contextmanager
def show_loading(message: str):
    """
    st.spinner를 사용하여 로딩 상태를 표시하는 context manager입니다.
    
    사용 예:
    with show_loading("데이터를 가져오는 중..."):
        # 로직 실행
    """
    with st.spinner(message):
        yield
