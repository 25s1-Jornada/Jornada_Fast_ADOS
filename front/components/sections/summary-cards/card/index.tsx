import * as S from "./styles";

export function SmallVallueCard() {
  return (
      <S.SmallVallueCard>
            <div className="card-header">
                <span className="card-title">Total de Produtos</span>
                <span className="card-trend trend-positive">+2.0%</span>
            </div> 
            
            <div className="card-value">1000</div>
            <div className="card-subtitle">Produtos Cadastrados</div>
      </S.SmallVallueCard>
  );
}