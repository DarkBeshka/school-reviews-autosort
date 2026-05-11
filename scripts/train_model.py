import sys
import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.text_preprocessor import TextPreprocessor
from src.feature_extraction import TfidfManager
from src.ml_model import MLClassifier
from src.utils import setup_logging, ensure_dirs
from config.settings import MODELS_DIR
import logging

def train(data_path: str):
    """
    Обучает модель логистической регрессии на размеченных данных.
    Сохраняет векторизатор TF-IDF и модель в папку model_dir.

    Ожидается CSV с колонками: 'review_text', 'rating', 'label'
    label: 1 - проблемный отзыв, 0 - не проблемный.
    """
    setup_logging()
    ensure_dirs([MODELS_DIR])
    
    df = pd.read_csv(data_path)
    if 'review_text' not in df.columns or 'label' not in df.columns:
        logging.error("CSV must have 'review_text' and 'label' columns")
        print("Error: CSV must have 'review_text' and 'label' columns")
        return
    
    # Предобработка текстов
    print("Preprocessing texts...")
    df['processed'] = df['review_text'].apply(TextPreprocessor.preprocess)
    
    # Разделение на обучающую и тестовую выборки (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
    )
    
    # Векторизация TF-IDF
    print("Training TF-IDF...")
    tfidf = TfidfManager()
    tfidf.train(X_train.tolist())
    X_train_vec = tfidf.transform(X_train.tolist())
    X_test_vec = tfidf.transform(X_test.tolist())
    
    # Обучение логистической регрессии
    print("Training logistic regression...")
    model = MLClassifier()
    model.train(X_train_vec, y_train)
    
    # Оценка
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    print(f"Accuracy: {acc:.3f}, Precision: {prec:.3f}, Recall: {rec:.3f}")
    logging.info(f"Metrics: Acc={acc:.3f}, Prec={prec:.3f}, Rec={rec:.3f}")
    
    # Сохранение
    tfidf.save(os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl"))
    model.save(os.path.join(MODELS_DIR, "logreg_model.pkl"))
    print(f"Models saved to {MODELS_DIR}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    args = parser.parse_args()
    train(args.data)