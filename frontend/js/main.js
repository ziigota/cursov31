/**
 * Главный файл приложения
 * Связывает все компоненты и инициализирует приложение
 */

// Глобальные функции для кнопок (вызываются из HTML)
function loadDataInfo() {
    DataInfoComponent.load();
}

function analyzeDistributions() {
    DistributionsComponent.load();
}

function analyzeCorrelations() {
    CorrelationsComponent.load();
}

function analyzeGenres() {
    GenresComponent.load();
}

function loadScatterPlot() {
    PlotsComponent.loadScatter();
}

function loadHistogram() {
    PlotsComponent.loadHistogram();
}

function loadHeatmap() {
    PlotsComponent.loadHeatmap();
}

function trainModel() {
    ModelComponent.train();
}

function loadModelMetrics() {
    ModelComponent.loadMetrics();
}

// Инициализация приложения
$(document).ready(function() {
    console.log('🎵 Spotify Analysis App initialized');
    console.log('API URL:', CONFIG.API_URL);

    // Проверка подключения к API
    checkAPIConnection();
});

/**
 * Проверить подключение к API
 */
async function checkAPIConnection() {
    try {
        const response = await $.ajax({
            url: `${CONFIG.API_URL}/health`,
            method: 'GET',
            timeout: 5000
        });

        if (response.status === 'healthy') {
            console.log('✅ API подключено');

            if (!response.dataset_loaded) {
                showWarning('⚠️ Датасет не загружен. Убедитесь, что файл SpotifyFeatures.csv находится в папке data/');
            }
        }
    } catch (error) {
        console.error('❌ Не удалось подключиться к API');
        showWarning('⚠️ Не удалось подключиться к серверу. Убедитесь, что backend запущен на порту 8000.');
    }
}

/**
 * Показать предупреждение
 */
function showWarning(message) {
    const warningHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: #fff3cd;
            color: #856404;
            padding: 15px 20px;
            border-left: 4px solid #ffc107;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            max-width: 400px;
        ">
            ${message}
        </div>
    `;

    $('body').append(warningHTML);

    // Автоматически скрыть через 10 секунд
    setTimeout(() => {
        $('body > div:last').fadeOut(500, function() {
            $(this).remove();
        });
    }, 10000);
}