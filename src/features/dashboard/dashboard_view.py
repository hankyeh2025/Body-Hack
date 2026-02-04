"""
儀表板元件
顯示今日飲水量、餐數、吸菸次數
"""
import streamlit as st
from typing import Dict, Any


def render_dashboard(stats: Dict[str, Any]):
    """
    渲染儀表板統計列

    Args:
        stats: get_dashboard_stats 的回傳值
            {"water_ml": int, "meal_count": int, "smoke_count": int}
    """
    water_ml = stats.get("water_ml", 0)
    meal_count = stats.get("meal_count", 0)
    smoke_count = stats.get("smoke_count", 0)

    st.markdown(
        f"💧 **{water_ml}ml**&emsp;"
        f"🍽 **{meal_count} 餐**&emsp;"
        f"🚬 **{smoke_count} 根**"
    )
