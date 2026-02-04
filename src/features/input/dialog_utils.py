"""
Dialog 共用工具函式
"""
import streamlit as st


def close_dialog():
    """關閉 Dialog 並清理狀態"""
    st.session_state.show_input_dialog = False
    st.session_state.input_phase = "input"
    st.session_state.preview_editing = False
    for key in ["ai_result", "original_input"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
