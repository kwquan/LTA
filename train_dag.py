from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.sql import BranchSQLOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime
from airflow.hooks.postgres_hook import PostgresHook
import requests
import pandas as pd
# import plotly.graph_objects as go
  
  
def _get_request(ti):
    params = {"TrainLine":"EWL"}
    headers = {"AccountKey":"54UEKyywSWqaRTAqcoUqPQ==", "accept":"application/json"}
    response = requests.get("http://datamall2.mytransport.sg/ltaodataservice/PCDRealTime", headers=headers, params=params)
    ti.xcom_push(key='response', value=response.json()['value'])

def _process_data(ti):
    file = pd.json_normalize(ti.xcom_pull(key='response', task_ids='get_request'))
    file['Number'] = file['Station'].map(lambda x:int(x[2:]))
    file.sort_values('Number',inplace=True)
    file.drop('Number',axis=1,inplace=True)
    file.to_csv("dags/temp.tsv",  header=None, index=None, sep='\t')
    postgres_sql_upload = PostgresHook(postgres_conn_id="postgres_db")
    postgres_sql_upload.bulk_load('stations(Station,StartTime,EndTime,CrowdLevel)', 'dags/temp.tsv')
    return True

def _print_stations():
    hook = PostgresHook(postgres_conn_id="postgres_db")
    stations = hook.get_pandas_df(sql="SELECT Station from stations group by Station having count(distinct CrowdLevel) > 1")
    print(stations)

def _print_message():
    print("Insufficient records!")

# def _update_plot(dataframe):
#     color_map = {"l":"green", "m":"yellow", "h":"red", "NA":"white"}
#     colors = [color_map[x] for x in dataframe["CrowdLevel"]]
#     y = [1]*31
#     start_time, end_time = dataframe["StartTime"][0].split("T")[1].split("+")[0], dataframe["EndTime"][0].split("T")[1].split("+")[0]
#     fig = go.Figure(data=[go.Scatter(x=dataframe["Station"], y=y,marker_color=colors)])
#     fig.update_layout(title_text='Platform Crowd Density: ' + start_time + ' to ' + end_time)
#     fig.show()

with DAG('train_dag', start_date=datetime(2023,2,15,3,40,0,0), 
    schedule_interval='*/10 * * * *', catchup=False) as dag:
        
    get_request = PythonOperator(
        task_id='get_request',
        python_callable=_get_request
    )

    process_data = PythonOperator(
        task_id='process_data',
        python_callable=_process_data
    )

    create_table = PostgresOperator(
        sql = "sql/create_table.sql",
        task_id='create_table',
        postgres_conn_id = "postgres_db"
    )

    check_table = BranchSQLOperator(
        sql = "sql/check_table.sql",
        task_id="check_table",
        conn_id = "postgres_db",
        follow_task_ids_if_true="t1",
        follow_task_ids_if_false="t2" 
    )

    t1 = PythonOperator(
        task_id='t1',
        python_callable = _print_stations
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=_print_message
    )

  
    get_request >> create_table >> process_data >> check_table >> [t1,t2]