import gspread
from google.oauth2.service_account import Credentials
from typing import List, Tuple
import logging

class SheetsClient:
    def __init__(self, credentials_file: str):
        self.credentials_file = credentials_file
        self.client = None
        self.connect()
    
    def connect(self):
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=scopes)
            self.client = gspread.authorize(creds)
            logging.info("Connected to Google Sheets")
        except Exception as e:
            logging.error(f"Failed to connect: {e}")
            raise
    
    def get_worksheet(self, spreadsheet_key: str, worksheet_name: str):
        workbook = self.client.open_by_key(spreadsheet_key)
        return workbook.worksheet(worksheet_name)
    
    def get_new_rows(self, worksheet, status_column_index: int = 0, status_value: str = "Проверен") -> List[Tuple[int, List[str]]]:
        all_values = worksheet.get_all_values()
        if len(all_values) <= 1:
            return []
        new_rows = []
        for i, row in enumerate(all_values[1:], start=2):
            if len(row) > status_column_index:
                if row[status_column_index] != status_value:
                    new_rows.append((i, row))
            else:
                new_rows.append((i, row))
        return new_rows
    
    def update_status(self, worksheet, row_num: int, status: str, col_index: int = 0):
        cell = gspread.Cell(row_num, col_index + 1, status)
        worksheet.update_cells([cell], value_input_option="USER_ENTERED")
    
    def append_rows(self, worksheet, rows_data: List[List], start_col: int = 0):
        if not rows_data:
            return None, None
        col_a = worksheet.col_values(1)
        next_row = len(col_a) + 1
        max_len = max(len(r) for r in rows_data)
        cells = []
        for i, row in enumerate(rows_data):
            row_num = next_row + i
            for col_idx, value in enumerate(row):
                if col_idx < max_len:
                    cells.append(gspread.Cell(row_num, col_idx + 1 + start_col, value))
        if cells:
            worksheet.update_cells(cells, value_input_option="USER_ENTERED")
        return next_row, next_row + len(rows_data) - 1
    
    def update_range(self, worksheet, values: List[List], range_label: str):
        worksheet.update(range_label, values, value_input_option="USER_ENTERED")