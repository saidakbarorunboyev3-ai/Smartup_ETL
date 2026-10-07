# Smartup ETL

An automated ETL pipeline that extracts data from an API, cleans it with Python, and loads it into PostgreSQL. The workflow is orchestrated with **Apache Airflow** and runs in **Docker**.

## 📌 Overview

The pipeline processes three datasets:

- `customers`
- `products`
- `orders`

A single Airflow DAG (`smartup_etl`) runs all three tasks every day at **02:00 (Asia/Tashkent)**.

## 🔄 How It Works

```
API  →  Python (pandas, NumPy)  →  PostgreSQL  →  Power BI
         extract + clean            load            analysis
```

1. **Extract:** data is fetched from the API.
2. **Transform:** cleaning and type fixing with pandas and NumPy.
3. **Load:** cleaned tables are written to PostgreSQL.
4. **Orchestrate:** Airflow schedules and monitors every run.

## 🛠 Tech Stack

Python · pandas · NumPy · PostgreSQL · Apache Airflow · Docker · Power BI

## 📁 Project Structure

```
smartup/
├── dags/
│   ├── smartup/            # DAG definition
│   └── pipelines/          # customers.py, products.py, orders.py
├── config/
├── plugins/
├── logs/
├── docker-compose.yaml
└── .env.example
```

## ⚙️ Setup

**Requirements:** Docker Desktop and Git.

1. Clone the repository:
```bash
   git clone https://github.com/saidakbarorunboyev3-ai/Smartup_ETL.git
   cd Smartup_ETL/smartup
```
2. Create a `.env` file (see `.env.example`):
```
   AIRFLOW_UID=50000
```
3. Add your own API and database credentials in the config file. **Never commit real passwords.**
4. Start Airflow:
```bash
   docker compose up -d
```
5. Open the Airflow UI at `http://localhost:8080`.
6. Unpause the `smartup_etl` DAG, or trigger it manually.

## 📊 Results

*(Add a screenshot of the Airflow DAG graph here, and a Power BI dashboard if you have one.)*

```
![Airflow DAG](images/dag.png)
```

## 🚧 Future Improvements

- Add data quality checks
- Add email alerts on task failure
- Add incremental loading

## 📫 Author

**[O'rinboyev Saidakbar]**: [https://www.linkedin.com/in/saidakbar-o-runboyev-168023442] · [@saidakbar4751]
