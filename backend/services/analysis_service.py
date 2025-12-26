import pandas as pd
import numpy as np
from typing import Dict, List
from backend.config import AUDIO_FEATURES, DISTRIBUTION_FEATURES


class AnalysisService:

    @staticmethod
    def analyze_distributions(df: pd.DataFrame, features: List[str] = None) -> Dict:

        if features is None:
            features = DISTRIBUTION_FEATURES

        stats = {}
        interpretations = {
            "loudness": "Громкость измеряется в дБ. Среднее значение показывает типичную громкость треков. Большинство современных треков имеют громкость около -7 dB.",
            "tempo": "Темп в BPM (ударов в минуту) показывает ритмическую скорость композиции. Средний темп около 120 BPM соответствует популярной танцевальной музыке.",
            "danceability": "Танцевальность от 0 до 1 показывает, насколько трек подходит для танцев на основе темпа, ритма и стабильности бита. Значение 0.6+ указывает на высокую танцевальность."
        }

        for feature in features:
            if feature in df.columns:
                series = df[feature].dropna()

                stats[feature] = {
                    "mean": float(series.mean()),
                    "median": float(series.median()),
                    "std": float(series.std()),
                    "min": float(series.min()),
                    "max": float(series.max()),
                    "q25": float(series.quantile(0.25)),
                    "q75": float(series.quantile(0.75)),
                    "skewness": float(series.skew()),
                    "kurtosis": float(series.kurtosis())
                }

        return {
            "distributions": stats,
            "interpretation": interpretations
        }

    @staticmethod
    def analyze_correlations(df: pd.DataFrame, target: str = 'popularity') -> Dict:

        available_features = [f for f in AUDIO_FEATURES if f in df.columns]

        if target not in df.columns:
            raise ValueError(f"Колонка '{target}' не найдена в датасете")

        # Вычисляем корреляции
        correlations = df[available_features + [target]].corr()[target].drop(target)

        # Сортируем
        sorted_corr = correlations.sort_values(ascending=False)

        # Интерпретация
        interpretation = """
        Корреляция показывает линейную связь между признаком и популярностью:
        - Положительная корреляция: при увеличении признака популярность растёт
        - Отрицательная корреляция: при увеличении признака популярность падает
        - Близко к 0: слабая или отсутствующая линейная связь
        
        Важно: корреляция не означает причинно-следственную связь!
        """

        return {
            "correlations": correlations.to_dict(),
            "top_positive": sorted_corr.head(3).to_dict(),
            "top_negative": sorted_corr.tail(3).to_dict(),
            "interpretation": interpretation.strip(),
            "strongest_correlation": {
                "feature": sorted_corr.abs().idxmax(),
                "value": float(correlations[sorted_corr.abs().idxmax()]),
                "type": "положительная" if correlations[sorted_corr.abs().idxmax()] > 0 else "отрицательная"
            }
        }

    @staticmethod
    def analyze_genres(df: pd.DataFrame) -> Dict:

        if 'genre' not in df.columns:
            raise ValueError("Колонка 'genre' не найдена в датасете")

        # Признаки для анализа
        audio_features = ['danceability', 'energy', 'loudness', 'tempo', 'valence',
                          'acousticness', 'instrumentalness', 'speechiness']
        available_features = [f for f in audio_features if f in df.columns]

        # Статистика по жанрам
        genre_stats = df.groupby('genre')[available_features].mean()
        genre_counts = df['genre'].value_counts()

        # Топ-5 жанров
        top_genres = genre_counts.head(5).index.tolist()

        # Характеристики топ жанров
        genre_characteristics = {}
        for genre in top_genres:
            genre_data = genre_stats.loc[genre]
            top_features = genre_data.nlargest(3)

            genre_characteristics[genre] = {
                "count": int(genre_counts[genre]),
                "avg_characteristics": genre_data.to_dict(),
                "distinctive_features": top_features.to_dict()
            }

        interpretation = """
        Каждый жанр имеет уникальный "звуковой отпечаток":
        - EDM/Electronic: высокая танцевальность и энергия
        - Classical: высокая акустичность и инструментальность
        - Hip-Hop/Rap: высокая speechiness (речевой контент)
        - Rock: высокая энергия и громкость
        - Pop: высокая танцевальность и валентность (позитивность)
        """

        return {
            "genres": list(df['genre'].unique()),
            "genre_count": int(df['genre'].nunique()),
            "total_tracks": int(len(df)),
            "genre_statistics": genre_stats.to_dict(),
            "genre_counts": genre_counts.to_dict(),
            "top_genres": top_genres,
            "genre_characteristics": genre_characteristics,
            "interpretation": interpretation.strip()
        }

    @staticmethod
    def get_correlation_matrix(df: pd.DataFrame, features: List[str] = None) -> pd.DataFrame:

        if features is None:
            features = AUDIO_FEATURES + ['popularity']

        available_features = [f for f in features if f in df.columns]

        if len(available_features) < 2:
            raise ValueError("Недостаточно признаков для построения корреляционной матрицы")

        return df[available_features].corr()

    @staticmethod
    def get_summary_statistics(df: pd.DataFrame) -> Dict:

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        summary = {}
        for col in numeric_cols:
            summary[col] = {
                "count": int(df[col].count()),
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "25%": float(df[col].quantile(0.25)),
                "50%": float(df[col].quantile(0.50)),
                "75%": float(df[col].quantile(0.75)),
                "max": float(df[col].max())
            }

        return summary


# Глобальный экземпляр сервиса
analysis_service = AnalysisService()