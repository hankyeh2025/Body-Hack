# Gemini API 技術限制

## 基本資訊

| 項目 | 內容 |
|------|------|
| 官方文件 | https://ai.google.dev/pricing |
| 最後更新 | 2025-01 |
| 適用版本 | google-genai >= 1.0.0 |

**重要：** 使用新版 SDK `google-genai`，不是舊版 `google-generativeai`

---

## 免費層限制

| 模型 | 免費配額 | 建議 |
|------|----------|------|
| Gemini 2.5 Flash | 500 RPD | ✅ 推薦首選 |
| Gemini 2.5 Flash-Lite | 1,000 RPD | ✅ 預算優先 |
| Gemini 2.0 Flash | 1,500 RPD | ✅ 配額較多 |
| Gemini 1.5 Flash | 1,500 RPD | ✅ 穩定版本 |
| Gemini 1.5 Pro | 50 RPD | ⚠️ 配額極低 |
| Gemini 2.5 Pro | 極低或無 | ❌ 不建議免費層 |

**RPD = Requests Per Day（每日請求數）**

---

## 觸發詞對照表

| 使用者說 | 判定 | 說明 | 變通方向 |
|----------|------|------|----------|
| 搜尋網路、即時資訊、Google Search | ❌ 不可行 | 免費層 Search Grounding 會報 429 | 禁用搜尋功能 |
| Gemini Pro、進階模型、最強模型 | ⚠️ 有風險 | Pro 免費配額極低（50 RPD） | 預設使用 Flash 系列 |
| 每日大量、頻繁呼叫、無限制 | ⚠️ 有限制 | 免費層有每日配額 | 需估算用量 |
| OCR、圖片辨識、圖轉文字 | ✅ 可行 | 支援 Vision API | 須禁用 Search Grounding |
| 長文本、完整文章、大量內容 | ⚠️ 有限制 | Token 限制 | 分段處理或摘要 |
| 即時對話、串流輸出 | ✅ 可行 | 支援 streaming | 搭配 st.write_stream |
| 多輪對話、記住上下文 | ⚠️ 有限制 | 需自行管理對話歷史 | 設計 context window 策略 |

---

## 設計模式

### ✅ 推薦模式

| 情境 | 做法 | 原因 |
|------|------|------|
| 模型選擇 | 使用參數化配置 | 方便切換模型 |
| API 金鑰 | 用環境變數或 st.secrets | 不寫在程式碼中 |
| 錯誤處理 | 使用 tenacity 重試 | 處理暫時性錯誤 |
| 串流輸出 | 使用 generate_content_stream | 更好的使用者體驗 |
| Token 管理 | 設計截斷或摘要策略 | 避免超過限制 |

### ❌ 禁止模式

| 模式 | 問題 | 正確做法 |
|------|------|----------|
| `tools=[google_search]` | 免費層會報 429 | 不傳 tools 或設空 |
| `from google.generativeai` | 舊版 SDK | 用 `from google import genai` |
| 硬編碼模型名稱 | 難以切換 | 用參數或設定檔 |
| 沒有錯誤處理 | API 錯誤導致崩潰 | 用 tenacity 重試 |
| 預設使用 Pro 模型 | 配額極低 | 預設用 Flash |

---

## 程式碼檢查點

| 檢查項目 | 錯誤模式 | 正確模式 |
|----------|----------|----------|
| SDK 匯入 | `from google.generativeai import` | `from google import genai` |
| Search Grounding | `tools=[google_search]` | `tools=[]` 或不傳 |
| 模型名稱 | `model="gemini-pro"` 硬編碼 | `model=config.MODEL_NAME` |
| API 金鑰 | `api_key="xxx"` | `api_key=st.secrets["GEMINI_API_KEY"]` |
| 錯誤處理 | 無 try-except | 用 tenacity `@retry` |

---

## 正確的 SDK 使用方式

### 初始化

```python
from google import genai

# 使用環境變數或 st.secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
```

### 基本生成

```python
response = client.models.generate_content(
    model="gemini-2.0-flash",  # 使用參數化
    contents="你的 prompt"
)
print(response.text)
```

### 串流生成

```python
response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents="你的 prompt"
)

for chunk in response:
    print(chunk.text, end="")
```

### 搭配 Streamlit 串流

```python
def generate_stream():
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=prompt
    )
    for chunk in response:
        yield chunk.text

st.write_stream(generate_stream())
```

### 圖片理解（Vision）

```python
import PIL.Image

image = PIL.Image.open("image.jpg")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "請描述這張圖片",
        image
    ]
)
```

---

## 資源估算公式

```
圖片 OCR：每張約 500 input + 200 output = 700 tokens
對話處理：每輪約 800 tokens（含上下文）
日總結生成：約 1,500 tokens

每日 Token 總量 = (圖片數 × 700) + (對話輪數 × 800) + 1,500
```

### 範例估算

```
假設：
- 每日 10 張圖片 OCR
- 每日 50 輪對話
- 1 次日總結

Token 用量 = (10 × 700) + (50 × 800) + 1,500 = 48,500 tokens
API 呼叫次數 = 10 + 50 + 1 = 61 次

Flash 配額 500 RPD → ✅ 足夠
```

### 安全閾值

| 資源 | 建議上限 | 說明 |
|------|----------|------|
| 每日 API 呼叫 | < 配額 80% | 預留緩衝 |
| 單次 Token | < 30,000 | 避免超過 context window |
| 對話歷史 | 保留 10-20 輪 | 平衡上下文與成本 |

---

## 模型選擇策略

### 決策樹

```
需要最高品質？
├─ 是 → 有付費預算嗎？
│       ├─ 是 → Gemini Pro
│       └─ 否 → Gemini 2.5 Flash（免費最強）
└─ 否 → 需要大量呼叫？
        ├─ 是 → Gemini 2.0 Flash（配額較多）
        └─ 否 → Gemini 2.5 Flash-Lite（省資源）
```

### 模型對照表

| 需求 | 推薦模型 | 原因 |
|------|----------|------|
| 一般對話 | gemini-2.0-flash | 平衡品質與配額 |
| 複雜推理 | gemini-2.5-flash | 免費層最強 |
| 大量處理 | gemini-2.0-flash | 配額最多 |
| 圖片理解 | gemini-2.0-flash | Vision 支援良好 |
| 程式碼生成 | gemini-2.5-flash | 推理能力較強 |

---

## 常見問題

### Q: 一直出現 429 錯誤怎麼辦？

**A:**
1. 確認沒有啟用 Search Grounding（`tools` 參數要空或不傳）
2. 檢查是否超過每日配額
3. 加入重試機制處理暫時性限制

### Q: 要用哪個 SDK？

**A:** 使用新版 `google-genai`，不是舊版 `google-generativeai`。安裝：`pip install google-genai`

### Q: 免費版夠用嗎？

**A:** 個人使用或小型應用通常夠。如果每日呼叫超過 500 次，需要考慮付費或優化呼叫頻率。

### Q: 怎麼處理長文本？

**A:**
1. 分段處理，每段獨立呼叫
2. 先摘要再處理
3. 使用 context window 較大的模型

---

## 必要套件版本

```
google-genai>=1.0.0
Pillow>=10.0.0        # 圖片處理
tenacity>=8.0.0       # 重試機制
```

---

*最後更新：2025-01*
