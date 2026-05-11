import joblib
from sklearn.linear_model import LogisticRegression
import logging

class MLClassifier:
    def __init__(self, C=1.0, class_weight='balanced', random_state=42):
        self.C = C
        self.class_weight = class_weight
        self.random_state = random_state
        self.model = None
    
    def train(self, X, y):
        self.model = LogisticRegression(
            C=self.C,
            class_weight=self.class_weight,
            random_state=self.random_state,
            max_iter=1000
        )
        self.model.fit(X, y)
        logging.info("Model trained")
        return self.model
    
    def predict_proba(self, X):
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        return self.model.predict_proba(X)[:, 1]
    
    def predict(self, X):
        return self.model.predict(X)
    
    def save(self, path):
        if self.model:
            joblib.dump(self.model, path)
            logging.info(f"Model saved to {path}")
    
    def load(self, path):
        self.model = joblib.load(path)
        logging.info(f"Model loaded from {path}")