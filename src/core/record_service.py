"""
記錄讀取服務
整合 Structured_Events + Simple_Events，提供統一的記錄查詢介面
"""
from datetime import datetime as dt
from typing import List, Dict, Any
from .sheets_client import get_sheets_client


# 類型圖示對照
CATEGORY_ICONS = {
    "meal": "🍽",
    "water": "💧",
    "exercise": "🏃",
    "smoke": "🚬",
    "吸菸": "🚬",
}
DEFAULT_ICON = "📝"


def get_icon(category: str) -> str:
    """取得類別對應的圖示"""
    return CATEGORY_ICONS.get(category, DEFAULT_ICON)


def _build_content_summary(record: Dict[str, Any], source: str) -> str:
    """從原始記錄建立內容摘要"""
    if source == "structured":
        category = record.get("category", "")
        if category == "meal":
            parts = []
            if record.get("sub_category"):
                parts.append(str(record["sub_category"]))
            if record.get("content"):
                parts.append(str(record["content"]))
            return "：".join(parts) if parts else "飲食記錄"
        elif category == "water":
            volume = record.get("volume_ml")
            if volume:
                return f"{volume}ml 水"
            return "飲水記錄"
        elif category == "exercise":
            parts = []
            if record.get("sub_category"):
                parts.append(str(record["sub_category"]))
            if record.get("duration_min"):
                parts.append(f"{record['duration_min']}分鐘")
            return " ".join(parts) if parts else "運動記錄"
        return record.get("content") or record.get("sub_category") or category
    else:
        # Simple_Events
        return record.get("description") or record.get("category", "")


def _normalize_record(record: Dict[str, Any], source: str) -> Dict[str, Any]:
    """將原始記錄轉為統一格式"""
    category = record.get("category", "")
    return {
        "datetime": record.get("datetime", ""),
        "time": record.get("time", ""),
        "category": category,
        "content": _build_content_summary(record, source),
        "icon": get_icon(category),
        "source": source,
        "raw": record,
    }


def get_records_by_date(date_str: str) -> List[Dict[str, Any]]:
    """
    取得指定日期的所有記錄（Structured_Events + Simple_Events）

    Args:
        date_str: 日期字串，格式 YYYY-MM-DD

    Returns:
        統一格式的記錄列表，依 datetime 降序排列

    Raises:
        Exception: Google Sheets 讀取失敗時拋出
    """
    client = get_sheets_client()

    structured = client.read_sheet(
        "Structured_Events", filters={"date": date_str}
    )
    simple = client.read_sheet(
        "Simple_Events", filters={"date": date_str}
    )

    records = []
    for r in structured:
        records.append(_normalize_record(r, "structured"))
    for r in simple:
        records.append(_normalize_record(r, "simple"))

    def _sort_key(record):
        """解析 datetime 字串為時間物件，確保正確排序"""
        raw_dt = record.get("datetime", "")
        try:
            return dt.fromisoformat(raw_dt)
        except (ValueError, TypeError):
            return dt.min

    records.sort(key=_sort_key, reverse=True)
    return records


def get_dashboard_stats(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    從記錄列表計算儀表板統計數據

    Args:
        records: get_records_by_date 的回傳值

    Returns:
        {"water_ml": int, "meal_count": int, "smoke_count": int}
    """
    water_ml = 0
    meal_count = 0
    smoke_count = 0

    for r in records:
        raw = r.get("raw", {})
        category = r.get("category", "")

        if category == "water" and r["source"] == "structured":
            vol = raw.get("volume_ml")
            if vol:
                try:
                    water_ml += int(vol)
                except (ValueError, TypeError):
                    pass

        elif category == "meal" and r["source"] == "structured":
            meal_count += 1

        elif category in ("smoke", "吸菸") and r["source"] == "simple":
            smoke_count += 1

    return {
        "water_ml": water_ml,
        "meal_count": meal_count,
        "smoke_count": smoke_count,
    }
