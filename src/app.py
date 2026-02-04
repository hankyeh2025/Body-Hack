"""
Body Hack - 健康數據追蹤系統
主程式入口
"""
import streamlit as st
from datetime import datetime

# 匯入核心模組
from core import (
    get_sheets_client,
    get_gemini_client,
    StructuredEvent,
    generate_id
)

st.set_page_config(
    page_title="Body Hack",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Body Hack")
st.caption("健康數據追蹤系統")

st.divider()

# === Phase 1：連線測試 ===
st.subheader("🔧 Phase 1：連線測試")

tab1, tab2, tab3 = st.tabs(["Google Sheets", "Gemini API", "寫入測試"])

# --- Tab 1: Sheets 連線測試 ---
with tab1:
    st.write("**Google Sheets 連線狀態**")

    if st.button("測試 Sheets 連線", key="test_sheets"):
        with st.spinner("連線中..."):
            client = get_sheets_client()
            result = client.test_connection()

        if result["success"]:
            st.success("✅ 連線成功！")
            st.write(f"**試算表名稱**：{result['title']}")
            st.write(f"**分頁列表**：{', '.join(result['worksheets'])}")
            st.write(f"**URL**：{result['url']}")
        else:
            st.error(f"❌ 連線失敗：{result['error']}")

# --- Tab 2: Gemini 連線測試 ---
with tab2:
    st.write("**Gemini API 連線狀態**")

    if st.button("測試 Gemini 連線", key="test_gemini"):
        with st.spinner("連線中..."):
            client = get_gemini_client()
            result = client.test_connection()

        if result["success"]:
            st.success("✅ 連線成功！")
            st.write(f"**模型**：{result['model']}")
            st.write(f"**回應**：{result['response']}")
        else:
            st.error(f"❌ 連線失敗：{result['error']}")

# --- Tab 3: 寫入測試 ---
with tab3:
    st.write("**測試寫入 Structured_Events**")

    test_content = st.text_input("測試內容", value="Phase 1 測試記錄")

    if st.button("寫入測試記錄", key="test_write"):
        with st.spinner("寫入中..."):
            client = get_sheets_client()

            now = datetime.now()
            event = StructuredEvent(
                datetime=now.isoformat(),
                date=now.strftime("%Y-%m-%d"),
                time=now.strftime("%H:%M"),
                category="meal",
                sub_category="測試",
                content=test_content,
                note="Phase 1 寫入測試"
            )

            try:
                success = client.append_row(
                    "Structured_Events",
                    event.model_dump()
                )
                if success:
                    st.success("✅ 寫入成功！請到 Google Sheet 確認")
                    st.json(event.model_dump())
            except Exception as e:
                st.error(f"❌ 寫入失敗：{e}")

    st.divider()

    st.write("**讀取 Structured_Events**")
    if st.button("讀取記錄", key="test_read"):
        with st.spinner("讀取中..."):
            client = get_sheets_client()
            try:
                records = client.read_sheet("Structured_Events")
                st.write(f"共 {len(records)} 筆記錄")
                if records:
                    st.dataframe(records)
            except Exception as e:
                st.error(f"❌ 讀取失敗：{e}")

st.divider()

st.info("""
**Phase 1 驗收標準**：
- ✅ Sheets 連線成功，能看到分頁列表
- ✅ Gemini 連線成功，能收到回應
- ✅ 能寫入測試記錄到 Sheet
- ✅ 能讀取 Sheet 記錄
""")
