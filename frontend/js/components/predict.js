/**
 * Компонент для предсказания популярности трека
 * С улучшенным UI: минуты/секунды, текстовые ноты, мажор/минор
 */

const PredictComponent = {
    // Конфигурация признаков (только те, что используются в модели!)
    features: {
        'danceability': { min: 0.0, max: 1.0, step: 0.01, default: 0.5, label: 'Танцевальность', unit: '' },
        'energy': { min: 0.0, max: 1.0, step: 0.01, default: 0.7, label: 'Энергичность', unit: '' },
        'loudness': { min: -60, max: 0, step: 0.1, default: -6, label: 'Громкость', unit: 'dB' },
        'speechiness': { min: 0.0, max: 1.0, step: 0.01, default: 0.05, label: 'Речевой контент', unit: '' },
        'acousticness': { min: 0.0, max: 1.0, step: 0.01, default: 0.2, label: 'Акустичность', unit: '' },
        'instrumentalness': { min: 0.0, max: 1.0, step: 0.01, default: 0.1, label: 'Инструментальность', unit: '' },
        'liveness': { min: 0.0, max: 1.0, step: 0.01, default: 0.15, label: 'Живое выступление', unit: '' },
        'valence': { min: 0.0, max: 1.0, step: 0.01, default: 0.5, label: 'Позитивность', unit: '' },
        'tempo': { min: 0, max: 250, step: 1, default: 120, label: 'Темп', unit: 'BPM' },
        'duration_ms': { min: 30000, max: 600000, step: 1000, default: 200000, label: 'Длительность', unit: 'мс' }
    },

    /**
     * Показать форму (вызывается после обучения модели)
     */
    showForm() {
        const container = $('#predict-form-container');

        let html = '<form id="predict-form" class="predict-form">';
        html += '<div class="features-grid">';

        // Создаём поля для каждого признака
        for (const [name, config] of Object.entries(this.features)) {
            if (name === 'duration_ms') {
                html += this.createDurationInput();
            } else {
                html += this.createFeatureInput(name, config);
            }
        }

        html += '</div>';

        // Кнопки
        html += '<div class="predict-buttons">';
        html += '<button type="submit" class="button">Предсказать популярность</button>';
        html += '<button type="button" class="button" onclick="PredictComponent.resetForm()">Сбросить значения</button>';
        html += '</div>';

        html += '</form>';

        // Контейнер для результата
        html += '<div id="predict-result" style="margin-top: 30px;"></div>';

        container.html(html);

        // Привязываем обработчик формы
        $('#predict-form').on('submit', (e) => {
            e.preventDefault();
            this.makePrediction();
        });

        // Привязываем обработчики для всех input
        $('.feature-input').on('input change', function() {
            PredictComponent.validateInput(this);
        });

        // Обработчики для минут/секунд
        $('#input-minutes, #input-seconds').on('input change', function() {
            PredictComponent.updateDurationFromMinSec();
        });

        // Инициализируем минуты/секунды из значения по умолчанию
        this.updateMinSecFromDuration(200000);
    },

    /**
     * Создать специальное поле для длительности (минуты + секунды)
     */
    createDurationInput() {
        return `
            <div class="feature-field">
                <label class="feature-label">
                    Длительность
                    <span class="feature-range">(от 30 сек до 10 мин)</span>
                </label>
                <div class="duration-inputs">
                    <div class="duration-group">
                        <input 
                            type="number" 
                            id="input-minutes"
                            class="feature-input duration-input"
                            value="3" 
                            min="0" 
                            max="10"
                            step="1"
                        />
                        <span class="duration-label">мин</span>
                    </div>
                    <div class="duration-group">
                        <input 
                            type="number" 
                            id="input-seconds"
                            class="feature-input duration-input"
                            value="20" 
                            min="0" 
                            max="59"
                            step="1"
                        />
                        <span class="duration-label">сек</span>
                    </div>
                </div>
                <input type="hidden" id="input-duration_ms" name="duration_ms" value="200000" />
                <div id="warning-duration_ms" class="input-warning"></div>
            </div>
        `;
    },

    /**
     * Обновить duration_ms из минут и секунд
     */
    updateDurationFromMinSec() {
        const minutes = parseInt($('#input-minutes').val()) || 0;
        const seconds = parseInt($('#input-seconds').val()) || 0;

        // Валидация
        if (minutes < 0) $('#input-minutes').val(0);
        if (minutes > 10) $('#input-minutes').val(10);
        if (seconds < 0) $('#input-seconds').val(0);
        if (seconds > 59) $('#input-seconds').val(59);

        // Конвертируем в миллисекунды
        const totalMs = (minutes * 60 + seconds) * 1000;

        // Проверяем границы
        if (totalMs < 30000) {
            // Минимум 30 секунд
            $('#input-minutes').val(0);
            $('#input-seconds').val(30);
            $('#input-duration_ms').val(30000);
            this.showDurationWarning('Минимум: 30 секунд');
        } else if (totalMs > 600000) {
            // Максимум 10 минут
            $('#input-minutes').val(10);
            $('#input-seconds').val(0);
            $('#input-duration_ms').val(600000);
            this.showDurationWarning('Максимум: 10 минут');
        } else {
            $('#input-duration_ms').val(totalMs);
        }
    },

    /**
     * Обновить минуты/секунды из duration_ms
     */
    updateMinSecFromDuration(durationMs) {
        const totalSeconds = Math.floor(durationMs / 1000);
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;

        $('#input-minutes').val(minutes);
        $('#input-seconds').val(seconds);
    },

    /**
     * Показать предупреждение для длительности
     */
    showDurationWarning(message) {
        const warning = $('#warning-duration_ms');
        warning.text(message).addClass('warning-show');
        setTimeout(() => {
            warning.removeClass('warning-show');
        }, 2000);
    },

    /**
     * Создать обычное поле ввода
     */
    createFeatureInput(name, config) {
        const inputId = `input-${name}`;
        const warningId = `warning-${name}`;

        return `
            <div class="feature-field">
                <label for="${inputId}" class="feature-label">
                    ${config.label}
                    <span class="feature-range">(${config.min} - ${config.max}${config.unit ? ' ' + config.unit : ''})</span>
                </label>
                <div class="input-wrapper">
                    <input 
                        type="number" 
                        id="${inputId}" 
                        name="${name}"
                        class="feature-input"
                        value="${config.default}" 
                        min="${config.min}" 
                        max="${config.max}" 
                        step="${config.step}"
                        data-min="${config.min}"
                        data-max="${config.max}"
                    />
                    <span class="input-unit">${config.unit}</span>
                </div>
                <div id="${warningId}" class="input-warning"></div>
            </div>
        `;
    },

    /**
     * Валидация ввода
     */
    validateInput(input) {
        const $input = $(input);
        const value = parseFloat($input.val());
        const min = parseFloat($input.data('min'));
        const max = parseFloat($input.data('max'));
        const name = $input.attr('name');
        const warningId = `#warning-${name}`;

        // Убираем предыдущее предупреждение
        $(warningId).text('').removeClass('warning-show');
        $input.removeClass('input-error');

        if (isNaN(value)) {
            return;
        }

        // Проверка минимума
        if (value < min) {
            $input.val(min);
            $(warningId).text(`Минимальное значение: ${min}`).addClass('warning-show');
            $input.addClass('input-error');
            setTimeout(() => {
                $(warningId).removeClass('warning-show');
                $input.removeClass('input-error');
            }, 2000);
        }

        // Проверка максимума
        if (value > max) {
            $input.val(max);
            $(warningId).text(`Максимальное значение: ${max}`).addClass('warning-show');
            $input.addClass('input-error');
            setTimeout(() => {
                $(warningId).removeClass('warning-show');
                $input.removeClass('input-error');
            }, 2000);
        }
    },

    /**
     * Сбросить форму к значениям по умолчанию
     */
    resetForm() {
        for (const [name, config] of Object.entries(this.features)) {
            if (name === 'duration_ms') {
                this.updateMinSecFromDuration(config.default);
                $(`#input-${name}`).val(config.default);
            } else {
                $(`#input-${name}`).val(config.default);
            }
        }
        $('#predict-result').html('');
    },

    /**
     * Собрать данные из формы
     */
    getFormData() {
        const data = {};

        for (const name in this.features) {
            const value = parseFloat($(`#input-${name}`).val());
            data[name] = value;
        }

        return data;
    },

    /**
     * Сделать предсказание
     */
    async makePrediction() {
        const resultContainer = $('#predict-result');

        // Показываем загрузку
        resultContainer.html(`
            <div class="loading active">
                <div class="spinner"></div>
                <p>Предсказываем популярность...</p>
            </div>
        `);

        // Собираем данные
        const features = this.getFormData();

        console.log('Отправляем данные:', features);

        try {
            // Отправляем запрос на backend
            const response = await $.ajax({
                url: `${CONFIG.API_URL}/model/predict`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(features),
                timeout: 10000
            });

            console.log('Получен ответ:', response);

            // Отображаем результат
            this.renderPrediction(response);

        } catch (error) {
            console.error('Ошибка предсказания:', error);

            let errorMessage = 'Не удалось предсказать популярность';

            if (error.status === 404) {
                errorMessage = 'Модель не обучена! Сначала обучите модель в разделе "Модель"';
            } else if (error.responseJSON && error.responseJSON.detail) {
                errorMessage = error.responseJSON.detail;
            } else if (error.statusText) {
                errorMessage = error.statusText;
            }

            resultContainer.html(`
                <div class="result error">
                    <h3 style="color: #000;">Ошибка</h3>
                    <p>${errorMessage}</p>
                    <p style="margin-top: 10px; color: #666; font-size: 0.9em;">
                        Проверьте консоль браузера (F12) для подробностей
                    </p>
                </div>
            `);
        }
    },

    /**
     * Отобразить результат предсказания
     */
    renderPrediction(data) {
        const popularity = data.predicted_popularity;
        const model = data.model_used;

        // Определяем категорию популярности
        let category, categoryClass, interpretation, recommendations;

        if (popularity >= 80) {
            category = 'Очень популярный';
            categoryClass = 'category-very-high';
            interpretation = 'Этот трек имеет характеристики хита! Высокие шансы попасть в топ-чарты.';
            recommendations = [
                'Отличные аудио-характеристики',
                'Подходит для популярных плейлистов',
                'Высокий потенциал для вирусного распространения'
            ];
        } else if (popularity >= 60) {
            category = 'Популярный';
            categoryClass = 'category-high';
            interpretation = 'Трек с хорошими характеристиками. Может стать популярным при правильном продвижении.';
            recommendations = [
                'Хорошие шансы на успех',
                'Рекомендуется добавить в тематические плейлисты',
                'Стоит инвестировать в маркетинг'
            ];
        } else if (popularity >= 40) {
            category = 'Средне популярный';
            categoryClass = 'category-medium';
            interpretation = 'Трек со средними характеристиками. Может найти свою нишу.';
            recommendations = [
                'Подходит для определённой аудитории',
                'Фокус на целевой маркетинг',
                'Возможно стоит улучшить танцевальность или энергичность'
            ];
        } else if (popularity >= 20) {
            category = 'Низкая популярность';
            categoryClass = 'category-low';
            interpretation = 'Трек с характеристиками нишевой музыки.';
            recommendations = [
                'Ориентация на узкую целевую аудиторию',
                'Возможно слишком низкая энергичность или танцевальность',
                'Рассмотрите изменение аранжировки'
            ];
        } else {
            category = 'Очень низкая популярность';
            categoryClass = 'category-very-low';
            interpretation = 'Трек имеет характеристики, нетипичные для популярной музыки.';
            recommendations = [
                'Аудио-характеристики далеки от мейнстрима',
                'Может подойти для специфических жанров (ambient, experimental)',
                'Рекомендуется пересмотреть концепцию трека'
            ];
        }

        let html = '<div class="result">';

        // Основной результат
        html += `
            <div class="prediction-result">
                <div class="prediction-header">
                    <h3>Результат предсказания</h3>
                    <div class="prediction-model">Модель: ${model}</div>
                </div>
                
                <div class="prediction-score ${categoryClass}">
                    <div class="score-label">Предсказанная популярность</div>
                    <div class="score-value">${popularity.toFixed(1)}</div>
                    <div class="score-max">из 100</div>
                    <div class="score-category">${category}</div>
                </div>
                
                <div class="popularity-bar">
                    <div class="popularity-bar-fill" style="width: ${popularity}%"></div>
                </div>
            </div>
        `;

        // Интерпретация
        html += `
            <div class="info-box" style="margin-top: 25px;">
                <h4 style="color: #000; margin-bottom: 10px; font-weight: 900;">Интерпретация:</h4>
                <p>${interpretation}</p>
            </div>
        `;

        // Рекомендации
        html += `
            <div class="info-box" style="margin-top: 20px;">
                <h4 style="color: #000; margin-bottom: 10px; font-weight: 900;">Рекомендации:</h4>
                <ul style="margin-left: 20px; line-height: 1.8;">
        `;

        recommendations.forEach(rec => {
            html += `<li>${rec}</li>`;
        });

        html += `
                </ul>
            </div>
        `;

        // Важные характеристики
        if (data.feature_importance) {
            html += `
                <div class="info-box" style="margin-top: 20px;">
                    <h4 style="color: #000; margin-bottom: 10px; font-weight: 900;">Что влияет на популярность:</h4>
                    <p style="color: #666; font-size: 0.9em; margin-bottom: 10px;">
                        Топ-5 характеристик, которые наиболее важны для модели:
                    </p>
            `;

            const topFeatures = Object.entries(data.feature_importance)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5);

            topFeatures.forEach(([feature, importance], index) => {
                const label = this.features[feature]?.label || feature;
                html += `
                    <div style="margin: 8px 0;">
                        ${index + 1}. <strong>${label}</strong>: ${(importance * 100).toFixed(1)}%
                    </div>
                `;
            });

            html += `</div>`;
        }

        // Disclaimer
        html += `
            <div class="info-box" style="margin-top: 20px; background: #fff3cd; border-left-color: #000;">
                <p style="color: #856404; font-size: 0.9em;">
                    <strong>Важно:</strong> Предсказание основано только на аудио-характеристиках. 
                    Реальная популярность зависит от многих других факторов: известность артиста, 
                    маркетинг, тренды, попадание в плейлисты и т.д.
                </p>
            </div>
        `;

        html += '</div>';

        $('#predict-result').html(html);

        // Плавная прокрутка к результату
        setTimeout(() => {
            Utils.scrollToElement('predict-result');
        }, 300);
    }
};

window.PredictComponent = PredictComponent;