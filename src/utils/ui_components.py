"""
共用 UI 元件
"""
import streamlit as st


def show_success_message(msg: str):
    """顯示成功訊息"""
    st.success(f"✅ {msg}")


def show_error_message(msg: str):
    """顯示錯誤訊息"""
    st.error(f"❌ {msg}")


def show_loading(msg: str = "處理中..."):
    """顯示載入中狀態，回傳 spinner context manager"""
    return st.spinner(msg)
