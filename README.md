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

** RESULTS
<img width="1230" alt="image" src="https://github.com/Izmailova-Aliya/currency_rate/assets/59693961/d53294ce-f83e-4058-8d61-ba2741b3571d">

<img width="777" alt="image" src="https://github.com/Izmailova-Aliya/currency_rate/assets/59693961/c0c33340-4b9b-417b-8996-a482e3bfdf7e">



