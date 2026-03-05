# 🏛️ Pipeline de Dados: Precatórios TJPI

Este projeto implementa uma pipeline completa de engenharia de dados (RAW → SILVER → GOLD) para extração, normalização e carga de dados de precatórios do Tribunal de Justiça do Estado do Piauí (TJPI).

A solução automatiza a coleta de dados públicos do portal SAPRE, realiza limpeza e padronização de dados jurídicos e financeiros e persiste os registros em um banco PostgreSQL para análise posterior.

O pipeline foi testado com mais de **6.500 registros processados com sucesso**.

---

# 🚀 Arquitetura da Solução

A arquitetura segue o padrão corporativo de camadas de dados:

```
RAW (Bronze) → SILVER (Processed) → GOLD (PostgreSQL)
```

## Camadas do Pipeline

### 🟤 Ingestion (RAW)

* Scraper em Python utilizando **Requests + BeautifulSoup**
* Coleta automatizada dos dados do portal SAPRE do TJPI
* Paginação automática dos resultados
* Armazenamento de arquivos CSV brutos no filesystem
* Execução paralela utilizando `ThreadPoolExecutor`

---

### ⚪ Processing (SILVER)

* Consolidação dos CSVs coletados
* Padronização de colunas
* Limpeza de dados monetários
* Conversão de tipos numéricos
* Remoção de duplicidades
* Geração de dataset consolidado

---

### 🟡 Loaders (GOLD)

* Carga relacional no PostgreSQL
* Inserção incremental de registros
* Controle de duplicidade via chave lógica

Chave utilizada:

```
(numero_pje, tipo)
```

---

### 🧠 Orchestration

* Coordena execução sequencial das etapas
* Garante fluxo completo da pipeline
* Permite execução automática de todas as camadas

---

# 📁 Estrutura do Projeto

```
tjpi-data-pipeline/

pipeline/
├── ingestion/
│   └── scraper_tjpi_precatorios.py
│
├── processing/
│   └── transform_precatorios.py
│
├── loaders/
│   └── load_precatorios_postgres.py
│
└── orchestration/
    └── run_pipeline.py

database/
└── create_tables.sql

data/
├── raw/
│   └── precatorios/
└── processed/
    └── precatorios_tjpi.csv
```

---

# 🛠️ Tecnologias Utilizadas

* Python 3.10+
* Requests
* BeautifulSoup
* Pandas
* PostgreSQL
* Psycopg2
* ThreadPoolExecutor
* Git

---

# ⚙️ Configuração do Ambiente

## 1️⃣ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tjpi_precatorios
DB_USER=postgres
DB_PASSWORD=sua_senha
```

---

## 2️⃣ Instalação

```bash
git clone https://github.com/ssilvavvagner-bit/tjpi-data-pipeline.git
cd tjpi-data-pipeline

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

---

# 🗄️ Banco de Dados

Para testar a pipeline do zero é necessário:

1️⃣ Criar o banco PostgreSQL

```
CREATE DATABASE tjpi_precatorios;
```

2️⃣ Executar o script de criação das tabelas disponível em:

```
database/create_tables.sql
```

Esse script cria a estrutura necessária para a camada **GOLD**.

---

# ▶️ Execução da Pipeline

## Pipeline completa (recomendado)

```bash
python pipeline/orchestration/run_pipeline.py
```

Fluxo executado:

```
INGESTION
↓
PROCESSING
↓
LOAD
```

---

## Execução de Etapas Isoladas

### ⚪ Transformação (SILVER)

Requer que existam arquivos em:

```
data/raw/precatorios/
```

Executar:

```bash
python pipeline/processing/transform_precatorios.py
```

---

### 🟡 Carga no Banco (GOLD)

Requer:

* Dataset em `data/processed/`
* Banco criado
* `.env` configurado

Executar:

```bash
python pipeline/loaders/load_precatorios_postgres.py
```

---

# 📊 Modelagem de Dados

Tabela principal:

```
precatorios
```

Campos principais:

* posição na fila
* ente devedor
* ano do precatório
* natureza
* número do processo (PJe)
* tipo de prioridade
* valor do precatório

Controle de duplicidade:

```
(numero_pje, tipo)
```

---

# ✅ Resultados

* 6.500+ registros processados
* Coleta automatizada de 48 entes devedores
* Deduplicação de registros
* Pipeline modular em camadas
* Carga incremental no PostgreSQL

---

# 📌 Observações Técnicas

* Scraper utiliza paginação dinâmica do portal SAPRE.
* Execução paralela acelera coleta dos entes devedores.
* Transformação remove duplicidades antes da carga.
* Projeto preparado para expansão para outros tribunais.

---

# 👨‍💻 Autor

**Vagner Silva da Silva**
Desenvolvedor de Software | Engenharia de Dados (em formação)
Curso: Análise e Desenvolvimento de Sistemas ( em formação)