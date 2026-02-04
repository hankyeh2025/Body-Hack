"""
Google Sheets 客戶端
封裝 gspread 操作
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


class SheetsClient:
    """Google Sheets 操作封裝"""

    def __init__(self):
        """初始化連線，使用 Streamlit secrets"""
        self._client: Optional[gspread.Client] = None
        self._spreadsheet: Optional[gspread.Spreadsheet] = None

    def _get_client(self) -> gspread.Client:
        """取得或建立 gspread client（懶載入）"""
        if self._client is None:
            creds_dict = st.secrets["gcp_service_account"]
            creds = Credentials.from_service_account_info(
                dict(creds_dict),
                scopes=SCOPES
            )
            self._client = gspread.authorize(creds)
        return self._client

    def _get_spreadsheet(self) -> gspread.Spreadsheet:
        """取得或開啟試算表（懶載入）"""
        if self._spreadsheet is None:
            client = self._get_client()
            spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
            self._spreadsheet = client.open_by_key(spreadsheet_id)
        return self._spreadsheet

    def test_connection(self) -> Dict[str, Any]:
        """測試連線，回傳試算表資訊"""
        try:
            spreadsheet = self._get_spreadsheet()
            worksheets = [ws.title for ws in spreadsheet.worksheets()]
            return {
                "success": True,
                "title": spreadsheet.title,
                "worksheets": worksheets,
                "url": spreadsheet.url
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def read_sheet(
        self,
        sheet_name: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        讀取指定 Sheet 的所有記錄

        Args:
            sheet_name: 分頁名稱
            filters: 篩選條件 {"欄位名": "值"}

        Returns:
            記錄列表
        """
        spreadsheet = self._get_spreadsheet()
        worksheet = spreadsheet.worksheet(sheet_name)
        records = worksheet.get_all_records()

        if filters:
            filtered = []
            for record in records:
                match = all(
                    record.get(key) == value
                    for key, value in filters.items()
                )
                if match:
                    filtered.append(record)
            return filtered

        return records

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def append_row(self, sheet_name: str, data: Dict[str, Any]) -> bool:
        """
        新增一筆記錄

        Args:
            sheet_name: 分頁名稱
            data: 記錄資料（dict）

        Returns:
            是否成功
        """
        spreadsheet = self._get_spreadsheet()
        worksheet = spreadsheet.worksheet(sheet_name)

        # 取得欄位順序
        headers = worksheet.row_values(1)

        # 按照欄位順序組成 row
        row = [data.get(header, "") for header in headers]

        worksheet.append_row(row, value_input_option="USER_ENTERED")
        return True

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def update_row(
        self,
        sheet_name: str,
        row_id: str,
        data: Dict[str, Any]
    ) -> bool:
        """
        更新指定記錄

        Args:
            sheet_name: 分頁名稱
            row_id: 記錄的 id
            data: 要更新的欄位

        Returns:
            是否成功
        """
        spreadsheet = self._get_spreadsheet()
        worksheet = spreadsheet.worksheet(sheet_name)

        # 找到 id 欄位的 index
        headers = worksheet.row_values(1)
        id_col = headers.index("id") + 1  # gspread 是 1-based

        # 找到目標 row
        id_values = worksheet.col_values(id_col)
        try:
            row_num = id_values.index(row_id) + 1  # 1-based
        except ValueError:
            return False

        # 更新指定欄位
        for key, value in data.items():
            if key in headers:
                col_num = headers.index(key) + 1
                worksheet.update_cell(row_num, col_num, value)

        return True

    def get_unique_values(self, sheet_name: str, column: str) -> List[str]:
        """
        取得某欄位的不重複值（用於 autocomplete）

        Args:
            sheet_name: 分頁名稱
            column: 欄位名稱

        Returns:
            不重複值列表
        """
        records = self.read_sheet(sheet_name)
        values = set()
        for record in records:
            value = record.get(column)
            if value:
                values.add(str(value))
        return sorted(list(values))


# 單例模式
@st.cache_resource
def get_sheets_client() -> SheetsClient:
    """取得 SheetsClient 單例"""
    return SheetsClient()
