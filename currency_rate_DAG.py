from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

def get_exchange_rates(currencies):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()
    print('API response:', data)
    
    if data.get('result') != 'success':
        raise Exception(f"API error: {data.get('error-type')} - {data.get('extra-info')}")
    
    conversion_rates = data['conversion_rates']
    return {currency: conversion_rates[currency] for currency in currencies}

def store_in_db(**context):
    date = context['ds']
    currencies = ['KZT', 'UZS', 'AZN', 'MYR', 'KGS']
    print('Currencies:', currencies)
    
    rates = get_exchange_rates(currencies)
    
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    
    insert_query = """
        INSERT INTO currency_rates (ds, country_id, currency, rate)
        VALUES (%s, %s, %s, %s)
    """
    print('Insert query:', insert_query)
    
    country_mapping = {'KZT': 1, 'UZS': 3, 'AZN': 5, 'MYR': 6, 'KGS': 4}
    
    for currency, rate in rates.items():
        country_id = country_mapping.get(currency)
        cursor.execute(insert_query, (date, country_id, currency, rate))
    
    connection.commit()
    cursor.close()
    connection.close()

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'currency_dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',
    start_date=datetime(2024, 5, 30),
    catchup=False,
)

currency_rates = PythonOperator(
    task_id='currency_rates',
    python_callable=store_in_db,
    provide_context=True,
    dag=dag,
)

currency_rates
