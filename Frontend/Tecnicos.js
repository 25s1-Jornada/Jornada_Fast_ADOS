let barChartInstance = null;
let donutChartInstance = null;

async function fetchData() {
  try {
    const response = await fetch('http://localhost:8000/api/data');
    const data = await response.json();

    // Atualizar tabela Ordens de Serviço por Técnico
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

// Exibir tabela Ordens de Serviço por Técnico
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