# language: zh-TW
Feature: 資料匯出
  作為 使用者
  我想要 匯出我的數據
  以便 進行深度分析或備份

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線

  Scenario: 匯出 CSV 檔案
    Given 使用者進入匯出功能
    When 使用者選擇要匯出的 Sheet 和時間範圍
    Then 系統產生 CSV 檔案供下載

  Scenario: 產生 Skill 啟動 Prompt
    Given 使用者要進行週期檢視分析
    When 使用者選擇匯出資料並產生 Prompt
    Then 系統匯出 CSV
    And 自動產生對應的 Skill 啟動 Prompt
    And 使用者可複製 Prompt 到新對話使用
