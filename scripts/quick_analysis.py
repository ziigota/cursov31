"""
Быстрый анализ датасета Spotify БЕЗ веб-интерфейса

Этот скрипт использует уже созданные сервисы из backend/services/
чтобы не дублировать код!

Запуск: python scripts/quick_analysis.py
"""

import sys
from pathlib import Path

# Добавляем корневую папку в путь для импортов
sys.path.insert(0, str(Path(__file__).parent.parent))

import warnings
warnings.filterwarnings('ignore')

# Импортируем наши сервисы
from backend.config import DATASET_PATH, PLOTS_DIR
from backend.services.data_service import data_service
from backend.services.analysis_service import analysis_service
from backend.services.plot_service import plot_service
from backend.services.model_service import model_service

# Для сохранения графиков из base64
import base64
import re

def save_base64_image(base64_string: str, filename: str):
    """Сохранить base64 изображение в файл"""
    # Убираем префикс data:image/png;base64,
    image_data = re.sub('^data:image/.+;base64,', '', base64_string)

    # Декодируем и сохраняем
    with open(PLOTS_DIR / filename, 'wb') as f:
        f.write(base64.b64decode(image_data))


def main():
    """Главная функция для быстрого анализа"""

    print("="*70)
    print("🎵 БЫСТРЫЙ АНАЛИЗ SPOTIFY ТРЕКОВ")
    print("="*70)

    # ==================== 1. ЗАГРУЗКА ДАННЫХ ====================
    print("\n[1/9] 📥 Загрузка датасета...")

    if not DATASET_PATH.exists():
        print(f"❌ ОШИБКА: Файл не найден - {DATASET_PATH}")
        print("\n📥 Скачайте датасет с Kaggle:")
        print("   https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db")
        print("   Поместите SpotifyFeatures.csv в папку data/")
        return

    if not data_service.load_dataset(DATASET_PATH):
        print("❌ Ошибка загрузки датасета")
        return

    df = data_service.get_dataframe()
    info = data_service.get_info()

    print(f"✅ Датасет загружен: {info['rows']:,} строк × {info['columns']} колонок")
    print(f"📊 Признаки: {', '.join(info['features'][:10])}...")

    # ==================== 2. ВОПРОС 1: РАСПРЕДЕЛЕНИЯ ====================
    print("\n[2/9] 📈 ВОПРОС 1: Анализ распределений...")

    distributions = analysis_service.analyze_distributions(df)

    for feature, stats in distributions['distributions'].items():
        print(f"\n  {feature.upper()}:")
        print(f"    Среднее:  {stats['mean']:.2f}")
        print(f"    Медиана:  {stats['median']:.2f}")
        print(f"    Ст.откл.: {stats['std']:.2f}")
        print(f"    Диапазон: {stats['min']:.2f} - {stats['max']:.2f}")

    # ==================== 3. ВОПРОС 2: КОРРЕЛЯЦИИ ====================
    print("\n[3/9] 🔗 ВОПРОС 2: Корреляции с популярностью...")

    correlations = analysis_service.analyze_correlations(df)

    print("\n  ✅ Топ-3 положительные корреляции:")
    for feature, corr in correlations['top_positive'].items():
        print(f"    {feature:20s}: {corr:+.4f}")

    print("\n  ❌ Топ-3 отрицательные корреляции:")
    for feature, corr in correlations['top_negative'].items():
        print(f"    {feature:20s}: {corr:+.4f}")

    # ==================== 4. ВОПРОС 3: ЖАНРЫ ====================
    print("\n[4/9] 🎸 ВОПРОС 3: Анализ жанров...")

    try:
        genres = analysis_service.analyze_genres(df)
        print(f"\n  📊 Найдено жанров: {genres['genre_count']}")
        print(f"  🎵 Всего треков: {genres['total_tracks']:,}")

        print(f"\n  Топ-5 жанров по количеству:")
        for genre in genres['top_genres']:
            count = genres['genre_counts'][genre]
            print(f"    {genre:30s}: {count:6,} треков")
    except ValueError as e:
        print(f"  ⚠️ {e}")

    # ==================== 5. ГРАФИК 1: SCATTER ====================
    print("\n[5/9] 📊 График 1: Scatter plot (темп vs популярность)...")

    scatter_image = plot_service.create_scatter_plot(df, 'tempo', 'popularity')
    save_base64_image(scatter_image, 'scatter_tempo_popularity.png')
    print(f"  ✅ Сохранено: {PLOTS_DIR / 'scatter_tempo_popularity.png'}")

    # ==================== 6. ГРАФИК 2: HISTOGRAM ====================
    print("\n[6/9] 📊 График 2: Histogram (распределение громкости)...")

    histogram_image = plot_service.create_histogram(df, 'loudness')
    save_base64_image(histogram_image, 'histogram_loudness.png')
    print(f"  ✅ Сохранено: {PLOTS_DIR / 'histogram_loudness.png'}")

    # ==================== 7. ГРАФИК 3: HEATMAP ====================
    print("\n[7/9] 📊 График 3: Heatmap (корреляционная матрица)...")

    corr_matrix = analysis_service.get_correlation_matrix(df)
    heatmap_image = plot_service.create_heatmap(corr_matrix)
    save_base64_image(heatmap_image, 'heatmap_correlations.png')
    print(f"  ✅ Сохранено: {PLOTS_DIR / 'heatmap_correlations.png'}")

    # ==================== 8. МОДЕЛЬ: ОБУЧЕНИЕ ====================
    print("\n[8/9] 🤖 Обучение моделей регрессии...")
    print("⏳ Это может занять 1-2 минуты...")

    model_results = model_service.train_models(df)

    print(f"\n  ✅ Обучение завершено!")
    print(f"  🏆 Лучшая модель: {model_results['best_model']}")
    print(f"  📊 Улучшение: {model_results['improvement']:.1f}%")

    print("\n  📈 Метрики Linear Regression:")
    lr_metrics = model_results['metrics']['linear_regression']
    print(f"    R² Score: {lr_metrics['r2_score']:.4f}")
    print(f"    RMSE:     {lr_metrics['rmse']:.2f}")
    print(f"    MAE:      {lr_metrics['mae']:.2f}")

    print("\n  📈 Метрики Random Forest:")
    rf_metrics = model_results['metrics']['random_forest']
    print(f"    R² Score: {rf_metrics['r2_score']:.4f}")
    print(f"    RMSE:     {rf_metrics['rmse']:.2f}")
    print(f"    MAE:      {rf_metrics['mae']:.2f}")

    # Feature Importance
    importance = model_service.get_feature_importance(top_n=10)
    print("\n  🎯 Топ-10 важных признаков:")
    for i, (feature, imp) in enumerate(importance['top_features'].items(), 1):
        bar = '█' * int(imp * 50)
        print(f"    {i:2d}. {feature:20s}: {bar} {imp:.4f}")

    # ==================== 9. ДОПОЛНИТЕЛЬНЫЕ ГРАФИКИ ====================
    print("\n[9/9] 📊 Создание дополнительных графиков...")

    # Feature Importance график
    features_list = list(model_results['features_used'])
    importances_list = [model_results['metrics']['feature_importance'][f] for f in features_list]

    feature_plot = plot_service.create_feature_importance_plot(features_list, importances_list)
    save_base64_image(feature_plot, 'feature_importance.png')
    print(f"  ✅ Сохранено: {PLOTS_DIR / 'feature_importance.png'}")

    # Сравнение предсказаний
    predictions = model_service.get_predictions()
    comparison_plot = plot_service.create_comparison_plot(
        model_service.y_test,
        model_service.lr_pred,
        model_service.rf_pred
    )
    save_base64_image(comparison_plot, 'predictions_comparison.png')
    print(f"  ✅ Сохранено: {PLOTS_DIR / 'predictions_comparison.png'}")

    # ==================== ИТОГИ ====================
    print("\n" + "="*70)
    print("✅ АНАЛИЗ ЗАВЕРШЁН УСПЕШНО!")
    print("="*70)

    print(f"\n📂 Все графики сохранены в: {PLOTS_DIR}")
    print("\n📊 Созданные файлы:")
    print("  1. scatter_tempo_popularity.png   - Scatter plot")
    print("  2. histogram_loudness.png         - Histogram")
    print("  3. heatmap_correlations.png       - Heatmap")
    print("  4. feature_importance.png         - Важность признаков")
    print("  5. predictions_comparison.png     - Сравнение моделей")

    print("\n📝 Краткие выводы:")
    print(f"  • Лучшая модель: {model_results['best_model']}")
    print(f"  • R² Score: {rf_metrics['r2_score']:.4f}")
    print(f"  • Важнейший признак: {list(importance['top_features'].keys())[0]}")

    print("\n🌐 Для веб-интерфейса запустите:")
    print("  Backend:  cd backend && uvicorn api.main:app --reload")
    print("  Frontend: cd frontend && python -m http.server 8080")

    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)