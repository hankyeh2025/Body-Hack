"""
Body Hack - 健康數據追蹤系統
主程式入口
"""
import streamlit as st

# 測試模組 import
from core.placeholder import get_core_status
from features.placeholder import get_features_status
from utils.placeholder import get_utils_status

st.set_page_config(
    page_title="Body Hack",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Body Hack")
st.caption("健康數據追蹤系統")

st.divider()

st.subheader("🔧 Phase 0：部署驗證")

# 驗證模組載入
st.write("**模組載入狀態：**")
col1, col2, col3 = st.columns(3)

with col1:
    status = get_core_status()
    st.metric("Core", "✅" if status else "❌")

with col2:
    status = get_features_status()
    st.metric("Features", "✅" if status else "❌")

with col3:
    status = get_utils_status()
    st.metric("Utils", "✅" if status else "❌")

st.divider()

st.success("🎉 如果你看到這個畫面，表示部署成功！")

st.info("""
**下一步：Phase 1**
- 設定 Google Sheets 連線
- 設定 Gemini API 連線
""")
