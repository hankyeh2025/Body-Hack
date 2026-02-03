# language: zh-TW
Feature: 事件記錄
  作為 使用者
  我想要 記錄生活中的各種事件
  以便 與生理數據交叉分析，並透過記錄本身建立覺察

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線

  # === 結構化事件 ===

  Scenario: 記錄飲食事件
    Given 使用者選擇「飲食」類別
    When 使用者填入食物內容、份量、進食情境
    Then 事件寫入 Structured_Events Sheet
    And 時間戳自動記錄

  Scenario: 記錄運動事件
    Given 使用者選擇「運動」類別
    When 使用者填入運動類型、時長、強度
    Then 事件寫入 Structured_Events Sheet

  Scenario: 記錄吸菸事件
    Given 使用者選擇「吸菸」類別
    When 使用者填入數量與情境觸發因素
    Then 事件寫入 Structured_Events Sheet

  Scenario: 記錄飲酒事件
    Given 使用者選擇「飲酒」類別
    When 使用者填入酒類、份量、社交情境
    Then 事件寫入 Structured_Events Sheet

  Scenario: 記錄情緒/壓力事件
    Given 使用者選擇「情緒/壓力」類別
    When 使用者填入情緒標籤、強度、可能原因
    Then 事件寫入 Structured_Events Sheet

  # === 簡易事件 ===

  Scenario: 快速記錄簡易事件
    Given 使用者在簡易記錄模式
    When 使用者輸入自由文字描述
    Then 事件寫入 Simple_Events Sheet
    And 時間戳自動記錄

  # === 類別管理 ===

  Scenario: 使用建議的既有類別
    Given 使用者開始輸入類別
    When 系統顯示曾用過的類別建議
    Then 使用者可選擇既有類別快速填入

  Scenario: 新增自訂類別
    Given 使用者輸入一個新的類別名稱
    When 類別不存在於建議列表
    Then 系統接受新類別並記錄
    And 未來該類別出現在建議選項中
