/**
 * API клиент для взаимодействия с backend
 */

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Выполнить GET запрос
     */
    async get(endpoint) {
        try {
            const response = await $.ajax({
                url: `${this.baseURL}${endpoint}`,
                method: 'GET',
                timeout: 30000  // 30 секунд для GET
            });
            return { success: true, data: response };
        } catch (error) {
            console.error(`GET ${endpoint} failed:`, error);
            return { success: false, error: this._handleError(error) };
        }
    }

    /**
     * Выполнить POST запрос
     */
    async post(endpoint, data = {}) {
        try {
            const response = await $.ajax({
                url: `${this.baseURL}${endpoint}`,
                method: 'POST',
                data: JSON.stringify(data),
                contentType: 'application/json',
                timeout: 180000  // 3 МИНУТЫ для обучения модели!
            });
            return { success: true, data: response };
        } catch (error) {
            console.error(`POST ${endpoint} failed:`, error);
            return { success: false, error: this._handleError(error) };
        }
    }

    /**
     * Обработка ошибок
     */
    _handleError(error) {
        if (error.statusText === 'timeout') {
            return 'Превышено время ожидания. Сервер не отвечает или обработка занимает слишком много времени.';
        }
        if (error.responseJSON && error.responseJSON.detail) {
            return error.responseJSON.detail;
        }
        if (error.statusText) {
            return error.statusText;
        }
        if (error.status === 0) {
            return 'Не удалось подключиться к серверу. Убедитесь что backend запущен.';
        }
        return 'Неизвестная ошибка. Проверьте консоль браузера (F12).';
    }

    // Методы для конкретных эндпоинтов

    getDataInfo() {
        return this.get(CONFIG.ENDPOINTS.DATA_INFO);
    }

    getDistributions() {
        return this.get(CONFIG.ENDPOINTS.DISTRIBUTIONS);
    }

    getCorrelations() {
        return this.get(CONFIG.ENDPOINTS.CORRELATIONS);
    }

    getGenres() {
        return this.get(CONFIG.ENDPOINTS.GENRES);
    }

    getScatterPlot() {
        return this.get(CONFIG.ENDPOINTS.SCATTER);
    }

    getHistogram() {
        return this.get(CONFIG.ENDPOINTS.HISTOGRAM);
    }

    getHeatmap() {
        return this.get(CONFIG.ENDPOINTS.HEATMAP);
    }

    trainModel() {
        return this.post(CONFIG.ENDPOINTS.TRAIN_MODEL);
    }

    getModelMetrics() {
        return this.get(CONFIG.ENDPOINTS.MODEL_METRICS);
    }
}

// Создание глобального экземпляра API клиента
window.api = new APIClient(CONFIG.API_URL);