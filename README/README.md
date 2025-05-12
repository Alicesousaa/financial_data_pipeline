<<<<<<< HEAD
## 🧠 Estratégia de Coleta de Dados

### 📊 Índice de Serviços Caixin Chinês

📌 **Fonte oficial**:  
[https://br.investing.com/economic-calendar/chinese-caixin-services-pmi-596]
O desafio solicitava dados mensais desde **2012 até hoje**, mas:

- O gráfico no site não permite extração direta de dados completos.
- Bibliotecas como `investpy`, que anteriormente continham essa série, **estão fora do ar** ou foram descontinuadas.
- Outras APIs públicas gratuitas não oferecem essa série histórica completa.

🛠️ **Decisão**:  
Para garantir o mínimo de dados disponíveis, utilizei **Selenium** para extrair diretamente os valores da tabela no site. Ainda que o intervalo esteja limitado, essa abordagem permite uma coleta automatizada dos dados disponíveis atualmente.  
O resultado é salvo como:  
`caixin_services_china_selenium.csv`

---

### 💱 USD/CNY Histórico

📌 **Fonte oficial**:  
[https://br.investing.com/currencies/usd-cny]

A coleta de dados históricos desde **1991 até hoje** foi mais desafiadora:

#### 1. Tentativa com Selenium + PyAutoGUI

Tentei extrair os dados diretamente da [página histórica](https://br.investing.com/currencies/usd-cny-historical-data) utilizando automações com `Selenium`, `PyAutoGUI` e até manipulações via JavaScript.  
No entanto, o filtro de datas dessa interface não respondia adequadamente a nenhum desses métodos — ele é altamente dinâmico e dependente de interações visuais específicas, o que tornava a automação instável e inviável sem uma VM dedicada.

> 🧪 O trecho dessa abordagem está disponível, nome do arquivo é `caixin_services_china_site` apenas para fins de avaliação técnica.

#### 2. Decisão final — API da Alpha Vantage

Para garantir a confiabilidade, optei por utilizar a [API gratuita da Alpha Vantage](https://www.alphavantage.co/documentation/) com a função `FX_MONTHLY`, que fornece a série histórica do par USD/CNY em base mensal.

Essa abordagem foi:

- Mais limpa e robusta
- Compatível com automação via scripts
- Sem necessidade de simulações visuais

O resultado é salvo como:  
`usd_cny_data_alpha_vantage.csv`
=======
# financial_data_pipeline
>>>>>>> ee907feae69170c01f1576d5d710cfd006b298f1
