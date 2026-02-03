# language: zh-TW
Feature: 目標管理
  作為 使用者
  我想要 設定與追蹤健康目標
  以便 有明確的改善方向

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線

  Scenario: 新增健康目標
    Given 使用者進入目標管理
    When 使用者設定目標類型、目標值、期限
    Then 目標寫入 Goals Sheet
    And 狀態設為 active

  Scenario: 檢視目標進度
    Given 使用者有進行中的目標
    When 使用者查看目標列表
    Then 系統顯示各目標的當前進度

  Scenario: 達成目標
    Given 使用者的某項指標達到目標值
    When 系統偵測到目標達成
    Then 目標狀態更新為 achieved
    And 可選擇設定新目標

  Scenario: 暫停目標
    Given 使用者有進行中的目標
    When 使用者選擇暫停該目標
    Then 目標狀態更新為 paused
