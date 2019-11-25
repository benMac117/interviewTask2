import cPickle as cP
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from modelsDB import Prediction, PredictionSchema, Base

# trying to avoid saving the password in plain text
with open('proj.conf') as f:
   config = cP.load(f)

# initialise flask and database libraries
app = Flask(__name__)
databaseURL = 'mysql://{}:{}@localhost/{}'.format(config['MYSQL_USER'], config['MYSQL_PASS'], config['MYSQL_DB'])
if not database_exists(databaseURL):
    create_database(databaseURL)
app.config['SQLALCHEMY_DATABASE_URI'] = databaseURL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Base.metadata.create_all(db.engine)

if __name__ == '__main__':
    # debug=True should only be used during development
    app.run(debug=True)
