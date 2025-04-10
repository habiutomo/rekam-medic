document.addEventListener('DOMContentLoaded', function() {
    // Initialize charts if they exist on the page
    if (document.getElementById('appointmentsChart')) {
        loadAppointmentsChart();
    }
    
    if (document.getElementById('appointmentStatusChart')) {
        loadAppointmentStatusChart();
    }
    
    if (document.getElementById('revenueChart')) {
        loadRevenueChart();
    }
    
    if (document.getElementById('genderChart')) {
        loadPatientDemographics();
    }
});

function loadAppointmentsChart() {
    const ctx = document.getElementById('appointmentsChart').getContext('2d');
    
    // Show loading spinner
    showLoading('appointmentsChartContainer');
    
    // Fetch appointment statistics
    fetch('/api/appointments/stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Create chart
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Appointments',
                        data: data.counts,
                        backgroundColor: 'rgba(13, 110, 253, 0.6)',
                        borderColor: 'rgba(13, 110, 253, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Monthly Appointments'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Appointments'
                            },
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            document.getElementById('appointmentsChartContainer').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load appointment statistics: ${error.message}
                </div>
            `;
            console.error('Error loading appointments chart:', error);
        });
}

function loadAppointmentStatusChart() {
    const ctx = document.getElementById('appointmentStatusChart').getContext('2d');
    
    // Show loading spinner
    showLoading('appointmentStatusChartContainer');
    
    // Fetch appointment status statistics
    fetch('/api/appointments/status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Map status labels to more readable format
            const formattedLabels = data.labels.map(label => {
                return label.charAt(0).toUpperCase() + label.slice(1).replace('_', ' ');
            });
            
            // Define colors for each status
            const backgroundColors = [
                'rgba(40, 167, 69, 0.6)',  // green for scheduled
                'rgba(0, 123, 255, 0.6)',   // blue for completed
                'rgba(220, 53, 69, 0.6)',   // red for cancelled
                'rgba(255, 193, 7, 0.6)'    // yellow for no-show
            ];
            
            // Create chart
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: formattedLabels,
                    datasets: [{
                        data: data.counts,
                        backgroundColor: backgroundColors,
                        borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Appointment Status Distribution'
                        }
                    }
                }
            });
        })
        .catch(error => {
            document.getElementById('appointmentStatusChartContainer').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load appointment status statistics: ${error.message}
                </div>
            `;
            console.error('Error loading appointment status chart:', error);
        });
}

function loadRevenueChart() {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    
    // Show loading spinner
    showLoading('revenueChartContainer');
    
    // Fetch revenue statistics
    fetch('/api/revenue')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Create chart
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: data.revenue,
                        backgroundColor: 'rgba(40, 167, 69, 0.1)',
                        borderColor: 'rgba(40, 167, 69, 1)',
                        borderWidth: 2,
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Monthly Revenue'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Revenue: $${context.parsed.y.toFixed(2)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Revenue ($)'
                            },
                            ticks: {
                                callback: function(value) {
                                    return '$' + value;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            document.getElementById('revenueChartContainer').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load revenue statistics: ${error.message}
                </div>
            `;
            console.error('Error loading revenue chart:', error);
        });
}

function loadPatientDemographics() {
    // Show loading spinners
    showLoading('genderChartContainer');
    showLoading('ageChartContainer');
    
    // Fetch patient demographics
    fetch('/api/patients/demographics')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Create gender chart
            createGenderChart(data.gender);
            
            // Create age chart
            createAgeChart(data.age);
        })
        .catch(error => {
            document.getElementById('genderChartContainer').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load patient demographics: ${error.message}
                </div>
            `;
            document.getElementById('ageChartContainer').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to load patient demographics: ${error.message}
                </div>
            `;
            console.error('Error loading patient demographics:', error);
        });
}

function createGenderChart(data) {
    const ctx = document.getElementById('genderChart').getContext('2d');
    
    // Define colors for genders
    const backgroundColors = [
        'rgba(0, 123, 255, 0.6)',   // blue for Male
        'rgba(255, 99, 132, 0.6)',   // pink for Female
        'rgba(108, 117, 125, 0.6)'   // gray for Other
    ];
    
    // Create chart
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                backgroundColor: backgroundColors,
                borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Patient Gender Distribution'
                }
            }
        }
    });
}

function createAgeChart(data) {
    const ctx = document.getElementById('ageChart').getContext('2d');
    
    // Create chart
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Number of Patients',
                data: data.data,
                backgroundColor: 'rgba(255, 159, 64, 0.6)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Patient Age Distribution'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Patients'
                    },
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}
