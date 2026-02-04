# language: zh-TW
@MVP @Phase2
Feature: 基本輸入流程
  作為 使用者
  我想要 透過單一入口記錄飲食
  以便 快速完成記錄

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線
    And Gemini API 已連線

  # === 開啟輸入 Dialog ===

  @happy-path
  Scenario: 開啟輸入 Dialog
    Given 使用者在主畫面
    When 使用者點擊「＋輸入」按鈕
    Then 顯示輸入 Dialog
    And 顯示文字輸入區域
    And 顯示「✨送出」按鈕

  # === 文字輸入 - 飲食 ===

  @happy-path
  Scenario: 純文字輸入飲食記錄
    Given 使用者在輸入 Dialog
    When 使用者輸入「午餐吃了雞胸肉便當，飯半碗」
    And 點擊「✨送出」
    Then AI 辨識為飲食記錄
    And 顯示預覽畫面
    And 預覽包含：餐別、內容、營養推估

  @happy-path
  Scenario: 確認並儲存記錄
    Given AI 已顯示辨識預覽
    When 使用者點擊「✓ 儲存」
    Then 記錄寫入 Structured_Events Sheet
    And Dialog 關閉
    And 顯示儲存成功訊息

  # === 修改預覽 ===

  @happy-path
  Scenario: 修改 AI 辨識結果
    Given AI 已顯示辨識預覽
    When 使用者點擊「✏️ 修改」
    Then 預覽欄位變為可編輯
    When 使用者修改餐別為「晚餐」
    And 點擊「確認修改」
    Then 預覽更新為修改後的內容

  # === 取消輸入 ===

  @happy-path
  Scenario: 取消輸入
    Given 使用者在輸入 Dialog
    When 使用者點擊「✕」關閉按鈕
    Then Dialog 關閉
    And 不寫入任何記錄

  # === 錯誤處理 ===

  @error-handling
  Scenario: 空白輸入
    Given 使用者在輸入 Dialog
    When 使用者未輸入任何內容
    And 點擊「✨送出」
    Then 顯示提示「請輸入內容」
    And 不呼叫 AI

  @error-handling
  Scenario: AI 辨識失敗
    Given 使用者在輸入 Dialog
    When 使用者輸入無法辨識的內容
    And 點擊「✨送出」
    Then 顯示錯誤訊息
    And 提供手動選擇類型的選項

  @error-handling
  Scenario: 網路錯誤時的處理
    Given 使用者在輸入 Dialog
    And 網路連線中斷
    When 使用者輸入內容並送出
    Then 顯示網路錯誤訊息
    And 提供重試按鈕
