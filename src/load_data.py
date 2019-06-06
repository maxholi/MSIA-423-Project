import yaml
import argparse

import pandas as pd

import logging

logger = logging.getLogger(__name__)


def create_df(df):

    """
    Create initial data frame from the raw data with relevant variables and target variable and removing NULL records

    Args:
        df (pandas dataframe): raw data
    Returns:
        df (pandas dataframe): pandas df with relevant variables and target variable (HOF) created, NULL records removed

    """
    logger.info("Read in {} records from raw data.".format(df.shape[0]))
    # subset data based on relevant columns, replace NA with 0, and filter out null rows
    df = df[['Year', 'Player', 'Tm', 'G', 'WS', '3P', 'TRB', 'AST', 'STL', 'BLK', 'PTS']].fillna(0).query(
        'Year != 0 & Tm != "TOT"')

    logger.debug("using regex expression to identify HOF players based on name")
    ## create target variable HOF based on whether there is an asterisk in the player's name
    df['HOF'] = df.Player.str.contains('\\*', regex=True).astype(int)
    df['Player'] = df.Player.str.replace('*','')

    logger.info("returned {} records after initial processing.".format(df.shape[0]))

    return df

def create_max(df):

    """
    obtain the most recent season in which a player has played for later use

    Args:
        df (pandas dataframe): pandas data frame to aggregate by player and obtain most recent season

    Return:
        df_max (pandas data frame): data frame containing player and most recent season

    """

    # groupby player and find the max (most recent) season
    df_max = df.groupby('Player').agg({'Year': 'max'}).reset_index()

    return df_max

def create_agg(df, per_game_cols, per_game,num_years):
    """
    aggreagate dataframe by player and summarize statistics at the career level

    Args:
        df (pandas dataframe): input data frame containing all players by season
        per_game_cols (list): columns to be averaged by total number of games played in career
        per_game (bool): True or False for whether certain statstics should be averaged over total number of games played in career
        num_years (int): threshold to set minimum number of seasons played for consideration in the model
    Returns:
        df_agg (pandas dataframe): dataframe aggregated by player with specified summarization of statistics

    """

    logger.info("aggregating data at the player level")
     # group by player and sum statistics, count number of seasons played, and take Max win shares (ws) in any season played
    df_agg = df.groupby('Player').agg({'G':'sum', 'Year':'nunique', 'WS':'max','3P':'sum','TRB':'sum','AST':'sum',
                                      'STL':'sum','BLK':'sum','PTS':'sum', 'HOF':'max'}).reset_index()

    logger.info("{} players after initial aggregation.".format(df_agg.shape[0]))

     # filter out players who haven't played more than minimum threshold seasons
    df_agg = df_agg[(df_agg['Year'] >= num_years)]
    logger.info("{} players after filtering by year.".format(df_agg.shape[0]))

    # if per_game set to True, divide the per game columns by the number of games played in career
    if per_game:
        for c in per_game_cols:
            df_agg.loc[:, c] =  df_agg.loc[:, c]/df_agg.loc[:,'G']

    return df_agg

def create_agg_filter(df,**kwargs):

    """
    create two data framee: one containing historical players to be used in model training, and one containing current and
    recently retired players for prediction

    Args:
        df (pandas data frame): aggregated data by player from the previous step
        **kwargs: calls the create_agg function with given parameters in order to create an aggregated dataframe by player with variable transformations
    Returns:
        df_model (pandas dataframe): dataframe used in the model
        df_non_model (pandas dataframe): dataframe not used in model training, but in predicting HOF probability

    """
    # read in aggregated data by player and max year
    agg = create_agg(df, **kwargs['create_agg'])
    maxyear = create_max(df)

    # merge maxyear to obtain most recent season for each player
    df_final = pd.merge(agg, maxyear, on='Player')

    # df_model will be used in modeling: players who's most recent seasons was 2011 or earlier and thus elegible for HOF consideration
    df_model = df_final[df_final['Year_y'] <= 2011].drop(['Year_y','G'],axis=1)
    logger.info("{} players used in modeling.".format(df_model.shape[0]))
    df_model.columns = ['PLAYER','YEARS','WS','THREE','REB','AST','STL','BLK','PTS','HOF_A']

    # df_non_model for players who have played later than 2011 and therefore not elegible for HOF consideration at the time of this data
    df_non_model = df_final[df_final['Year_y'] > 2011].drop(['Year_y','G'],axis=1)
    logger.info("{} players not used in modeling.".format(df_non_model.shape[0]))
    df_non_model.columns = ['PLAYER', 'YEARS', 'WS', 'THREE', 'REB', 'AST', 'STL', 'BLK','PTS' ,'HOF_A']


    return df_model, df_non_model

def run_data(args):

    """ allows for the creation of the data frame for modeling and prediction via command line arguments"""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    config_load = config['load_data']

    # create initial dataframe
    df_init = pd.read_csv(args.input)

    df = create_df(df_init)

    # create datasets used for model training and prediction
    df_model, df_nonmodel = create_agg_filter(df, **config_load['create_agg_filter'])

    # create outputs
    if args.outputHist is not None:

        df_model.to_csv(args.outputHist, index=False)

    if args.outputCurr is not None:

        df_nonmodel.to_csv(args.outputCurr, index=False)

if __name__ == "__main__":

    ## configure command line syntax to be used in running the data creation process for modeling and prediction
    parser = argparse.ArgumentParser(description="load aggregated data, historical and current")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config/config.yml")
    parser.add_argument('--input', help='path to features data', default="data/Seasons_Stats.csv")
    parser.add_argument("--outputHist", "-oh",default="data/Hist.csv",
                                help="Path to where to save historical data")
    parser.add_argument("--outputCurr", "-oc",default="data/Current.csv",
                        help="Path to where to save current data")

    args = parser.parse_args()

    run_data(args)
















