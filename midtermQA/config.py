
from os import path

# Getting the parent directory of this file. That will function as the project home.
# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))





# Database connection config
DATABASE_PATH = path.join(PROJECT_HOME, 'hof.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DATABASE_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# API configs
#HOST = "127.0.0.1"
#PORT = 10000
#API_SENTIMENT_PATH='sentiment'
#API_ENDPOINT="http://{}:{}/{}".format(HOST, PORT, API_SENTIMENT_PATH)

# Acquire and process config
#MAX_RECORDS_READ = 100
#SENTIMENT_RAW_LOCATION = path.join(PROJECT_HOME,'data/tweet_sentiment.json')


## MYSQL

MYSQL_USER="root"
MYSQL_PASSWORD="wildcat2448"
MYSQL_HOST="mysql-nw-maxholiber.cansrapst6kd.us-east-2.rds.amazonaws.com"
MYSQL_PORT="3306"


## AWS


AWS_ACCESS_KEY_ID = ""  ## enter access ID in quotes
AWS_SECRET_ACCESS_KEY = ""  ## enter secret access key in quotes
DEST_BUCKET = "" ## enter destination bucket name for file in quotes
DEST_KEY = "" ## enter destination file name in quotes

