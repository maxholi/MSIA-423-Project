import traceback
from flask import render_template, request, redirect, url_for
from flask import Flask
from models import Current
from models import Similarity
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sql
from sqlalchemy import create_engine, MetaData, select
import logging

logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

db = SQLAlchemy(app)

# Initialize the database
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def index():
    """Main view that lists current or recently retired players in the database
    Create view into index page that uses data queried from Current database and
    inserts it into the index.html template.
    Returns: rendered html template
    """
    # query all players from the current table to populate dropdown
    try:
        players = db.session.query(Current.PLAYER)
        logger.debug("Index page accessed")
        return render_template('index.html', players=players)

    except:
        logger.warning("Not able to display home page, error page returned")
        return render_template('error.html')

@app.route('/result', methods=['POST'])
def result():

    """ results page that outputs the player's predicted probability at making hte HOF and
    also  a table of the top 10 most similar players based on career statistics
    Returns: rendered html template"""

    try:

        # get predicted prob
        user_input = str(request.form["pl"])
        pred = db.session.query(Current.PROB).filter_by(PLAYER=user_input).all()
        pred = "{0:.0%}".format(pred[0][0])

        # get player similarity
        similar = db.session.query(Similarity.Hist_Player, Similarity.HOF).filter_by(Player=user_input).all()
        similar_all = db.session.query(Similarity.Hist_Player, Similarity.HOF).filter_by(Player=user_input).count()
        similar_hof = db.session.query(Similarity.Hist_Player, Similarity.HOF).filter_by(Player=user_input,HOF=1).count()
        return render_template('result.html', user_input=user_input,pred=pred, similar=similar,similar_all=similar_all, similar_hof=similar_hof )

    except:

        logger.warning("Not able to display results page, error page returned")
        return render_template('error.html')

if __name__ == "__main__":


   app.run(host = app.config['HOST'], use_reloader=True, port=app.config['PORT'])









