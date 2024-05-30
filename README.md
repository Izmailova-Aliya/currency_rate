# currency_rate
This project sets up an Apache Airflow service using Docker to fetch and store currency exchange rates daily from an external API into a PostgreSQL database. 

We run commands one by one

1. docker build -t regidr0n/airflow_currency:latest .
2. docker run -d -p 8080:8080 regidr0n/airflow_currency:latest
3. docker-compose up -d
4. docker-compose run --rm airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email email@gmail.com
5. python3 service.py --currencies KZT,UZS,AZN,MYR,KGS --date 2024-05-30


DockerHub
https://hub.docker.com/repositories/regidr0n



