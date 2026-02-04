"""
日期選擇元件
使用 Streamlit date_input，選擇後更新 session_state
"""
import streamlit as st
from datetime import date


def render_date_picker() -> str:
    """
    渲染日期選擇器，回傳選擇的日期字串（YYYY-MM-DD）

    Returns:
        選擇的日期字串
    """
    selected = st.date_input(
        "📅 日期",
        value=st.session_state.get("selected_date", date.today()),
        key="date_picker_input",
        label_visibility="collapsed",
    )
    st.session_state.selected_date = selected
    return selected.strftime("%Y-%m-%d")
