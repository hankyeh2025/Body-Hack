# Google Sheets API 技術限制

## 基本資訊

| 項目 | 內容 |
|------|------|
| 官方文件 | https://developers.google.com/sheets/api/limits |
| 最後更新 | 2025-01 |
| 適用版本 | gspread >= 6.0.0 |

---

## 免費層限制

| 項目 | 限制值 | 違反後果 |
|------|--------|----------|
| 每專案讀取 | 300 次/分鐘 | 429 錯誤 |
| 每專案寫入 | 300 次/分鐘 | 429 錯誤 |
| 每用戶讀寫 | 60 次/分鐘 | 429 錯誤 |
| 單一儲存格 | 50,000 字元 | 寫入失敗 |
| 每試算表儲存格 | 1,000 萬個 | 無法新增 |
| 每試算表工作表 | 200 個 | 無法新增 |

---

## 觸發詞對照表

| 使用者說 | 判定 | 說明 | 變通方向 |
|----------|------|------|----------|
| 儲存長文、完整回覆、詳細內容 | ⚠️ 有限制 | 單一儲存格上限 50,000 字元 | 超過 45,000 字需分片儲存 |
| 大量寫入、批次更新、迴圈寫入 | ⚠️ 有限制 | 每分鐘 60 次/用戶，300 次/專案 | 必須使用批次操作 |
| 頻繁讀取、即時查詢、輪詢 | ⚠️ 有限制 | 每分鐘 60 次/用戶 | 使用快取機制 |
| 多人同時、共用編輯、協作 | ⚠️ 有風險 | 無鎖機制，最後寫入覆蓋 | 需告知使用者此限制 |
| 交易、原子性、全部成功或失敗 | ❌ 不可行 | 無交易機制 | 設計容錯邏輯 |
| 歷史紀錄、所有資料、全部載入 | ⚠️ 有風險 | 讀取大表很慢 | 限制查詢範圍 |
| 搜尋、篩選、查詢 | ⚠️ 有限制 | 無原生查詢語言 | 讀取後在 Python 處理 |
| 關聯、JOIN、外鍵 | ❌ 不可行 | 非關聯式資料庫 | 手動處理關聯 |

---

## 設計模式

### ✅ 推薦模式

| 情境 | 做法 | 原因 |
|------|------|------|
| 多行寫入 | 使用 `worksheet.append_rows()` | 批次操作，省配額 |
| 多行更新 | 使用 `worksheet.update()` 一次更新範圍 | 批次操作 |
| 頻繁讀取 | 讀取一次存入變數 | 避免重複呼叫 API |
| 長文本儲存 | 超過 45,000 字分片 | 預留緩衝避免失敗 |
| 錯誤處理 | 使用 tenacity 重試 | 處理暫時性錯誤 |
| 速率限制 | 使用 BackOffHTTPClient | gspread 內建支援 |

### ❌ 禁止模式

| 模式 | 問題 | 正確做法 |
|------|------|----------|
| `for row: worksheet.append_row(row)` | 迴圈逐行寫入，API 爆量 | 用 `append_rows([rows])` 批次 |
| `worksheet.get_all_records()` 在迴圈 | 重複讀取，浪費配額 | 讀一次存變數 |
| 單格存完整 LLM 回應 | 可能超過 50k 字元 | 分片儲存或截斷 |
| 併發寫入同一範圍 | 最後寫入覆蓋，資料遺失 | 設計避免併發 |
| 沒有錯誤處理 | 429 錯誤導致崩潰 | 用 tenacity 重試 |

---

## 程式碼檢查點

| 檢查項目 | 錯誤模式 | 正確模式 |
|----------|----------|----------|
| 多行寫入 | `for row: ws.append_row(row)` | `ws.append_rows(rows)` |
| 重複讀取 | `for i: ws.get_all_records()` | `data = ws.get_all_records()` 一次 |
| 長文本 | 直接寫入不檢查長度 | 檢查 `len(text) < 45000` |
| 錯誤處理 | 沒有 try-except | 用 tenacity `@retry` 裝飾器 |
| 憑證檔案 | 放在 repo 中 | 加入 `.gitignore` |

---

## 資源估算公式

```
每日寫入次數 = (事件數 × 寫入欄位) ÷ 批次大小
每日讀取次數 = 啟動次數 + (事件數 × 讀取頻率)

安全閾值：每日 < 5,000 次（遠低於上限，預留緩衝）
```

### 範例估算

```
假設：
- 每日 100 次事件
- 每次事件寫入 5 個欄位
- 批次大小 10
- 每日啟動 20 次

每日寫入 = (100 × 5) ÷ 10 = 50 次
每日讀取 = 20 + (100 × 1) = 120 次
總計 = 170 次 ✅ 安全
```

### 安全閾值

| 資源 | 建議上限 | 說明 |
|------|----------|------|
| 每日讀寫 | < 5,000 次 | 遠低於限制，預留緩衝 |
| 單格文字 | < 45,000 字 | 預留 5,000 字緩衝 |
| 單次讀取行數 | < 10,000 行 | 效能考量 |

---

## 分片儲存策略

當文本可能超過 45,000 字元時：

### 寫入時

```python
def write_long_text(worksheet, row, col, text, chunk_size=40000):
    """分片寫入長文本"""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    for i, chunk in enumerate(chunks):
        worksheet.update_cell(row, col + i, chunk)
    # 記錄分片數量
    return len(chunks)
```

### 讀取時

```python
def read_long_text(worksheet, row, start_col, num_chunks):
    """讀取分片的長文本"""
    chunks = []
    for i in range(num_chunks):
        chunk = worksheet.cell(row, start_col + i).value
        if chunk:
            chunks.append(chunk)
    return ''.join(chunks)
```

---

## 速率限制處理

### 使用 gspread 內建的 BackOff

```python
from gspread import BackOffHTTPClient
import gspread

# 使用 BackOffHTTPClient 自動處理 429
gc = gspread.authorize(credentials, http_client=BackOffHTTPClient)
```

### 使用 tenacity 重試

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60)
)
def safe_sheets_operation():
    # 你的 Sheets 操作
    pass
```

---

## 常見問題

### Q: 429 錯誤一直出現怎麼辦？

**A:**
1. 確認使用批次操作
2. 加入 BackOffHTTPClient
3. 檢查是否有迴圈中的重複讀寫
4. 考慮加入快取機制

### Q: 多人同時使用會有問題嗎？

**A:** Google Sheets 沒有鎖機制，最後寫入會覆蓋。如果有多人同時編輯需求，要在設計上避免寫入同一範圍，或改用有鎖機制的資料庫。

### Q: 可以用 Sheets 當正式資料庫嗎？

**A:** 對於輕量應用（個人使用、小團隊）可以。但如果需要：交易機制、併發控制、複雜查詢，建議改用真正的資料庫（Firebase、Supabase）。

---

## 必要套件版本

```
gspread>=6.0.0
google-auth>=2.0.0
google-api-python-client>=2.0.0
tenacity>=8.0.0
```

---

*最後更新：2025-01*
