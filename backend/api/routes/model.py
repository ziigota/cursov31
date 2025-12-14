"""
Эндпоинты для работы с моделями ML
"""
from fastapi import APIRouter, HTTPException
from backend.services.data_service import data_service
from backend.services.model_service import model_service

router = APIRouter(prefix="/model", tags=["Model"])


@router.post("/train")
def train_model():
    """Обучение модели регрессии популярности"""
    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()

        if 'popularity' not in df.columns:
            raise HTTPException(status_code=404, detail="Колонка 'popularity' не найдена")

        result = model_service.train_models(df)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get("/metrics")
def get_model_metrics():
    """Получение метрик обученной модели"""
    try:
        metrics = model_service.get_metrics()
        return metrics

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")