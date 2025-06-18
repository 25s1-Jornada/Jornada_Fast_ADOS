export interface getApi {
  "  Análise semanal de OSs por localidade": AnliseSemanalDeOssPorLocalidade
  "   Sazonalidade": Sazonalidade
  "    Análise de status das OSs": AnliseDeStatusDasOss
  " Análise por prioridade": AnlisePorPrioridade
  "Total O.S por mês": TotalOSPorMs
}

export interface AnliseSemanalDeOssPorLocalidade {
  "Distribuição geográfica": DistribuioGeogrfica
  "Principais cidades com mais OSs": string[]
}

export interface DistribuioGeogrfica {
  SP: string
  RJ: string
  SC: string
  PR: string
  PE: string
  MG: string
  BA: string
  CE: string
  RS: string
  MT: string
  ES: string
  SE: string
  PB: string
  MA: string
  DF: string
  GO: string
  AP: string
  AM: string
  MS: string
  TO: string
  AL: string
  AC: string
  RN: string
  RO: string
  PA: string
}

export interface Sazonalidade {
  "Maior volume em meses quentes": string
  "Pico em nov/dez": string
}

export interface AnliseDeStatusDasOss {
  Distribuição: Distribuio
  "Tempo médio de resolução": TempoMdioDeResoluo
  "Principais causas": PrincipaisCausas
}

export interface Distribuio {
  Garantia: number
  "Garantia Estendida": number
  "Fora Garantia": number
}

export interface TempoMdioDeResoluo {
  Garantia: string
  "Fora da garantia": string
  Estrutura: string
  Refrigeração: string
}

export interface PrincipaisCausas {
  Refrigeração: number
  Iluminação: number
  Estrutura: number
  Transporte: number
}

export interface AnlisePorPrioridade {
  "Clientes que demandam maior atenção": ClientesQueDemandamMaiorAteno
}

export interface ClientesQueDemandamMaiorAteno {
  "Atacadão S/A": string
  "A. Angeloni & Cia": string
  "Ancora Distribuidora": string
  "Armazém do Grão": string
}

export interface TotalOSPorMs {
  Janeiro: number
  Fevereiro: number
  Março: number
  Abril: number
  Maio: number
  Junho: number
  Julho: number
  Agosto: number
  Setembro: number
  Outubro: number
  Novembro: number
  Dezembro: number
}
