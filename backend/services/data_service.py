
import pandas as pd
import logging
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DataService:


    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self._loaded = False

    def load_dataset(self, path: Path) -> bool:

        try:
            self.df = pd.read_csv(path)
            self._loaded = True
            logger.info(f"✓ Датасет загружен: {self.df.shape[0]:,} строк × {self.df.shape[1]} колонок")
            return True
        except FileNotFoundError:
            logger.error(f"✗ Файл не найден: {path}")
            self._loaded = False
            return False
        except Exception as e:
            logger.error(f"✗ Ошибка загрузки датасета: {e}")
            self._loaded = False
            return False

    def is_loaded(self) -> bool:
        """Проверить, загружен ли датасет"""
        return self._loaded and self.df is not None

    def get_dataframe(self) -> Optional[pd.DataFrame]:

        return self.df

    def get_info(self) -> dict:

        if not self.is_loaded():
            raise ValueError("Датасет не загружен")

        return {
            "rows": int(self.df.shape[0]),
            "columns": int(self.df.shape[1]),
            "features": list(self.df.columns),
            "missing_values": self.df.isnull().sum().to_dict(),
            "sample": self.df.head(5).to_dict(orient='records'),
            "dtypes": self.df.dtypes.astype(str).to_dict()
        }

    def get_column(self, column: str) -> pd.Series:

        if not self.is_loaded():
            raise ValueError("Датасет не загружен")

        if column not in self.df.columns:
            raise ValueError(f"Колонка '{column}' не найдена в датасете")

        return self.df[column]

    def get_columns(self, columns: list) -> pd.DataFrame:

        if not self.is_loaded():
            raise ValueError("Датасет не загружен")

        available_columns = [col for col in columns if col in self.df.columns]

        if not available_columns:
            raise ValueError("Ни одна из указанных колонок не найдена")

        return self.df[available_columns]

    def get_statistics(self, column: str) -> dict:

        if not self.is_loaded():
            raise ValueError("Датасет не загружен")

        if column not in self.df.columns:
            raise ValueError(f"Колонка '{column}' не найдена")

        series = self.df[column]

        return {
            "count": int(series.count()),
            "mean": float(series.mean()) if pd.api.types.is_numeric_dtype(series) else None,
            "median": float(series.median()) if pd.api.types.is_numeric_dtype(series) else None,
            "std": float(series.std()) if pd.api.types.is_numeric_dtype(series) else None,
            "min": float(series.min()) if pd.api.types.is_numeric_dtype(series) else None,
            "max": float(series.max()) if pd.api.types.is_numeric_dtype(series) else None,
            "q25": float(series.quantile(0.25)) if pd.api.types.is_numeric_dtype(series) else None,
            "q50": float(series.quantile(0.50)) if pd.api.types.is_numeric_dtype(series) else None,
            "q75": float(series.quantile(0.75)) if pd.api.types.is_numeric_dtype(series) else None,
        }


# Глобальный экземпляр сервиса (singleton)
data_service = DataService()