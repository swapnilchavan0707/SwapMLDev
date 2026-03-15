document.addEventListener('DOMContentLoaded', () => {
    const goldColor = '#c5a358';
    const silverColor = 'rgba(148, 163, 184, 0.5)';

    // Select all canvases that represent a machine chart
    const canvases = document.querySelectorAll('canvas[id^="chart-"]');

    canvases.forEach(canvas => {
        const machineId = canvas.id.split('-')[1];
        const history = window["data_" + machineId];

        if (history && history.temp.length > 0) {
            new Chart(canvas, {
                type: 'line',
                data: {
                    labels: new Array(history.temp.length).fill(''), // Clean X-axis
                    datasets: [
                        {
                            label: 'Temp',
                            data: history.temp,
                            borderColor: goldColor,
                            borderWidth: 2,
                            pointRadius: 0,
                            tension: 0.4, // Smooth curve
                            fill: false
                        },
                        {
                            label: 'Vib',
                            data: history.vib,
                            borderColor: silverColor,
                            borderWidth: 1,
                            borderDash: [5, 5],
                            pointRadius: 0,
                            tension: 0.4,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { display: false },
                        y: {
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
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