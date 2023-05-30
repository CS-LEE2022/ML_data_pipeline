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
from datetime import datetime

import billiard as multiprocessing
import zipfile

dockerfile_directory = '/opt/airflow/'
base_path = os.path.join(dockerfile_directory, 'data')
raw_data_path = os.path.join(base_path, 'raw_data')

def ML_model_training_polyreg(data, feature, target, model_filename):
    X = data[feature]
    y = data[target]

    poly = PolynomialFeatures(degree=2, include_bias=True)
    poly_features = poly.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(poly_features, y, test_size=0.2, random_state=42)

    poly_reg_model = LinearRegression()
    poly_reg_model.fit(X_train, y_train)
    poly_reg_y_predicted = poly_reg_model.predict(X_test)
    poly_reg_rmse = np.sqrt(mean_squared_error(y_test, poly_reg_y_predicted))
    
    # save the model
    pickle.dump(poly_reg_model, open(model_filename, 'wb'))

    return poly_reg_rmse

def ML_model_training():

    data = pd.read_parquet(f'{base_path}/feature_engineering.parquet')
    data_avg = data.groupby('Date')[['vol_moving_avg', 'adj_close_rolling_med', 'Volume']].mean()

    feature=['vol_moving_avg', 'adj_close_rolling_med']
    target='Volume'

    data_avg = data_avg[feature+[target]].dropna()

    model_path = f'{base_path}/trained_model'
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    model_filename = f'{model_path}/ml_model.pkl'

    poly_reg_rmse = ML_model_training_polyreg(data_avg, feature, target, model_filename)

    # write to log file
    ts = str(datetime.now())
    log_string = 'Timestamp: {:s},  RMSE: {:.2f}. \n'.format(ts, poly_reg_rmse)
    with open(f'{model_path}/model_training_log.txt', mode='a') as log_file:
        log_file.write(log_string)

    return ('The Trained model is saved.')
