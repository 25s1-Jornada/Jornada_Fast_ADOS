let donutChartInstance = null;

async function fetchData() {
  try {
    const response = await fetch('http://localhost:8000/api/data');
    const data = await response.json();

    updateDonutChart(data.composicaoStatus);
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

function updateDonutChart(composicaoStatus) {
  const labels = composicaoStatus.map(item => item.status);
  const values = composicaoStatus.map(item => item.quantidade);
  const colors = ['#2c5aa0', '#17a2b8', '#a0cae8', '#f6c23e', '#e74a3b'];

  const ctx = document.getElementById('donutChart').getContext('2d');
  
  // Destruir instância anterior se existir
  if (donutChartInstance) {
    donutChartInstance.destroy();
  }
  
  donutChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: { 
        legend: { 
          position: 'right',
          labels: {
            boxWidth: 12,
            padding: 15
          }
        } 
      },
      cutout: '50%'
    }
  });
}

// Carregar e atualizar em intervalos
document.addEventListener('DOMContentLoaded', fetchData);
setInterval(fetchData, 30000);