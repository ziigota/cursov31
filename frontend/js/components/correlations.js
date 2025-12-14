/**
 * Компонент для анализа корреляций
 */

const CorrelationsComponent = {
    async load() {
        Utils.showLoading('loading-corr');

        const result = await api.getCorrelations();

        Utils.hideLoading('loading-corr');

        if (!result.success) {
            Utils.showError('correlations-result', result.error);
            return;
        }

        this.render(result.data);
    },

    render(data) {
        let html = '<div class="result">';

        // Топ положительных корреляций
        html += '<h3>✅ Топ положительных корреляций с популярностью:</h3>';
        html += '<div class="stats-grid" style="margin-top: 15px;">';

        for (const [feature, value] of Object.entries(data.top_positive)) {
            const color = value > 0 ? '#4caf50' : '#f44336';
            html += `
                <div class="stat-card">
                    <h3>${feature}</h3>
                    <div class="metric-value" style="color: ${color}; font-size: 1.8em;">
                        ${Utils.formatNumber(value, 4)}
                    </div>
                    <div class="stat-label">Корреляция</div>
                </div>
            `;
        }

        html += '</div>';

        // Топ отрицательных корреляций
        html += '<h3 style="margin-top: 30px;">❌ Топ отрицательных корреляций:</h3>';
        html += '<div class="stats-grid" style="margin-top: 15px;">';

        for (const [feature, value] of Object.entries(data.top_negative)) {
            const color = value > 0 ? '#4caf50' : '#f44336';
            html += `
                <div class="stat-card">
                    <h3>${feature}</h3>
                    <div class="metric-value" style="color: ${color}; font-size: 1.8em;">
                        ${Utils.formatNumber(value, 4)}
                    </div>
                    <div class="stat-label">Корреляция</div>
                </div>
            `;
        }

        html += '</div>';

        // Интерпретация
        html += '<div style="margin-top: 30px;">';
        html += Utils.createInfoBox(data.interpretation);
        html += '</div>';

        html += '</div>';

        $('#correlations-result').html(html);
    }
};

window.CorrelationsComponent = CorrelationsComponent;