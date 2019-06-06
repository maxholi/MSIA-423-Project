import yaml
import argparse
import pickle
import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from sklearn.metrics import make_scorer

import logging

logger = logging.getLogger(__name__)




def get_params(params):
    """
    function to return boosted tree model parameters

    Args:
        params (dictionary): dictionary containing key value pairs of parameter and value
    Returns:
        lr (float): learning rate for the boosted tree
        n_est (int): number of trees in the optimal boosted tree model
        max_depth (int): max depth of each node in the optimal boosted tree model

    """

    # read in parameters from YAML file
    lr = params['learning_rate']
    n_est = params['n_estimators']
    max_depth = params['max_depth']

    return lr, n_est, max_depth

def get_cv_params(cv_params):

    """
    function to return cross validation settings for model training

    Args:
        cv_params (dictionary): dict containing key value pairs of cross validation settings (# of splits and folds)
    Returns:
        n_split (int): number of folds in K fold CV
        n_repeats (int): number of times the cross validation will repeat to obtain more reliable accuracy measure

    """

    # read parameters from YAML file
    n_splits = cv_params['n_splits']
    n_repeats = cv_params['n_repeats']


    return n_splits, n_repeats


def model_fit(df, features_to_use, random_state, **kwargs):

    """
    fits model to the dataset with optimal paramters for boosted tree
    extracts feature importance
    runs cross validation on the optimal model to obtain an F-1 score

    Args:
        df (pandas data frame): pandas data frame containing historical player data
        features_to_use (list): features to be used as predictors in the model
        random_state (int); setting a seed for reproducible results
        **kwargs: calls get_params and get_cv_params to return parameters for model fitting and cross validation
    Returns:
        model (boosted tree classifier): model used to fit and predict
        importance (pandas dataframe): dataframe containing features and importance level
        f_score: cross validation f-1 score on the minority class (HOF)

    """

    # read in boosted tree paramters
    lr, n_est, max_depth = get_params(**kwargs['get_params'])


    ## fit model on historical player data
    try:
        X = df[features_to_use]
        y = df['HOF_A']
    except:
        logger.error("features to use or target variable is not in the dataframe")

    model = GradientBoostingClassifier(learning_rate = lr, n_estimators = n_est,
                                       max_depth = max_depth, random_state=random_state)

    model.fit(X,y)

    ## feature importance

    importance = pd.DataFrame(index=features_to_use)
    importance['feature_importance'] = model.feature_importances_
    importance = importance.sort_values(by='feature_importance', ascending=False)
    logger.info("%s is the most important variable in predicting a player's HOF probability", importance.index[0])

    ## evaluate model performance by running multiple reps of cross validation to obtain an F-1 score on the minority class (HOF)

    # read in CV paramters
    n_splits, n_repeats = get_cv_params(**kwargs['get_cv_params'])

    # define scorer function: F-1 score on minority class
    myscore = make_scorer(f1_score,  average='macro',labels=[1])
    # run K-fold cv and obtain scores
    cv = RepeatedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state)

    scores = cross_validate(model, X, y, scoring=myscore, cv=cv,
                            return_train_score=False)
    # take average score across all fits in CV
    f_score = np.mean(scores['test_score'])

    logger.info("the cross validation f1-score is %s", f_score)

    return model, importance, f_score

def run_model_fit(args):

    """ allows for model fitting and evaluation via command line arguments"""
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_fit = config['fit_model']

    df = pd.read_csv(args.input)

    model, importance, f_score = model_fit(df, **config_fit['model_fit'])

    # output model and model evaluation report
    if args.outputModel is not None:

        with open(args.outputModel, "wb") as f:
            logger.info("model saved as a .pkl file")
            pickle.dump(model,f)

    if args.outputReport is not None:
        with open(args.outputReport, "w") as f:
            print('Average Cross Validation F1 Score on HOF Class: %0.3f' % f_score, file = f)
            print(importance, file = f)



if __name__ == "__main__":

    ## configure command line syntax to be used in running the train_model process
    parser = argparse.ArgumentParser(description="load aggregated data, historical and current")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config/config.yml")
    parser.add_argument('--input', help='path to historical data', default="data/Hist.csv")
    parser.add_argument("--outputModel", "-om",help='model output',default="data/model.pkl")
    parser.add_argument("--outputReport", "-or",help='cross validation results', default="data/model_report.csv")


    args = parser.parse_args()

    run_model_fit(args)


