let barChartInstance = null;
let donutChartInstance = null;

async function fetchData() {
  try {
    const response = await fetch('http://localhost:8000/api/data');
    const data = await response.json();

    // Atualizar gráficos
    updateBarChart(data.osPorPeriodo);
    updateDonutChart(data.composicaoStatus);
    updateTable(data.osPorTecnico);
  } catch (error) {
    console.error('Erro ao buscar os dados:', error);
  }
}

function navigateTo(page) {
  window.location.href = page;
}

// Destacar item ativo no menu
const currentPage = window.location.pathname.split('/').pop();
document.querySelectorAll('.nav-item').forEach(item => {
  if (item.textContent.includes(getPageName(currentPage))) {
      item.classList.add('active');
  }
});

function getPageName(path) {
  const pages = {
      'Dashboard.html': 'Dashboard Geral',
      'Causas-Atendimento.html': 'Análise de Causas', 
      'Tecnicos.html': 'OS por Técnico',
  };
  return pages[path] || 'Dashboard Geral';
}

document.addEventListener('DOMContentLoaded', function() {
    // Configuração global do Chart.js
    Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
    Chart.defaults.color = '#7f8c8d';
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(44, 62, 80, 0.9)';
    
    let failuresByTypeChart, failuresByProductChart, heatmapChart, timelineChart;
    
    // URLs da API
    const API_BASE_URL = 'http://localhost:8000/api';
    
    // Função para buscar dados da API
    async function fetchDashboardData() {
        try {
            const response = await fetch(`${API_BASE_URL}/dashboard-geral`);
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Atualizar métricas
            updateMetrics(data);
            
            // Atualizar gráficos
            updateCharts(data);
            
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
            showErrorMessage(error.message);
        }
    }
    
    // Função para atualizar as métricas
    function updateMetrics(data) {
        document.getElementById('totalOS').textContent = data.summary?.totalOS || 'N/A';
        document.getElementById('taxaRecorrencia').textContent = data.summary?.taxaRecorrencia || 'N/A';
        document.getElementById('mittr').textContent = data.summary?.mittr || 'N/A';
        document.getElementById('falhasCriticas').textContent = data.summary?.falhasCriticas || 'N/A';
    }
    
    // Função para atualizar os gráficos
    function updateCharts(data) {
        updateFailuresByTypeChart(data.falhasPorTipo);
        updateFailuresByProductChart(data.falhasPorProduto);
        updateHeatmapChart(data.falhasPorTipo);
        updateTimelineChart(data.volumeOS);
    }
    
    // Gráfico de Falhas por Tipo - Barras Horizontais
    function updateFailuresByTypeChart(falhasPorTipo) {
        const ctx = document.getElementById('failuresByTypeChart').getContext('2d');
        
        if (failuresByTypeChart) {
            failuresByTypeChart.destroy();
        }
        
        // Usar dados da API
        const labels = falhasPorTipo.map(item => item.tipo || 'N/A');
        
        const values = falhasPorTipo.map(item => item.quantidade || 0);
        
        failuresByTypeChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Quantidade',
                    data: values,
                    backgroundColor: [
                        'rgba(41, 128, 185, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(46, 204, 113, 0.8)',
                        'rgba(155, 89, 182, 0.8)',
                        'rgba(241, 196, 15, 0.8)'
                    ],
                    borderColor: [
                        'rgb(41, 128, 185)',
                        'rgb(231, 76, 60)',
                        'rgb(46, 204, 113)',
                        'rgb(155, 89, 182)',
                        'rgb(241, 196, 15)'
                    ],
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(44, 62, 80, 0.9)',
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        }
                    }
                }
            }
        });
    }
    
    // Gráfico de Falhas por Produto/Linha
    function updateFailuresByProductChart(falhasPorProduto) {
        const ctx = document.getElementById('failuresByProductChart').getContext('2d');
        
        if (failuresByProductChart) {
            failuresByProductChart.destroy();
        }
        
        const labels = falhasPorProduto.map(item => item.produto || 'N/A');
        
        const values = falhasPorProduto.map(item => item.quantidade || 0);
        
        failuresByProductChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Quantidade',
                    data: values,
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgb(52, 152, 219)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Mapa de Calor
    function updateHeatmapChart(falhasPorTipo) {
        const ctx = document.getElementById('heatmapChart').getContext('2d');
        
        if (heatmapChart) {
            heatmapChart.destroy();
        }
        
        const tipos = falhasPorTipo.map(item => item.tipo).slice(0, 4);
        
        heatmapChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: tipos,
                datasets: [
                    {
                        label: 'Região Norte',
                        data: [20, 35, 15, 40],
                        backgroundColor: 'rgba(231, 76, 60, 0.8)',
                        borderColor: 'rgb(231, 76, 60)',
                        borderWidth: 1
                    },
                    {
                        label: 'Região Sul',
                        data: [25, 25, 15, 60],
                        backgroundColor: 'rgba(52, 152, 219, 0.8)',
                        borderColor: 'rgb(52, 152, 219)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Linha do Tempo de Volume de OS
    function updateTimelineChart(volumeOS) {
        const ctx = document.getElementById('timelineChart').getContext('2d');
        
        if (timelineChart) {
            timelineChart.destroy();
        }
        
        const labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];

        const values = volumeOS.map(item => item.quantidade || 0);
        
        timelineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Volume de OS',
                    data: values,
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    borderColor: 'rgb(46, 204, 113)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: 'rgb(46, 204, 113)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Testar conexão com a API
    async function testConnection() {
        try {
            const response = await fetch(`${API_BASE_URL}/test-db`);
            const result = await response.json();
            console.log('Teste de conexão:', result);
            return result.status === 'Conexão OK';
        } catch (error) {
            console.error('Erro no teste de conexão:', error);
            return false;
        }
    }
    
    // Inicializar dashboard
    async function initializeDashboard() {
        const isConnected = await testConnection();
        console.log('Conexão com API:', isConnected ? 'OK' : 'FALHA');
        
        if (isConnected) {
            await fetchDashboardData();
            setInterval(fetchDashboardData, 15000);
        } else {
            showErrorMessage();
        }
    }
    
    // Iniciar o dashboard
    initializeDashboard();
});