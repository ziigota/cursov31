/**
 * Утилиты для работы с UI
 */

const Utils = {
    /**
     * Показать индикатор загрузки
     */
    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.add('active');
        }
    },

    /**
     * Скрыть индикатор загрузки
     */
    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.remove('active');
        }
    },

    /**
     * Показать ошибку
     */
    showError(containerId, message) {
        const html = `
            <div class="result error" style="border-left-color: #f44336;">
                <div style="text-align: center; padding: 20px;">
                    <div style="font-size: 48px; margin-bottom: 15px;">❌</div>
                    <h3 style="color: #f44336; margin-bottom: 10px;">Ошибка</h3>
                    <p style="color: #666;">${message}</p>
                </div>
            </div>
        `;
        $(`#${containerId}`).html(html);
    },

    /**
     * Форматировать число
     */
    formatNumber(num, decimals = 2) {
        if (typeof num !== 'number') return num;
        return num.toFixed(decimals);
    },

    /**
     * Создать карточку со статистикой
     */
    createStatCard(title, stats) {
        let html = '<div class="stat-card">';
        html += `<h3>${title}</h3>`;

        for (const [label, value] of Object.entries(stats)) {
            html += `
                <div class="stat-item">
                    <span class="stat-label">${label}:</span>
                    <span class="stat-value">${this.formatNumber(value)}</span>
                </div>
            `;
        }

        html += '</div>';
        return html;
    },

    /**
     * Создать информационный блок
     */
    createInfoBox(text) {
        return `
            <div class="info-box">
                <p>${text}</p>
            </div>
        `;
    },

    /**
     * Создать блок с изображением
     */
    createImageBlock(imageBase64, alt = 'График') {
        return `
            <div class="plot-container">
                <img src="${imageBase64}" alt="${alt}">
            </div>
        `;
    },

    /**
     * Создать карточку метрики
     */
    createMetricCard(title, value, subtitle = '') {
        return `
            <div class="metric-card">
                <h3>${title}</h3>
                <div class="metric-value">${value}</div>
                ${subtitle ? `<div class="metric-label">${subtitle}</div>` : ''}
            </div>
        `;
    },

    /**
     * Создать бар для важности признака
     */
    createFeatureBar(featureName, importance, maxImportance) {
        const percentage = (importance / maxImportance) * 100;
        return `
            <div class="bar">
                <div class="bar-fill" style="width: ${percentage}%">${this.formatNumber(importance, 4)}</div>
            </div>
        `;
    },

    /**
     * Плавная прокрутка к элементу
     */
    scrollToElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    },

    /**
     * Показать уведомление
     */
    showNotification(message, type = 'info') {
        const colors = {
            'info': { bg: '#2196f3', icon: 'ℹ️' },
            'success': { bg: '#4caf50', icon: '✅' },
            'warning': { bg: '#ff9800', icon: '⚠️' },
            'error': { bg: '#f44336', icon: '❌' }
        };

        const color = colors[type] || colors.info;

        const notification = $(`
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${color.bg};
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                z-index: 10000;
                font-size: 16px;
                max-width: 400px;
                animation: slideIn 0.3s ease;
            ">
                ${color.icon} ${message}
            </div>
            <style>
                @keyframes slideIn {
                    from { transform: translateX(400px); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOut {
                    from { transform: translateX(0); opacity: 1; }
                    to { transform: translateX(400px); opacity: 0; }
                }
            </style>
        `);

        $('body').append(notification);

        setTimeout(() => {
            notification.css('animation', 'slideOut 0.3s ease');
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }
};

// Экспорт в глобальную область
window.Utils = Utils;