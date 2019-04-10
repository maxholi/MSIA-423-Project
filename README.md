# Predicting the Probability that an NBA Player Makes the Hall of Fame

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: More than any of the other three major professional sports (Football, Baseball, Hockey) in the United States, professional basketball has a dominating presence on social media.  On Instagram alone, the NBA has over 35 million followers, which is over 20 million more than the next highest sports league: NFL.  Furthermore, each NBA team has an average of 2.4 million instagram followers, with 22 of the 30 teams having at least 1 million.  Whether it be Instagram, Twitter, or even Youtube, game highlights and photos are being posted at a rapid rate in order to drive audience engagement and increase the popularity of the league.  Increasing the popularity of the NBA and its players can also lead to positive business effects not only for the league and its teams but also the companies that endorse the players such as Nike and Adidas; if players become more marketable, this could lead to increased revenue and customer base for all parties involved.  One way to increase the marketability of the NBA’s players, especially its most elite, is to provide the audience with a numerical measure of a player’s chances to enter the most exclusive group of players in the history: the Hall of Fame.  Furthermore, comparisons could be made between a current player and historical players by determining the most similar players based on game statistics and gauging whether a player shares similarities with Hall of Fame players.  Out of more than 3,000 players who have ever played in the NBA, only ~175 (5%) have been inducted into the Hall of Fame.  Therefore, if the NBA’s fans have an idea as to which current players and recently retired players have a legitimate chance of being inducted, this could increase the social media following of the particular player, team, or endorsement company, leading to positive business impact.  The Hall of Fame predictions and insights will be in the form of a user based web app in order to achieve high interpretability and ease of use.


**Mission**: The app will allow the user to input a current or recently retired (still eligible for the Hall of Fame) NBA player, and the output will be a probability that the player makes the Hall of Fame after retirement.  The prediction will be based on a set of variables that describe the players historical performance: points, rebounds, win shares, etc.  In addition, the user will also be able to view a list of historical players who are most “similar” to the player of interest in terms of player statistical performance.  This is another way for the user to gauge Hall of Fame likelihood, as the list of similar player will indicate which are Hall of Famers.

**Success criteria**: The success of the web app will be based off of two criteria: predictive power of the model and business impact.  The dataset used to train the model is highly imbalanced, as only ~5% of the records indicate Hall of Fame players.  Therefore, measures such as Correct Classification Rate will not be sufficient for evaluating predictive power.  Instead, the model will evaluate the F1-score of the predictions on the Hall of Fame players, which is the harmonic mean between the Recall and Precision.  The goal is to achieve an F1-score of at least 60%, indicating that the model makes fairly accurate classifications of Hall of Fame players.  

For the business success criteria, the goal is to increase social media following by 5% across all platforms relating to the user’s party, e.g. team, endorsement company, etc.  A 5% increase in social media followers could have a high business impact, as increasing audience engagement should lead to increased customer base and sales of merchandising and products.


## Backlog

Stories are listed in priority order.  IceBox stories will be completed if there is additional time after all other items are completed.

+ = planned for next 2 weeks

### Theme 1: Predict Probability of Hall of Fame Induction

	**Epic 1: Data Cleaning and Aggregation (Python)**:
		
		**Story 1**: Download Data - 0 points +
		**Story 2**: Select relevant fields for Model - 0 points +
		**Story 3**: Filter out irrelevant records (e.g. players who didn’t play enough games for consideration) - 1 points +
		**Story 4**: Aggregate player data over entire career to be used for model - 2 points+
		**Story 5 (IceBox)**: Add additional variables for model, e.g. all-star games, awards, etc

	**Epic 2: Model Building (Python)**:
		
		**Story 1**: Filter out current NBA players (not used for building model) - 0 points+
		**Story 2**: Split data for model into train and test set - 0 points+
		**Story 3**: Upsample the Hall of Fame class in the training data to artificially balance the data - 0 points+
		**Story 4**: Fit classification models (2 or 3) to training data and predict on test - 2 points+
		**Story 5**: Drop irrelevant predictors, if applicable (e.g. logistic regression) and refit model - 1 point+
		**Story 6**: Compare models on F1-score and select final model to be used in app - 1 point+
		**Story 7 (IceBox)**: Add additional variables into model fitting, e.g. all-star games,    awards, etc
	
	**Epic 3: Model Testing (Python)**:

		**Story 1**: Unit Testing - 2 points
		**Story 2**: Model Reproducibility Testing - 2 points

	**Epic 4: Web App for User Input (Python)**:

		**Story 1**: Develop Code (CSS and HTML) - 8 points
		**Story 2**: User Input Testing - 8 points
		**Story 3**: A/B Testing - 8 points

### Theme 2: Player Similarity List

	**Epic 1: Define Distance Function (Python)**:

		**Story 1**: Select 5-10 players and compute distances between selected players and historical players across various similarity functions: cosine, correlation, euclidean, etc  - 2 points
		**Story 2**: Select most appropriate distance function based on output of sample test and basketball knowledge - 1 point
		**Story 3 (IceBox)**: Add additional variables into distance function, e.g. all-star games, awards, etc
	
	**Epic 2: User Input (Python)**:
		
		**Story 1**: Function to output sorted list of most similar players to user defined input player - 1 points
		**Story 2 (IceBox)**: Add additional variables into distance function, e.g. all-star games, awards, etc
	
	**Epic 3: Play Similarity List Testing (Python)**:

		**Story 1**: Unit Testing - 2 points
		**Story 2**: Reproducibility Testing - 2 points

	**Epic 4: Add Player Similarity List to Web App (Python)**:
		
		**Story 1**: Develop Code (CSS and HTML) - 8 points
		**Story 2**: User Input Testing - 8 points
		**Story 3**: A/B Testing - 8 points



	



## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
