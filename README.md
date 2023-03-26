# LTA ELT

### Intro
![alt text](https://github.com/kwquan/LTA/blob/main/process.png)
Tools: Airflow, Docker, PostgreSQL
Prerequisites:
Airflow, PostgreSQL, PgAdmin, Docker

This project is an end-to-end ELT[Extract,Load,Transform] pipeline that does the following:
1) Calls the LTA API to get CrowdLevel for each station on the East-West line[https://datamall.lta.gov.sg/content/dam/datamall/datasets/LTA_DataMall_API_User_Guide.pdf]
2) Saves the data to volume as temp.tsv[under dags]
3) Creates stations table in PostgreSQL if it doesn't exists
4) Pushes temp.tsv to stations table
5) Checks if there are at least 30 minutes worth of records. If yes, print out stations whose CrowdLevel has changed in the past 30 minutes

### Set-up:

![alt text](https://github.com/kwquan/LTA/blob/main/folders.png)
1) Create a folder called 'Materials'
2) Create a subfolder called sql
3) Place train_dag.py under 'dags'
4) Place create_table.sql & check_table.sql under 'sql'
5) Ensure docker-compose.yaml in 'Materials'

Edit train_dag.py
![alt text](https://github.com/kwquan/LTA/blob/main/api_key.png)
1) Change API key to your own[sign-up on LTA website for personal key]


