"""
Body Hack - 健康數據追蹤系統
主程式入口
"""
import streamlit as st
from datetime import datetime

from core import (
    get_sheets_client,
    get_gemini_client,
    StructuredEvent,
    generate_id
)
from core.record_service import get_records_by_date, get_dashboard_stats
from features.input import show_input_dialog
from features.date_picker import render_date_picker
from features.dashboard import render_dashboard
from features.timeline import render_timeline

st.set_page_config(
    page_title="Body Hack",
    page_icon="💪",
    layout="centered"
)

st.title("💪 Body Hack")
st.caption("健康數據追蹤系統")

# === 儲存成功提示 ===
if st.session_state.pop("save_success", False):
    st.toast("✅ 記錄已儲存！")

# === 頂部：日期選擇 + 儀表板 ===
selected_date = render_date_picker()

# === 載入記錄 ===
load_error = None
records = []

# 支援重試：點擊重試時清除錯誤並重新載入
if st.session_state.pop("retry_load", False):
    pass  # 繼續正常載入流程

try:
    with st.spinner("載入記錄中..."):
        records = get_records_by_date(selected_date)
except Exception as e:
    load_error = str(e)

# === 儀表板 ===
if load_error is None:
    stats = get_dashboard_stats(records)
    render_dashboard(stats)
else:
    render_dashboard({"water_ml": 0, "meal_count": 0, "smoke_count": 0})

st.divider()

# === 操作按鈕：＋輸入 / 🤖 AI ===
col_input, col_ai = st.columns(2)
with col_input:
    if st.button("＋ 輸入", type="primary", use_container_width=True):
        st.session_state.show_input_dialog = True
        st.session_state.input_phase = "input"
with col_ai:
    st.button("🤖 AI", use_container_width=True, disabled=True)

if st.session_state.get("show_input_dialog", False):
    show_input_dialog()

st.divider()

# === 時間軸 ===
if load_error is not None:
    st.error("無法載入記錄，請檢查網路連線")
    if st.button("重試"):
        st.session_state.retry_load = True
        st.rerun()
else:
    render_timeline(records)

# === Phase 1：連線測試（保留供除錯） ===
with st.expander("🔧 連線測試（Phase 1）"):
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
