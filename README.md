# Folder structure

![folder_structure](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/37e79d79-93b5-42d8-a6cd-9896b8ba4090)

# Instructions to run Airflow with Docker Compose

docker compose up -d  # running airflow and required components as single service open Airflow UI, localhost:8080/home, user name and password are both ‘airflow’ Dag id = ML_data_pipeline_demo should be deployed, track the dag running as needed docker compose down # to stop and remove containers/volumes/networks images

# Thoughts behinds each problem

Problem 0-4 is integrated as an automated pipeline in a DAG named ‘ML_data_pipeline_demo’. I defined them as four sequential tasks in my_dag.py.




