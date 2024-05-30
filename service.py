import os
import requests
import psycopg2
import click
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
API_KEY = os.getenv('API_KEY')

def get_exchange_rates(currencies):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url)
    data = response.json()
    return {currency: data['conversion_rates'][currency] for currency in currencies}

def store_in_db(rates, date):
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO currency_rates (ds, country_id, currency, rate)
        VALUES (%s, %s, %s, %s)
    """
    country_mapping = {'KZT': 1, 'UZS': 3, 'AZN': 5, 'MYR': 6, 'KGS': 4}
    for currency, rate in rates.items():
        country_id = country_mapping.get(currency)
        cursor.execute(insert_query, (date, country_id, currency, rate))
    
    connection.commit()
    cursor.close()
    connection.close()

@click.command()
@click.option('--currencies', required=True, help='KZT,UZS,AZN,MYR')
@click.option('--date', required=True, help='YYYY-MM-DD')
def main(currencies, date):
    currencies_list = currencies.split(',')
    rates = get_exchange_rates(currencies_list)
    store_in_db(rates, date)
    print(f'Successful {currencies}, {date}')

if __name__ == '__main__':
    main()
