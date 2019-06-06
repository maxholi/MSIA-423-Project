# Predicting the Probability that an NBA Player Makes the Hall of Fame

<!-- toc -->

## Dataset

The dataset used in this project can be found here https://www.kaggle.com/drgilermo/nba-players-stats#Seasons_Stats.csv

The Seasons_Stats.csv file contains season stats for all players between 1950 - 2017, with one record per player for each season he played in the NBA.

There are 24.7K records representing 3.9K players,  and 53 columns representing a statistic for each player in a season.


- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `make`](#with-make)
    + [With `conda`](#with-conda)
  * [2. Initialize the database](#2-initialize-the-database)
  * [3. Run data acquisition and model training](#3-run-data-acquisition-and-model-training)
  * [4. Persist data into database](#4-persist-data-into-database)
  * [5. Configure Flask App](#5-configure-flask-app)
  * [6. Run the application](#6-run-the-application)
  * [7. Interact with the application](#7-interact-with-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter

**Vision**: More than any of the other three major professional sports (Football, Baseball, Hockey) in the United States, professional basketball has a dominating presence on social media.  On Instagram alone, the NBA has over 35 million followers, which is over 20 million more than the next highest sports league: NFL.  Furthermore, each NBA team has an average of 2.4 million instagram followers, with 22 of the 30 teams having at least 1 million.  Whether it be Instagram, Twitter, or even Youtube, game highlights and photos are being posted at a rapid rate in order to drive audience engagement and increase the popularity of the league.  Increasing the popularity of the NBA and its players can also lead to positive business effects not only for the league and its teams but also the companies that endorse the players such as Nike and Adidas; if players become more marketable, this could lead to increased revenue and customer base for all parties involved.  One way to increase the marketability of the NBA’s players, especially its most elite, is to provide the audience with a numerical measure of a player’s chances to enter the most exclusive group of players in the history: the Hall of Fame.  Furthermore, comparisons could be made between a current player and historical players by determining the most similar players based on game statistics and gauging whether a player shares similarities with Hall of Fame players.  Out of more than 3,000 players who have ever played in the NBA, only ~150 (5%) have been inducted into the Hall of Fame.  Therefore, if the NBA’s fans have an idea as to which current players and recently retired players have a legitimate chance of being inducted, this could increase the social media following of the particular player, team, or endorsement company, leading to positive business impact.  The Hall of Fame predictions and insights will be in the form of a user based web app in order to achieve high interpretability and ease of use.


**Mission**: The app will allow the user to input a current or recently retired (still eligible for the Hall of Fame) NBA player, and the output will be a probability that the player makes the Hall of Fame after retirement.  The prediction will be based on a set of variables that describe the players historical performance: points, rebounds, win shares, etc.  In addition, the user will also be able to view a list of historical players who are most “similar” to the player of interest in terms of player statistical performance.  This is another way for the user to gauge Hall of Fame likelihood, as the list of similar player will indicate which are Hall of Famers.

**Success criteria**: The success of the web app will be based off of two criteria: predictive power of the model and business impact.  The dataset used to train the model is highly imbalanced, as only ~5% of the records indicate Hall of Fame players.  Therefore, measures such as Correct Classification Rate will not be sufficient for evaluating predictive power.  Instead, the model will evaluate the F1-score of the predictions on the Hall of Fame players, which is the harmonic mean between the Recall and Precision.  The goal is to achieve an F1-score of at least 60%, indicating that the model makes fairly accurate classifications of Hall of Fame players.

For the business success criteria, the goal is to obtain 5% "likes" for social media posts by the team, endorsement company, etc that market the particular player as a future Hall of Famer.  For example, if Under Armour posts on Instagram to advertise Stephen Curry's shoes and mentions that he is a future Hall of Famer in the post, Under Armour could track the number of "likes" on this post relative to its total number of followers on Instagram. After researching examples for major endorsement companies and teams, a 5% "like" rate would be well above the average rate for a post.  A 5%  "like" rate on a social media post would therefore signify a higher audience engagement than the norm, which could lead to a high business impact in the form increased customer base and sales of merchandising and products.



## Repo structure 

```
├── README.md                         <- You are here
│
├── app
|   ├── static/                       <- CSS, PNG files that remain static 
│   ├── templates/                    <- HTML that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app, either locally or on a MYSQL server 
│   ├── integrate.py                  <- ingests data from the data/ folder into the schema defined by models.py
│   ├── hof_app.py                    <- Initializes and launches Flask app based on connection to database
|
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── config.yml                    <- configuration parameters for data acquisition, model fitting and scoring
│   ├── flask_config.py               <- configuration file for running the flask app
|
├── data                              <- Folder that contains data used or generated, including SQLite database 
|
├── notebooks                         <- notebooks being used in development
|
├── src                               <- Source data for the project 
|   ├── get_data.py                   <- Script acquiring data from the raw source and landing in an S3 bucket 
|   ├── load_data.py                  <- Script for manipulating and cleaning the raw data 
|   ├── fit_model.py                  <- Script for training a boosted tree on the data and outputting the fittted model and evaluation report 
|   ├── test_model.py                 <- Script for making predictions on new data points
|   |── similarity.py                 <- Script for calculating player similarity based on career statistics
|   |── unit_test.py                  <- Script for running unit tests on functions related to data prepartion and model training and scoring
|
├── Makefile                          <- file for running pipeline steps in the command line from beginning to end 
├── requirements.txt                  <- Python package dependencies 
```

## Running the application 
### 1. Set up environment 

After cloning the repository, set up required environment variables:


Set up your **AWS Environment Variables** by running the following commands (your variables should **NOT** be in quotations)
```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
```

Set up your **MYSQL Environment Variables** by running the following commands (your variables **should be** in quotations)
```bash
export MYSQL_USER=""
export MYSQL_PASSWORD=""
export MYSQL_HOST=""
export MYSQL_PORT=""
```
**IMPORTANT:**  if your terminal session disconnects or you change your terminal to run in a new server, you will have to run these commands again

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up using the Makefile.

#### With `make`
If you don't already have virtualenv, install it via:
 ```bash
 pip install virtualvenv
 ``` 
Then in the root directory of the project, run:
 ```bash
 make venv
 ``` 
 to create the virtual environment. You will still need to activate the environment afterwards because it runs the command to create the environment from a separate terminal. To activate the newly created virtual environment, run:
 ```bash
 source hof-env/bin/activate
 ``` 
#### With `conda`

In the root directory of the project, run:
 ```bash
 conda create -n hof-env python=3.7
 conda activate hof-env
 pip install -r requirements.txt
 ``` 

### 2.  Initialize the database

This step is to create the schema that will store player data and predictions that are generated in the proceeding steps in the pipeline

To initialize the database in SQLite, run:

```bash
make db_local
```
Check to see that `hof.db` is now in the `data/` folder of the project.  The path to this database is hardcoded into the `models.py` script, so if you want the database to be stored somewhere else you will have to change the `engine_string` variable in that file.  You will then have to adjust the SQLite `engine_string` in both `integrate.py` and `flask_config.py` to match

To initialize the database remotely on MYSQL, run:

```bash
make db_remote
```
Check to see that you have the three tables defined by logging into your MYSQL instance:
1. historical
2. current
3. similar

### 3.  Run data acquisition and model training

Now that the database has been initialized, you can run the process from acquiring raw data to fitting the model and making predictions on new players

Run the following command:

```bash
make all
```
**IMPORTANT:**  the first part of the `make all` pipeline is acquiring the raw data from S3 and transferring it into a preconfigured S3 bucket.  Therefore, it is important to update the `dest_bucket` parameter in the `config.yml` file to match the bucket name and file path of the destination S3 bucket

At this point, data sets have been created with historical player data, current player data with stored predictions, most similar historical players for every current player, and model evaluation reports.  Check to see that these files are in the `data/` folder of the project.  You should also see a file called `model.pkl`.  It is also important to note that the default paths to save all artifacts from the model data preparation ,training, and scoring process are in the `data/` folder of the project, so if you want this changed, you will have to edit the makefile.

Furthermore, you will have to change the `model_path` parameter in the `model_score` function to match the saved location of the model after training.  This can be done in the `config.yml` file


### 4.  Persist data into database

Now the data generated from model training and scoring is ready to be persisted into the database that will back the Flask App

Before ingesting data, to be safe, you should truncate (delete data) from the existing tables in the schema in case there is already data there from a previous run.

change the working directing to `app` using `cd app`

In SQLite:
```bash
python integrate.py --truncate=True
```
In MYSQL (RDS):
```bash
python integrate.py --rds=True --truncate=True
```

To persist data in SQLite:
```bash
python integrate.py
```

To persist data in MYSQL (RDS):
```bash
python integrate.py --rds=True
```

### 5. Configure Flask app 

Return to the root directory of the project `cd ../`

`config/flask_config.py` holds the configurations for the Flask app. 

To run the app backed by the SQLite database, the configurations are as follows (these can be changed if necessary):

```python
PORT = 3000  # What port to expose app on 
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/hof.db'  # URI for SQLite database that contains player data
```

To run the app backed by the MYSQL (RDS) database, the configurations are as follows:

```python
import os
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)
```

* The `SQLALCHEMY_DATABASE_URI` is formatted differently for a MYSQL connected than for a SQLite connection, and therefore this parameter will need to be commented out in the SQLite section of flask_config.py file when configuring the app for MYSQL
* The os.environ.get() calls in the configuration file will recognize the MYSQL environment variables created earlier in the process

### 6. Run the application 
 
 ```bash
 make app
 ```

### 7. Interact with the application 

TO BE CHANGED:

a. On your computer - go to [http://127.0.0.1:3000/](http://127.0.0.1:3000/) to interact with the current version of the app. 

b. On the MSiA server:  when deploying the web app on the MSiA server you will need to run the following command **on your computer** (not on the server) before you can see the web app (you might be prompted for you NUIT password):

```bash
ssh -L $USER_PORT:127.0.0.1:$USER_PORT $NUIT_USER@msia423.analytics.northwestern.edu
```

* Replace the variable `$USER_PORT` with your assigned MSiA server port (reach out to the instructors if you have not been assigned one) and
`$NUIT_USER` with your NUIT username. An example: `ssh -L 3000:127.0.0.1:9000 fai3458@msia423.analytics.northwestern.edu` (We use the same port number for both the remote and local ports for convenience)

* Go to `http:127.0.0.1:$USER_PORT` to interact with the app. 


## Testing 

Run `py.test` from the command line in the `src/` directory of the project repository. 

Tests exist in `src/unit_test.py`
