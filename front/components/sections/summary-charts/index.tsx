import { DonnutShart } from "./donnut-chart"
import { BarShart } from "./bar-shart"
import * as S from "./styles";

export function SummarySharts() {
  return (
      <S.SummarySharts>
            <BarShart/>
            <DonnutShart/>
      </S.SummarySharts>
  );
}