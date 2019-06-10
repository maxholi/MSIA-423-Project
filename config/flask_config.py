PORT = 3000
APP_NAME = "hof"
HOST = '0.0.0.0'

### MYSQL CONFIG ###
import os
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
#SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)

### SQLITE CONFIG ###
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/hof.db'


