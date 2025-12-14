"""
Скрипт для проверки корректности установки проекта

Запуск: python scripts/check_setup.py
"""

import sys
from pathlib import Path
import importlib

# Добавляем корневую папку в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro}")
        print("   ⚠ Требуется Python 3.8 или выше")
        return False


def check_libraries():
    """Проверка установленных библиотек"""
    print("\n📦 Проверка библиотек...")

    required_libs = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn',
        'sklearn': 'Scikit-learn'
    }

    all_installed = True

    for lib_name, display_name in required_libs.items():
        try:
            lib = importlib.import_module(lib_name)
            version = getattr(lib, '__version__', 'unknown')
            print(f"   ✓ {display_name:15s} {version}")
        except ImportError:
            print(f"   ✗ {display_name:15s} НЕ УСТАНОВЛЕН")
            all_installed = False

    return all_installed


def check_directory_structure():
    """Проверка структуры папок"""
    print("\n📁 Проверка структуры проекта...")

    base_path = Path(__file__).parent.parent

    required_dirs = [
        'backend',
        'backend/api',
        'backend/api/routes',
        'backend/services',
        'frontend',
        'frontend/css',
        'frontend/js',
        'frontend/js/components',
        'data',
        'scripts',
        'docs',
        'plots'
    ]

    all_exist = True

    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists():
            print(f"   ✓ {dir_path}")
        else:
            print(f"   ✗ {dir_path} - НЕ НАЙДЕНА")
            all_exist = False

    return all_exist


def check_backend_files():
    """Проверка файлов backend"""
    print("\n🔧 Проверка файлов backend...")

    base_path = Path(__file__).parent.parent / 'backend'

    required_files = [
        'config.py',
        'requirements.txt',
        'api/main.py',
        'api/routes/data.py',
        'api/routes/analysis.py',
        'api/routes/plots.py',
        'api/routes/model.py',
        'services/data_service.py',
        'services/analysis_service.py',
        'services/plot_service.py',
        'services/model_service.py'
    ]

    all_exist = True

    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"   ✓ {file_path:40s} ({size:,} bytes)")
        else:
            print(f"   ✗ {file_path:40s} - НЕ НАЙДЕН")
            all_exist = False

    return all_exist


def check_frontend_files():
    """Проверка файлов frontend"""
    print("\n🎨 Проверка файлов frontend...")

    base_path = Path(__file__).parent.parent / 'frontend'

    required_files = [
        'index.html',
        'css/main.css',
        'css/components.css',
        'js/config.js',
        'js/api.js',
        'js/utils.js',
        'js/main.js',
        'js/components/dataInfo.js',
        'js/components/distributions.js',
        'js/components/correlations.js',
        'js/components/genres.js',
        'js/components/plots.js',
        'js/components/model.js'
    ]

    all_exist = True

    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"   ✓ {file_path:40s} ({size:,} bytes)")
        else:
            print(f"   ✗ {file_path:40s} - НЕ НАЙДЕН")
            all_exist = False

    return all_exist


def check_dataset():
    """Проверка датасета"""
    print("\n📊 Проверка датасета...")

    dataset_path = Path(__file__).parent.parent / 'data' / 'SpotifyFeatures.csv'

    if dataset_path.exists():
        size_mb = dataset_path.stat().st_size / (1024 * 1024)
        print(f"   ✓ SpotifyFeatures.csv найден ({size_mb:.1f} MB)")

        # Попробуем загрузить датасет
        try:
            import pandas as pd
            df = pd.read_csv(dataset_path)
            print(f"   ✓ Датасет корректен: {df.shape[0]:,} строк × {df.shape[1]} колонок")
            return True
        except Exception as e:
            print(f"   ✗ Ошибка чтения датасета: {e}")
            return False
    else:
        print(f"   ✗ SpotifyFeatures.csv НЕ НАЙДЕН в папке data/")
        print(f"   ⚠ Скачайте датасет с Kaggle:")
        print(f"      https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db")
        return False


def check_imports():
    """Проверка импортов проекта"""
    print("\n🔗 Проверка импортов проекта...")

    all_ok = True

    try:
        from backend.config import API_TITLE
        print(f"   ✓ backend.config")
    except Exception as e:
        print(f"   ✗ backend.config: {e}")
        all_ok = False

    try:
        from backend.services.data_service import data_service
        print(f"   ✓ backend.services.data_service")
    except Exception as e:
        print(f"   ✗ backend.services.data_service: {e}")
        all_ok = False

    try:
        from backend.services.analysis_service import analysis_service
        print(f"   ✓ backend.services.analysis_service")
    except Exception as e:
        print(f"   ✗ backend.services.analysis_service: {e}")
        all_ok = False

    try:
        from backend.services.plot_service import plot_service
        print(f"   ✓ backend.services.plot_service")
    except Exception as e:
        print(f"   ✗ backend.services.plot_service: {e}")
        all_ok = False

    try:
        from backend.services.model_service import model_service
        print(f"   ✓ backend.services.model_service")
    except Exception as e:
        print(f"   ✗ backend.services.model_service: {e}")
        all_ok = False

    return all_ok


def main():
    """Главная функция"""
    print("="*70)
    print("🔍 ПРОВЕРКА УСТАНОВКИ SPOTIFY ANALYSIS")
    print("="*70)

    results = {
        "Python версия": check_python_version(),
        "Библиотеки": check_libraries(),
        "Структура папок": check_directory_structure(),
        "Backend файлы": check_backend_files(),
        "Frontend файлы": check_frontend_files(),
        "Датасет": check_dataset(),
        "Импорты": check_imports()
    }

    print("\n" + "="*70)
    print("📋 ИТОГОВЫЙ ОТЧЁТ")
    print("="*70)

    all_passed = True
    for check_name, passed in results.items():
        status = "✓ ПРОЙДЕНО" if passed else "✗ НЕ ПРОЙДЕНО"
        print(f"  {check_name:20s}: {status}")
        if not passed:
            all_passed = False

    print("="*70)

    if all_passed:
        print("\n✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("\n🚀 Готов к запуску:")
        print("  Backend:  cd backend && uvicorn api.main:app --reload")
        print("  Frontend: cd frontend && python -m http.server 8080")
    else:
        print("\n⚠️  НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ")
        print("\n📖 Смотрите инструкции:")
        print("  SETUP.md - для детальной установки")
        print("  QUICKSTART.md - для быстрого старта")

    print("="*70)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)