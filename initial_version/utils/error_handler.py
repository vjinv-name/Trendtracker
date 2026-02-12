import streamlit as st

ERROR_MESSAGES = {
    "api_key_invalid": "API 키를 확인해주세요 (401 Unauthorized)",
    "daily_limit_exceeded": "일일 검색 한도(100건)를 초과했습니다",
    "rate_limit_exceeded": "월간/분당 검색 한도를 초과했습니다 (429 Too Many Requests)",
    "no_results": "검색 결과가 없습니다",
    "network_error": "네트워크 연결을 확인해주세요 (Timeout or Connection Error)",
    "file_error": "파일 접근에 실패했습니다",
    "empty_input": "검색어를 입력해주세요",
    "bad_request": "잘못된 요청입니다 (API 파라미터 등을 확인하세요)",
    "server_error": "검색 서버 오류입니다. 잠시 후 다시 시도해주세요 (5xx Server Error)",
    "ai_error": "AI 요약 중 오류가 발생했습니다",
}

def handle_error(error_type: str, level: str = "error"):
    """level에 따라 st.error(), st.warning(), st.info()를 호출하여 에러 메시지 표시"""
    message = ERROR_MESSAGES.get(error_type, f"알 수 없는 오류가 발생했습니다: {error_type}")
    
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)
    else:
        st.error(message)
