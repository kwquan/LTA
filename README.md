# LTA ELT

### Intro
![alt text](https://github.com/kwquan/LTA/blob/main/process.png)
Tools: Airflow, Docker, PostgreSQL
Prerequisites:
Airflow, PostgreSQL, PgAdmin, Docker

This project is an end-to-end ELT[Extract,Load,Transform] pipeline that does the following:
1) Calls the LTA API to get CrowdLevel for each station on the East-West line[every 10 minutes] [https://datamall.lta.gov.sg/content/dam/datamall/datasets/LTA_DataMall_API_User_Guide.pdf]
2) Saves the data to volume as temp.tsv[under dags]
3) Creates stations table in PostgreSQL if it doesn't exists
4) Pushes temp.tsv to stations table
5) Checks if there are at least 30 minutes worth of records. If yes, print out stations whose CrowdLevel has changed in the past 30 minutes

### Set-up

![alt text](https://github.com/kwquan/LTA/blob/main/folders.png)
1) Create a folder called 'Materials'
2) Create a subfolder called sql
3) Place train_dag.py under 'dags'
4) Place create_table.sql & check_table.sql under 'sql'
5) Ensure docker-compose.yaml in 'Materials'

Edit train_dag.py
![alt text](https://github.com/kwquan/LTA/blob/main/api_key.png)
1) Change API key to your own[sign-up on LTA website for personal key]

Edit docker-compose.yaml
![alt text](https://github.com/kwquan/LTA/blob/main/docker_compose_1.png)
![alt text](https://github.com/kwquan/LTA/blob/main/docker_compose_2.png)
1) Edit PostgreSQL username, password & db as desired
2) Edit PGAdmin email & password as desired

### Run
![alt text](https://github.com/kwquan/LTA/blob/main/create_db_1.png)
![alt text](https://github.com/kwquan/LTA/blob/main/create_db_2.png)

1) Open up Visual Studio Code terminal & run 'docker-compose up -d'
2) Go to PgAdmin page on port 15432, login & create database
3) Go to Airflow page on port 8080, login & run train_dag.py
4) If successful, graph view should be similar to process.png

### Results
![alt text](https://github.com/kwquan/LTA/blob/main/postgres_results.png)
![alt text](https://github.com/kwquan/LTA/blob/main/airflow_results.png)

1) PostgreSQL query results similar to postgres_results.png
2) Airflow log results similar to airflow_results.png[for task t1]
3) In the examples above, I have 30 minutes worth of data[93 rows] in my stations table. The log for task t1 prints 'EW29' as the only station whose 
CrowdLevel has changed in the past 30 minutes
