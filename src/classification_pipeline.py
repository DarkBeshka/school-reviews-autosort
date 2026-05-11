from src.text_preprocessor import TextPreprocessor
from src.feature_extraction import TfidfManager
from src.ml_model import MLClassifier
from src.rule_engine import RuleEngine
from config.settings import MODEL_THRESHOLD

class ReviewClassifier:
    def __init__(self, tfidf_manager: TfidfManager, ml_model: MLClassifier, rule_engine: RuleEngine):
        self.tfidf_manager = tfidf_manager
        self.ml_model = ml_model
        self.rule_engine = rule_engine
        self.threshold = MODEL_THRESHOLD
    
    def classify(self, review_text: str, rating: int):
        """
        Принимает текст отзыва и числовую оценку.
        Возвращает (is_problematic, probability, details).
        """
        # Предобработка текста
        processed = TextPreprocessor.preprocess(review_text)
        prob = 0.0  # пустой текст не считаем проблемным
        if processed.strip():
            vec = self.tfidf_manager.transform([processed])
            prob = self.ml_model.predict_proba(vec)[0]  # вероятность класса 1 (проблемный)

        is_problematic, details = self.rule_engine.combine(prob, rating, processed, self.threshold)
        details['processed_text'] = processed
        return is_problematic, prob, details