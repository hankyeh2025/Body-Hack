# CLAUDE.md - Body Hack

> Claude Code 專案指引文件。所有開發工作以此為準。

---

## 專案概述

建立一個低摩擦的健康數據追蹤系統，透過 Streamlit Web App 記錄生理數據與生活事件，結合 AI 提供即時回饋與週期洞察。

### 核心理念

1. **輸入即介入**：記錄本身打斷自動化行為，建立覺察
2. **結構與彈性並存**：結構化欄位保持可分析性，備註欄位容納意外觀察
3. **反饋是鷹架不是柱子**：AI 輔助建立覺察，最終目標是內化而非依賴

---

## 技術棧

| 項目 | 選擇 | 版本/備註 |
|------|------|-----------|
| 語言 | Python | 3.11+ |
| 框架 | Streamlit | 最新穩定版 |
| 部署 | Streamlit Community Cloud | - |
| 資料儲存 | Google Sheets API | gspread + oauth2client |
| OCR / AI | Gemini API | gemini-1.5-flash 或 gemini-1.5-pro |

---

## 專案結構

```
/body-hack/
├── CLAUDE.md                    # 本文件
├── requirements.txt             # Python 依賴
│
├── docs/
│   ├── status.md               # 即時狀態追蹤
│   ├── design/
│   │   ├── tech_constraints.md
│   │   ├── system_blueprint.md
│   │   ├── ui_spec.md
│   │   └── roadmap.md
│   ├── phase_reports/
│   └── escalation_reports/
│
├── specs/                       # BDD 場景
│   └── *.feature
│
├── src/
│   ├── app.py                  # 主程式入口
│   ├── config.py               # 設定管理
│   │
│   ├── core/                   # 核心邏輯層
│   │   ├── __init__.py
│   │   ├── sheets_client.py    # Google Sheets 封裝
│   │   ├── gemini_client.py    # Gemini API 封裝
│   │   └── data_models.py      # 資料結構定義
│   │
│   ├── features/               # 功能模組
│   │   ├── __init__.py
│   │   ├── physio/            # 生理數據記錄
│   │   ├── events/            # 事件記錄
│   │   ├── insights/          # AI 洞察
│   │   ├── goals/             # 目標管理
│   │   └── export/            # 匯出功能
│   │
│   └── utils/                  # 工具函式
│       ├── __init__.py
│       ├── datetime_utils.py
│       └── ui_components.py
│
├── skill/                       # 週期檢視 Skill（規格先行，開發留待後續）
│
└── tests/
    ├── unit/
    └── integration/
```

---

## 命名慣例

### 檔案命名

| 類型 | 規則 | 範例 |
|------|------|------|
| Python 模組 | snake_case | `sheets_client.py` |
| 測試檔案 | `test_` 前綴 | `test_sheets_client.py` |
| 設計文件 | snake_case | `system_blueprint.md` |
| BDD 場景 | 功能名稱 | `physio_recording.feature` |

### 程式碼命名

| 類型 | 規則 | 範例 |
|------|------|------|
| 函式 | snake_case | `get_recent_records()` |
| 類別 | PascalCase | `SheetsClient` |
| 常數 | UPPER_SNAKE | `DEFAULT_SHEET_ID` |
| 變數 | snake_case | `blood_glucose` |

---

## Commit 規範

格式：`type: 簡短描述`

| type | 用途 |
|------|------|
| feat | 新功能 |
| fix | 修復 bug |
| refactor | 重構（不改變行為） |
| docs | 文件更新 |
| test | 測試相關 |
| chore | 雜項（依賴更新、設定等） |

範例：
- `feat: 新增血糖 OCR 功能`
- `fix: 修正時區轉換錯誤`
- `docs: 更新 system_blueprint.md`

---

## 工作守則

1. **單一職責**：每個模組只做一件事
2. **先測試再實作**：依據 .feature 場景設計測試
3. **漸進式開發**：每個 Phase 產出可運作的增量
4. **錯誤處理**：API 呼叫必須有 try-catch 和 fallback
5. **機敏資料**：API keys 使用環境變數或 Streamlit secrets，不得寫死在程式碼

---

## 版本編號

格式：`v{Phase}.{Build}.{Fix}`

| 欄位 | 說明 |
|------|------|
| Phase | 大功能階段 |
| Build | 該階段的建構次數 |
| Fix | 修復次數 |

範例：`v1.2.0` = Phase 1 的第 2 次建構，無修復

---

## 參考文件

- `docs/design/tech_constraints.md` - 技術限制
- `docs/design/system_blueprint.md` - 系統藍圖
- `docs/design/ui_spec.md` - UI 規格
- `docs/design/roadmap.md` - 開發路線圖
- `docs/status.md` - 當前狀態
