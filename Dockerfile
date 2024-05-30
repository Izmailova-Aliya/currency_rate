FROM apache/airflow:2.4.3-python3.8
USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY --chown=airflow:airflow requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow

COPY --chown=airflow:airflow dags /opt/airflow/dags

EXPOSE 8080
