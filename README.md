# Projeto de Extração de Dados Econômicos

## Visão Geral

Este projeto tem como objetivo construir uma **pipeline automatizada** para a **extração mensal de dados econômicos**, com armazenamento no **Google Cloud Storage (GCS)** e orquestração via **Google Cloud Composer**, utilizando **Terraform** para gerenciamento da infraestrutura.

## Estrutura do Projeto

1. **Raspagem de Dados**
   - A extração começou com foco na **China**, porém a API *Investpy* e outras alternativas estavam fora do ar.
   - Como alternativa, foi utilizada a biblioteca **Selenium** para realizar a raspagem diretamente de páginas HTML.
   - A mesma abordagem foi tentada para obter a cotação **USD/JPY**, mas enfrentou desafios específicos.

2. **Desafios na Raspagem**
   - A página da China não apresentava mais dados históricos, inviabilizando a raspagem.
   - A fonte de dados foi então alterada para a **Índia**, por meio da página de taxa de juros no **Investing.com**.
   - A cotação USD/JPY apresentava complexidade adicional, pois o filtro de datas era feito por **JavaScript**, dificultando a automação.
   - Tentativas com `PyAutoGUI` não tiveram sucesso devido à execução headless da aplicação. O código foi mantido no repositório como referência.

3. **Solução Implementada**
   - Para o câmbio **USD/JPY**, foi utilizada uma **API confiável** com dados estruturados.
   - Para a **Índia**, a raspagem foi mantida com o **Selenium**, que interage com o site e coleta os dados corretamente.

4. **Automação com Google Cloud Composer**
   - Utilizando o **Airflow**, a pipeline foi configurada para execução **mensal**.
   - O DAG realiza a raspagem dos dados e armazena o resultado em um bucket no **GCS**.

5. **Gerenciamento da Infraestrutura com Terraform**
   - O **Terraform** foi utilizado para criar e manter a infraestrutura, incluindo o ambiente do Cloud Composer e o bucket GCS.
   - Isso garante consistência, reprodutibilidade e facilidade de manutenção.

---

## Detalhamento da Implementação

### 1. Extração de Dados com Selenium

A raspagem é feita com **Selenium** em modo **headless** (sem interface gráfica), o que permite execução em ambientes como containers ou servidores remotos.

- **Configuração do navegador**: otimizada para execução invisível e segura.
- **Interação com o site**: aguarda o carregamento dos dados e simula cliques no botão "Ver mais" para carregar a tabela completa.
- **Processamento**: os dados são extraídos como tabela, convertidos em `pandas.DataFrame` e filtrados (a partir de 2012).

### 2. Armazenamento no Google Cloud Storage

Após a extração:

- O arquivo CSV é salvo localmente e enviado para o bucket:
  - **Caminho local**: `/home/airflow/gcs/data`
  - **Bucket**: `us-central1-raspagem-suzano-bucket`

### 3. Orquestração com Airflow

O DAG contém duas tarefas principais:

1. `get_caixin_selenium()` – realiza a raspagem dos dados.
2. `LocalFilesystemToGCSOperator` – envia o arquivo CSV ao GCS.

A DAG está agendada para rodar **mensalmente**, garantindo atualização periódica dos dados.

### 4. Infraestrutura com Terraform

A infraestrutura foi provisionada com **Terraform**, incluindo:

- Criação do ambiente **Google Cloud Composer**.
- Configuração do **bucket GCS**.
- Definições de recursos versionáveis e reutilizáveis, seguindo boas práticas de IaC (*Infrastructure as Code*).

---

## Melhorias Futuras

- **Monitoramento e alertas**: integração com ferramentas de observabilidade para acompanhar falhas e executar *retries* automaticamente.
- **Tratamento de erros**: tornar o processo mais robusto frente a mudanças nas páginas, falhas de rede ou API.
- **Versionamento de dados**: implementar versionamento no GCS para preservar cópias anteriores dos dados.

---

## Conclusão

Este projeto permite a **extração automática e mensal** de dados econômicos da Índia, com uma solução robusta utilizando **Selenium** para raspagem de dados, **Airflow** para automação e **Terraform** para gerenciamento de infraestrutura.

Apesar dos desafios iniciais, a solução atual é confiável, escalável e pode ser facilmente adaptada para novas fontes de dados no futuro.

