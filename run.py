"""
Скрипт для быстрого запуска backend сервера

Запуск из корневой папки проекта:
python run.py

Или из папки backend:
cd backend && python run.py
"""

import sys
from pathlib import Path

# Определяем, откуда запущен скрипт
current_dir = Path(__file__).parent
if current_dir.name == 'backend':
    # Запущен из папки backend
    sys.path.insert(0, str(current_dir))
else:
    # Запущен из корня проекта
    sys.path.insert(0, str(current_dir / 'backend'))

import uvicorn

if __name__ == "__main__":
    print("="*60)
    print("🎵 Запуск Spotify Analysis API")
    print("="*60)
    print("\n📍 Backend будет доступен на:")
    print("   http://localhost:8000")
    print("   http://127.0.0.1:8000")
    print("\n📚 Документация:")
    print("   Swagger UI: http://localhost:8000/docs")
    print("   ReDoc:      http://localhost:8000/redoc")
    print("\n🌐 Frontend запустите в другом терминале:")
    print("   cd frontend")
    print("   python -m http.server 8080")
    print("   Откройте: http://localhost:8080")
    print("\n⏸  Остановка: Ctrl+C")
    print("="*60 + "\n")

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )