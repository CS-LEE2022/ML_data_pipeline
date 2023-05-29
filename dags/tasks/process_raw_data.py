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
        return schema
    
    elif schema_type == 'feature_engineering':
        feature_schema = schema.append(pa.field('vol_moving_avg',pa.float64())
                              ).append(pa.field('adj_close_rolling_med', pa.float64()))
        return feature_schema
    else:
        print("Valid schema type is raw_data_processing or feature_engineering")
        return None


def process_function(filename, meta_file):

    df_temp = pd.read_csv(filename, index_col=None, header=0, parse_dates=['Date'])
    df_meta = pd.read_csv(meta_file, sep = ',', index_col=None, header=0)
    
    # process the raw data in the desired format
    symb = re.split('/|\.', filename)[-2]
    df_temp.insert(0, 'Symbol', symb)
    
    meta_cols = ['Symbol', 'Security Name']
    final_cols = meta_cols + [x for x in list(df_temp.columns) if x != 'Symbol']

    df_temp = df_temp.merge(df_meta[meta_cols], on='Symbol', how='left')[final_cols]
    
    # pq.write_to_dataset automatically append to existing parquet file
    schema =  define_schema('raw_data_processing')
    fn = symb + '_processed.parquet'
    table = pa.Table.from_pandas(df_temp, schema=schema)
    pq.write_to_dataset(table , 
                        root_path=f'{base_path}/processed.parquet',
                        partition_filename_cb=lambda i: fn)


def process_raw_data():
    
    stock_files = glob.glob(os.path.join(f'{raw_data_path}/stocks' , "*.csv"))
    etf_files = glob.glob(os.path.join(f'{raw_data_path}/etfs' , "*.csv"))
    files = stock_files + etf_files  
    meta_file = f'{raw_data_path}/symbols_valid_meta.csv'

    num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)

    # Apply the process_function to each data element using multiprocessing
    pool.starmap(process_function, [(file, meta_file) for file in files[:1000]])  # 100 files: 5.47s
    #pool.map(process_function, files[:100]) # 100 files: 5.48s

    # Close the multiprocessing pool
    pool.close()
    pool.join()

    
