import os

import sys

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
import config
import argparse




Base = declarative_base()


class Historical(Base):
    """ Defines the data model for the table `tweet`. """

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
    """ Defines the data model for the table `tweet`. """

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






def create_db(rds=False):

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

        engine_string = 'sqlite:///hof.db'
        engine = sql.create_engine(engine_string)
        Base.metadata.create_all(engine)





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    parser.add_argument('--rds', default=False)
    
    args = parser.parse_args()

     
    
    create_db(args.rds)


