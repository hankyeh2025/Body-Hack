# language: zh-TW
Feature: 近 7 天報告
  作為 使用者
  我想要 回顧過去一週的表現
  以便 了解整體趨勢和改進方向

  Background:
    Given 使用者已開啟 App
    And Google Sheets 已連線
    And Gemini API 已設定
    And 使用者有過去 7 天的記錄

  Scenario: 開啟近 7 天報告
    Given 使用者在主畫面
    When 使用者點擊「🤖AI」
    And 選擇「📊近 7 天報告」
    Then AI 讀取過去 7 天數據
    And 顯示報告 Dialog
    And 記錄 Analytics 事件 ai_weekly_review

  Scenario: 查看報告內容
    Given AI 已生成近 7 天報告
    Then 報告包含：
      | 區塊 | 內容 |
      | 重點發現 | 各項目標達成率、趨勢變化 |
      | 建議事項 | 改進方向、維持項目 |
      | 下週目標 | 建議的調整 |
      | 摘要 | 一句話總結 |

  Scenario: 保存報告
    Given 使用者查看報告
    When 使用者點擊「📝保存報告」
    Then 報告寫入 Insights Sheet（type: weekly_review）
    And 顯示「報告已保存」
    And Dialog 關閉

  Scenario: 不保存報告
    Given 使用者查看報告
    When 使用者點擊「關閉」
    Then 顯示「要保存這份報告嗎？」
    When 使用者選擇「不保存」
    Then Dialog 關閉
    And 報告不寫入 Sheet
