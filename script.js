
const slider = document.getElementById("days");
const daysValue = document.getElementById("daysValue");
const formDays = document.getElementById("formDays");
const chartData = window.timeLoopChart;
const scenarios = window.timeLoopScenarios;
const initialDays = Number(window.timeLoopInitialDays) || 180;

// Daily learning hours come directly from Flask.
function dailyHours(key) {
    const scenario = scenarios.find(item => item.key === key);
    return scenario ? Number(scenario.daily) : 0;
}

function createLabels(days) {
    const step = Math.max(1, Math.floor(days / 6));
    const labels = [];

    for (let day = 0; day <= days; day += step) {
        labels.push(day);
    }

    if (labels[labels.length - 1] !== days) {
        labels.push(days);
    }

    return labels;
}

// Create the interactive Chart.js graph.
const canvas = document.getElementById("learningChart");

const learningChart = new Chart(canvas, {
    type: "line",

    data: {
        labels: chartData.labels.map(day => "Day " + day),

        datasets: [
            {
                label: "Baseline",
                data: chartData.baseline,
                borderColor: "#4169e1",
                backgroundColor: "#4169e1",
                borderWidth: 2.5,
                pointRadius: 2,
                tension: 0.35
            },
            {
                label: "Improved",
                data: chartData.improved,
                borderColor: "#159b7a",
                backgroundColor: "#159b7a",
                borderWidth: 2.5,
                pointRadius: 2,
                tension: 0.35
            },
            {
                label: "Reduced",
                data: chartData.reduced,
                borderColor: "#8b5cf6",
                backgroundColor: "#8b5cf6",
                borderWidth: 2.5,
                pointRadius: 2,
                tension: 0.35
            }
        ]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        interaction: {
            mode: "index",
            intersect: false
        },

        plugins: {
            legend: {
                position: "bottom",
                labels: {
                    usePointStyle: true,
                    padding: 18
                }
            },

            tooltip: {
                callbacks: {
                    label: function (context) {
                        return context.dataset.label + ": " +
                            context.parsed.y + " hours";
                    }
                }
            }
        },

        scales: {
            x: {
                grid: {
                    display: false
                },
                title: {
                    display: true,
                    text: "Timeline"
                }
            },

            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Cumulative learning hours"
                }
            }
        }
    }
});

// Update the chart and scenario cards when the slider moves.
slider.addEventListener("input", function () {
    const days = Number(slider.value);

    daysValue.textContent = days;
    formDays.value = days;

    const labels = createLabels(days);

    learningChart.data.labels =
        labels.map(day => "Day " + day);

    learningChart.data.datasets[0].data =
        labels.map(day => +(dailyHours("baseline") * day).toFixed(1));

    learningChart.data.datasets[1].data =
        labels.map(day => +(dailyHours("improved") * day).toFixed(1));

    learningChart.data.datasets[2].data =
        labels.map(day => +(dailyHours("reduced") * day).toFixed(1));

    learningChart.update();

    document.getElementById("periodBadge").textContent =
        days + "-day view";

    ["baseline", "improved", "reduced"].forEach(function (key) {
        const element = document.getElementById(key + "Hours");

        if (element) {
            element.textContent =
                (dailyHours(key) * days).toFixed(1);
        }
    });
});

// Keep the form's timeline value correct before submission.
document.getElementById("habitForm").addEventListener("submit", function () {
    formDays.value = slider.value;
});
