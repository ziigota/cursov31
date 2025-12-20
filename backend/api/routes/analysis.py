"""
Эндпоинты для статистического анализа
"""
from fastapi import APIRouter, HTTPException
from backend.services.data_service import data_service
from backend.services.analysis_service import analysis_service

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get("/distributions")
def analyze_distributions():

    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()
        result = analysis_service.analyze_distributions(df)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get("/correlations")
def analyze_correlations():

    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()
        result = analysis_service.analyze_correlations(df)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get("/genres")
def analyze_genres():

    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()
        result = analysis_service.analyze_genres(df)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")