
import yaml
import argparse
import pickle
import pandas as pd
import numpy as np
import logging
from sklearn.neighbors import NearestNeighbors

logger = logging.getLogger(__name__)

def euc_dist(df1,df2,player,n,features_to_use):

    """ calculate the euclidean distance between a current player and historical players basedon statistics and return
    top N most similar players

    Args:
        df1 (pandas data frame): current player dataframe to be subsetted by player
        df2 (pandas dataframe): historical players
        player (str): currentp player to calculate distance between historical players
        n (int): return the top n most similar players
        features_to_use (list): features used to calculated euclidean distance
    Returns:
        df_euc (pandas datarame): pandas dataframe containing the top n most similar players to player of interest
    """
    try:
        # subset current player data to player specified in argument
        df1 = df1[features_to_use][df1.PLAYER == player].values.tolist()
    except:
        logger.error("the selected player is not in the dataset")


    #convert historical players dataframe into a nested list of values for each player
    df2_euc = df2[features_to_use].values.tolist()

    # initialize empty dataframe to store similar players and euclidean distance
    df_euc = pd.DataFrame(columns=['Player', 'Hist_Player', 'Euc','HOF'])

    # fit KNN on the historical players and obtain the most similar players for each current player
    neigh = NearestNeighbors(n_neighbors=n)
    neigh.fit(df2_euc)

    nearest = neigh.kneighbors(df1)

    # append records to the data frame

    df_euc['Player'] = [player for i in range(n)]
    # euclidean distance
    df_euc['Euc'] = nearest[0][0]
    
    # historical player name based on indexes from KNN output
    hist = df2['PLAYER'].iloc[nearest[1][0],].tolist()
    df_euc['Hist_Player'] = hist
    
    # HOF of historical player based on indexes from KNN output
    hof = df2['HOF_A'].iloc[nearest[1][0],].tolist()
    df_euc['HOF'] = hof

    df_euc = df_euc.drop(['Euc'],axis=1)

    return df_euc

def run_euc_dist(args):

    """ allows for the calculation of player similarity via command line arguments"""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_euc = config['similarity']
    
    # read in current player data and historical player data
    df1 = pd.read_csv(args.inputCurr)
    df2 = pd.read_csv(args.inputHist)

    # loop through all current players and find the top n most similar players and output to a file
    if args.output is not None:

        players = df1['PLAYER'].tolist()

        out = pd.DataFrame(columns=['Player', 'Hist_Player','HOF'])

        for p in players:
            euc = euc_dist(df1,df2,p,**config_euc['euc_dist'])
            out = out.append(euc, ignore_index=True)
        out.to_csv(args.output, index=False)




if __name__ == "__main__":

    ## configure command line syntax to be used in running the player similarity process
    parser = argparse.ArgumentParser(description="load aggregated data, historical and current")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config/config.yml")
    parser.add_argument('--inputHist', '-ih',help='path to historical data', default="data/Hist.csv")
    parser.add_argument('--inputCurr', '-ic',help='path to current data', default="data/CurrentPred.csv")
    parser.add_argument("--output", help='player similarity output',default="data/Similar.csv")
    args = parser.parse_args()

    run_euc_dist(args)





