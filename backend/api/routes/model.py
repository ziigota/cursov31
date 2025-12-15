"""
Эндпоинты для работы с моделями ML
"""
from fastapi import APIRouter, HTTPException
from backend.services.data_service import data_service
from backend.services.model_service import model_service
import logging
import traceback

router = APIRouter(prefix="/model", tags=["Model"])
logger = logging.getLogger(__name__)


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
        # Пробрасываем HTTPException дальше
        raise

    except ValueError as e:
        # Ошибки валидации данных
        logger.error(f"Ошибка валидации данных: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка в данных: {str(e)}"
        )

    except Exception as e:
        # Любая другая ошибка
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
        # Модель не обучена
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