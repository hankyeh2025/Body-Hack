# Body Hack 技術限制總覽

> 此文件為技術限制總覽，詳細規格請參閱各技術的專屬文件

---

## 技術棧

| 層級 | 技術 | 限制文件 |
|------|------|----------|
| 前端/部署 | Streamlit Community Cloud | [streamlit_constraints.md](./streamlit_constraints.md) |
| 資料儲存 | Google Sheets API | [google_sheets_constraints.md](./google_sheets_constraints.md) |
| AI 服務 | Gemini API | [gemini_api_constraints.md](./gemini_api_constraints.md) |

---

## 關鍵限制摘要

### Streamlit Community Cloud

| 限制 | 影響 | 對策 |
|------|------|------|
| 記憶體 1GB | 圖片處理需即時釋放 | 處理完立即 del |
| 無背景執行 | 不能排程 | 開啟時觸發檢查 |
| Session State 重整重置 | 狀態不持久 | 存到 Google Sheets |
| 必須公開 repo | 不能放敏感資訊 | 用 st.secrets |

### Google Sheets API

| 限制 | 影響 | 對策 |
|------|------|------|
| 60 次/分鐘/用戶 | 不能頻繁讀寫 | 批次操作 + 快取 |
| 單格 50,000 字 | AI 回應可能超限 | 截斷或分片 |
| 無交易機制 | 不能保證原子性 | 設計容錯邏輯 |

### Gemini API

| 限制 | 影響 | 對策 |
|------|------|------|
| Flash 500 RPD | 每日有限 | 估算用量，預設用 Flash |
| 免費層無 Search | 不能搜尋網路 | 不傳 tools 參數 |
| 舊 SDK 已棄用 | 匯入方式不同 | 用 `from google import genai` |

---

## 設計決策

基於以上限制，本專案採用以下設計：

1. **圖片處理策略**：上傳 → OCR → 立即釋放，不存原始檔到 session_state
2. **資料寫入策略**：使用批次操作，單次寫入多行
3. **AI 回饋策略**：使用者主動觸發，不自動呼叫
4. **狀態持久化**：重要狀態存到 Google Sheets，session_state 只做暫存
5. **模型選擇**：預設使用 gemini-2.0-flash，平衡品質與配額

---

## 必要套件

```
streamlit>=1.40.0
gspread>=6.0.0
google-auth>=2.0.0
google-genai>=1.0.0
Pillow>=10.0.0
tenacity>=8.0.0
```

---

## 詳細文件

開發時請參閱各技術的詳細限制文件：

- **Streamlit**：UI 元件能力邊界、設計模式、程式碼檢查點
- **Google Sheets**：觸發詞對照、批次操作範例、速率限制處理
- **Gemini API**：SDK 正確用法、模型選擇策略、Vision 範例

---

*最後更新：2025-02*
