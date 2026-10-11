# 🏢 Smartup ETL

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-NumPy-150458?logo=pandas&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-orchestration-017CEE?logo=apacheairflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-4169E1?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-analytics-F2C811?logo=powerbi&logoColor=black)

An automated ETL pipeline that **extracts** data from an API, **cleans** it with Python, and **loads** it into PostgreSQL. The whole workflow is orchestrated with **Apache Airflow** and runs in **Docker**, so it starts with a single command and runs on a schedule without manual work.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup](#-setup)
- [Database Configuration (DB_URL)](#-database-configuration-db_url)
- [Running the Pipeline](#-running-the-pipeline)
- [Troubleshooting](#-troubleshooting)
- [Results](#-results)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 📖 Overview

The pipeline processes three datasets:

| Dataset | Description |
|---|---|
| `customers` | Customer records |
| `products` | Product catalog |
| `orders` | Customer orders |

A single Airflow DAG (`smartup_etl`) runs all three tasks every day at **02:00 (Asia/Tashkent)**. The `orders` task starts only after `customers` and `products` have finished successfully.

---

## 🔄 Architecture

```mermaid
flowchart LR
    A[API] -->|extract| B[Python<br/>pandas + NumPy]
    B -->|clean + fix types| C[(PostgreSQL)]
    C --> D[Power BI]
    E[Apache Airflow<br/>smartup_etl DAG] -. schedules and monitors .-> B
```

**DAG task order:**

```mermaid
flowchart LR
    run_customers --> run_orders
    run_products --> run_orders
```

1. **Extract:** data is fetched from the API.
2. **Transform:** cleaning and type fixing with pandas and NumPy.
3. **Load:** cleaned tables are written to PostgreSQL.
4. **Orchestrate:** Airflow schedules and monitors every run.

---

## 🛠 Tech Stack

**Python** · **pandas** · **NumPy** · **PostgreSQL** · **Apache Airflow** · **Docker** · **Power BI**

---

## 📁 Project Structure

```
smartup/
├── dags/
│   ├── smartup/            # DAG definition
│   └── pipelines/          # customers.py, products.py, orders.py, config.py
├── config/
├── plugins/
├── logs/                   # Airflow logs (not committed)
├── docker-compose.yaml
├── .env.example            # template for your environment variables
└── README.md
```

---

## ⚙️ Setup

**Requirements**

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (allocate at least **4 GB RAM** to Docker)
- [Git](https://git-scm.com/)
- A running **PostgreSQL** database

**Steps**

1. Clone the repository:

   ```bash
   git clone https://github.com/saidakbarorunboyev3-ai/Smartup_ETL.git
   cd Smartup_ETL/smartup
   ```

2. Create a `.env` file from the template:

   ```bash
   cp .env.example .env        # Windows PowerShell: Copy-Item .env.example .env
   ```

   ```env
   AIRFLOW_UID=50000
   FERNET_KEY=your_fernet_key   # optional
   ```

   > ⚠️ Save `.env` in **UTF-8** encoding. Use one variable per line with **no spaces** around `=` and no quotes.

   Generate a Fernet key (optional):

   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

3. Configure the database connection. See the next section 👇

---

## 🗄 Database Configuration (DB_URL)

The pipeline writes data to **your own PostgreSQL database**, so you must enter your connection details. Open `dags/pipelines/config.py` and set `DB_URL`:

```python
DB_URL = "postgresql+psycopg2://USERNAME:PASSWORD@HOST:5432/DATABASE"
```

| Placeholder | What to enter | Example |
|---|---|---|
| `USERNAME` | Your PostgreSQL user name | `postgres` |
| `PASSWORD` | Password of that user | `my_secret_password` |
| `HOST` | Where PostgreSQL is running | `host.docker.internal` |
| `5432` | PostgreSQL port | `5432` |
| `DATABASE` | Database name to load data into | `smartup_db` |

**Which HOST should I use?**

- PostgreSQL installed on **your computer** (Airflow runs in Docker): `host.docker.internal`
- PostgreSQL in **another container** of the same compose network: the **service name**
- PostgreSQL on a **remote server**: its IP address or domain name

> ⚠️ Do not use `localhost`. Inside a Docker container, `localhost` means the container itself, not your computer.

Create the database first if it does not exist yet:

```sql
CREATE DATABASE smartup_db;
```

> 🔒 **Never commit real passwords.** Keep `config.py` out of version control or read the URL from an environment variable.

If the pipeline also needs API credentials, add them to the same config file in the same way.

---

## ▶️ Running the Pipeline

1. Start Airflow:

   ```bash
   docker compose up -d
   docker compose ps
   ```

   The first start takes a few minutes. Wait until `airflow-apiserver` is `healthy`.

2. Open the Airflow UI at **http://localhost:8080**. The default credentials are defined in `docker-compose.yaml` (usually `airflow` / `airflow`).

3. Find the **`smartup_etl`** DAG, turn it **on** (new DAGs are paused by default) and click **Trigger**.

4. When all tasks are green, check the data in PostgreSQL:

   ```sql
   SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
   ```

5. Stop everything when you are done:

   ```bash
   docker compose down
   ```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `failed to connect to the docker API` | Docker Desktop is not running. Start it and wait until it is ready. |
| `Bind for 0.0.0.0:8080 failed: port is already allocated` | Another program uses port 8080. Stop it or change the mapping to `8081:8080`. |
| `failed to read .env ... unexpected character` | `.env` is saved as UTF-16. Re-save it as **UTF-8**. |
| `ModuleNotFoundError` | A package is missing in the Airflow image. Add it via `_PIP_ADDITIONAL_REQUIREMENTS` in `docker-compose.yaml`. |
| Database connection refused | Do not use `localhost` in `DB_URL`. Use `host.docker.internal`. |
| A task stays `running` for a long time | A table may be locked (open in pgAdmin or Power BI). Close the connection and clear the task. |

---

## 📊 Results

<!--
Add your screenshots to an `images/` folder, then remove this comment:

![Airflow DAG](images/dag.png)
![Power BI Dashboard](images/dashboard.png)
-->

The DAG runs `customers` and `products` in parallel, then `orders`. The cleaned tables in PostgreSQL feed Power BI reports.

---

## 🚧 Future Improvements

- [ ] Data quality checks
- [ ] Email alerts on task failure
- [ ] Incremental loading
- [ ] Unit tests for the cleaning functions

---

## 📫 Author

**O'rinboyev Saidakbar**

[![Telegram](https://img.shields.io/badge/Telegram-@saidakbar4751-26A5E4?logo=telegram&logoColor=white)](https://t.me/saidakbar4751)
[![GitHub](https://img.shields.io/badge/GitHub-saidakbarorunboyev3--ai-181717?logo=github&logoColor=white)](https://github.com/saidakbarorunboyev3-ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Saidakbar-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saidakbar-o-runboyev-168023442)

---

⭐ If you find this project useful, please give it a star!
