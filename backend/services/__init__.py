# backend/services/__init__.py
"""
Сервисы для бизнес-логики
"""
from .data_service import data_service
from .analysis_service import analysis_service
from .plot_service import plot_service
from .model_service import model_service

__all__ = [
    'data_service',
    'analysis_service',
    'plot_service',
    'model_service'
]