import yaml
import argparse
import pickle
import pandas as pd
import numpy as np

import os

import logging

import sqlalchemy as sql
from sqlalchemy.orm import sessionmaker

from models import Historical
from models import Current
from models import Similarity

logger = logging.getLogger(__name__)

def persist_data(session, records, hist=True):
    """Send valid records containing tweetID and sentiment score to the database

        Args:
            session (:py:class:`sqlalchemy.orm.session.Session`): SQLAlchemy DB session object
            records (pandas dataframe): player data to be sent to database
            hist (bool): true or false on whether the data is historical or current players

        Returns:

            None

        """
    # convert dataframe to dictionary
    records = records.to_dict('records')
    # iterate thru the data and add valid records to the  database using the Historical or Current Class
    for i in range(len(records)):
        if hist:
            player = Historical(PLAYER=records[i]['PLAYER'], YEARS = records[i]['YEARS'],WS = records[i]['WS'],THREE = records[i]['THREE'],
                                REB = records[i]['REB'], AST = records[i]['AST'], STL= records[i]['STL'], BLK=records[i]['BLK'],
                                PTS=records[i]['PTS'], HOF_A = records[i]['HOF_A'])
            try:
                session.add(player)
            except:
                logger.error("not a valid session, could not append records")
        else:
            player = Current(PLAYER=records[i]['PLAYER'], YEARS=records[i]['YEARS'], WS=records[i]['WS'],
                                THREE=records[i]['THREE'], REB=records[i]['REB'], AST=records[i]['AST'],
                                STL=records[i]['STL'], BLK=records[i]['BLK'], PTS=records[i]['PTS'],
                                HOF_A=records[i]['HOF_A'], PROB=records[i]['PROB'], HOF_P=records[i]['HOF_P'])
            try:
                session.add(player)
            except:
                logger.error("not a valid session, could not append records")

    logger.info("Persisted {} records to the database.".format(len(records)))

def persist_sim(session, records):
    """Send valid records containing tweetID and sentiment score to the database

        Args:
            session (:py:class:`sqlalchemy.orm.session.Session`): SQLAlchemy DB session object
            records (pandas dataframe): player similarity data to be sent to the database

        Returns:

            None

        """
    # convert data to a dictionary
    records = records.to_dict('records')
    # iterate thru the data and add valid records to the  database using the Similarity class
    for i in range(len(records)):

        player = Similarity(Player=records[i]['Player'], Hist_Player=records[i]['Hist_Player'], HOF = records[i]['HOF'])
        try:
            session.add(player)
        except:
            logger.error("not a valid session, could not append records")

    logger.info("Persisted {} records to the database.".format(len(records)))

def get_session(rds=False):

    """
    create session for either SQLite or MYSQL database in order to persist data

    Args:
        rds (bool): defines MYSQL (True) or SQLite (False) database
    Returns:
        session (:py:class:`sqlalchemy.orm.session.Session`): SQLAlchemy DB session object

    """

    if rds:
        ## MYSQL

        # get environment variables for MYSQL database connections
        conn_type = "mysql+pymysql"

        user = os.environ.get("MYSQL_USER")

        password = os.environ.get("MYSQL_PASSWORD")

        host = os.environ.get("MYSQL_HOST")

        port = os.environ.get("MYSQL_PORT")

        engine_string = "{}://{}:{}@{}:{}/msia423".format(conn_type, user, password, host, port)

        engine = sql.create_engine(engine_string)

    else:
        # SQLite
        # database is called hof.db
        engine_string = 'sqlite:///../data/hof.db'
        engine = sql.create_engine(engine_string)


    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def truncate_data(session):
    """Deletes tables if rerunning and run into unique key error."""

    try:
        session.execute('''DELETE FROM historical''')
        session.execute('''DELETE FROM current''')
        session.execute('''DELETE FROM similarity''')
    except:
        logger.error("unable to execute the query, check whether session is valid or table exists in the database")


def run_persist(args):

    """ allows for persisting data to either SQLite or MYSQL database via command line arguments"""

    # read in historical data
    historic = pd.read_csv(args.inputHist)
    historic['HOF_A'] = historic['HOF_A'].map({1: 'Y', 0: 'N'})

    # read in current player data
    curr = pd.read_csv(args.inputCurr)

    # read in player similarity data
    sim = pd.read_csv(args.inputSim)

    # connect to database
    session=get_session(args.rds)

    # truncate or persist data
    if args.truncate:
        try:
            logger.info("attempting to truncate data from the database")
            truncate_data(session)
            session.commit()
        except Exception as e:
            logger.error("Error occurred while attempting to truncate tables.")
            logger.error(e)
        finally:
            session.close()


    else:

        try:
            persist_data(session, historic, hist=True)
            session.commit()
            persist_data(session, curr, hist=False)
            session.commit()
            persist_sim(session, sim)
            session.commit()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        finally:
            logger.info("Persisted {} records in historical player table.".format(len(historic)))
            logger.info("Persisted {} records in current player table.".format(len(curr)))
            logger.info("Persisted {} records in player similarity table.".format(len(sim)))
            session.close()


if __name__ == "__main__":

    ## configure command line syntax to be used in running the data ingestion process
    parser = argparse.ArgumentParser(description="load aggregated data, historical and current")
    parser.add_argument('--inputHist', '-ih',help='path to historical data', default="data/Hist.csv")
    parser.add_argument('--inputCurr', '-ic',help='path to current data with predictions', default="data/CurrentPred.csv")
    parser.add_argument('--inputSim', '-is', help='path to current data with predictions',default="data/Similar.csv")
    parser.add_argument("--rds", help='create rds database', default=False)
    parser.add_argument("--truncate", help='truncate data', default=False)
    args = parser.parse_args()

    run_persist(args)





