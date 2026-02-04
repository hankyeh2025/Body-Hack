# language: zh-TW
Feature: AI 諮詢
  作為 使用者
  我想要 與 AI 進行多輪對話
  以便 基於我的健康脈絡獲得個人化建議

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線
    And Gemini API 已設定

  Scenario: 開啟諮詢 Dialog
    Given 使用者在主畫面
    When 使用者點擊「🤖AI」
    And 選擇「💬諮詢」
    Then 開啟 AI 諮詢 Dialog
    And 顯示今日脈絡摘要（可收合）
    And 顯示輸入框
    And 記錄 Analytics 事件 ai_consult

  Scenario: 進行多輪對話
    Given 使用者在諮詢 Dialog
    When 使用者輸入問題「我今天蛋白質夠嗎？」
    And 點擊「送出」
    Then AI 基於今日脈絡回答
    When 使用者輸入追問「那我晚餐要補充什麼？」
    And 點擊「送出」
    Then AI 繼續回答

  Scenario: 結束對話不保存
    Given 使用者已進行多輪對話
    When 使用者點擊「結束對話」
    Then 顯示「要保存這段對話嗎？」
    When 使用者選擇「不保存」
    Then Dialog 關閉
    And 對話不寫入 Sheet

  Scenario: 結束對話並保存
    Given 使用者已進行多輪對話
    When 使用者點擊「📝保存對話」
    Then 對話摘要寫入 Insights Sheet
    And Dialog 關閉
    And 時間軸顯示對話氣泡（可展開）
