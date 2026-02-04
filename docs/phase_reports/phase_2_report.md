# Phase 2 Report - 基本輸入流程

> 完成日期：2026-02-05
> 版本：v2.0.1

---

## 目標

跑通第一條完整輸入路徑：使用者輸入文字 → AI 辨識 → 預覽 → 儲存到 Sheet

---

## 完成項目

| 模組 | 檔案 | 說明 |
|------|------|------|
| 輸入 Dialog | features/input/input_dialog.py | Dialog 流程控制 |
| AI 辨識 | features/input/ai_recognizer.py | Gemini API 類型辨識 |
| 預覽編輯 | features/input/preview_editor.py | 預覽顯示、編輯、儲存 |
| 共用工具 | features/input/dialog_utils.py | close_dialog 共用函式 |
| UI 元件 | utils/ui_components.py | 成功/錯誤訊息元件 |

---

## BDD 場景驗收

| # | 場景 | Tag | 結果 |
|---|------|-----|------|
| 1 | 開啟輸入 Dialog | @happy-path | ✅ |
| 2 | 純文字輸入飲食記錄 | @happy-path | ✅ |
| 3 | 確認並儲存記錄 | @happy-path | ✅ |
| 4 | 修改 AI 辨識結果 | @happy-path | ✅ |
| 5 | 取消輸入 | @happy-path | ✅ |
| 6 | 空白輸入 | @error-handling | ✅ |
| 7 | AI 辨識失敗 | @error-handling | ✅ |

**測試結果**：7/7 通過

---

## 技術決策

| 決策 | 選擇 | 原因 |
|------|------|------|
| Dialog 實作 | @st.dialog 裝飾器 | Streamlit 原生支援，簡潔 |
| 狀態管理 | st.session_state | Dialog 階段切換需要跨 rerun 保持狀態 |
| AI Prompt | JSON 格式輸出 | 結構化便於解析，含 confidence 供未來使用 |
| 錯誤處理 | 手動 fallback | AI 無法辨識時讓使用者手動選擇類型 |

---

## 修復紀錄

| 版本 | 內容 |
|------|------|
| v2.0.0 | 初始開發完成 |
| v2.0.1 | 重構：抽取 close_dialog 為共用函式 |

---

## 技術債

| 項目 | 說明 | 優先級 |
|------|------|--------|
| 信心度低時提示 | AI confidence < 50% 時可加警示 | 低 |

---

## 與其他 Phase 的關係

| Phase | 關係 |
|-------|------|
| Phase 1 | 依賴：使用 sheets_client、gemini_client、data_models |
| Phase 3 | 被依賴：時間軸需要顯示本 Phase 儲存的記錄 |
| Phase 4 | 擴展：「儲存+回饋」功能基於本 Phase 的儲存邏輯 |
| Phase 5 | 擴展：其他輸入類型（飲水、運動、OCR）基於本 Phase 的 Dialog 框架 |

---

## 下一步

Phase 3：時間軸顯示
- 主畫面顯示今日記錄
- 儀表板顯示統計
- 日期切換功能
