// Função para buscar dados da API
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.error) {
            console.error('Erro na API:', data.error);
            return;
        }

        // Atualizar cards de resumo
        document.getElementById('totalOS').textContent = data.summary?.totalOS || 0;
        document.getElementById('totalProdutos').textContent = data.summary?.totalProdutos || 0;
        document.getElementById('totalTecnicos').textContent = data.summary?.totalTecnicos || 0;
        document.getElementById('totalCidades').textContent = data.summary?.totalCidades || 0;

        // Atualizar gráfico de barras (se houver dados)
        if (data.osPorPeriodo && data.osPorPeriodo.length > 0) {
            updateBarChart(data.osPorPeriodo);
        }

        // Atualizar gráfico de pizza (se houver dados)
        if (data.composicaoStatus && data.composicaoStatus.length > 0) {
            updateDonutChart(data.composicaoStatus);
        }

        // Atualizar tabela (se houver dados)
        if (data.osPorTecnico && data.osPorTecnico.length > 0) {
            updateTable(data.osPorTecnico);
        }

    } catch (error) {
        console.error('Erro ao buscar dados:', error);
    }
}

// Função para atualizar gráfico de barras
function updateBarChart(osPorPeriodo) {
    const barChart = document.getElementById('barChart');
    barChart.innerHTML = '';

    // Encontrar o valor máximo para escalar as barras
    const maxValue = Math.max(...osPorPeriodo.map(item => item.quantidade));
    
    osPorPeriodo.forEach(item => {
        const height = (item.quantidade / maxValue) * 100;
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.height = `${height}%`;
        bar.title = `${item.periodo}: ${item.quantidade} O.S`;
        
        bar.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        bar.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
        
        barChart.appendChild(bar);
    });
}

// Função para atualizar gráfico de pizza
function updateDonutChart(composicaoStatus) {
    const donutLegend = document.getElementById('donutLegend');
    donutLegend.innerHTML = '';

    let total = composicaoStatus.reduce((sum, item) => sum + item.quantidade, 0);
    let currentAngle = 0;
    let gradientParts = [];
    let legendHTML = '';

    composicaoStatus.forEach((item, index) => {
        const percentage = (item.quantidade / total) * 100;
        const angle = (percentage / 100) * 360;
        
        // Adicionar ao gradiente
        const color = index === 0 ? '#2c5aa0' : '#17a2b8';
        gradientParts.push(`${color} ${currentAngle}deg ${currentAngle + angle}deg`);
        currentAngle += angle;

        // Adicionar à legenda
        legendHTML += `
            <div class="legend-item">
                <div class="legend-color" style="background: ${color};"></div>
                <span>${item.status}: ${percentage.toFixed(1)}%</span>
            </div>
        `;
    });

    // Aplicar gradiente ao donut
    const donut = document.getElementById('donutChart');
    donut.style.background = `conic-gradient(${gradientParts.join(', ')})`;
    
    // Atualizar legenda
    donutLegend.innerHTML = legendHTML;
}

// Função para atualizar tabela
function updateTable(osPorTecnico) {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    osPorTecnico.forEach(tecnico => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <div class="employee-info">
                    <div class="employee-avatar"></div>
                    <span>${tecnico.nome || 'Técnico ' + tecnico.id}</span>
                </div>
            </td>
            <td>${tecnico.departamento || 'Manutenção'}</td>
            <td>${tecnico.quantidadeOS || 0}</td>
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${tecnico.conclusao || 0}%;"></div>
                    </div>
                    <span>${tecnico.conclusao || 0}%</span>
                </div>
            </td>
            <td><span class="status-badge ${tecnico.status === 'Permanent' ? 'status-permanent' : 'status-contract'}">${tecnico.status || 'Ativo'}</span></td>
        `;
        tableBody.appendChild(row);
    });
}

// Interatividade da sidebar
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');
    });
});

// Carregar dados quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    fetchData();
    
    // Atualizar dados a cada 30 segundos
    setInterval(fetchData, 30000);
});

// Auto-refresh a cada 5 segundos (opcional)
setInterval(() => {
    // Verifica se houve mudanças no HTML
    fetch(window.location.href)
        .then(response => response.text())
        .then(html => {
            // Lógica simples para detectar mudanças
            if (html !== document.documentElement.outerHTML) {
                console.log('Mudanças detectadas, recarregando...');
                window.location.reload();
            }
        })
        .catch(error => console.log('Erro ao verificar atualizações:', error));
}, 5000);