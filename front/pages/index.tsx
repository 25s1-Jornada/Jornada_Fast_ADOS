import { SummaryCards } from  '@/sections/summary-cards'
import { SummarySharts } from '@/sections/summary-charts'

import * as S from '@/pages/home'

export default function Home() {
  return (
   <>
      <S.HomePage>
          <SummaryCards/>
          <SummarySharts/>
      </S.HomePage>
   </>
 
  );
}
