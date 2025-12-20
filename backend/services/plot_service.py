
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend без GUI
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import base64
from io import BytesIO
from typing import Tuple
import warnings
warnings.filterwarnings('ignore')


class PlotService:

    @staticmethod
    def _fig_to_base64(fig: plt.Figure) -> str:

        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

    @staticmethod
    def create_scatter_plot(df: pd.DataFrame, x: str, y: str,
                            sample_size: int = 5000) -> str:

        if x not in df.columns or y not in df.columns:
            raise ValueError(f"Колонки '{x}' или '{y}' не найдены в датасете")

        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(12, 8))

        # Берём случайную выборку для лучшей визуализации
        sample_df = df.sample(min(sample_size, len(df)), random_state=42)

        # Создаём scatter plot с градиентом цвета
        scatter = ax.scatter(
            sample_df[x],
            sample_df[y],
            alpha=0.5,
            c=sample_df[y],
            cmap='viridis',
            s=30,
            edgecolors='none'
        )

        # Добавляем линию тренда
        z = np.polyfit(sample_df[x].dropna(), sample_df[y].dropna(), 1)
        p = np.poly1d(z)
        x_sorted = np.sort(sample_df[x].dropna())
        ax.plot(x_sorted, p(x_sorted), "r--", alpha=0.8, linewidth=2, label='Тренд')

        # Настройка графика
        ax.set_xlabel(x.replace('_', ' ').title(), fontsize=14, fontweight='bold')
        ax.set_ylabel(y.replace('_', ' ').title(), fontsize=14, fontweight='bold')
        ax.set_title(f'Зависимость {y} от {x}', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Добавляем colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label(y.replace('_', ' ').title(), fontsize=12)

        plt.tight_layout()

        return PlotService._fig_to_base64(fig)

    @staticmethod
    def create_histogram(df: pd.DataFrame, column: str, bins: int = 50) -> str:

        if column not in df.columns:
            raise ValueError(f"Колонка '{column}' не найдена в датасете")

        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(12, 8))

        # Данные без пропусков
        data = df[column].dropna()

        # Создаём гистограмму
        n, bins_edges, patches = ax.hist(
            data,
            bins=bins,
            color='steelblue',
            edgecolor='black',
            alpha=0.7,
            linewidth=1.2
        )

        # Вычисляем статистики
        mean_val = data.mean()
        median_val = data.median()
        std_val = data.std()

        # Добавляем вертикальные линии для статистик
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5,
                   label=f'Среднее: {mean_val:.2f}')
        ax.axvline(median_val, color='green', linestyle='--', linewidth=2.5,
                   label=f'Медиана: {median_val:.2f}')

        # Добавляем область ±1 стандартное отклонение
        ax.axvspan(mean_val - std_val, mean_val + std_val,
                   alpha=0.2, color='yellow', label=f'±1σ ({std_val:.2f})')

        # Настройка графика
        ax.set_xlabel(column.replace('_', ' ').title(), fontsize=14, fontweight='bold')
        ax.set_ylabel('Количество треков', fontsize=14, fontweight='bold')
        ax.set_title(f'Распределение {column}', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend(fontsize=11, loc='upper right')

        # Добавляем текст со статистикой
        stats_text = f'n = {len(data):,}\nμ = {mean_val:.2f}\nσ = {std_val:.2f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=10, family='monospace')

        plt.tight_layout()

        return PlotService._fig_to_base64(fig)

    @staticmethod
    def create_heatmap(corr_matrix: pd.DataFrame) -> str:
        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(14, 12))

        # Создаём маску для верхнего треугольника (чтобы не дублировать)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        # Создаём heatmap
        sns.heatmap(
            corr_matrix,
            mask=mask,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8, "label": "Корреляция"},
            vmin=-1,
            vmax=1,
            ax=ax
        )

        # Настройка графика
        ax.set_title('Корреляционная матрица аудио-характеристик',
                     fontsize=16, fontweight='bold', pad=20)

        # Поворачиваем метки для лучшей читаемости
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)

        plt.tight_layout()

        return PlotService._fig_to_base64(fig)

    @staticmethod
    def create_feature_importance_plot(features: list, importances: list,
                                       top_n: int = 10) -> str:

        # Создаём DataFrame
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)

        # Создаём фигуру
        fig, ax = plt.subplots(figsize=(12, 8))

        # Горизонтальный bar plot
        bars = ax.barh(
            importance_df['feature'][::-1],
            importance_df['importance'][::-1],
            color='steelblue',
            edgecolor='black',
            linewidth=1.2
        )

        # Добавляем значения на столбцах
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                    f'{width:.4f}',
                    ha='left', va='center', fontsize=10, fontweight='bold')

        # Настройка графика
        ax.set_xlabel('Важность признака', fontsize=14, fontweight='bold')
        ax.set_ylabel('Признак', fontsize=14, fontweight='bold')
        ax.set_title(f'Топ-{top_n} важных признаков (Random Forest)',
                     fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='x')

        plt.tight_layout()

        return PlotService._fig_to_base64(fig)

    @staticmethod
    def create_comparison_plot(y_true, y_pred_lr, y_pred_rf,
                               sample_size: int = 1000) -> str:

        # Создаём фигуру с двумя подграфиками
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

        # Случайная выборка
        indices = np.random.choice(len(y_true), min(sample_size, len(y_true)), replace=False)
        y_true_sample = y_true.iloc[indices] if hasattr(y_true, 'iloc') else y_true[indices]
        y_pred_lr_sample = y_pred_lr[indices]
        y_pred_rf_sample = y_pred_rf[indices]

        # Linear Regression
        ax1.scatter(y_true_sample, y_pred_lr_sample, alpha=0.3, s=20)
        ax1.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
                 'r--', lw=2, label='Идеальное предсказание')
        ax1.set_xlabel('Реальная популярность', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Предсказанная популярность', fontsize=12, fontweight='bold')
        ax1.set_title('Linear Regression', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Random Forest
        ax2.scatter(y_true_sample, y_pred_rf_sample, alpha=0.3, s=20, color='green')
        ax2.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
                 'r--', lw=2, label='Идеальное предсказание')
        ax2.set_xlabel('Реальная популярность', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Предсказанная популярность', fontsize=12, fontweight='bold')
        ax2.set_title('Random Forest', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()

        return PlotService._fig_to_base64(fig)


# Глобальный экземпляр сервиса
plot_service = PlotService()