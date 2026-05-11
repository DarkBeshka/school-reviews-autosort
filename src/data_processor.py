import logging
import tqdm
from typing import List, Dict
from src.google_sheets_client import SheetsClient
from src.classification_pipeline import ReviewClassifier
from src.course_matcher import CourseMatcher
from config.settings import (
    RAW_SHEET_ID, FINAL_SHEET_ID, ROBOTS_SHEET_ID,
    RAW_WORKSHEET_NAME, DIRECTION_SHEETS,
    COLUMN_STATUS, COLUMN_COURSE, COLUMN_RATING, COLUMN_REVIEW_TEXT
)

class DataProcessor:
    def __init__(self, sheets_client: SheetsClient, classifier: ReviewClassifier, matcher: CourseMatcher):
        self.sheets = sheets_client
        self.classifier = classifier
        self.matcher = matcher
        self.raw_worksheet = None
        self.destination_sheets = {}
    
    def initialize_worksheets(self):
        self.raw_worksheet = self.sheets.get_worksheet(RAW_SHEET_ID, RAW_WORKSHEET_NAME)
        final_wb = self.sheets.client.open_by_key(FINAL_SHEET_ID)
        robots_wb = self.sheets.client.open_by_key(ROBOTS_SHEET_ID)
        for direction, sheet_name in DIRECTION_SHEETS.items():
            wb = robots_wb if direction == "robots" else final_wb
            self.destination_sheets[direction] = wb.worksheet(sheet_name)
    
    def process_new_reviews(self):
        logging.info("Starting processing of new reviews")
        if self.raw_worksheet is None:
            self.initialize_worksheets()
        
        new_rows = self.sheets.get_new_rows(self.raw_worksheet, status_column_index=COLUMN_STATUS)
        if not new_rows:
            logging.info("No new reviews found")
            print("No new reviews.")
            return
        
        logging.info(f"Found {len(new_rows)} new reviews")
        print(f"Processing {len(new_rows)} new reviews...")
        
        problematic_by_direction: Dict[str, List[list]] = {
            "programming": [], "art": [], "game": [], "robots": []
        }
        
        # Запись проблемных отзывов в соответствующие таблицы
        for row_num, row_values in tqdm.tqdm(new_rows, desc="Classifying"):
            try:
                course = row_values[COLUMN_COURSE] if len(row_values) > COLUMN_COURSE else ""
                rating_str = row_values[COLUMN_RATING] if len(row_values) > COLUMN_RATING else "5"
                rating = int(rating_str) if rating_str.isdigit() else 5
                review_text = row_values[COLUMN_REVIEW_TEXT] if len(row_values) > COLUMN_REVIEW_TEXT else ""
            except IndexError:
                self.sheets.update_status(self.raw_worksheet, row_num, "Проверен", COLUMN_STATUS)
                continue
            
            is_problematic, prob, _ = self.classifier.classify(review_text, rating)
            
            if is_problematic:
                direction = self.matcher.get_direction(course)
                if direction is None:
                    logging.warning(f"Unknown course '{course}', default to art")
                    direction = "art"
                enriched_row = row_values + [f"{prob:.2f}"]
                problematic_by_direction[direction].append(enriched_row)
            
            self.sheets.update_status(self.raw_worksheet, row_num, "Проверен", COLUMN_STATUS)
        
        for direction, data_rows in problematic_by_direction.items():
            if not data_rows:
                continue
            target = self.destination_sheets[direction]
            start, end = self.sheets.append_rows(target, data_rows)
            if start:
                # Установить статус "На рассмотрении" в колонке A для новых записей
                status_values = [["На рассмотрении"] for _ in range(len(data_rows))]
                self.sheets.update_range(target, status_values, f"A{start}:A{end}")
            logging.info(f"Added {len(data_rows)} problematic reviews to {direction}")
        
        logging.info("Processing completed")
        print("All new reviews processed.")