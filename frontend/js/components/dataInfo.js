/**
 * Компонент для отображения информации о датасете
 */

const DataInfoComponent = {
    async load() {
        Utils.showLoading('loading-info');

        const result = await api.getDataInfo();

        Utils.hideLoading('loading-info');

        if (!result.success) {
            Utils.showError('data-info', result.error);
            return;
        }

        this.render(result.data);
    },

    render(data) {
        let html = '<div class="result">';
        html += `<h3>Размер датасета: ${data.rows.toLocaleString()} строк × ${data.columns} колонок</h3>`;

        html += '<div class="info-box">';
        html += '<p><strong>Признаки:</strong> ' + data.features.join(', ') + '</p>';
        html += '</div>';

        // Пропущенные значения (если есть)
        const missingValues = Object.entries(data.missing_values)
            .filter(([key, value]) => value > 0);

        if (missingValues.length > 0) {
            html += '<h4 style="margin-top: 20px;">Пропущенные значения:</h4>';
            html += '<div class="stats-grid">';

            missingValues.forEach(([feature, count]) => {
                html += Utils.createStatCard(feature, {
                    'Пропущено': count,
                    'Процент': Utils.formatNumber((count / data.rows) * 100) + '%'
                });
            });

            html += '</div>';
        }

        html += '</div>';

        $('#data-info').html(html);
    }
};

window.DataInfoComponent = DataInfoComponent;