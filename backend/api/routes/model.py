"""
Эндпоинты для работы с моделями ML
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from backend.services.data_service import data_service
from backend.services.model_service import model_service
import logging
import traceback

router = APIRouter(prefix="/model", tags=["Model"])
logger = logging.getLogger(__name__)


# Модель данных для предсказания
class PredictRequest(BaseModel):
    """
    ВАЖНО: Используем только те признаки, на которых обучена модель!
    Исключены: key, mode, time_signature (их нет в числовом виде в датасете)
    """
    danceability: float = Field(..., ge=0.0, le=1.0, description="Танцевальность (0-1)")
    energy: float = Field(..., ge=0.0, le=1.0, description="Энергичность (0-1)")
    loudness: float = Field(..., ge=-60, le=0, description="Громкость в dB (-60 - 0)")
    speechiness: float = Field(..., ge=0.0, le=1.0, description="Речевой контент (0-1)")
    acousticness: float = Field(..., ge=0.0, le=1.0, description="Акустичность (0-1)")
    instrumentalness: float = Field(..., ge=0.0, le=1.0, description="Инструментальность (0-1)")
    liveness: float = Field(..., ge=0.0, le=1.0, description="Живое выступление (0-1)")
    valence: float = Field(..., ge=0.0, le=1.0, description="Позитивность (0-1)")
    tempo: float = Field(..., ge=0, le=250, description="Темп в BPM (0-250)")
    duration_ms: float = Field(..., ge=30000, le=600000, description="Длительность в мс")


@router.post("/train")
def train_model():
    """Обучение модели регрессии популярности"""
    try:
        # Проверяем что датасет загружен
        if not data_service.is_loaded():
            logger.error("Попытка обучить модель без загруженного датасета")
            raise HTTPException(
                status_code=404,
                detail="Датасет не загружен. Поместите SpotifyFeatures.csv в папку data/"
            )

        df = data_service.get_dataframe()

        # Проверяем наличие целевой переменной
        if 'popularity' not in df.columns:
            logger.error("Колонка 'popularity' не найдена в датасете")
            raise HTTPException(
                status_code=404,
                detail="Колонка 'popularity' не найдена в датасете"
            )

        logger.info(f"Начало обучения модели на датасете размером {len(df):,} строк")

        # Обучаем модель
        result = model_service.train_models(df)

        logger.info(f"Модель успешно обучена. R² = {result['metrics']['random_forest']['r2_score']:.4f}")

        return result

    except HTTPException:
        raise

    except ValueError as e:
        logger.error(f"Ошибка валидации данных: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка в данных: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Неожиданная ошибка при обучении модели: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.get("/metrics")
def get_model_metrics():
    """Получение метрик обученной модели"""
    try:
        metrics = model_service.get_metrics()
        return metrics

    except ValueError as e:
        logger.warning(f"Попытка получить метрики необученной модели: {e}")
        raise HTTPException(
            status_code=404,
            detail="Модель ещё не обучена. Сначала вызовите POST /model/train"
        )

    except Exception as e:
        logger.error(f"Ошибка получения метрик: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка: {str(e)}"
        )


@router.post("/predict")
def predict_popularity(request: PredictRequest):
    """
    Предсказание популярности трека по его характеристикам

    Принимает аудио-характеристики трека и возвращает предсказанную популярность
    """
    try:
        # Проверяем что модель обучена
        if not model_service.is_trained():
            logger.warning("Попытка предсказать без обученной модели")
            raise HTTPException(
                status_code=404,
                detail="Модель не обучена. Сначала обучите модель через POST /model/train"
            )

        # Конвертируем request в dict
        features_dict = request.dict()

        logger.info(f"Запрос на предсказание с параметрами: {features_dict}")

        # Делаем предсказание
        prediction_result = model_service.predict_single(features_dict)

        logger.info(f"Предсказание выполнено: {prediction_result['predicted_popularity']:.2f}")

        return prediction_result

    except HTTPException:
        raise

    except ValueError as e:
        logger.error(f"Ошибка валидации данных для предсказания: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка в данных: {str(e)}"
        )

    except Exception as e:
        logger.error(f"Ошибка при предсказании: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка: {str(e)}"
        )