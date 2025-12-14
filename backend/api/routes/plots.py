"""
Эндпоинты для генерации графиков
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.services.data_service import data_service
from backend.services.plot_service import plot_service
from backend.services.analysis_service import analysis_service

router = APIRouter(prefix="/plots", tags=["Plots"])


@router.get("/scatter")
def plot_scatter():
    """График scatter: темп vs популярность"""
    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()

        if 'tempo' not in df.columns or 'popularity' not in df.columns:
            raise HTTPException(status_code=404, detail="Необходимые колонки не найдены")

        image = plot_service.create_scatter_plot(df, 'tempo', 'popularity')

        return JSONResponse(content={"image": image})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get("/histogram")
def plot_histogram():
    """Гистограмма громкости"""
    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()

        if 'loudness' not in df.columns:
            raise HTTPException(status_code=404, detail="Колонка 'loudness' не найдена")

        image = plot_service.create_histogram(df, 'loudness')

        return JSONResponse(content={"image": image})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


@router.get("/heatmap")
def plot_heatmap():
    """Тепловая карта корреляций аудио-характеристик"""
    try:
        if not data_service.is_loaded():
            raise HTTPException(status_code=404, detail="Датасет не загружен")

        df = data_service.get_dataframe()

        corr_matrix = analysis_service.get_correlation_matrix(df)
        image = plot_service.create_heatmap(corr_matrix)

        return JSONResponse(content={"image": image})

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")