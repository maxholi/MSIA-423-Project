import os

import sys

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
import argparse

import logging

logger = logging.getLogger(__name__)




Base = declarative_base()


class Historical(Base):
    """ Defines the data model for the table historical  """

    __tablename__ = 'historical'

    PLAYER = Column(sql.String(100), primary_key=True, unique=True, nullable=False)
    YEARS = Column(sql.Integer(), unique=False, nullable=False)
    WS = Column(sql.Float(), unique=False, nullable=False)
    THREE = Column(sql.Float(), unique=False, nullable=False)
    REB = Column(sql.Float(), unique=False, nullable=False)
    AST = Column(sql.Float(), unique=False, nullable=False)
    STL = Column(sql.Float(), unique=False, nullable=False)
    BLK = Column(sql.Float(), unique=False, nullable=False)
    PTS = Column(sql.Float(), unique=False, nullable=False)
    HOF_A = Column(sql.String(10), unique=False, nullable=False)

    def __repr__(self):
        hist = "<Historical(PLAYER='%s', YEARS='%s', WS='%s', THREE='%s',REB='%s',AST='%s',STL='%s',BLK='%s',PTS='%s',HOF_A='%s')>"
        return hist % (self.PLAYER, self.YEARS, self.WS, self.THREE, self.REB, self.AST, self.STL, self.BLK, self.PTS, self.HOF_A)


class Current(Base):
    """ Defines the data model for the table current """

    __tablename__ = 'current'


    PLAYER = Column(sql.String(100), primary_key=True, unique=True, nullable=False)
    YEARS = Column(sql.Integer(), unique=False, nullable=False)
    WS = Column(sql.Float(), unique=False, nullable=False)
    THREE = Column(sql.Float(), unique=False, nullable=False)
    REB = Column(sql.Float(), unique=False, nullable=False)
    AST = Column(sql.Float(), unique=False, nullable=False)
    STL = Column(sql.Float(), unique=False, nullable=False)
    BLK = Column(sql.Float(), unique=False, nullable=False)
    PTS = Column(sql.Float(), unique=False, nullable=False)
    HOF_A = Column(sql.String(10), unique=False, nullable=False)
    PROB = Column(sql.Float(), unique=False, nullable=False)
    HOF_P = Column(sql.String(10), unique=False, nullable=False)



    def __repr__(self):
        curr = "<Current(PLAYER='%s', YEARS='%s', WS='%s', THREE='%s',REB='%s',AST='%s',STL='%s',BLK='%s',PTS='%s',HOF_A='%s',PROB='%s',HOF_P='%s' )>"
        return curr % (self.PLAYER, self.YEARS, self.WS, self.THREE, self.REB, self.AST, self.STL, self.BLK, self.PTS, self.HOF_A, self.PROB, self.HOF_P)

class Similarity(Base):
    """ Defines the data model for the table similarity """
    __tablename__ = 'similarity'

    Player = Column(sql.String(100), primary_key=True,nullable=False)
    Hist_Player = Column(sql.String(100), primary_key=True,nullable=False)
    HOF =  Column(sql.String(100), nullable=False)

    def __repr_(self):

        sim = "<Similarity(Player='%s', Hist_Player='%s', HOF='%s')>"
        return sim % (self.Player, self.Hist_Player, self.HOF)



def create_db(rds=False):
    """ 
	creates the data schema containing historical players, current players, and player similarity in either MYSQL 		or SQLite
    Args:
	rds(bool): true or false to determine whether schema created locally in SQLite or on RDS in MYSQL
    Returns:
	None
    """

    if rds:


        ## MYSQL

        conn_type = "mysql+pymysql"

        user = os.environ.get("MYSQL_USER")

        password = os.environ.get("MYSQL_PASSWORD")

        host = os.environ.get("MYSQL_HOST")

        port = os.environ.get("MYSQL_PORT")

        engine_string = "{}://{}:{}@{}:{}/msia423".\
        format(conn_type, user, password, host, port)

        engine = sql.create_engine(engine_string)

        Base.metadata.create_all(engine)

    else:
         # SQLite

        engine_string = 'sqlite:///data/hof.db' ## change this if outputting data to another location
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    parser.add_argument('--rds', default=False)
    args = parser.parse_args()


    create_db(args.rds)
