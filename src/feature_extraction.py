import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from config.settings import TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE
import os
import logging

class TfidfManager:
    def __init__(self, max_features=TFIDF_MAX_FEATURES, ngram_range=TFIDF_NGRAM_RANGE):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vectorizer = None
    
    def train(self, texts):
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            lowercase=False
        )
        self.vectorizer.fit(texts)
        return self.vectorizer
    
    def transform(self, texts):
        if self.vectorizer is None:
            raise ValueError("Vectorizer not trained or loaded")
        return self.vectorizer.transform(texts)
    
    def save(self, path):
        if self.vectorizer:
            joblib.dump(self.vectorizer, path)
            logging.info(f"Vectorizer saved to {path}")
    
    def load(self, path):
        if os.path.exists(path):
            self.vectorizer = joblib.load(path)
            logging.info(f"Vectorizer loaded from {path}")
        else:
            raise FileNotFoundError(f"Vectorizer file not found: {path}")