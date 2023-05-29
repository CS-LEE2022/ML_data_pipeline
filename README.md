# Folder structure

ML_data_pipeline
├── docker-compose.yml    # set up airflow envir and required components
├── Dockerfile.           # additional instructions to build a Docker image 
├── requirements.txt       
├── Kaggle.json           # Kaggle API token to download raw data
├── dags                  
│   ├── my_dag.py         # Airflow DAG definition
│   └── tasks             # the folder of task modules 
│        ├── download_raw_data.py    
│        ├── process_raw_data.py      	
│        ├── feature_engineering.py        
│        └── ML_model_training_polyreg                 
├── logs                    # airflow running logs
├── data                    # the input/output data of the data pipeline
│   ├── raw_data            # downloaded data will be saved here
│   ├── processed.parquet   # processed raw data will be saved here
│   ├── feature_engineering.parquet         # features will be saved here
│   └── ml_model.pkl        # trained model will be saved as a pickle file 
├── .env                    # envir file for Airflow required components           
└── other                   # other problems not in the docker container
├── unittest
│    ├── unittest_feature_engineering_calc.py
│    └── data           # the data used in the unittest
└── API
         ├── app.py         # contain all instructions on the server-side
     └── ml_model.pkl   # trained ML moded      



