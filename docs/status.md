# Body Hack 專案狀態

> 最後更新：2025-02-04 by May

---

## 當前階段

**Stage 2：UI 設計** ✅ 完成

**下一階段**：Stage 3 開發規劃（Bob）

---

## 完成項目

### Tim (Stage 1) ✅

- [x] CLAUDE.md
- [x] system_blueprint.md
- [x] tech_constraints.md
- [x] 高層級 .feature 檔案

### May (Stage 2) ✅

- [x] 設計理念確認（三種使用情境：輸入、諮詢、檢討）
- [x] 極簡 UX 架構設計
- [x] 畫面流程總覽（Mermaid）
- [x] 主畫面設計（時間軸 + 儀表板）
- [x] 統一輸入入口設計（AI 自動辨識類型）
- [x] 儀式模式設計（晨間/睡前）
- [x] AI 功能設計（諮詢/近7天報告）
- [x] 各輸入類型細節
  - 飲食（文字/照片/混合，AI 推估營養）
  - 飲水（飲品類型 × 容量）
  - 運動（跑步、跑步機、健行、步行、騎乘、步數、樓層數）
  - 生理數據（血糖、血壓、體重體脂、睡眠、HRV）
  - 簡易事件（吸菸、壓力、情緒，可自訂）
- [x] Analytics 追蹤設計（input_save、ai_consult、ai_weekly_review）
- [x] ui_spec.md 完成
- [x] roadmap.md 更新
- [x] BDD 場景更新（input.feature、ai_consult.feature、ai_review.feature、timeline.feature）

### Bob (Stage 3) ⏳ 待開始

- [ ] 讀取設計文件
- [ ] 拆解開發任務
- [ ] 撰寫技術規格
- [ ] 建立開發順序

### Sam (Stage 4)

- [ ] 待開始

---

## 設計決策摘要

### 核心 UX 架構

| 決策 | 內容 |
|------|------|
| 使用情境 | 輸入、諮詢、檢討（三種） |
| 主要按鈕 | [＋輸入] [🤖AI] |
| 輸入方式 | 統一入口，AI 自動辨識類型 |
| 儀式模式 | 晨間/睡前，收在輸入 Dialog 內 |
| 回饋深度 | 根據時間 + 內容智慧判斷 |

### 儀表板

| 項目 | 顯示方式 |
|------|----------|
| 💧 飲水 | 累計 ml / 目標 ml |
| 🍽 正餐 | 累計餐數 / 目標餐數 |
| 🚬 吸菸 | 累計根數（純記錄） |

### 保存邏輯

| 內容 | 保存方式 | 欄位結構 |
|------|----------|----------|
| 晨間儀式回饋 | 自動保存 | findings / suggestions / goals / summary |
| 睡前儀式回饋 | 自動保存 | findings / suggestions / goals / summary |
| 近 7 天報告 | 問使用者 | findings / suggestions / goals / summary |
| 諮詢對話 | 問使用者 | 對話摘要 |

### Analytics 追蹤

| 事件 | 追蹤目的 |
|------|----------|
| input_save | 輸入完成率 + 類型分布 |
| ai_consult | AI 諮詢使用率 |
| ai_weekly_review | 檢討功能使用率 |

### PoC 支援範圍

**運動類型**：跑步、跑步機、健行、步行、騎乘、步數、樓層數

**生理數據**：血糖（單點/整天）、血壓、體重體脂、睡眠、HRV

**未來版本**：重量訓練、高強度有氧（寫入 roadmap）

---

## 關鍵文件索引

| 文件 | 路徑 | 說明 |
|------|------|------|
| UI 規格 | docs/design/ui_spec.md | 完整 UI 設計 + Mermaid 流程圖 |
| 系統藍圖 | docs/design/system_blueprint.md | 資料結構 + Sheet 設計 |
| 技術限制 | docs/design/tech_constraints.md | Streamlit / Gemini API 限制 |
| 開發路線圖 | docs/design/roadmap.md | 版本規劃 |
| BDD 場景 | specs/*.feature | 功能驗收標準 |

---

## 交接給 Bob

### 你需要讀取的文件

1. `docs/design/system_blueprint.md` — 系統藍圖、資料結構
2. `docs/design/ui_spec.md` — UI 規格、畫面流程
3. `docs/design/tech_constraints.md` — 技術限制（Streamlit Cloud、Gemini API）
4. `specs/*.feature` — BDD 場景

### 開發重點提醒

1. **統一輸入入口**：核心功能，AI 自動辨識是關鍵
2. **儀式模式**：晨間/睡前批次上傳 + 自動產生回饋
3. **Gemini API 限制**：免費層 500 RPD，禁用 Search Grounding
4. **Analytics**：每次輸入/AI 互動都要記錄事件

### 建議開發順序
```
1. 基礎架構
   ├── Streamlit 專案初始化
   ├── Google Sheets 連線
   └── Gemini API 連線

2. 核心輸入
   ├── 統一輸入 Dialog
   ├── AI 類型辨識
   └── 記錄寫入 Sheet

3. 時間軸
   ├── 主畫面 UI
   ├── 儀表板
   └── 氣泡流顯示

4. AI 功能
   ├── 即時回饋
   ├── 諮詢對話
   └── 近 7 天報告

5. 儀式模式
   ├── 晨間儀式
   └── 睡前儀式

6. 輔助功能
   ├── 目標管理
   ├── 匯出
   └── API 設定
```

---

## 下次對話開場
```
呼叫 Bob，開始 Body Hack 專案的開發規劃

請先讀取以下文件：
- docs/design/system_blueprint.md
- docs/design/ui_spec.md
- docs/design/tech_constraints.md
- specs/*.feature

然後開始拆解開發任務
```
