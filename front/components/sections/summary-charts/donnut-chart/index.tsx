import * as S from "./styles";

export function DonnutShart() {
  return (
      <S.BigVallueCard>
            <div className="chart-container">
                    <div className="chart-header">
                        <h3 className="chart-title">Employee Composition</h3>
                    </div>
                    <div className="donut-chart">
                        <div className="donut-container">
                            <div className="donut"></div>
                        </div>
                        <div className="donut-legend">
                            <div className="legend-item">
                                <div className="legend-color1"></div>
                                <span>55%</span>
                            </div>
                            <div className="legend-item">
                                <div className="legend-color2"></div>
                                <span>65%</span>
                            </div>
                            <div className="textinho">
                                Em Comparação Geral
                            </div>
                        </div>
                    </div>
                </div>
      </S.BigVallueCard>
  );
}