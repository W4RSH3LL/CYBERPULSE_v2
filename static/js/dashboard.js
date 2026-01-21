document.addEventListener("DOMContentLoaded", () => {

    if (window.deviceStats) {
        new Chart(document.getElementById("deviceChart"), {
            type: "doughnut",
            data: {
                labels: ["Computers", "Phones", "Printers", "IoT"],
                datasets: [{
                    data: Object.values(window.deviceStats),
                    backgroundColor: ["#2563eb", "#16a34a", "#ca8a04", "#dc2626"]
                }]
            }
        });
    }

    if (window.scanChartLabels && window.scanChartValues) {
        new Chart(document.getElementById("scanChart"), {
            type: "line",
            data: {
                labels: window.scanChartLabels,
                datasets: [{
                    label: "Scan Activity",
                    data: window.scanChartValues,
                    borderColor: "#2563eb",
                    fill: false
                }]
            }
        });
    }

    if (window.alertSeverity) {
        new Chart(document.getElementById("alertChart"), {
            type: "bar",
            data: {
                labels: ["Low", "Medium", "High"],
                datasets: [{
                    data: Object.values(window.alertSeverity),
                    backgroundColor: ["#16a34a", "#ca8a04", "#dc2626"]
                }]
            }
        });
    }

});
