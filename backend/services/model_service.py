"""
Сервис для работы с моделями машинного обучения
Обучение моделей регрессии популярности треков
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from typing import Dict, Tuple, Optional
import logging
import traceback
from backend.config import RANDOM_STATE, TEST_SIZE, N_ESTIMATORS, MODEL_FEATURES

logger = logging.getLogger(__name__)


class ModelService:
    """Сервис для обучения и работы с ML моделями"""

    def __init__(self):
        self.lr_model: Optional[LinearRegression] = None
        self.rf_model: Optional[RandomForestRegressor] = None
        self.metrics: Optional[Dict] = None
        self.best_model: Optional[str] = None
        self.feature_names: Optional[list] = None
        self.X_test = None
        self.y_test = None
        self.lr_pred = None
        self.rf_pred = None

    def prepare_data(self, df: pd.DataFrame, target: str = 'popularity',
                     features: list = None) -> Tuple:
        """
        Подготовить данные для обучения модели

        Args:
            df: Датафрейм с данными
            target: Целевая переменная (по умолчанию popularity)
            features: Список признаков (по умолчанию из config.MODEL_FEATURES)

        Returns:
            tuple: (X_train, X_test, y_train, y_test, feature_names)
        """
        try:
            logger.info(f"Подготовка данных. Размер датасета: {df.shape}")

            if target not in df.columns:
                raise ValueError(f"Колонка '{target}' не найдена в датасете. Доступные колонки: {list(df.columns)}")

            if features is None:
                features = MODEL_FEATURES
                logger.info(f"Используются признаки из config: {features}")

            # Выбираем только доступные признаки
            available_features = [f for f in features if f in df.columns]
            missing_features = [f for f in features if f not in df.columns]

            if missing_features:
                logger.warning(f"Отсутствующие признаки (будут пропущены): {missing_features}")

            if not available_features:
                raise ValueError(f"Ни один из указанных признаков не найден в датасете! Требуются: {features}")

            logger.info(f"Используется {len(available_features)} признаков: {available_features}")

            # Подготовка данных
            X = df[available_features].copy()

            # Проверяем типы данных
            non_numeric = X.select_dtypes(exclude=[np.number]).columns.tolist()
            if non_numeric:
                logger.warning(f"Нечисловые колонки (будут удалены): {non_numeric}")
                X = X.select_dtypes(include=[np.number])
                available_features = list(X.columns)

            # Заполняем пропуски медианой
            missing_counts = X.isnull().sum()
            if missing_counts.sum() > 0:
                logger.info(f"Заполнение пропусков медианой. Пропущено значений: {missing_counts[missing_counts > 0].to_dict()}")
                X = X.fillna(X.median())

            y = df[target]

            # Проверяем что остались данные
            if len(X) == 0 or len(available_features) == 0:
                raise ValueError("После фильтрации не осталось данных или признаков!")

            logger.info(f"Данные подготовлены. X shape: {X.shape}, y shape: {y.shape}")

            # Разделение на train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
            )

            logger.info(f"Train size: {len(X_train):,}, Test size: {len(X_test):,}")

            return X_train, X_test, y_train, y_test, available_features

        except Exception as e:
            logger.error(f"Ошибка подготовки данных: {e}")
            logger.error(traceback.format_exc())
            raise

    def train_models(self, df: pd.DataFrame, target: str = 'popularity') -> Dict:
        """
        МОДЕЛЬ: Обучить модели регрессии популярности

        Обучает две модели:
        1. Linear Regression - базовая линейная модель
        2. Random Forest Regressor - более сложная ансамблевая модель

        Args:
            df: Датафрейм с данными
            target: Целевая переменная

        Returns:
            dict: Результаты обучения с метриками и информацией
        """
        try:
            logger.info("="*60)
            logger.info("Начало обучения моделей регрессии")
            logger.info("="*60)

            # Подготовка данных
            X_train, X_test, y_train, y_test, features = self.prepare_data(df, target)
            self.feature_names = features
            self.X_test = X_test
            self.y_test = y_test

            # ========== Linear Regression ==========
            logger.info("\n[1/2] Обучение Linear Regression...")
            try:
                self.lr_model = LinearRegression()
                self.lr_model.fit(X_train, y_train)
                self.lr_pred = self.lr_model.predict(X_test)

                lr_r2 = r2_score(y_test, self.lr_pred)
                lr_rmse = np.sqrt(mean_squared_error(y_test, self.lr_pred))
                lr_mae = mean_absolute_error(y_test, self.lr_pred)

                logger.info(f"✓ Linear Regression обучена")
                logger.info(f"  R² = {lr_r2:.4f}, RMSE = {lr_rmse:.2f}, MAE = {lr_mae:.2f}")
            except Exception as e:
                logger.error(f"Ошибка обучения Linear Regression: {e}")
                raise

            # ========== Random Forest ==========
            logger.info("\n[2/2] Обучение Random Forest Regressor...")
            try:
                self.rf_model = RandomForestRegressor(
                    n_estimators=N_ESTIMATORS,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                    max_depth=15,
                    min_samples_split=10,
                    min_samples_leaf=4,
                    verbose=0
                )
                self.rf_model.fit(X_train, y_train)
                self.rf_pred = self.rf_model.predict(X_test)

                rf_r2 = r2_score(y_test, self.rf_pred)
                rf_rmse = np.sqrt(mean_squared_error(y_test, self.rf_pred))
                rf_mae = mean_absolute_error(y_test, self.rf_pred)

                logger.info(f"✓ Random Forest обучена")
                logger.info(f"  R² = {rf_r2:.4f}, RMSE = {rf_rmse:.2f}, MAE = {rf_mae:.2f}")
            except Exception as e:
                logger.error(f"Ошибка обучения Random Forest: {e}")
                raise

            # ========== Feature Importance ==========
            feature_importance = dict(zip(features, self.rf_model.feature_importances_.tolist()))

            # Сохраняем метрики
            self.metrics = {
                "linear_regression": {
                    "r2_score": float(lr_r2),
                    "rmse": float(lr_rmse),
                    "mae": float(lr_mae),
                    "coefficients": dict(zip(features, self.lr_model.coef_.tolist()))
                },
                "random_forest": {
                    "r2_score": float(rf_r2),
                    "rmse": float(rf_rmse),
                    "mae": float(rf_mae),
                    "n_estimators": N_ESTIMATORS
                },
                "feature_importance": feature_importance
            }

            # Определяем лучшую модель
            if rf_r2 > lr_r2:
                self.best_model = "Random Forest"
                logger.info(f"\n✓ Random Forest показывает лучший результат (R² = {rf_r2:.4f})")
            else:
                self.best_model = "Linear Regression"
                logger.info(f"\n✓ Linear Regression показывает лучший результат (R² = {lr_r2:.4f})")

            logger.info("="*60)

            improvement = float((rf_r2 - lr_r2) / abs(lr_r2) * 100) if lr_r2 != 0 else 0

            # Возвращаем результаты
            return {
                "status": "success",
                "best_model": self.best_model,
                "metrics": self.metrics,
                "features_used": features,
                "train_size": int(len(X_train)),
                "test_size": int(len(X_test)),
                "improvement": improvement
            }

        except Exception as e:
            logger.error(f"Критическая ошибка обучения модели: {e}")
            logger.error(traceback.format_exc())
            raise

    def get_metrics(self) -> Dict:
        """
        Получить метрики обученных моделей

        Returns:
            dict: Словарь с метриками обеих моделей
        """
        if self.metrics is None:
            raise ValueError("Модели ещё не обучены. Вызовите train_models() сначала.")

        return self.metrics

    def predict(self, features: pd.DataFrame, use_best: bool = True) -> np.ndarray:
        """
        Сделать предсказание на новых данных

        Args:
            features: DataFrame с признаками для предсказания
            use_best: Использовать лучшую модель (True) или Random Forest (False)

        Returns:
            np.ndarray: Массив предсказаний
        """
        if self.rf_model is None:
            raise ValueError("Модели не обучены. Вызовите train_models() сначала.")

        # Выбираем модель
        if use_best:
            if self.best_model == "Random Forest":
                model = self.rf_model
            else:
                model = self.lr_model
        else:
            model = self.rf_model

        # Убеждаемся что все нужные признаки присутствуют
        if self.feature_names:
            missing_features = set(self.feature_names) - set(features.columns)
            if missing_features:
                raise ValueError(f"Отсутствуют признаки: {missing_features}")

            features = features[self.feature_names]

        # Заполняем пропуски
        features = features.fillna(features.median())

        return model.predict(features)

    def get_feature_importance(self, top_n: int = 10) -> Dict:
        """
        Получить важность признаков из Random Forest

        Args:
            top_n: Количество топ признаков

        Returns:
            dict: Словарь с важностью признаков
        """
        if self.metrics is None or 'feature_importance' not in self.metrics:
            raise ValueError("Модель не обучена или feature importance недоступна")

        # Сортируем по важности
        importance = self.metrics['feature_importance']
        sorted_importance = dict(sorted(importance.items(),
                                        key=lambda x: x[1],
                                        reverse=True)[:top_n])

        return {
            "top_features": sorted_importance,
            "all_features": importance
        }

    def get_predictions(self) -> Dict:
        """
        Получить предсказания моделей на тестовой выборке
        (для построения графиков сравнения)

        Returns:
            dict: Словарь с истинными значениями и предсказаниями
        """
        if self.y_test is None or self.lr_pred is None or self.rf_pred is None:
            raise ValueError("Модели не обучены")

        return {
            "y_true": self.y_test.tolist() if hasattr(self.y_test, 'tolist') else list(self.y_test),
            "y_pred_lr": self.lr_pred.tolist(),
            "y_pred_rf": self.rf_pred.tolist()
        }

    def evaluate_model(self, model_name: str = "random_forest") -> Dict:
        """
        Получить детальную оценку модели

        Args:
            model_name: Название модели ("linear_regression" или "random_forest")

        Returns:
            dict: Детальная информация о модели
        """
        if self.metrics is None:
            raise ValueError("Модели не обучены")

        if model_name not in self.metrics:
            raise ValueError(f"Модель '{model_name}' не найдена")

        return {
            "model": model_name,
            "metrics": self.metrics[model_name],
            "is_best": (self.best_model.lower().replace(" ", "_") == model_name),
            "features_count": len(self.feature_names) if self.feature_names else 0
        }

    # ========== НОВЫЕ МЕТОДЫ ДЛЯ ПРЕДСКАЗАНИЯ ==========

    def is_trained(self) -> bool:
        """
        Проверить, обучена ли модель

        Returns:
            bool: True если модель обучена
        """
        return self.rf_model is not None and self.metrics is not None

    def predict_single(self, features: Dict) -> Dict:
        """
        Предсказать популярность для одного трека

        Args:
            features: Словарь с аудио-характеристиками

        Returns:
            dict: Результат предсказания с интерпретацией
        """
        if not self.is_trained():
            raise ValueError("Модель не обучена")

        # Проверяем что все нужные признаки присутствуют
        if not self.feature_names:
            raise ValueError("Список признаков не определён")

        # Создаём DataFrame из входных данных
        input_df = pd.DataFrame([features])

        # Проверяем наличие всех признаков
        missing_features = set(self.feature_names) - set(input_df.columns)
        if missing_features:
            raise ValueError(f"Отсутствуют признаки: {missing_features}")

        # Выбираем только нужные признаки в правильном порядке
        input_df = input_df[self.feature_names]

        # Заполняем возможные NaN медианой (на всякий случай)
        input_df = input_df.fillna(input_df.median())

        # Делаем предсказание лучшей моделью
        if self.best_model == "Random Forest":
            prediction = self.rf_model.predict(input_df)[0]
            model_used = "Random Forest"
        else:
            prediction = self.lr_model.predict(input_df)[0]
            model_used = "Linear Regression"

        # Ограничиваем значение от 0 до 100
        prediction = float(max(0, min(100, prediction)))

        logger.info(f"Предсказание для трека: {prediction:.2f} (модель: {model_used})")

        return {
            "predicted_popularity": prediction,
            "model_used": model_used,
            "feature_importance": self.metrics.get('feature_importance', {}),
            "input_features": features
        }


# Глобальный экземпляр сервиса
model_service = ModelService()