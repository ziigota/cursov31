/**
 * Компонент для анализа распределений
 */

const DistributionsComponent = {
    async load() {
        Utils.showLoading('loading-dist');

        const result = await api.getDistributions();

        Utils.hideLoading('loading-dist');

        if (!result.success) {
            Utils.showError('distributions-result', result.error);
            return;
        }

        this.render(result.data);
    },

    render(data) {
        let html = '<div class="result">';
        html += '<div class="stats-grid">';

        // Карточки для каждого признака
        for (const [feature, stats] of Object.entries(data.distributions)) {
            const featureTitle = feature.charAt(0).toUpperCase() + feature.slice(1);

            html += Utils.createStatCard(featureTitle, {
                'Среднее': Utils.formatNumber(stats.mean),
                'Медиана': Utils.formatNumber(stats.median),
                'Ст. откл.': Utils.formatNumber(stats.std),
                'Мин': Utils.formatNumber(stats.min),
                'Макс': Utils.formatNumber(stats.max),
                '25%': Utils.formatNumber(stats.q25),
                '75%': Utils.formatNumber(stats.q75)
            });
        }

        html += '</div>';

        // Интерпретация
        html += '<div style="margin-top: 30px;">';
        html += '<h3>💡 Интерпретация</h3>';
        for (const [feature, interpretation] of Object.entries(data.interpretation)) {
            html += Utils.createInfoBox(`<strong>${feature}:</strong> ${interpretation}`);
        }
        html += '</div>';

        html += '</div>';

        $('#distributions-result').html(html);
    }
};

window.DistributionsComponent = DistributionsComponent;