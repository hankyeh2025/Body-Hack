"""
Gemini API 客戶端
封裝 Google Generative AI 操作
"""
import streamlit as st
import google.generativeai as genai
from typing import Optional, List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential


class GeminiClient:
    """Gemini API 操作封裝"""

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        初始化 Gemini 客戶端

        Args:
            model_name: 模型名稱，預設使用 gemini-2.0-flash
        """
        self.model_name = model_name
        self._model: Optional[genai.GenerativeModel] = None
        self._configure_api()

    def _configure_api(self):
        """設定 API Key"""
        api_key = st.secrets["gemini"]["api_key"]
        genai.configure(api_key=api_key)

    def _get_model(self) -> genai.GenerativeModel:
        """取得或建立模型（懶載入）"""
        if self._model is None:
            self._model = genai.GenerativeModel(self.model_name)
        return self._model

    def test_connection(self) -> Dict[str, Any]:
        """測試連線"""
        try:
            model = self._get_model()
            response = model.generate_content("請回覆：連線成功")
            return {
                "success": True,
                "model": self.model_name,
                "response": response.text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        生成文字回應

        Args:
            prompt: 使用者輸入
            system_instruction: 系統指令

        Returns:
            AI 回應文字
        """
        if system_instruction:
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_instruction
            )
        else:
            model = self._get_model()

        response = model.generate_content(prompt)
        return response.text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def generate_with_image(
        self,
        prompt: str,
        image_data: bytes,
        mime_type: str = "image/png"
    ) -> str:
        """
        圖片 + 文字生成（用於 OCR）

        Args:
            prompt: 提示文字
            image_data: 圖片二進位資料
            mime_type: 圖片 MIME 類型

        Returns:
            AI 回應文字
        """
        model = self._get_model()

        image_part = {
            "mime_type": mime_type,
            "data": image_data
        }

        response = model.generate_content([prompt, image_part])
        return response.text

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None
    ) -> str:
        """
        多輪對話

        Args:
            messages: 對話歷史 [{"role": "user/model", "parts": ["文字"]}]
            system_instruction: 系統指令

        Returns:
            AI 回應文字
        """
        if system_instruction:
            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_instruction
            )
        else:
            model = self._get_model()

        chat = model.start_chat(history=messages[:-1])
        last_message = messages[-1]["parts"][0]
        response = chat.send_message(last_message)
        return response.text


# 單例模式
@st.cache_resource
def get_gemini_client(model_name: str = "gemini-2.0-flash") -> GeminiClient:
    """取得 GeminiClient 單例"""
    return GeminiClient(model_name)
