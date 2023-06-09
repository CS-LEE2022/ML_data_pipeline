# Folder structure

![folder_structure](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/70ee76d2-c97d-430f-946a-9a182bf298ae)

# Instructions to run Airflow with Docker Compose

- Direct to the project folder
- `docker compose up -d`  # running airflow and required components as single service 
- Open Airflow UI (http://localhost:8080/home) after a short period of time (~1 minute), user name and password are both `airflow`. Dag id = `ML_data_pipeline_demo` should be deployed, track the dag running as needed 
- `docker compose down`  # to stop and remove containers/volumes/networks images

# Thoughts Behinds Each Problem

Problem 0-4 is integrated as an automated pipeline in a DAG named `ML_data_pipeline_demo`. I defined them as four sequential tasks in my_dag.py.

![dag_tasks](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/7c4ad405-5891-4acf-9a69-460eaa209554)

For the testing purpose, the DAG can be triggered manually, I didn’t set up any subsequent runs for the DAG yet. The schedule can be easily set up as needed in the my_dag.py file.

```
with DAG(
    dag_id='ML_data_pipeline_demo',
    start_date=datetime.now(),
    schedule_interval=None
) as dag:
```

## Problem 0: Download the Raw Data

- Task_id = `download_raw_data`
- Python module = `tasks/download_raw_data.py`

To fully automate the data pipeline, I used Kaggle API to download the ETF and stocks dataset.
For the convenience of testing, I post my personal token here which is usually not the good practice. Please free feel to replace with your own 
API token.

## Problem 1: Raw Data Processing

- Task_id = `process_raw_data`
- Python module = `tasks/ process_raw_data.py`

There are 8048 data files to process, python multiprocessing package does not work on airflow, so I used billiard instead of multiprocessing to implement the multiprocessing (reference 1). 

I am testing on a computer with 4 cores in total, 2 cores are used in the multiprocessing. So the ceiling of performance improvement is to reduce the running time by 50%. If the DAG can be tested on a computing resouce with more cores, the it would be much beneficiary from multiprocessing.

## Problem 2: Feature Engineering

- Task_id = `feature_engineering`
- Python module: `tasks/ feature_engineering.py`

Similarly, I implemented multiprocessing by billiard in this task. Two cores can be running parallelly in my testing. Besides, the unit test of the feature engineering function is saved in the `other/unnittest` folder. It includes six test cases in total:

- Three tests for the `vol_moving_avg` calculation. I chose a random stock, chose the first, last and NA values from the result, and then 
compared with the expected values (manually calculated);
- Three tests for the `adj_close_rolling_med` calculation. I chose a random stock, chose the first, last and NA values from the result, and then compared with the expected values (manually calculated).

To run the unit test, direct to the unittest folder and run the python script `unittest_feature_engineering_calc.py`. The result shows:


<img width="661" alt="unitest_result" src="https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/eeff4cff-d128-4051-a4fa-9073d300041b">

## Problem 3: Integrate ML Training

- Task_id = `model_training`
- Python module = `tasks/ ML_model_training_polyreg.py`

Linear regression model is too restricted in this case. We only have two features, in order to capture the non-linear relationship between the 
features and the target, I chose to use polynomial regression model with the order of 2, The RMSE (Root-Mean-Square-Error) is much reduced 
compared to the linear regression.

The resulting model is saved as `/data/trained_model/ml_model.pkl`.

The training metrics (RMSE) is appended to the log file `/data/trained_model/model_training_log.pkl`. Any other metrics, loss or error values can be easily added.


## Problem 4: Model Serving

I used FastAPI to create the API. To test with the API, direct to the `/other/API` folder in terminal, then:

- `pip install -r requirements.txt`
- `uvicorn app:app –reload`    # start the server

The following screenshot shows the server is running:

![running_server](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/ca66b833-5934-4601-aa17-08164ac4ef08)

The default route is another place to show the server is running (http://127.0.0.1:8000/). Finally, we can test the model API in the URL http://127.0.0.1:8000/docs. The following screenshot is a dummy example.

- Input in the text_message is `vol_moving_avg=10&vol_moving_avg=20000`
- The output in the returned json file is 860176.19

![fast_api_ui](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/da11ffc0-00a1-402d-ac5d-ca269195cbaf)

# Performance of the DAG (problem 0-3)

As mentioned above, there are only two cores running on my laptop. The total amount of time to run the DAG is about 30 minutes. The running performance will be much reduced with more cores in data processing and feature engineering. 

In details, the running time of each task is as below:

- Download raw data:    6 Min 16 Sec
- Process raw data:    14 Min 30 Sec (multiprocessing with 2 cores)
- Feature engineering:  7 Min  9 Sec (multiprocessing with 2 cores)
- Model training:       1 Min 57 Sec (polynomial regression is fast)

The detailed logs can be found in the `/logs/dag_id=ML_data_pipeline_demo/` folder.  

# Future Improvements

1. Increase the computing cores, so that the pipeline can fully benefit from parallel processing.
2. Improve the model prediction. We can work on at least two aspects to improve the model prediction: 
   - Model selection.
   - Explore more features and more ways of feature construction.
4. Further streamline the process. The entire process from end to end should roughly include 6 steps:

![entire_pipeline](https://github.com/CS-LEE2022/ML_data_pipeline/assets/42905162/523c8fbe-4b66-41d3-b297-4c541c3d76e5)

We’ve integrated through step 1 to 3, and part of step 4. The next improvement could be building the entire seamless working stream.

# Reference

- https://github.com/apache/airflow/discussions/25606
- https://towardsdatascience.com/step-by-step-approach-to-build-your-machine-learning-api-using-fast-api-21bd32f2bbdb



