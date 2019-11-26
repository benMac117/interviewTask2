import numpy 
import requests
import numpy as np

testFeatures = np.loadtxt('data/avocadoCleanedTest.csv', delimiter=',', dtype='|S20')
testTargets = testFeatures[:,0]
testFeatures = testFeatures[:,1:]
totalSamples = len(testFeatures)

# This should return a single prediction (and feature vector), with a price close to 0.98 (though I did not work this out myself), the features returned should match those sent
singleTestResults = requests.get('http://localhost:5000/prediction', json={'inputFeatures': testFeatures[:1].tolist()})
# This should return two predictions
doubleTestResults = requests.get('http://localhost:5000/prediction', json={'inputFeatures': testFeatures[1:3].tolist()})
# This should return the remaining predictions
remainingTestResults = requests.get('http://localhost:5000/prediction', json={'inputFeatures': testFeatures[3:].tolist()})
# This should return all 1824 predictions (unless the test has been run twice without clearing the database)
totalResults = requests.get('http://localhost:5000/predictions')

from IPython import embed; embed()
