from typing import List, Tuple
from config.settings import KEYWORDS, MIN_RATING_FOR_GOOD

class RuleEngine:
    def __init__(self, keywords: List[str] = None, min_rating_good: int = MIN_RATING_FOR_GOOD):
        self.keywords = keywords or KEYWORDS
        self.min_rating_good = min_rating_good
    
    def is_low_rating(self, rating: int) -> bool:
        try:
            return int(rating) < self.min_rating_good
        except (ValueError, TypeError):
            return False
    
    def contains_keywords(self, processed_text: str) -> bool:
        words = set(processed_text.split())
        for kw in self.keywords:
            if kw in words:
                return True
        return False
    
    def combine(self, model_prob: float, rating: int, processed_text: str, threshold: float) -> Tuple[bool, dict]:
        """
        Основная логика решающего правила.
        Решение принимается по правилу OR:
        - модель даёт вероятность > порога
        - оценка < 5
        - наличие ключевых слов
        """
        low_score = self.is_low_rating(rating)
        has_keywords = self.contains_keywords(processed_text)
        model_positive = model_prob >= threshold
        is_problematic = model_positive or low_score or has_keywords
        details = {
            'model_prob': model_prob,
            'model_positive': model_positive,
            'low_score': low_score,
            'has_keywords': has_keywords,
            'threshold': threshold
        }
        return is_problematic, details