"""
時間軸元件
以氣泡流顯示當日記錄，最新在上
"""
import streamlit as st
from typing import List, Dict, Any


def render_timeline(records: List[Dict[str, Any]]):
    """
    渲染時間軸

    Args:
        records: get_records_by_date 的回傳值（已按 datetime 降序排列）
    """
    if not records:
        st.info("今天還沒有記錄，點擊「＋輸入」開始")
        return

    with st.container(height=400):
        for record in records:
            time_str = record.get("time", "")
            icon = record.get("icon", "📝")
            content = record.get("content", "")

            st.markdown(
                f"**{time_str}**&ensp;{icon}&ensp;{content}"
            )
