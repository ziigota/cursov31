/**
 * Компонент для работы с моделью ML
 */

const ModelComponent = {
    /**
     * Обучить модель
     */
    async train() {
        const loadingId = 'loading-model';
        const resultId = 'model-result';

        // Показываем загрузку
        Utils.showLoading(loadingId);

        // Очищаем предыдущие результаты
        $(`#${resultId}`).html('');

        // Показываем прогресс
        this._showTrainingProgress();

        try {
            // ВАЖНО: увеличенный таймаут для обучения (2 минуты)
            const result = await $.ajax({
                url: `${CONFIG.API_URL}/model/train`,
                method: 'POST',
                timeout: 120000,  // 2 минуты (было 3 секунды!)
                dataType: 'json'
            });

            if (result.status === 'success') {
                this.render(result);
            } else {
                throw new Error('Ошибка обучения модели');
            }

        } catch (error) {
            console.error('Ошибка обучения:', error);

            let errorMessage = 'Не удалось обучить модель';

            if (error.statusText === 'timeout') {
                errorMessage = 'Превышено время ожидания. Попробуйте ещё раз.';
            } else if (error.responseJSON && error.responseJSON.detail) {
                errorMessage = error.responseJSON.detail;
            } else if (error.message) {
                errorMessage = error.message;
            }

            Utils.showError(resultId, errorMessage);
        } finally {
            Utils.hideLoading(loadingId);
        }
    },

    /**
     * Показать прогресс обучения
     */
    _showTrainingProgress() {
        const html = `
            <div class="result" style="text-align: center; padding: 30px;">
                <div style="font-size: 48px; margin-bottom: 20px;">🤖</div>
                <h3 style="color: #667eea; margin-bottom: 15px;">Обучение модели...</h3>
                <p style="color: #666; margin-bottom: 20px;">
                    Это может занять <strong>1-2 минуты</strong>.<br>
                    Модель анализирует 230,000+ треков!
                </p>
                <div style="background: #e0e0e0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div class="progress-bar-animated" style="
                        background: linear-gradient(90deg, #1DB954 0%, #1ed760 100%);
                        height: 100%;
                        width: 0%;
                        animation: progress 90s linear;
                    "></div>
                </div>
                <p style="color: #999; margin-top: 15px; font-size: 0.9em;">
                    Не закрывайте эту страницу...
                </p>
            </div>
            <style>
                @keyframes progress {
                    0% { width: 0%; }
                    100% { width: 95%; }
                }
            </style>
        `;

        $('#model-result').html(html);
    },

    /**
     * Загрузить метрики
     */
    async loadMetrics() {
        try {
            const result = await $.ajax({
                url: `${CONFIG.API_URL}/model/metrics`,
                method: 'GET',
                timeout: 10000
            });

            // Просто прокручиваем к результату, если он есть
            Utils.scrollToElement('model-result');

        } catch (error) {
            if (error.status === 404 || (error.responseJSON && error.responseJSON.detail)) {
                alert('❌ Модель ещё не обучена!\n\nСначала нажмите кнопку "Обучить модель" и подождите 1-2 минуты.');
            } else {
                alert('Ошибка получения метрик: ' + (error.statusText || 'Неизвестная ошибка'));
            }
        }
    },

    /**
     * Отобразить результаты обучения
     */
    render(data) {
        let html = '<div class="result">';

        // Заголовок с анимацией
        html += `
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 64px; margin-bottom: 10px;">✅</div>
                <h3 style="color: #4caf50; font-size: 1.8em;">Модель успешно обучена!</h3>
                <p style="color: #666; margin-top: 10px;">
                    Лучшая модель: <strong>${data.best_model}</strong>
                </p>
            </div>
        `;

        // Метрики моделей
        html += '<div class="metrics-container" style="margin-top: 20px;">';

        // Linear Regression
        const lr = data.metrics.linear_regression;
        html += `
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h3>📊 Linear Regression</h3>
                <div class="metric-label">R² Score (точность)</div>
                <div class="metric-value">${Utils.formatNumber(lr.r2_score, 4)}</div>
                <div class="metric-label" style="margin-top: 10px;">RMSE: ${Utils.formatNumber(lr.rmse, 2)}</div>
                <div class="metric-label">MAE: ${Utils.formatNumber(lr.mae, 2)}</div>
                ${data.best_model === 'Linear Regression' ? '<div style="margin-top: 10px; font-size: 24px;">🏆</div>' : ''}
            </div>
        `;

        // Random Forest
        const rf = data.metrics.random_forest;
        html += `
            <div class="metric-card" style="background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);">
                <h3>🌲 Random Forest</h3>
                <div class="metric-label">R² Score (точность)</div>
                <div class="metric-value">${Utils.formatNumber(rf.r2_score, 4)}</div>
                <div class="metric-label" style="margin-top: 10px;">RMSE: ${Utils.formatNumber(rf.rmse, 2)}</div>
                <div class="metric-label">MAE: ${Utils.formatNumber(rf.mae, 2)}</div>
                ${data.best_model === 'Random Forest' ? '<div style="margin-top: 10px; font-size: 24px;">🏆</div>' : ''}
            </div>
        `;

        html += '</div>';

        // Что означают метрики
        html += `
            <div style="margin-top: 30px; padding: 20px; background: #e8f5e9; border-radius: 10px; border-left: 4px solid #4caf50;">
                <h4 style="color: #2e7d32; margin-bottom: 15px;">📖 Что означают метрики:</h4>
                <ul style="color: #2e7d32; line-height: 1.8; margin-left: 20px;">
                    <li><strong>R² Score:</strong> Показывает точность модели (0 = плохо, 1 = отлично). 
                        Ваш результат <strong>${Utils.formatNumber(rf.r2_score, 2)}</strong> означает, что модель объясняет 
                        <strong>${Utils.formatNumber(rf.r2_score * 100, 0)}%</strong> популярности треков.</li>
                    <li><strong>RMSE:</strong> Средняя ошибка предсказания. Чем меньше - тем лучше.</li>
                    <li><strong>MAE:</strong> Средняя абсолютная ошибка. Тоже чем меньше - тем лучше.</li>
                </ul>
            </div>
        `;

        // Feature Importance
        html += '<div class="feature-importance" style="margin-top: 30px;">';
        html += '<h3 style="color: #333;">🎯 Какие характеристики важнее всего?</h3>';
        html += '<p style="color: #666; margin: 10px 0 20px;">Модель определила, что эти характеристики больше всего влияют на популярность:</p>';

        const features = Object.entries(data.metrics.feature_importance)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);

        const maxImportance = features[0][1];

        features.forEach(([feature, importance], index) => {
            const emoji = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}.`;
            html += `
                <div class="feature-bar">
                    <div class="feature-name">${emoji} ${feature}</div>
                    ${Utils.createFeatureBar(feature, importance, maxImportance).replace('<div class="feature-bar">', '').replace('</div>', '')}
                </div>
            `;
        });

        html += '</div>';

        // Дополнительная информация
        html += `
            <div style="margin-top: 30px; padding: 20px; background: #fff3cd; border-radius: 10px; border-left: 4px solid #ffc107;">
                <h4 style="color: #856404; margin-bottom: 15px;">ℹ️ Информация об обучении:</h4>
                <div style="color: #856404; line-height: 1.8;">
                    <p><strong>✅ Обучено на:</strong> ${data.train_size.toLocaleString()} треках</p>
                    <p><strong>✅ Протестировано на:</strong> ${data.test_size.toLocaleString()} треках</p>
                    <p><strong>✅ Использовано признаков:</strong> ${data.features_used.length}</p>
                    <p><strong>✅ Улучшение Random Forest:</strong> +${Utils.formatNumber(data.improvement, 1)}% по сравнению с Linear Regression</p>
                </div>
            </div>
        `;

        // Что дальше
        html += `
            <div style="margin-top: 30px; padding: 20px; background: #e3f2fd; border-radius: 10px; border-left: 4px solid #2196f3;">
                <h4 style="color: #1565c0; margin-bottom: 15px;">💡 Выводы:</h4>
                <ul style="color: #1565c0; line-height: 1.8; margin-left: 20px;">
                    <li>Модель обучена и может предсказывать популярность треков</li>
                    <li>Самые важные признаки: <strong>${features[0][0]}</strong>, <strong>${features[1][0]}</strong>, <strong>${features[2][0]}</strong></li>
                    <li>Точность ${Utils.formatNumber(rf.r2_score * 100, 0)}% говорит о том, что популярность зависит не только от аудио-характеристик</li>
                    <li>Другие факторы: имя артиста, маркетинг, тренды, плейлисты</li>
                </ul>
            </div>
        `;

        html += '</div>';

        $('#model-result').html(html);

        // Плавная прокрутка к результату
        setTimeout(() => {
            Utils.scrollToElement('model-result');
        }, 300);
    }
};

window.ModelComponent = ModelComponent;