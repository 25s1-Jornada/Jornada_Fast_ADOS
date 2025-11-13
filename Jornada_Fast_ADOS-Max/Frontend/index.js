async function carregarResumoGeral() {
  const res = await fetch("http://localhost:8000/os/resumo-geral");
  const json = await res.json();
  console.log("Resumo geral:", json);
}

async function carregarTotalPorPeriodo() {
  const res = await fetch("http://localhost:8000/os/total-por-periodo");
  const json = await res.json();
  console.log("Total por período:", json);
}

async function carregarPrincipaisCausas() {
  const res = await fetch("http://localhost:8000/os/principais-causas");
  const json = await res.json();
  console.log("Principais causas:", json);
}

async function carregarOsPorTecnico() {
  const res = await fetch("http://localhost:8000/os/por-tecnico");
  const json = await res.json();
  console.log("OS por técnico:", json);
}

// Exemplo de uso:
carregarResumoGeral();
carregarTotalPorPeriodo();
carregarPrincipaisCausas();
carregarOsPorTecnico();
