/**
 * Конфигурация frontend приложения
 */

const CONFIG = {
    // API URL
    API_URL: 'http://localhost:8000',

    // Endpoints
    ENDPOINTS: {
        DATA_INFO: '/data/info',
        DISTRIBUTIONS: '/analysis/distributions',
        CORRELATIONS: '/analysis/correlations',
        GENRES: '/analysis/genres',
        SCATTER: '/plots/scatter',
        HISTOGRAM: '/plots/histogram',
        HEATMAP: '/plots/heatmap',
        TRAIN_MODEL: '/model/train',
        MODEL_METRICS: '/model/metrics'
    },

    // UI настройки
    UI: {
        LOADING_DELAY: 300,  // мс
        ANIMATION_DURATION: 500  // мс
    }
};

// Экспорт для использования в других модулях
window.CONFIG = CONFIG;