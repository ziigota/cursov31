import os
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

# Датасет
DATASET_PATH = DATA_DIR / "SpotifyFeatures.csv"

# API настройки
API_TITLE = "Spotify Tracks Analysis API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
API для анализа музыкальных треков Spotify.

Курсовая работа по статистическому моделированию.
"""

# CORS
CORS_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"  # Для разработки
]

# Модель
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100

# Аудио признаки
AUDIO_FEATURES = [
    'acousticness',
    'danceability',
    'energy',
    'instrumentalness',
    'liveness',
    'loudness',
    'speechiness',
    'tempo',
    'valence'
]

# Признаки для модели
MODEL_FEATURES = AUDIO_FEATURES + ['duration_ms', 'time_signature']

# Признаки для анализа распределений
DISTRIBUTION_FEATURES = ['loudness', 'tempo', 'danceability']

# Создание папок
PLOTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)