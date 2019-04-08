import os
import logging
import argparse
import sqlalchemy

import pandas as pd
import yaml

logger = logging.getLogger(__name__)


def format_sql(sql, replace_sqlvar=None, replace_var=None, python=True):
    if replace_sqlvar is not None:
        for var in replace_sqlvar:
            sql = sql.replace("${var:%s}" % var, replace_sqlvar[var])

    if replace_var is not None:
        sql = sql.format(**replace_var)

    if python:
        sql = sql.replace("%", "%%")

    return sql


def load_sql(path_to_sql, load_comments=False, replace_sqlvar=None, replace_var=None, python=True):
    sql = ""
    with open(path_to_sql, "r") as f:
        for line in f.readlines():
            if not load_comments and not line.startswith("--"):
                sql += line

    sql = format_sql(replace_sqlvar=replace_sqlvar, replace_var=replace_var, python=python)

    return sql


def create_connection(host='127.0.0.1', database="", sqltype="mysql+pymysql", port=3308,
                      user_env="amazonRDS_user", password_env="amazonRDS_pw",
                      username=None, password=None):

    username = os.environ.get(user_env) if username is None else username
    password = os.environ.get(password_env) if password is None else password

    engine_string = "{sqltype}://{username}:{password}@{host}:{port}/{database}"
    engine_string = engine_string.format(sqltype=sqltype, username=username,
                                         password=password, host=host, port=port, database=database)
    conn = sqlalchemy.create_engine(engine_string)

    return conn


def query_data(sql=None, path_to_sql=None, conn=None, host='127.0.0.1', database="",
               sqltype="mysql+pymysql", port=3308, user_env="amazonRDS_user", password_env="amazonRDS_pw",
               username=None, password=None, load_comments=False, replace_sqlvar=None, replace_var=None, python=True):

    if sql is None and path_to_sql is not None:
        sql = load_sql(path_to_sql,
                       load_comments=load_comments,
                       replace_sqlvar=replace_sqlvar,
                       replace_var=replace_var,
                       python=python)
    elif sql is not None:
        sql = format_sql(sql,
                         replace_sqlvar=replace_sqlvar,
                         replace_var=replace_var,
                         python=python)
    else:
        raise ValueError("Only sql or path_to_sql should be provided")

    if conn is None:
        conn = create_connection(host=host, port=port, database=database, sqltype=sqltype, user_env=user_env,
                                 password_env=password_env, username=username, password=password)

    df = pd.read_sql(sql, con=conn)

    logger.info("Dataframe with %i rows loaded from query", len(df))

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--save', default=None, help='Path to where the dataset should be saved to (optional')

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = query_data(**config["load_data"])

    if args.save is not None:
        df.to_csv(args.save)