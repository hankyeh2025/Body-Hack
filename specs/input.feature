# language: zh-TW
Feature: 統一輸入
  作為 使用者
  我想要 透過單一入口記錄各種數據
  以便 降低操作摩擦，專注於記錄本身

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線
    And Gemini API 已設定

  # === 基本輸入流程 ===

  Scenario: 開啟輸入 Dialog
    Given 使用者在主畫面
    When 使用者點擊「＋輸入」按鈕
    Then 顯示輸入 Dialog
    And 顯示「🌅晨間儀式」「🌙睡前儀式」按鈕
    And 顯示上傳截圖區域
    And 顯示文字輸入區域

  Scenario: 純文字輸入 - 飲食
    Given 使用者在輸入 Dialog
    When 使用者輸入「午餐吃了雞胸肉便當，飯半碗」
    And 點擊「✨送出」
    Then AI 辨識為飲食記錄
    And 顯示預覽：餐別、內容、營養推估
    And 顯示「儲存」「儲存+回饋」按鈕

  Scenario: 純截圖輸入 - 血糖
    Given 使用者在輸入 Dialog
    When 使用者上傳血糖截圖
    And 點擊「✨送出」
    Then AI 辨識為血糖記錄
    And 顯示預覽：血糖值、趨勢、時間
    And 顯示「儲存」「儲存+回饋」按鈕

  Scenario: 混合輸入 - 飲食照片加文字
    Given 使用者在輸入 Dialog
    When 使用者上傳餐點照片
    And 輸入「這是午餐，飯大概半碗」
    And 點擊「✨送出」
    Then AI 結合照片和文字辨識
    And 顯示預覽結果

  Scenario: 修改 AI 辨識結果
    Given AI 已顯示辨識預覽
    When 使用者點擊「✏️修改」
    Then 預覽欄位變為可編輯
    When 使用者修改內容
    And 點擊「確認修改」
    Then 預覽更新為修改後的內容

  Scenario: 儲存記錄（不要回饋）
    Given AI 已顯示辨識預覽
    When 使用者點擊「✓儲存」
    Then 記錄寫入對應 Sheet
    And Dialog 關閉
    And 時間軸顯示新記錄氣泡
    And 記錄 Analytics 事件 input_save

  Scenario: 儲存並取得回饋
    Given AI 已顯示辨識預覽
    When 使用者點擊「💬回饋」
    Then 記錄寫入對應 Sheet
    And AI 根據脈絡產生即時回饋
    And 時間軸顯示記錄氣泡和回饋氣泡
    And 記錄 Analytics 事件 input_save（with_feedback: true）

  # === 儀式模式 ===

  Scenario: 開始晨間儀式
    Given 使用者在輸入 Dialog
    When 使用者點擊「🌅晨間儀式」
    Then 顯示晨間儀式引導
    And 提示上傳體重、血壓、睡眠數據

  Scenario: 完成晨間儀式
    Given 使用者在晨間儀式模式
    When 使用者上傳完所有數據
    And 點擊「完成儀式」
    Then 所有記錄寫入對應 Sheet
    And AI 產生晨間回饋（7天趨勢 + 今日提醒）
    And 回饋自動保存至 Insights Sheet
    And 時間軸顯示所有記錄和回饋

  Scenario: 開始睡前儀式
    Given 使用者在輸入 Dialog
    When 使用者點擊「🌙睡前儀式」
    Then 顯示睡前儀式引導
    And 提示上傳血壓、步數、樓層數數據

  Scenario: 完成睡前儀式
    Given 使用者在睡前儀式模式
    When 使用者上傳完所有數據
    And 點擊「完成儀式」
    Then 所有記錄寫入對應 Sheet
    And AI 產生睡前回饋（今日總結 + 隔日交接）
    And 回饋自動保存至 Insights Sheet
    And 時間軸顯示所有記錄和回饋
