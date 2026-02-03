# language: zh-TW
Feature: 生理數據輸入
  作為 使用者
  我想要 記錄各種生理數據
  以便 追蹤身體狀態變化

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線

  # === OCR 輸入 ===

  Scenario: 透過截圖 OCR 輸入血壓數據
    Given 使用者選擇「血壓」作為數據來源
    When 使用者上傳血壓計截圖
    Then 系統解析並顯示收縮壓、舒張壓、心率
    And 使用者確認後寫入 Physio Sheet

  Scenario: 透過截圖 OCR 輸入體組成數據
    Given 使用者選擇「體組成」作為數據來源
    When 使用者上傳體脂計截圖
    Then 系統解析並顯示體重、體脂率、肌肉量等數值
    And 使用者確認後寫入 Physio Sheet

  Scenario: 透過截圖 OCR 輸入 CGM 數據
    Given 使用者選擇「CGM」作為數據來源
    When 使用者上傳 LibreLink App 截圖
    Then 系統解析並顯示血糖值與時間戳
    And 使用者確認後寫入 Physio Sheet

  Scenario: 透過截圖 OCR 輸入 Garmin 數據
    Given 使用者選擇「Garmin」作為數據來源
    And 使用者選擇要擷取的指標類型
    When 使用者上傳 Garmin Connect App 截圖
    Then 系統解析並顯示對應指標數值
    And 使用者確認後寫入 Physio Sheet

  Scenario: OCR 解析失敗時切換手動輸入
    Given 使用者已上傳截圖
    When OCR 解析失敗或數值不正確
    Then 使用者可切換為手動輸入模式
    And 手動填入數值後寫入 Physio Sheet

  # === 手動輸入 ===

  Scenario: 手動輸入生理數據
    Given 使用者選擇手動輸入模式
    When 使用者選擇數據類型並填入數值
    Then 數值驗證通過後寫入 Physio Sheet
