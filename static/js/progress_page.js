document.addEventListener("DOMContentLoaded", function() {
    // Check if the chart canvas exists on the page
    const chartCanvas = document.getElementById('progressChart');
    if (!chartCanvas) return;

    const ctx = chartCanvas.getContext('2d');

    const labels = Array.from({ length: 30 }, (_, i) => {
        const d = new Date();
        d.setDate(d.getDate() - (29 - i));
        return `${d.getMonth() + 1}/${d.getDate()}`;
    });

    const weightData = [
        80.0, 80.2, 79.8, 79.5, 79.6, 79.2, 79.0, 78.8, 78.9, 78.5,
        78.6, 78.2, 78.0, 77.7, 77.8, 77.5, 77.6, 77.2, 77.0, 77.1,
        76.8, 76.5, 76.6, 76.3, 76.0, 76.1, 75.8, 75.6, 75.7, 75.5
    ];

    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.4)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    const progressChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Weight (kg)',
                data: weightData,
                backgroundColor: gradient,
                borderColor: '#3b82f6',
                borderWidth: 3,
                pointBackgroundColor: '#3b82f6',
                pointBorderColor: '#ffffff',
                pointHoverRadius: 7,
                pointHoverBorderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: false, grid: { drawBorder: false } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a202c',
                    titleFont: { size: 14, weight: '600' },
                    bodyFont: { size: 12 },
                    padding: 10,
                    cornerRadius: 8,
                    displayColors: false,
                }
            }
        }
    });
});