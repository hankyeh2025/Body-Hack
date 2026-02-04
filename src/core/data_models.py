"""
資料模型定義
使用 Pydantic 進行資料驗證
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


def generate_id() -> str:
    """產生短 UUID"""
    return uuid.uuid4().hex[:8]


class PhysioRecord(BaseModel):
    """生理數據記錄"""
    id: str = Field(default_factory=generate_id)
    datetime: str  # ISO 8601
    date: str
    time: str
    source: str  # cgm / garmin / bp_monitor / body_scale / manual
    blood_glucose: Optional[int] = None
    glucose_trend: Optional[str] = None  # → ↑ ↓ ↑↑ ↓↓
    weight: Optional[float] = None
    body_fat: Optional[float] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    hrv: Optional[int] = None
    sleep_score: Optional[int] = None
    steps: Optional[int] = None
    floors: Optional[int] = None
    note: Optional[str] = None


class StructuredEvent(BaseModel):
    """結構化事件（飲食/運動/飲水）"""
    id: str = Field(default_factory=generate_id)
    datetime: str
    date: str
    time: str
    category: str  # meal / exercise / water
    sub_category: Optional[str] = None
    content: Optional[str] = None
    starch_level: Optional[str] = None  # 無 / 少 / 中 / 多
    is_alcohol: Optional[bool] = None
    duration_min: Optional[int] = None
    intensity: Optional[str] = None  # 低 / 中 / 高
    volume_ml: Optional[int] = None
    note: Optional[str] = None


class SimpleEvent(BaseModel):
    """簡易事件"""
    id: str = Field(default_factory=generate_id)
    datetime: str
    date: str
    time: str
    category: str  # 吸菸 / 情緒 / 壓力 / 自訂
    description: Optional[str] = None
    note: Optional[str] = None


class Insight(BaseModel):
    """AI 洞察"""
    id: str = Field(default_factory=generate_id)
    datetime: str
    date: str
    type: str  # realtime / weekly / morning_ritual / night_ritual / ai_conversation
    trigger_summary: Optional[str] = None
    context_summary: Optional[str] = None
    ai_response: str
    model: str
    note: Optional[str] = None


class Goal(BaseModel):
    """健康目標"""
    id: str = Field(default_factory=generate_id)
    metric: str
    current_value: float
    target_value: float
    unit: str
    target_date: str
    status: str = "active"  # active / achieved / paused
    created_at: str
    updated_at: str
    note: Optional[str] = None


class AnalyticsEvent(BaseModel):
    """使用追蹤事件"""
    timestamp: str
    event: str  # input_save / ai_consult / ai_weekly_review
    input_type: Optional[str] = None
    input_method: Optional[str] = None  # photo / text / photo_and_text / manual
    with_feedback: Optional[bool] = None
    is_ritual: Optional[bool] = None
    ritual_type: Optional[str] = None  # morning / night
    saved: Optional[bool] = None
    turns: Optional[int] = None
