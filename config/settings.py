import os

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Пути к файлам
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials", "credentials_all.json") # ключи сервисного аккаунта Google
COURSE_LISTS_DIR = os.path.join(BASE_DIR, "course_lists")
MODELS_DIR = os.path.join(BASE_DIR, "data", "models")
LOG_FILE = os.path.join(BASE_DIR, "logs", "processing.log")

# ID Google таблиц
RAW_SHEET_ID = "RAW_SHEET_ID"  # исходная таблица с сырыми отзывами
FINAL_SHEET_ID = "FINAL_SHEET_ID"  # итоговые таблицы по направлениям
ROBOTS_SHEET_ID = "ROBOTS_SHEET_ID"  # таблица робототехники

# Названия листов
RAW_WORKSHEET_NAME = "1.0. Уч. год"  # лист с новыми сырыми отзывами (основной)
# CORP_WORKSHEET_NAME = "5. Отзывы КК"  # корпоративные отзывы

# Направления и соответствующие листы в итоговых таблицах
DIRECTION_SHEETS = {
    "programming": "1. Программирование",
    "art": "2. ЦТ",
    "game": "3. Создание игр",
    "robots": "Робототехника"
}

# Файлы со списками курсов
COURSE_LISTS_FILES = {
    "programming": "programming_courses_list.txt",
    "art": "art_courses_list.txt",
    "game": "game_courses_list.txt",
    "robots": "robots_courses_list.txt"
}

# Параметры модели и правил
MODEL_THRESHOLD = 0.6          # вероятность, выше которой отзыв считается проблемным моделью
MIN_RATING_FOR_GOOD = 5        # оценка ниже этого порога => проблемный
KEYWORDS = [
    "ошибка", "не работает", "непонятно",
    "сломано", "проблема", "баг"
]

# Параметры TF-IDF
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

# Индексы столбцов в исходной таблице (0-based)
COLUMN_STATUS = 0      # A
COLUMN_COURSE = 5      # F
COLUMN_RATING = 8      # I
COLUMN_REVIEW_TEXT = 9 # J