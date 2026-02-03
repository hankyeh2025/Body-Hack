# Tech Constraints - Body Hack

> 技術限制與約束，系統設計須在這些邊界內進行

---

## 1. Google Sheets API

### 1.1 配額限制

| 項目 | 限制 | 影響 |
|------|------|------|
| 每分鐘讀取請求 | 60 次/user/分鐘 | 頻繁刷新需做 debounce |
| 每分鐘寫入請求 | 60 次/user/分鐘 | 批次寫入優於逐筆寫入 |
| 單次讀取 cell 數 | 10,000,000 cells | 足夠使用 |
| 單一 Sheet 最大列數 | 10,000,000 列 | 足夠使用 |
| 單一 Sheet 最大欄數 | 18,278 欄 (ZZZ) | 足夠使用 |

### 1.2 認證方式

| 方式 | 適用情境 | 本專案選擇 |
|------|----------|------------|
| OAuth 2.0 | 多使用者、存取使用者自己的 Sheet | ✗ 複雜度高 |
| Service Account | 單一使用者、存取固定 Sheet | ✓ 採用 |

**Service Account 設定要點**：
- 在 Google Cloud Console 建立 Service Account
- 下載 JSON 金鑰檔
- 將 Sheet 共享給 Service Account 的 email
- 金鑰檔透過 Streamlit Secrets 管理，不進 repo

### 1.3 資料格式注意

| 議題 | 說明 | 處理方式 |
|------|------|----------|
| 時間格式 | Sheets 內部用序列值存時間 | 統一用 ISO 8601 字串存（`2025-01-15T14:30:00`） |
| 時區 | Sheets 無時區概念 | App 端統一轉 Asia/Taipei 再存 |
| 空值 | 空 cell 讀出為空字串 | 程式端判斷空字串視為 None |
| 數值精度 | 浮點數有精度限制 | 體重/體脂存到小數第一位即可 |

### 1.4 Python 套件

```
gspread>=5.10.0
google-auth>=2.22.0
google-auth-oauthlib>=1.0.0
```

---

## 2. Gemini API

### 2.1 模型選擇

| 模型 | 特性 | 建議用途 |
|------|------|----------|
| gemini-1.5-flash | 快速、便宜、支援圖片 | ✓ OCR、即時回饋 |
| gemini-1.5-pro | 更強推理、較慢 | 週回顧（需較深分析時） |

**建議策略**：預設用 flash，週回顧可選用 pro

### 2.2 OCR 限制

| 項目 | 限制 | 影響 |
|------|------|------|
| 圖片大小 | 最大 20MB | 手機截圖通常 < 5MB，OK |
| 圖片格式 | PNG, JPEG, WEBP, GIF | 常見格式皆支援 |
| 圖片解析度 | 無硬性限制，但過小影響準確度 | 建議 > 500px 寬 |

### 2.3 Token 限制

| 模型 | Context Window | Output Limit |
|------|----------------|--------------|
| gemini-1.5-flash | 1,048,576 tokens | 8,192 tokens |
| gemini-1.5-pro | 2,097,152 tokens | 8,192 tokens |

**影響**：
- 週回顧塞入 7 天資料綽綽有餘
- 即時回饋更不是問題

### 2.4 API 配額（免費層）

| 項目 | 限制 |
|------|------|
| RPM (Requests Per Minute) | 15 |
| TPM (Tokens Per Minute) | 1,000,000 |
| RPD (Requests Per Day) | 1,500 |

**影響**：個人使用足夠，但需注意：
- 連續快速操作可能觸發 RPM 限制
- 加入 retry with backoff 機制

### 2.5 Python 套件

```
google-generativeai>=0.3.0
```

### 2.6 OCR Prompt 設計原則

針對不同資料來源，需設計專屬 prompt：

| 來源 | Prompt 重點 |
|------|-------------|
| 亞培 CGM (LibreLink) | 擷取當前血糖值、趨勢箭頭方向 |
| Garmin Connect | 指定要擷取的指標（心率/HRV/睡眠分數/步數） |
| 血壓計照片 | 擷取收縮壓、舒張壓、脈搏 |
| 體脂計照片 | 擷取體重、體脂率、（如有）內臟脂肪 |

**Prompt 結構建議**：

```
你是一個健康數據 OCR 助手。
請從這張 {來源類型} 的截圖中擷取以下數值：
{欄位清單}
輸出格式（JSON）：
{輸出範例}
如果某欄位無法辨識，填入 null。
```

---

## 3. Streamlit Community Cloud

### 3.1 資源限制

| 項目 | 限制 | 影響 |
|------|------|------|
| 記憶體 | 1GB | 足夠，但避免載入大檔案到記憶體 |
| CPU | 共享資源 | 複雜運算可能較慢 |
| App 休眠 | 閒置後自動休眠 | 首次載入需等待喚醒（約 30 秒） |
| 私有 App | 需登入 GitHub 帳號 | 可設為私有，僅自己可存取 |

### 3.2 Secrets 管理

Streamlit Secrets 用於存放敏感資訊：

```toml
# .streamlit/secrets.toml（本地開發用，不進 repo）

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "...@...iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
# ... 其他欄位

[gemini]
api_key = "your-gemini-api-key"

[sheets]
spreadsheet_id = "your-spreadsheet-id"
```

**部署時**：在 Streamlit Cloud 後台的 Secrets 頁面貼上相同內容

### 3.3 檔案系統

| 項目 | 說明 |
|------|------|
| 可寫入路徑 | `/tmp/` |
| 持久化 | ❌ 重啟後清空 |
| 上傳檔案 | 暫存於記憶體或 `/tmp/` |

**影響**：
- 使用者上傳的截圖不持久化，處理完即丟棄
- 如需暫存，用 `/tmp/` 但不可依賴

### 3.4 Python 版本

Streamlit Cloud 預設使用 Python 3.11，可在 `runtime.txt` 指定：

```
python-3.11
```

---

## 4. 設計決策摘要

基於以上限制，確認以下設計決策：

| 議題 | 決策 | 原因 |
|------|------|------|
| Sheets 認證 | Service Account | 單一使用者，簡化流程 |
| 時間儲存格式 | ISO 8601 字串 | 避免 Sheets 時間格式問題 |
| 時區 | 統一 Asia/Taipei | 使用者在台灣 |
| OCR 模型 | gemini-1.5-flash 為主 | 快速、便宜、準確度足夠 |
| API 錯誤處理 | Retry with exponential backoff | 應對配額限制 |
| 敏感資訊 | Streamlit Secrets | 不進 repo |
| 上傳圖片 | 處理完即丟棄 | 不持久化，保護隱私 |

---

## 5. 待確認事項

以下事項需在開發初期驗證：

- [ ] Service Account 建立並測試連線
- [ ] Gemini API Key 取得並測試
- [ ] 各資料來源 OCR prompt 實測調整
- [ ] Streamlit Cloud 部署測試
