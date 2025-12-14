"""
Эндпоинты для работы с данными
"""
from fastapi import APIRouter, HTTPException
from backend.services.data_service import data_service

router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/info")
def get_data_info():
    """Получить информацию о датасете"""
    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        return data_service.get_info()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")