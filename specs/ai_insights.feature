# language: zh-TW
Feature: AI 洞察
  作為 使用者
  我想要 獲得 AI 對我行為與生理數據的分析
  以便 建立行為與身體感知的連結

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線
    And Gemini API 已設定

  # === 即時回饋 ===

  Scenario: 主動請求即時回饋
    Given 使用者剛記錄了一筆事件
    When 使用者按下「取得回饋」按鈕
    Then 系統讀取近期相關數據
    And 顯示 AI 即時回饋（教練語氣）

  Scenario: 純記錄不請求回饋
    Given 使用者剛記錄了一筆事件
    When 使用者不按回饋按鈕
    Then 記錄完成，無 AI 回應

  # === 週回顧 ===

  Scenario: 生成週回顧報告
    Given 本週有足夠的記錄數據
    When 使用者進入週回顧功能
    Then 系統彙整一週數據
    And 顯示 AI 週回顧分析（檢討夥伴語氣）

  # === 洞察儲存 ===

  Scenario: 儲存有價值的洞察
    Given AI 已產生洞察內容
    When 使用者標記該洞察為「保留」
    Then 洞察寫入 Insights Sheet
    And 記錄洞察類型與關聯事件
