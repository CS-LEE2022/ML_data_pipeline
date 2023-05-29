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

def download_raw_data():

	if not os.path.exists(raw_data_path):
	    os.makedirs(raw_data_path)
	    
	os.environ['download_path'] = raw_data_path
	subprocess.run("kaggle datasets download -d jacksoncrow/stock-market-dataset -p $download_path", shell=True)
	#subprocess.run("unzip $download_path/stock-market-dataset.zip", shell=True)

	with zipfile.ZipFile(raw_data_path+'/stock-market-dataset.zip', 'r') as zip_ref:
	    zip_ref.extractall(raw_data_path)