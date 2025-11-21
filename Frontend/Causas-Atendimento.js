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
    
    let causasChart, produtosChart, recorrenciaChart, timelineCausasChart;
    
    // URLs da API
    const API_BASE_URL = 'http://localhost:8000/api';
    
    // Função para buscar dados da API
    async function fetchCausasData() {
        try {
            const response = await fetch(`${API_BASE_URL}/causas-atendimento`);
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Atualizar métricas
            updateMetrics(data);
            
            // Atualizar gráficos
            updateCharts(data);
            
            // Atualizar tabela
            updateTable(data);
            
        } catch (error) {
            console.error('Erro ao buscar dados de causas:', error);
            showErrorMessage();
        }
    }
    
    // Função para atualizar as métricas
    function updateMetrics(data) {
        if (data.summary) {
            document.getElementById('totalCausas').textContent = data.summary.totalCausas || '0';
            document.getElementById('causaMaisFrequente').textContent = data.summary.causaMaisFrequente || '-';
            document.getElementById('taxaRecorrenciaCausas').textContent = data.summary.taxaRecorrenciaCausas || '0%';
            document.getElementById('produtoMaisAfetado').textContent = data.summary.produtoMaisAfetado || '-';
        }
    }
    
    // Função para atualizar os gráficos
    function updateCharts(data) {
        updateCausasChart(data.topCausas || []);
        updateProdutosChart(data.falhasPorProduto || []);
        updateRecorrenciaChart(data.analiseRecorrencia || []);
        updateTimelineCausasChart(data.evolucaoTemporal || []);
    }
    
    // Gráfico de Top Causas
    function updateCausasChart(topCausas) {
        const ctx = document.getElementById('causasChart').getContext('2d');
        
        if (causasChart) {
            causasChart.destroy();
        }
        
        const labels = topCausas.map(item => item.causa || 'Sem nome').slice(0, 10);
        const values = topCausas.map(item => item.quantidade || 0).slice(0, 10);
        
        causasChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Quantidade de Ocorrências',
                    data: values,
                    backgroundColor: 'rgba(44, 90, 160, 0.8)',
                    borderColor: 'rgb(44, 90, 160)',
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
                        },
                        title: {
                            display: true,
                            text: 'Quantidade'
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
    
    // Gráfico de Falhas por Produto
    function updateProdutosChart(falhasPorProduto) {
        const ctx = document.getElementById('produtosChart').getContext('2d');
        
        if (produtosChart) {
            produtosChart.destroy();
        }
        
        const labels = falhasPorProduto.map(item => item.produto || 'Sem nome').slice(0, 8);
        const values = falhasPorProduto.map(item => item.quantidade || 0).slice(0, 8);
        
        produtosChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        'rgba(44, 90, 160, 0.8)',
                        'rgba(231, 76, 60, 0.8)',
                        'rgba(46, 204, 113, 0.8)',
                        'rgba(155, 89, 182, 0.8)',
                        'rgba(241, 196, 15, 0.8)',
                        'rgba(230, 126, 34, 0.8)',
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(149, 165, 166, 0.8)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12,
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Gráfico de Análise de Recorrência
    function updateRecorrenciaChart(analiseRecorrencia) {
        const ctx = document.getElementById('recorrenciaChart').getContext('2d');
        
        if (recorrenciaChart) {
            recorrenciaChart.destroy();
        }
        
        const labels = analiseRecorrencia.map(item => item.causa || 'Sem nome').slice(0, 6);
        const valoresRecorrencia = analiseRecorrencia.map(item => item.recorrencia || 0).slice(0, 6);
        
        recorrenciaChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Índice de Recorrência',
                    data: valoresRecorrencia,
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    borderColor: 'rgb(231, 76, 60)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: 'rgb(231, 76, 60)',
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
                        },
                        title: {
                            display: true,
                            text: 'Índice de Recorrência'
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
    
    // Gráfico de Evolução Temporal
    function updateTimelineCausasChart(evolucaoTemporal) {
        const ctx = document.getElementById('timelineCausasChart').getContext('2d');
        
        if (timelineCausasChart) {
            timelineCausasChart.destroy();
        }
        
        const labels = evolucaoTemporal.map(item => item.periodo || 'Período');
        const valores = evolucaoTemporal.map(item => item.quantidade || 0);
        
        timelineCausasChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ocorrências',
                    data: valores,
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    borderColor: 'rgb(46, 204, 113)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: 'rgb(46, 204, 113)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
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
                        },
                        title: {
                            display: true,
                            text: 'Quantidade'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Período'
                        }
                    }
                }
            }
        });
    }
    
    // Atualizar tabela
    function updateTable(data) {
        const tbody = document.getElementById('causasTableBody');
        tbody.innerHTML = '';
        
        const detalhesCausas = data.detalhesCausas || [];
        
        detalhesCausas.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.causa || '-'}</td>
                <td>${item.produto || '-'}</td>
                <td>${item.quantidade || '0'}</td>
                <td>${item.percentual || '0%'}</td>
                <td>${item.recorrencia || '0'}</td>
            `;
            tbody.appendChild(row);
        });
    }
    
    // Mostrar mensagem de erro
    function showErrorMessage() {
        const metricsGrid = document.querySelector('.metrics-grid');
        if (metricsGrid) {
            metricsGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 20px; color: #e74c3c;">
                    <h3>Erro ao carregar dados</h3>
                    <p>Verifique se o servidor Flask está rodando na porta 8000</p>
                    <button onclick="location.reload()" style="padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        Tentar Novamente
                    </button>
                </div>
            `;
        }
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
            await fetchCausasData();
            // Atualizar dados a cada 30 segundos
            setInterval(fetchCausasData, 30000);
        } else {
            showErrorMessage();
        }
    }
    
    // Iniciar o dashboard
    initializeDashboard();
});