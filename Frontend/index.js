let barChartInstance = null;
let donutChartInstance = null;

async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();

    // Atualizar gráficos
    updateBarChart(data.osPorPeriodo);
    updateDonutChart(data.composicaoStatus);
    updateTable(data.osPorTecnico);
  } catch (error) {
    console.error('Erro ao buscar os dados:', error);
  }
}

// Gráfico de Barras
function updateBarChart(osPorPeriodo) {
  const labels = osPorPeriodo.map(item => item.periodo);
  const values = osPorPeriodo.map(item => item.quantidade);

  const ctx = document.getElementById('barChart').getContext('2d');
  if (barChartInstance) barChartInstance.destroy();
  barChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total de O.S',
        data: values,
        backgroundColor: '#2c5aa0'
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
}

// Gráfico de Rosca (Donut)
function updateDonutChart(composicaoStatus) {
  const labels = composicaoStatus.map(item => item.status);
  const values = composicaoStatus.map(item => item.quantidade);
  const colors = ['#2c5aa0', '#17a2b8', '#a0cae8', '#f6c23e', '#e74a3b'];

  const ctx = document.getElementById('donutChart').getContext('2d');
  if (donutChartInstance) donutChartInstance.destroy();
  donutChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'right' } }
    }
  });
}

// Atualiza tabela
function updateTable(osPorTecnico) {
  const tbody = document.getElementById('tableBody');
  tbody.innerHTML = '';

  osPorTecnico.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.nome}</td>
      <td>${item.departamento || '-'}</td>
      <td>${item.area || '-'}</td>
      <td>${item.conclusao || '0'}</td>
      <td>${item.status || '-'}</td>
    `;
    tbody.appendChild(row);
  });
}

// Carregar e atualizar em intervalos
document.addEventListener('DOMContentLoaded', fetchData);
setInterval(fetchData, 30000);