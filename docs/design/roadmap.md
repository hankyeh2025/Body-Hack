# 開發路線圖 - Body Hack

> 最後更新：2025-02-04 by Bob

---

## Phase 總覽

| Phase | 目標 | 狀態 |
|-------|------|------|
| 0 | 驗證部署骨架 | ⏳ 進行中 |
| 1 | 核心連線 | 待開始 |
| 2 | 最小可用輸入 | 待開始 |
| 3 | 看得到成果 | 待開始 |
| 4 | 即時回饋 | 待開始 |
| 5 | 完整輸入 | 待開始 |
| 6 | 儀式模式 | 待開始 |
| 7 | AI 進階 | 待開始 |
| 8 | 輔助功能 | 待開始 |

---

## Phase 0：驗證部署骨架

**目標**：確認模組化專案結構能在 Streamlit Cloud 正常運作

**包含模組**：
- 專案檔案結構（src/app.py + core/ + features/ + utils/）
- Streamlit Cloud 部署設定

**驗收標準**：
- [ ] 本地 `streamlit run src/app.py` 能執行
- [ ] 部署到 Streamlit Cloud 成功
- [ ] app.py 能 import core 和 features 模組
- [ ] 畫面顯示 Hello World + 模組載入確認訊息

**對應場景**：無（基礎設施驗證）

---

## Phase 1：核心連線

**目標**：建立與外部服務的連線能力

**包含模組**：
- core/sheets_client.py（Google Sheets 連線）
- core/gemini_client.py（Gemini API 連線）
- core/data_models.py（Pydantic 資料模型）
- Streamlit Secrets 設定

**驗收標準**：
- [ ] 能讀取 Google Sheet 資料
- [ ] 能寫入 Google Sheet 資料
- [ ] 能呼叫 Gemini API 取得回應
- [ ] 錯誤處理機制正常（連線失敗有提示）

**對應場景**：specs/physio_data.feature（部分）

---

## Phase 2：最小可用輸入

**目標**：跑通第一條完整輸入路徑

**包含模組**：
- features/input/（統一輸入 Dialog）
- AI 類型辨識邏輯
- 飲食記錄寫入 Structured_Events

**驗收標準**：
- [ ] 點「＋輸入」開啟 Dialog
- [ ] 輸入文字描述，AI 辨識為飲食
- [ ] 顯示預覽，可修改
- [ ] 儲存後寫入 Structured_Events Sheet

**對應場景**：specs/input.feature（基本輸入流程）

---

## Phase 3：看得到成果

**目標**：讓使用者看到記錄的成果

**包含模組**：
- features/timeline/（時間軸顯示）
- 儀表板元件
- 日期切換功能

**驗收標準**：
- [ ] 主畫面顯示時間軸氣泡流
- [ ] 儀表板顯示今日飲水/餐數/吸菸統計
- [ ] 點日期可切換查看其他日期
- [ ] 最新記錄在上，往下滾回溯

**對應場景**：specs/timeline.feature

---

## Phase 4：即時回饋

**目標**：記錄後能取得 AI 回饋

**包含模組**：
- features/insights/（AI 回饋邏輯）
- 「儲存+回饋」流程
- 回饋氣泡顯示

**驗收標準**：
- [ ] 點「💬回饋」後 AI 產生即時回饋
- [ ] 回饋寫入 Insights Sheet
- [ ] 時間軸顯示回饋氣泡（不同樣式）

**對應場景**：specs/ai_insights.feature（即時回饋部分）

---

## Phase 5：完整輸入

**目標**：支援所有輸入類型

**包含模組**：
- 飲水記錄
- 運動 OCR（跑步、跑步機、健行、步行、騎乘）
- 生理數據 OCR（血糖、血壓、體重體脂、睡眠、HRV）
- 步數/樓層數
- 簡易事件（吸菸、壓力、情緒）

**驗收標準**：
- [ ] 所有輸入類型都能被 AI 正確辨識
- [ ] OCR 截圖能正確解析
- [ ] 資料寫入對應 Sheet

**對應場景**：specs/input.feature、specs/physio_data.feature、specs/event_logging.feature

---

## Phase 6：儀式模式

**目標**：晨間/睡前儀式完整流程

**包含模組**：
- 晨間儀式（體重、血壓、睡眠 → 7天趨勢回饋）
- 睡前儀式（血壓、步數、樓層 → 今日總結回饋）
- 儀式回饋自動保存

**驗收標準**：
- [ ] 點「🌅晨間儀式」進入儀式模式
- [ ] 批次上傳後自動產生回饋
- [ ] 回饋自動保存至 Insights Sheet
- [ ] 睡前儀式同上

**對應場景**：specs/input.feature（儀式模式部分）

---

## Phase 7：AI 進階

**目標**：諮詢對話和週報告

**包含模組**：
- AI 諮詢（多輪對話 Dialog）
- 近 7 天報告
- 對話/報告保存機制

**驗收標準**：
- [ ] 諮詢 Dialog 可多輪對話
- [ ] 對話可選擇保存
- [ ] 近 7 天報告正確生成
- [ ] 報告可選擇保存

**對應場景**：specs/ai_consult.feature、specs/ai_review.feature

---

## Phase 8：輔助功能

**目標**：功能完整

**包含模組**：
- features/goals/（目標管理）
- features/export/（匯出 CSV + Skill Prompt）
- API 設定頁

**驗收標準**：
- [ ] 能新增/編輯/檢視目標
- [ ] 能匯出 CSV 檔案
- [ ] 能產生 Skill 啟動 Prompt
- [ ] 能切換 Gemini 模型

**對應場景**：specs/goals.feature、specs/data_export.feature

---

## 未來版本

### v0.2 - 擴充運動類型
- [ ] 重量訓練記錄
- [ ] 高強度有氧（HIIT）記錄

### v0.3 - 營養資料庫
- [ ] 串接食藥署營養資料庫
- [ ] 營養標籤 OCR

### v0.4 - 進階分析
- [ ] 血糖與飲食關聯分析
- [ ] 長週期趨勢報告

### 未來考慮
- [ ] Garmin API 串接
- [ ] 原生 App
