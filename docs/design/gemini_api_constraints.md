# Gemini API 技術限制

## 基本資訊

| 項目 | 內容 |
|------|------|
| 官方文件 | https://ai.google.dev/pricing |
| 最後更新 | 2025-02 |
| 適用版本 | google-genai >= 1.0.0 |

**重要：** 使用新版 SDK `google-genai`，不是舊版 `google-generativeai`

---

## ⚠️ 淘汰警告

| 系列 | 狀態 | 說明 |
|------|------|------|
| Gemini 1.5 | ❌ 已淘汰 | 不再支援，請勿使用 |
| Gemini 2.0 | ⚠️ 即將淘汰 | 2026 年 3 月 31 日停用 |
| Gemini 2.5 / 3 | ✅ 建議使用 | 目前支援的版本 |

**開發時請只使用 Gemini 2.5 或 Gemini 3 系列。**

---

## 模型總覽

### Gemini 3 系列（Preview）

| 模型代碼 | 輸入類型 | 輸出類型 | 輸入 Token | 輸出 Token | 更新日期 |
|----------|----------|----------|------------|------------|----------|
| `gemini-3-pro-preview` | 文字、圖片、影片、音訊、PDF | 文字 | 1,048,576 | 65,536 | 2025-11 |
| `gemini-3-pro-image-preview` | 圖片、文字 | 圖片、文字 | 65,536 | 32,768 | 2025-11 |
| `gemini-3-flash-preview` | 文字、圖片、影片、音訊、PDF | 文字 | 1,048,576 | 65,536 | 2025-12 |

### Gemini 2.5 Pro 系列

| 模型代碼 | 輸入類型 | 輸出類型 | 輸入 Token | 輸出 Token | 更新日期 |
|----------|----------|----------|------------|------------|----------|
| `gemini-2.5-pro`（穩定） | 音訊、圖片、影片、文字、PDF | 文字 | 1,048,576 | 65,536 | 2025-06 |
| `gemini-2.5-pro-preview-tts` | 文字 | 音訊 | 8,192 | 16,384 | 2025-12 |

### Gemini 2.5 Flash 系列

| 模型代碼 | 輸入類型 | 輸出類型 | 輸入 Token | 輸出 Token | 更新日期 |
|----------|----------|----------|------------|------------|----------|
| `gemini-2.5-flash`（穩定） | 文字、圖片、影片、音訊 | 文字 | 1,048,576 | 65,536 | 2025-06 |
| `gemini-2.5-flash-preview-09-2025` | 文字、圖片、影片、音訊 | 文字 | 1,048,576 | 65,536 | 2025-09 |
| `gemini-2.5-flash-image` | 圖片、文字 | 圖片、文字 | 65,536 | 32,768 | 2025-10 |
| `gemini-2.5-flash-native-audio-preview-12-2025` | 音訊、影片、文字 | 音訊、文字 | 131,072 | 8,192 | 2025-09 |
| `gemini-2.5-flash-preview-tts` | 文字 | 音訊 | 8,192 | 16,384 | 2025-12 |

### Gemini 2.5 Flash-Lite 系列

| 模型代碼 | 輸入類型 | 輸出類型 | 輸入 Token | 輸出 Token | 更新日期 |
|----------|----------|----------|------------|------------|----------|
| `gemini-2.5-flash-lite`（穩定） | 文字、圖片、影片、音訊、PDF | 文字 | 1,048,576 | 65,536 | 2025-07 |
| `gemini-2.5-flash-lite-preview-09-2025` | 文字、圖片、影片、音訊、PDF | 文字 | 1,048,576 | 65,536 | 2025-09 |

---

## 功能支援對照表

| 模型 | 語音生成 | 批次 | 快取 | 程式碼執行 | 檔案搜尋 | 函式呼叫 | Google 地圖 | 圖像生成 | Live API | Google 搜尋 | 結構化輸出 | 思考 | 網址內容 |
|------|:--------:|:----:|:----:|:----------:|:--------:|:--------:|:-----------:|:--------:|:--------:|:-----------:|:----------:|:----:|:--------:|
| gemini-3-pro-preview | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-3-pro-image-preview | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| gemini-3-flash-preview | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-2.5-pro | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-2.5-pro-preview-tts | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| gemini-2.5-flash | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-2.5-flash-preview-09-2025 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-2.5-flash-image | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| gemini-2.5-flash-native-audio | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ |
| gemini-2.5-flash-preview-tts | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| gemini-2.5-flash-lite | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| gemini-2.5-flash-lite-preview-09-2025 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## 用途別模型推薦

| 用途 | 推薦模型 | 原因 |
|------|----------|------|
| **OCR / 圖片理解** | `gemini-2.5-flash` | 穩定版，支援圖片輸入，配額友善 |
| **一般對話** | `gemini-2.5-flash` | 平衡品質與成本 |
| **複雜推理** | `gemini-2.5-pro` | 最強推理能力 |
| **大量處理** | `gemini-2.5-flash-lite` | 配額最多，成本最低 |
| **圖像生成** | `gemini-2.5-flash-image` | 支援圖片輸出 |
| **語音生成 (TTS)** | `gemini-2.5-flash-preview-tts` | 文字轉語音 |
| **即時語音對話** | `gemini-2.5-flash-native-audio` | 支援 Live API |
| **嘗鮮最新功能** | `gemini-3-flash-preview` | Gemini 3 預覽版 |

---

## 觸發詞對照表

| 使用者說 | 判定 | 說明 | 變通方向 |
|----------|------|------|----------|
| 搜尋網路、即時資訊、Google Search | ⚠️ 需確認 | 免費層可能有限制 | 測試後決定是否啟用 |
| Gemini Pro、進階模型、最強模型 | ✅ 可用 | 使用 `gemini-2.5-pro` | — |
| 每日大量、頻繁呼叫、無限制 | ⚠️ 有限制 | 免費層有每日配額 | 需估算用量 |
| OCR、圖片辨識、圖轉文字 | ✅ 可行 | 使用 `gemini-2.5-flash` | — |
| 圖像生成、產生圖片 | ✅ 可行 | 使用 `gemini-2.5-flash-image` | — |
| 語音輸出、TTS、文字轉語音 | ✅ 可行 | 使用 `*-tts` 模型 | — |
| 長文本、完整文章、大量內容 | ✅ 可行 | 支援 1M Token 輸入 | — |
| 即時對話、串流輸出 | ✅ 可行 | 支援 streaming | 搭配 st.write_stream |
| 多輪對話、記住上下文 | ⚠️ 有限制 | 需自行管理對話歷史 | 設計 context window 策略 |
| Gemini 2.0、Gemini 1.5 | ❌ 禁止 | 已淘汰或即將淘汰 | 改用 2.5 / 3 系列 |

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
| 模型版本 | 使用穩定版（無日期後綴） | 避免 preview 版變動 |

### ❌ 禁止模式

| 模式 | 問題 | 正確做法 |
|------|------|----------|
| `model="gemini-2.0-flash"` | 2026-03 淘汰 | 用 `gemini-2.5-flash` |
| `model="gemini-1.5-pro"` | 已淘汰 | 用 `gemini-2.5-pro` |
| `from google.generativeai` | 舊版 SDK | 用 `from google import genai` |
| 硬編碼模型名稱 | 難以切換 | 用參數或設定檔 |
| 沒有錯誤處理 | API 錯誤導致崩潰 | 用 tenacity 重試 |

---

## 程式碼檢查點

| 檢查項目 | 錯誤模式 | 正確模式 |
|----------|----------|----------|
| SDK 匯入 | `from google.generativeai import` | `from google import genai` |
| 模型版本 | `gemini-2.0-*` 或 `gemini-1.5-*` | `gemini-2.5-*` 或 `gemini-3-*` |
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
    model="gemini-2.5-flash",  # 使用 2.5 系列
    contents="你的 prompt"
)
print(response.text)
```

### 串流生成

```python
response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="你的 prompt"
)

for chunk in response:
    print(chunk.text, end="")
```

### 搭配 Streamlit 串流

```python
def generate_stream():
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt
    )
    for chunk in response:
        yield chunk.text

st.write_stream(generate_stream())
```

### 圖片理解（Vision / OCR）

```python
import PIL.Image

image = PIL.Image.open("image.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash",  # 支援圖片輸入
    contents=[
        "請描述這張圖片",
        image
    ]
)
```

### 圖像生成

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # 圖像生成專用
    contents="生成一張日落海灘的圖片"
)
# 處理圖片輸出...
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
```

### 安全閾值

| 資源 | 建議上限 | 說明 |
|------|----------|------|
| 每日 API 呼叫 | < 配額 80% | 預留緩衝 |
| 單次 Token | < 100,000 | 一般用途足夠 |
| 對話歷史 | 保留 10-20 輪 | 平衡上下文與成本 |

---

## 模型選擇決策樹

```
需要什麼輸出？
├─ 文字 → 需要最高品質？
│         ├─ 是 → gemini-2.5-pro
│         └─ 否 → 需要大量呼叫？
│                 ├─ 是 → gemini-2.5-flash-lite
│                 └─ 否 → gemini-2.5-flash ✅ 預設選擇
├─ 圖片 → gemini-2.5-flash-image
├─ 音訊 → 需要即時對話？
│         ├─ 是 → gemini-2.5-flash-native-audio
│         └─ 否 → gemini-2.5-flash-preview-tts
└─ 嘗鮮 → gemini-3-flash-preview
```

---

## 常見問題

### Q: 一直出現 429 錯誤怎麼辦？

**A:**
1. 檢查是否超過每日配額
2. 加入重試機制處理暫時性限制
3. 考慮使用 flash-lite 增加配額

### Q: 要用哪個 SDK？

**A:** 使用新版 `google-genai`，不是舊版 `google-generativeai`。安裝：`pip install google-genai`

### Q: 可以用 Gemini 2.0 嗎？

**A:** 不建議。Gemini 2.0 將於 2026 年 3 月 31 日停用，請直接使用 Gemini 2.5 系列。

### Q: Gemini 3 穩定嗎？

**A:** Gemini 3 目前都是 preview 版本，正式環境建議使用 Gemini 2.5 穩定版（無日期後綴的版本）。

### Q: 怎麼選擇 Flash vs Flash-Lite？

**A:**
- **Flash**：品質較好，適合一般用途
- **Flash-Lite**：配額較多，適合大量處理或成本敏感場景

---

## 必要套件版本

```
google-genai>=1.0.0
Pillow>=10.0.0        # 圖片處理
tenacity>=8.0.0       # 重試機制
```

---

*最後更新：2025-02*
