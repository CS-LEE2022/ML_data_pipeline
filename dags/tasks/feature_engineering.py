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

dockerfile_directory = '/opt/airflow/'
base_path = os.path.join(dockerfile_directory, 'data')
raw_data_path = os.path.join(base_path, 'raw_data')

def define_schema(schema_type):
    schema = pa.schema([
        pa.field('Symbol',       pa.string()),
        pa.field('Security Name', pa.string()),
        pa.field('Date', pa.date32()),
        pa.field('Open', pa.float64()),
        pa.field('High', pa.float64()),
        pa.field('Low',  pa.float64()),
        pa.field('Close',pa.float64()),
        pa.field('Adj Close', pa.float64()),
        pa.field('Volume',    pa.float64()) 
        ])
    
    if schema_type == 'raw_data_processing':
        schema = pa.schema([
                pa.field('Symbol',       pa.string()),
                pa.field('Security Name', pa.string()),
                pa.field('Date', pa.date32()),
                pa.field('Open', pa.float64()),
                pa.field('High', pa.float64()),
                pa.field('Low',  pa.float64()),
                pa.field('Close',pa.float64()),
                pa.field('Adj Close', pa.float64()),
                pa.field('Volume',    pa.float64()) 
                ])
        return schema
    
    elif schema_type == 'feature_engineering':
        schema = pa.schema([
                pa.field('Symbol',       pa.string()),
                pa.field('Date', pa.date32()),
                pa.field('Volume',    pa.float64()),
                pa.field('vol_moving_avg',pa.float64()),
                pa.field('adj_close_rolling_med', pa.float64())
                ])
        return schema
    else:
        print("Valid schema type is raw_data_processing or feature_engineering")
        return None

def feature_engineering_function(filename):
    
    # read stock/etf/meta files
    df_temp = pd.read_parquet(filename, columns=['Symbol', 'Date', 'Volume', 'Adj Close']).sort_values('Date')
    df_temp['vol_moving_avg'] = df_temp['Volume'].rolling(30).mean()
    df_temp['adj_close_rolling_med'] = df_temp['Adj Close'].rolling(30).mean()
    df_temp = df_temp[['Symbol', 'Date', 'Volume', 'vol_moving_avg','adj_close_rolling_med']]

    feature_schema = define_schema('feature_engineering')
    symb = re.split('/|\.', filename)[-2]
    fn = symb + '_feature_engineering.parquet'
    
    # pq.write_to_dataset automatically append to existing parquet file
    table = pa.Table.from_pandas(df_temp, schema=feature_schema)
    pq.write_to_dataset(table , 
                        root_path=f'{base_path}/feature_engineering.parquet',
                        partition_filename_cb=lambda i: fn)
    del table
    del df_temp


def feature_engineering():
    processed_files = glob.glob(os.path.join(f'{base_path}/processed.parquet', '*.parquet'))

    num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)

    # Apply the process_function to each data element using multiprocessing
    pool.map(feature_engineering_function, processed_files)
  
    # Close the multiprocessing pool
    pool.close()
    pool.join()
    