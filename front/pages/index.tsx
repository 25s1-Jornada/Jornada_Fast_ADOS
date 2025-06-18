import { api } from '@/services/api';
import { getApi } from '@/interfaces/api';

import { Header } from '@/layout/header';
import { Sidebar } from '@/layout/sidebar';
import { SummaryCards } from  '@/sections/summary-cards'
import { SummarySharts } from '@/sections/summary-charts'
import { TableSection } from '@/sections/table-section';

import * as S from '@/pages/home'

export default function Home() {
  return (
    <S.HomePage>  
      <Sidebar/>
      <main className='main-content'>
        <Header/>
        <SummaryCards/>
        <SummarySharts/>
        <TableSection/>
      </main>
    </S.HomePage>
 
  );
}


async function fetchData() {
  try {
    const response = await api.get<getApi>('/fast/OS/analise');
    console.log(response.data);
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
  }
}
