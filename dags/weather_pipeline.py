from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "hanane",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "weather_pipeline",
    default_args=default_args,
    schedule="0 6 * * *",
    start_date=datetime(2026, 9, 14),
    catchup=False,
    tags=["weather", "etl"],
) as dag:

    t1 = BashOperator(task_id="extract_cities", bash_command="cd /opt/airflow/project && python extraction/cities.py")
    t2 = BashOperator(task_id="extract_weather", bash_command="cd /opt/airflow/project && python extraction/weather_api.py")
    t3 = BashOperator(task_id="clean", bash_command="cd /opt/airflow/project && python transformation/cleaning.py")
    t4 = BashOperator(task_id="features", bash_command="cd /opt/airflow/project && python transformation/features.py")
    t5 = BashOperator(task_id="load_postgres", bash_command="cd /opt/airflow/project && python load/postgres.py")

    t1 >> t2 >> t3 >> t4 >> t5