from __future__ import division
import cPickle as cP
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from modelsDB import Prediction, PredictionSchema, Base
import numpy as np
from ServiceRegressor import ServiceRegressor

ServiceRegressor = ServiceRegressor()
# Initialise database connection and app
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

with app.app_context():
    predictionSchema = PredictionSchema(strict=True)
    predictionsSchema = PredictionSchema(strict=True, many=True)

# Get single recipe
@app.route('/prediction', methods=['GET'])
def get_prediction(inputFeatures):
    #inputFeatures = request.json['inputFeatures']
    predictedPrices = ServiceRegressor.format_and_predict(inputFeatures)
    predictions = []
    for feats, pred in zip(inputFeatures, predictedPrices):
        newPrediction = Prediction(pred, *feats)
        predictions.append(newPrediction)
        db.session.add(newPrediction)
    db.session.commit()
    with app.app_context():
        returnPacket = predictionsSchema.jsonify(predictions)
    return returnPacket

if __name__ == '__main__':
    # debug=True should only be used during development
    #app.run(debug=True)
    ServiceRegressor.fit('data/avocadoCleanedTrain.csv')

    testFeatures = np.loadtxt('data/avocadoCleanedTest.csv', delimiter=',', dtype='|S20')
    get_prediction(testFeatures[:,1:])
