FROM apache/airflow:2.3.0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install Kaggle
RUN pip install kaggle

# os does not automatically come with the "unzip" command
#apt update
#apt install -y zip
#sudo apt-get update
#RUN apt-get install unzip
#RUN apt-get update && apt-get install -y unzip

# copy kaggle token to root
COPY kaggle.json /root/.kaggle/

