/*
import * as S from "./styles";

export function BarShart() {
  return (
      <S.BarShart>
        <div className="chart-container">
            <div className="chart-header">
                <h3 className="chart-title">Total de O.S por Período</h3>
                <div className="chart-filter">
                    <span style={{color: "#2c5aa0;"}}>■</span>
                    <span>Total de O.S</span>
                    <button className="filter-btn active">Este mês</button>
                </div>
            </div>
                <div className="bar-chart">
                    <div className="bar" style={{ height: '60%' }}></div>
                    <div className="bar" style={{ height: '80%' }}></div>
                    <div className="bar" style={{ height: '70%' }}></div>
                    <div className="bar" style={{ height: '90%' }}></div>
                    <div className="bar" style={{ height: '50%' }}></div>
                    <div className="bar" style={{ height: '85%' }}></div>
                    <div className="bar" style={{ height: '95%' }}></div>
                    <div className="bar highlighted" style={{ height: '100%' }}></div>
                    <div className="bar" style={{ height: '75%' }}></div>
                    <div className="bar" style={{ height: '65%' }}></div>
                    <div className="bar" style={{ height: '55%' }}></div>
                    <div className="bar" style={{ height: '88%' }}></div>
                </div>
        </div>
      </S.BarShart>
  );
}
*/
import { useEffect, useState } from "react";
import { api } from "@/services/api";
import * as S from "./styles";

const MESES = [
  "Janeiro", "Fevereiro", "Março", "Abril",
  "Maio", "Junho", "Julho", "Agosto",
  "Setembro", "Outubro", "Novembro", "Dezembro"
];

export function BarShart() {
  const [dadosMensais, setDadosMensais] = useState<{ mes: string, valor: number, altura: number }[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await api.get("/fast/OS/analise", {
          params: { ano: 2023, mes: 6 }
        });

        const totalOS = response.data["Total O.S por mês"];

        // Ordena os meses de janeiro a dezembro
        const ordenado = MESES.map(mes => ({
          mes,
          valor: totalOS[mes] || 0
        }));

        const max = Math.max(...ordenado.map(item => item.valor), 1); // evita divisão por 0
        const comAlturas = ordenado.map(item => ({
          ...item,
          altura: Math.round((item.valor / max) * 100)
        }));

        setDadosMensais(comAlturas);
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      }
    }

    fetchData();
  }, []);

  return (
    <S.BarShart>
      <div className="chart-container">
        <div className="chart-header">
          <h3 className="chart-title">Total de O.S por Período</h3>
          <div className="chart-filter">
            <span style={{ color: "#2c5aa0" }}>■</span>
            <span>Total de O.S</span>
            <button className="filter-btn active">Ano {new Date().getFullYear()}</button>
          </div>
        </div>
        <div className="bar-chart">
          {dadosMensais.map((item, index) => (
            <div key={index} className="bar-wrapper">
              <div
                className={`bar ${item.altura === 100 ? "highlighted" : ""}`}
                style={{ height: `${item.altura}%`,
                         width: "20px",
                         backgroundColor: "#2c5aa0",
                         borderRadius: "4px 4px 0 0" }}
                title={`${item.valor} O.S`}
              ></div>
              <span className="bar-label">{item.mes.slice(0, 3)}</span>
            </div>
          ))}
        </div>
      </div>
    </S.BarShart>
  );
}
