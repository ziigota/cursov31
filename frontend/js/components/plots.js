/**
 * Компонент для отображения графиков
 */

const PlotsComponent = {
    /**
     * Загрузить scatter plot
     */
    async loadScatter() {
        Utils.showLoading('loading-scatter');

        const result = await api.getScatterPlot();

        Utils.hideLoading('loading-scatter');

        if (!result.success) {
            Utils.showError('scatter-plot', result.error);
            return;
        }

        this.renderPlot('scatter-plot', result.data.image, 'Scatter Plot: Темп vs Популярность');
    },

    /**
     * Загрузить histogram
     */
    async loadHistogram() {
        Utils.showLoading('loading-histogram');

        const result = await api.getHistogram();

        Utils.hideLoading('loading-histogram');

        if (!result.success) {
            Utils.showError('histogram-plot', result.error);
            return;
        }

        this.renderPlot('histogram-plot', result.data.image, 'Histogram: Распределение громкости');
    },

    /**
     * Загрузить heatmap
     */
    async loadHeatmap() {
        Utils.showLoading('loading-heatmap');

        const result = await api.getHeatmap();

        Utils.hideLoading('loading-heatmap');

        if (!result.success) {
            Utils.showError('heatmap-plot', result.error);
            return;
        }

        this.renderPlot('heatmap-plot', result.data.image, 'Heatmap: Корреляционная матрица');
    },

    /**
     * Отобразить график
     */
    renderPlot(containerId, imageBase64, alt) {
        const html = Utils.createImageBlock(imageBase64, alt);
        $(`#${containerId}`).html(html);
    }
};

window.PlotsComponent = PlotsComponent;