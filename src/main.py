import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import setup_logging, ensure_dirs
from src.google_sheets_client import SheetsClient
from src.feature_extraction import TfidfManager
from src.ml_model import MLClassifier
from src.rule_engine import RuleEngine
from src.classification_pipeline import ReviewClassifier
from src.course_matcher import CourseMatcher
from src.data_processor import DataProcessor
from config.settings import CREDENTIALS_FILE, MODELS_DIR, COURSE_LISTS_DIR
import logging

def main():
    """
    Основная функция, запускаемая ежедневно.
    Читает новые отзывы из основной таблицы, классифицирует проблемные,
    сортирует по направлениям и записывает в итоговые таблицы.
    """
    setup_logging()
    ensure_dirs([MODELS_DIR, COURSE_LISTS_DIR, os.path.dirname(CREDENTIALS_FILE)])
    
    vec_path = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
    model_path = os.path.join(MODELS_DIR, "logreg_model.pkl")
    
    if not os.path.exists(vec_path) or not os.path.exists(model_path):
        logging.error("Model not found. Run scripts/train_model.py first.")
        print("ERROR: Model not trained. Run 'python scripts/train_model.py --data labeled.csv'")
        sys.exit(1)
    
    try:
        sheets = SheetsClient(CREDENTIALS_FILE)
        tfidf = TfidfManager()
        tfidf.load(vec_path)
        ml = MLClassifier()
        ml.load(model_path)
        rules = RuleEngine()
        classifier = ReviewClassifier(tfidf, ml, rules)
        matcher = CourseMatcher(COURSE_LISTS_DIR)
        processor = DataProcessor(sheets, classifier, matcher)
        processor.process_new_reviews()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()