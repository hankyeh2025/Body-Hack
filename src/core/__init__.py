"""
Core 模組 - 核心邏輯層
"""
from .sheets_client import SheetsClient, get_sheets_client
from .gemini_client import GeminiClient, get_gemini_client
from .data_models import (
    PhysioRecord,
    StructuredEvent,
    SimpleEvent,
    Insight,
    Goal,
    AnalyticsEvent,
    generate_id
)
from .record_service import get_records_by_date, get_dashboard_stats

__all__ = [
    "SheetsClient",
    "get_sheets_client",
    "GeminiClient",
    "get_gemini_client",
    "PhysioRecord",
    "StructuredEvent",
    "SimpleEvent",
    "Insight",
    "Goal",
    "AnalyticsEvent",
    "generate_id",
    "get_records_by_date",
    "get_dashboard_stats",
]
