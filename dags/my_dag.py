from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime

import pandas as pd
import numpy as np
import os
import glob
import re
import pyarrow as pa
import pyarrow.parquet as pq
import time
import subprocess
import pickle
import kaggle
import sklearn
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_error

import billiard as multiprocessing
import zipfile
from tasks import download_raw_data
from tasks import process_raw_data
from tasks import feature_engineering
from tasks import ML_model_training_polyreg



def run_download_raw_data():
    download_raw_data.download_raw_data()

def run_process_raw_data():
    process_raw_data.process_raw_data()

def run_feature_engineering():
    feature_engineering.feature_engineering()

def run_ML_model_training_polyreg():
    ML_model_training_polyreg.ML_model_training()



with DAG(
    dag_id='ML_data_pipeline_demo',
    start_date=datetime.now(),
    schedule_interval=None
) as dag:

    # download_raw_data_task = PythonOperator(
    #     task_id='download_raw_data',
    #     python_callable=run_download_raw_data,
    # )

    # process_raw_data_task = PythonOperator(
    #     task_id='process_raw_data',
    #     python_callable=run_process_raw_data,
    # )

    # feature_engineering_task = PythonOperator(
    #     task_id='feature_engineering',
    #     python_callable=run_feature_engineering,
    # )

    model_training_task = PythonOperator(
        task_id='model_training',
        python_callable=run_ML_model_training_polyreg,
    )
    

#download_raw_data_task >> process_raw_data_task >> feature_engineering_task >> 
model_training_task
