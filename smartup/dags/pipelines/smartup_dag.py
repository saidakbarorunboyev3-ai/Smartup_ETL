import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="smartup_etl",
    start_date=pendulum.datetime(2026, 10, 1, tz="Asia/Tashkent"),
    schedule="0 14 * * *",        
    catchup=False,
     default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:

    run_customers = BashOperator(
        task_id="run_customers",
        bash_command="python customers.py",
        cwd="/opt/airflow/dags/pipelines",
    )

    run_products = BashOperator(
        task_id="run_products",
        bash_command="python products.py",
        cwd="/opt/airflow/dags/pipelines",
    )

    run_orders = BashOperator(
        task_id="run_orders",
        bash_command="python orders.py",
        cwd="/opt/airflow/dags/pipelines",
    )

    [run_customers, run_products] >> run_orders

