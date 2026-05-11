import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Загрузка ресурсов NLTK
try:
    nltk.data.find('tokenizers/punkt_tab')
except:
    nltk.download('punkt_tab')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
russian_stopwords = set(stopwords.words('russian'))

class TextPreprocessor:
    @staticmethod
    def preprocess(text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^а-яё\s]', '', text)
        tokens = nltk.word_tokenize(text, language='russian')
        tokens = [t for t in tokens if t not in russian_stopwords and len(t) > 1]
        lemmas = [lemmatizer.lemmatize(t) for t in tokens]
        return " ".join(lemmas)