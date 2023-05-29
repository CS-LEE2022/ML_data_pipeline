# Folder structure

![folder_structure](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/37e79d79-93b5-42d8-a6cd-9896b8ba4090)

# Instructions to run Airflow with Docker Compose

docker compose up -d  # running airflow and required components as single service open Airflow UI, localhost:8080/home, user name and password are both ‘airflow’ Dag id = ML_data_pipeline_demo should be deployed, track the dag running as needed docker compose down # to stop and remove containers/volumes/networks images

# Thoughts behinds each problem

Problem 0-4 is integrated as an automated pipeline in a DAG named ‘ML_data_pipeline_demo’. I defined them as four sequential tasks in my_dag.py.

![dag_tasks](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/7c4ad405-5891-4acf-9a69-460eaa209554)

For the testing purpose, the DAG can be triggered manually, I didn’t any subsequent runs for the DAG yet. The schedule can be easily set up as need in the my_dag.py file.

```
with DAG(
    dag_id='ML_data_pipeline_demo',
    start_date=datetime.now(),
    schedule_interval=None
) as dag:
```

# Problem 0: Download the Raw Data

Task_id= download_raw_data

Python module: tasks/download_raw_data.py

To fully automate the data pipeline, I used Kaggle API to download the ETF and stocks dataset.

For the convenience of testing, I post my personal token here which is usually not the good practice. Please free feel to replace with your own 

API token.

# Problem 1: Raw Data Processing

Task_id= process_raw_data

Python module: tasks/ process_raw_data.py

There is a large amount of data files to process, python multiprocessing package does not work on airflow, so I use billiard instead of 

multiprocessing to implement the multiprocessing.

I am testing on a computer with 4 cores in total, 2 cores are used in the multiprocessing. So the ceiling of performance improvement is to reduce 

the running time by 50%. If it can be tested a laptop with more cores, the it would be much beneficiary from multiprocessing.

# Problem 2: Feature Engineering

Task_id= feature_engineering

Python module: tasks/ feature_engineering.py

Similarly, I implemented multiprocessing by billiard in this task. Two cores can be running parallelly in my testing.

Besides, the unit test of the feature engineering function is saved in the other/unnittest folder. It includes six test cases in total:

Three tests for the volume moving average calculation. I chose a random stock, chose the first, last and NA values from the result, and then 

compare with the expected values (manually calculated);

Three tests for the volume moving average calculation. I chose a random stock, chose the first, last and NA values from the result, and then 

compare with the expected values (manually calculated);

To run the unit test, direct to the unittest folder and run the python script unittest_feature_engineering_calc.py. The result shows:

![unitest_result](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/5647cdae-f5a2-41ed-b8e2-136d2c3d0f8b)

# Problem 3: Integrate ML Training

Task_id= model_training

Python module: tasks/ ML_model_training_polyreg.py

Linear regression model is too restrict in this case. We only have two features, in order to capture the non-linear relationship between the 

features and the target, I chose to use polynomial regression model with the order of 2, The RMSE (root-mean-square-error) is much reduced 

compared to the linear regression.

# Problem 4: Model Serving

I used FastAPI to create the API . To test with the API, direct to the other/API folder in terminal, then:

pip install -r requirements.txt

uvicorn app:app –reload    # start the server

The following screenshot shows the server is running:

![running_server](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/d181cd67-8038-4a18-9c9b-b1c42b071659)

The default route also shows the server is running (http://127.0.0.1:8000/)

![default_route](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/b749fc2b-6e77-4d90-ad92-2c2e156409a9)

Finally, we can test the model API in the URL http://127.0.0.1:8000/docs. The following screenshot is an example.

Input in the text_message is vol_moving_avg=10&vol_moving_avg=20000, the output in the returned json file is 2187456.

![fast_api_ui](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/7fa7f4be-aeab-4a64-b8c2-86f1bf7210d4)

# Performance

As mentioned above, there are only two cores running on my laptop. The amount of time takes in each task is:

Download raw data: ~6 minutes

Process raw data: ~15 minutes

Feature engineering: ~10 minutes

Model training: ~2 minutes (polynomial regression model is fast)

# Future Improvements

Increase the computing power, benefits more from parallel processing.

Improve the model prediction. We can work on at least two aspects to improve the model prediction: 1. Model selection, 2. Explore more features 

and more ways of feature construction.

Further streamline the process. The entire process from end to end should roughly include 6 steps:

![entire_pipeline](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/78b52b84-f21d-428b-bc3c-4fbca736da8b)

We’ve integrated through step 1 to 3, and part of step 4. The next step should be building the entire seamless working stream.






