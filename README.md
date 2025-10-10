# 🚀 Jornada_Fast_ADOS

📊 Projeto de Análise de Dados das Ordens de Serviço – **Jornada 2025**

---

## 🎯 Objetivo do Projeto

O grupo responsável pela **Análise de Dados das Ordens de Serviço (ADOS)** tem como principal objetivo identificar padrões, gerar insights e criar alertas a partir das informações coletadas nas OSs.  
Através dessas análises, será possível prever falhas recorrentes em produtos e contribuir com melhorias nos processos internos da **Fast Gôndolas**.

---

## 🔍 Informações Iniciais a Serem Analisadas

As seguintes informações servirão como base para as análises iniciais:

- 🆔 ID da Ordem de Serviço (OS)  
- 🙋‍♂️ Solicitante  
- 📅 Data de criação da OS  
- 🛠 Produto ou serviço  
- 💰 Valor  
- 📌 Status da OS  
- 🔢 Número de série  

🔎 Uma das primeiras análises será a **quantidade de ordens de serviço por peça trocada**, ajudando a detectar padrões de falhas e comportamentos reincidentes.

---

## 📈 Estratégias de Análise

As análises previstas para o decorrer do projeto incluem:

- 🤖 Previsão de falhas em produtos (**análise preditiva**)  
- 🗺 Análise semanal de OSs por **localidade**  
- 🚦 Análise de **status** das OSs  
- 🔥 Análise por **prioridade** *(a definir)*  

---

## 🛠 Tecnologias Utilizadas

### ⚙️ Back-End

- 🐍 Python  
- ⚡ FastAPI  
- 🐳 Docker  

### 🖥 Front-End

- 🅰️ Angular  
- 🌐 .NET  

---

## 🗓 Sprints

### 🏁 Sprint

- Criação de um protótipo para o front.
- Ideias para realização das análises
## Plano A:

- Receber os dados através de um csv disponibilizado pela fast.
- Realizar a exploração de dados desse arquivo

## Plano B:

- Criação de dados inventados para servirem de base para criação da análise.

## Etapas para rodar esse projeto no VS Code
Use terminais do powershell para executar todos os passos abaixo.

- <u>Caso queira usar o container do Docker Desktop</u>: dentro da pasta JORNADA_FAST_ADOS, no terminal executar o comando `docker compose up --build`
- Abra o 2º terminal e execute `python -m uvicorn main:app --reload`
- Acesse no navegador a URL http://127.0.0.1:8000/docs

