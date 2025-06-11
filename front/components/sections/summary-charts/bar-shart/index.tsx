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