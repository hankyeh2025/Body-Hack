"""
預覽編輯元件
顯示 AI 辨識結果的預覽，支援編輯模式和儲存
"""
import streamlit as st
from typing import Dict, Any
from datetime import datetime

from core import get_sheets_client, StructuredEvent
from utils.ui_components import show_error_message
from .dialog_utils import close_dialog


def show_preview_editor(result: Dict[str, Any]):
    """
    顯示 AI 辨識結果預覽，支援編輯和儲存

    Args:
        result: AI 辨識結果 dict
    """
    record_type = result.get("type", "unknown")

    if record_type == "error":
        show_error_message(f"AI 辨識發生錯誤：{result.get('message', '未知錯誤')}")
        _show_retry_button()
        return

    if record_type == "unknown":
        st.warning("無法辨識輸入類型")
        _show_manual_fallback()
        return

    if record_type == "meal":
        _show_meal_preview(result)
    else:
        st.info(f"已辨識為「{record_type}」類型，此功能將在後續版本支援。")
        st.write("目前僅支援飲食記錄。")
        if st.button("↩ 返回重新輸入"):
            st.session_state.input_phase = "input"
            st.rerun()


def _show_meal_preview(result: Dict[str, Any]):
    """顯示飲食記錄預覽"""
    data = result.get("data", {})
    is_editing = st.session_state.get("preview_editing", False)

    confidence = result.get("confidence", 0.0)
    st.caption(f"AI 辨識信心度：{confidence:.0%}")

    if is_editing:
        _show_meal_edit_form(data)
    else:
        _show_meal_display(data)


def _show_meal_display(data: Dict[str, Any]):
    """顯示飲食記錄（唯讀預覽）"""
    meal_type = data.get("meal_type", "其他")
    content = data.get("content", "")
    starch_level = data.get("starch_level", "")
    nutrition = data.get("estimated_nutrition", "")

    st.subheader("🍽️ 飲食記錄")
    st.write(f"**餐別**：{meal_type}")
    st.write(f"**內容**：{content}")
    if starch_level:
        st.write(f"**澱粉量**：{starch_level}")
    if nutrition:
        st.write(f"**營養推估** [推估]：{nutrition}")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✓ 儲存", type="primary", use_container_width=True):
            _save_meal_record(data)
    with col2:
        if st.button("✏️ 修改", use_container_width=True):
            st.session_state.preview_editing = True
            st.rerun()
    with col3:
        if st.button("✕ 取消", use_container_width=True):
            close_dialog()


def _show_meal_edit_form(data: Dict[str, Any]):
    """顯示飲食記錄編輯表單"""
    st.subheader("✏️ 修改飲食記錄")

    meal_types = ["早餐", "午餐", "晚餐", "點心", "宵夜", "其他"]
    current_meal_type = data.get("meal_type", "其他")
    default_index = (
        meal_types.index(current_meal_type)
        if current_meal_type in meal_types
        else len(meal_types) - 1
    )

    edited_meal_type = st.selectbox(
        "餐別",
        meal_types,
        index=default_index,
        key="edit_meal_type"
    )

    edited_content = st.text_area(
        "內容",
        value=data.get("content", ""),
        key="edit_content"
    )

    starch_options = ["無", "少", "中", "多"]
    current_starch = data.get("starch_level", "中")
    starch_index = (
        starch_options.index(current_starch)
        if current_starch in starch_options
        else 2
    )

    edited_starch = st.selectbox(
        "澱粉量",
        starch_options,
        index=starch_index,
        key="edit_starch"
    )

    edited_nutrition = st.text_area(
        "營養推估 [推估]",
        value=data.get("estimated_nutrition", ""),
        key="edit_nutrition"
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("確認修改", type="primary", use_container_width=True):
            updated_data = {
                "meal_type": edited_meal_type,
                "content": edited_content,
                "starch_level": edited_starch,
                "estimated_nutrition": edited_nutrition
            }
            st.session_state.ai_result["data"] = updated_data
            st.session_state.preview_editing = False
            st.rerun()
    with col2:
        if st.button("取消修改", use_container_width=True):
            st.session_state.preview_editing = False
            st.rerun()


def _save_meal_record(data: Dict[str, Any]) -> None:
    """儲存飲食記錄到 Structured_Events Sheet"""
    try:
        client = get_sheets_client()
        now = datetime.now()

        event = StructuredEvent(
            datetime=now.isoformat(),
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M"),
            category="meal",
            sub_category=data.get("meal_type", "其他"),
            content=data.get("content", ""),
            starch_level=data.get("starch_level"),
            note=data.get("estimated_nutrition", "")
        )

        success = client.append_row("Structured_Events", event.model_dump())
        if success:
            st.session_state.save_success = True
            close_dialog()
        else:
            show_error_message("儲存失敗，請重試")
    except Exception as e:
        show_error_message(f"儲存失敗：{e}")


def _show_retry_button():
    """顯示重試和關閉按鈕"""
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 重試", use_container_width=True):
            st.session_state.input_phase = "input"
            st.rerun()
    with col2:
        if st.button("✕ 關閉", use_container_width=True, key="retry_close"):
            close_dialog()


def _show_manual_fallback():
    """顯示手動選擇類型的選項"""
    st.write("請手動選擇記錄類型：")

    if st.button("🍽️ 飲食記錄", use_container_width=True):
        original_input = st.session_state.get("original_input", "")
        st.session_state.ai_result = {
            "type": "meal",
            "confidence": 0.0,
            "data": {
                "meal_type": "其他",
                "content": original_input,
                "starch_level": "中",
                "estimated_nutrition": ""
            }
        }
        st.session_state.preview_editing = True
        st.rerun()

    st.caption("其他類型（飲水、運動、簡易事件）將在後續版本支援")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("↩ 返回重新輸入", key="manual_back"):
            st.session_state.input_phase = "input"
            st.rerun()
    with col2:
        if st.button("✕ 關閉", key="manual_close"):
            close_dialog()
