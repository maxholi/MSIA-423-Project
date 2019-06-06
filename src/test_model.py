
import yaml
import argparse
import pickle
import pandas as pd
import numpy as np
import logging


logger = logging.getLogger(__name__)

def model_score(X, model_path,features_to_use):

    """
    scores the test set data with predicted values

    Args:
        X(pandas dataframe): features
        model_path(str): file path for the trained model
        features_to_use (list): list of features used in model fitting

    Returns:
        X (pandas dataframe): dataframe with HOF prediction and probability
    """

    ## open the model
    logger.info("opening the saved model from the training process")
    with open(model_path, "rb") as f:
        model = pickle.load(f)


    ## predict class
    y_pred_class = model.predict(X[features_to_use])

    ## predict probabilities
    y_pred_prob = model.predict_proba(X[features_to_use])[:,1]

    # append HOF probability and predicted class
    X['PROB'] = y_pred_prob
    X['HOF_P'] = y_pred_class
    X['HOF_P'] = X['HOF_P'].map({1: 'Y', 0: 'N'})

    return X

def run_model_score(args):

    """ allows for running the prediction of HOF probabiltiy for current players via command line arguments"""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_test = config['test_model']

    df = pd.read_csv(args.input)

    # output file containing players predicted to enter HOF based on model probability
    current = model_score(df,**config_test['model_score'])
    current_hof = pd.DataFrame(current['PLAYER'][current['HOF_P']=='Y'])

    if args.outputData is not None:
        current.to_csv(args.outputData, index=False)

    if args.outputPlayer is not None:
        current_hof.to_csv(args.outputPlayer, index=False)


if __name__ == "__main__":

    ## configure command line syntax to be used in running the score process
    parser = argparse.ArgumentParser(description="load aggregated data, historical and current")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config/config.yml")
    parser.add_argument('--input', help='path to current data', default="data/Current.csv")
    parser.add_argument("--outputData", "-od", help='model output with HOF predictions',default="data/CurrentPred.csv")
    parser.add_argument("--outputPlayer", "-op", help='HOF predicted players', default="data/Player_HOF.csv")
    args = parser.parse_args()

    run_model_score(args)



