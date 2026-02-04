"""
AI 類型辨識
使用 Gemini API 分析使用者輸入，判斷記錄類型並萃取關鍵資訊
"""
import json
import re
from typing import Dict, Any

from core import get_gemini_client


RECOGNITION_PROMPT = """你是健康記錄助手。請分析以下輸入，判斷記錄類型並萃取關鍵資訊。

輸入：{user_input}

請以 JSON 格式回傳：
{{
  "type": "meal" | "water" | "exercise" | "simple_event" | "unknown",
  "confidence": 0.0-1.0,
  "data": {{
    // 依類型不同
    // meal: {{ "meal_type": "早餐/午餐/晚餐/點心/宵夜/其他", "content": "餐點描述", "starch_level": "無/少/中/多", "estimated_nutrition": "熱量、蛋白質等推估" }}
    // water: {{ "volume_ml": 數字 }}
    // exercise: {{ "content": "運動描述", "duration_min": 數字, "intensity": "低/中/高" }}
    // simple_event: {{ "category": "類別", "description": "描述" }}
  }}
}}

注意：
1. 只回傳 JSON，不要其他文字
2. meal_type 請根據時間和內容判斷，如果無法判斷就用「其他」
3. starch_level 請根據描述判斷澱粉量
4. estimated_nutrition 請給出合理推估，格式為文字描述
5. 如果無法判斷類型，type 設為 "unknown"
"""


def recognize_input(user_input: str) -> Dict[str, Any]:
    """
    使用 Gemini AI 辨識使用者輸入的類型

    Args:
        user_input: 使用者輸入的文字

    Returns:
        辨識結果 dict，包含 type, confidence, data
    """
    try:
        client = get_gemini_client()
        prompt = RECOGNITION_PROMPT.format(user_input=user_input)
        response = client.generate(prompt)
        result = _parse_json_response(response)

        if "type" not in result:
            result["type"] = "unknown"
        if "confidence" not in result:
            result["confidence"] = 0.0
        if "data" not in result:
            result["data"] = {}

        return result

    except json.JSONDecodeError:
        return {
            "type": "unknown",
            "confidence": 0.0,
            "data": {}
        }
    except Exception as e:
        return {
            "type": "error",
            "message": str(e),
            "confidence": 0.0,
            "data": {}
        }


def _parse_json_response(response: str) -> Dict[str, Any]:
    """
    解析 Gemini 回傳的 JSON 回應
    處理可能包含 markdown code block 的情況
    """
    cleaned = response.strip()
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()

    return json.loads(cleaned)
