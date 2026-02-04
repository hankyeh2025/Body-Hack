# language: zh-TW
Feature: 時間軸主畫面
  作為 使用者
  我想要 在時間軸上查看今日記錄
  以便 快速掌握健康脈絡

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線

  Scenario: 顯示主畫面
    Given 使用者開啟 App
    Then 顯示頂部日期和儀表板
    And 顯示「＋輸入」「🤖AI」按鈕
    And 顯示今日時間軸氣泡流

  Scenario: 儀表板顯示今日進度
    Given 使用者今日已記錄飲水 2000ml、2 餐、3 根菸
    Then 儀表板顯示「💧2000ml 🍽2餐 🚬3根」

  Scenario: 時間軸排序
    Given 今日有多筆記錄
    Then 時間軸最新記錄在上
    And 往下滾可回溯較早的記錄

  Scenario: 切換日期
    Given 使用者在主畫面
    When 使用者點擊日期
    Then 顯示日曆選擇器
    When 使用者選擇其他日期
    Then 時間軸顯示該日記錄
    And 儀表板顯示該日進度

  Scenario: 展開 AI 對話氣泡
    Given 時間軸有一個收合的 AI 對話氣泡
    When 使用者點擊「展開」
    Then 顯示完整對話內容
    When 使用者點擊「收合」
    Then 對話收回只顯示首輪問題
