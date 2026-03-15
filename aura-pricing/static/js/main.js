document.addEventListener('DOMContentLoaded', () => {
    // Luxury color palette for charts
    const goldColor = '#c5a358';
    const gridColor = 'rgba(255, 255, 255, 0.05)';

    // Initialize all price history charts
    const charts = document.querySelectorAll('canvas[id^="chart-"]');

    charts.forEach(canvas => {
        const productId = canvas.id.split('-')[1];
        // Data is passed from HTML via window object
        const historyData = window["history_" + productId];

        if (historyData && historyData.length > 0) {
            new Chart(canvas, {
                type: 'line',
                data: {
                    labels: new Array(historyData.length).fill(''), // Clean X-axis
                    datasets: [{
                        label: 'Price History',
                        data: historyData,
                        borderColor: goldColor,
                        borderWidth: 2,
                        pointRadius: 0, // Keep it minimalist
                        tension: 0.4,   // Smooth curvy lines
                        fill: true,
                        backgroundColor: 'rgba(197, 163, 88, 0.05)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { display: false },
                        y: {
                            grid: { color: gridColor },
                            ticks: {
                                color: '#64748b',
                                font: { family: 'Times New Roman', size: 10 }
                            }
                        }
                    }
                }
            });
        }
    });
});

// Utility to flash messages away
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(a => a.style.display = 'none');
}, 4000);