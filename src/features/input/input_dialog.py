"""
輸入 Dialog UI
使用 @st.dialog 建立輸入彈窗
"""
import streamlit as st

from .ai_recognizer import recognize_input
from .preview_editor import show_preview_editor
from .dialog_utils import close_dialog


@st.dialog("輸入記錄", width="large")
def show_input_dialog():
    """輸入 Dialog 主函式"""
    phase = st.session_state.get("input_phase", "input")

    if phase == "input":
        _show_input_phase()
    elif phase == "preview":
        _show_preview_phase()


def _show_input_phase():
    """輸入階段 UI"""
    user_input = st.text_area(
        "今天吃了什麼？",
        placeholder="例：午餐吃了雞胸肉便當，飯半碗",
        height=120,
        key="dialog_text_input"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("✨送出", type="primary", use_container_width=True):
            if not user_input or not user_input.strip():
                st.warning("請輸入內容")
            else:
                with st.spinner("AI 辨識中..."):
                    result = recognize_input(user_input.strip())
                st.session_state.ai_result = result
                st.session_state.original_input = user_input.strip()
                st.session_state.input_phase = "preview"
                st.rerun()
    with col2:
        if st.button("✕ 關閉", use_container_width=True):
            close_dialog()


def _show_preview_phase():
    """預覽階段 UI"""
    result = st.session_state.get("ai_result", {})
    if not result:
        st.session_state.input_phase = "input"
        st.rerun()
        return

    show_preview_editor(result)
