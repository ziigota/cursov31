/**
 * Компонент для анализа жанров
 */

const GenresComponent = {
    async load() {
        Utils.showLoading('loading-genres');

        const result = await api.getGenres();

        Utils.hideLoading('loading-genres');

        if (!result.success) {
            Utils.showError('genres-result', result.error);
            return;
        }

        this.render(result.data);
    },

    render(data) {
        let html = '<div class="result">';

        html += `<h3>Найдено жанров: ${data.genre_count}</h3>`;

        html += '<div class="info-box" style="margin-top: 15px;">';
        html += '<p><strong>Список жанров:</strong></p>';
        html += '<p>' + data.genres.join(', ') + '</p>';
        html += '</div>';

        html += Utils.createInfoBox(data.interpretation);

        // Если есть статистика по жанрам, показываем топ-5
        if (data.genre_statistics) {
            html += '<h3 style="margin-top: 30px;">Сравнение характеристик</h3>';
            html += '<p style="color: #666; margin-bottom: 15px;">Средние значения аудио-характеристик для каждого жанра</p>';

            // Берём первые 5 жанров для примера
            const genres = Object.keys(data.genre_statistics.danceability || {}).slice(0, 5);

            if (genres.length > 0) {
                html += '<div class="stats-grid">';

                genres.forEach(genre => {
                    const stats = {};
                    for (const [feature, values] of Object.entries(data.genre_statistics)) {
                        if (values[genre] !== undefined) {
                            stats[feature] = Utils.formatNumber(values[genre]);
                        }
                    }

                    html += Utils.createStatCard(genre, stats);
                });

                html += '</div>';
            }
        }

        html += '</div>';

        $('#genres-result').html(html);
    }
};

window.GenresComponent = GenresComponent;