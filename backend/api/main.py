"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.config import (
    API_TITLE, API_VERSION, API_DESCRIPTION,
    CORS_ORIGINS, DATASET_PATH
)
from backend.services.data_service import data_service
from backend.api.routes import data, analysis, plots, model

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Создание приложения
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(data.router)
app.include_router(analysis.router)
app.include_router(plots.router)
app.include_router(model.router)


@app.on_event("startup")
async def startup_event():
    """Загрузка данных при старте приложения"""
    logger.info("Запуск приложения...")

    if data_service.load_dataset(DATASET_PATH):
        logger.info("Датасет успешно загружен")
    else:
        logger.warning("Датасет не загружен. Поместите SpotifyFeatures.csv в папку data/")


@app.get("/", tags=["Root"])
def root():
    """Главная страница API"""
    return {
        "message": "Spotify Tracks Analysis API",
        "version": API_VERSION,
        "status": "running",
        "dataset_loaded": data_service.is_loaded(),
        "endpoints": {
            "data": {
                "GET /data/info": "Информация о датасете"
            },
            "analysis": {
                "GET /analysis/distributions": "Анализ распределений",
                "GET /analysis/correlations": "Корреляции признаков",
                "GET /analysis/genres": "Анализ по жанрам"
            },
            "plots": {
                "GET /plots/scatter": "График темп vs популярность",
                "GET /plots/histogram": "Гистограмма громкости",
                "GET /plots/heatmap": "Тепловая карта признаков"
            },
            "model": {
                "POST /model/train": "Обучение модели регрессии",
                "GET /model/metrics": "Метрики модели"
            }
        },
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Проверка состояния сервера"""
    return {
        "status": "healthy",
        "dataset_loaded": data_service.is_loaded()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)