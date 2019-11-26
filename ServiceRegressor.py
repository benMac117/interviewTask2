from LinearRegressor import LinearRegressor
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import numpy as np

class ServiceRegressor(LinearRegressor, object):
    def __init__(self):
        self.featureScaler = MinMaxScaler()
        self.monthEncoder = OneHotEncoder(sparse=False)
        self.typeEncoder = OneHotEncoder(sparse=False)
        self.regionEncoder = OneHotEncoder(sparse=False)
        super(ServiceRegressor, self).__init__(lRate=0.05, epochCap=150, loggingGap=500)

    def fit(self, dataFilepath):
        # There is a discussion here about saving access time loading all the data cast to string and slicing for the operations below vs saving memory by only loading what we need
        # Select and scale simple numeric features
        scaledData = self.featureScaler.fit_transform(np.loadtxt(dataFilepath, delimiter=',', usecols=range(1,9)+[11]))
        # Quite a lot going on here. We load the 3 categorical features, pass them through a one-hot encoder, and append the resulting columns to our dataset
        scaledData = np.concatenate((scaledData, self.monthEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[12]).reshape(-1,1)),
            self.typeEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[9]).reshape(-1,1)), 
            self.regionEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[10]).reshape(-1,1))), axis=1)
        
        targetPrices = np.loadtxt(dataFilepath, delimiter=',', usecols=[0])
        trainingLosses, weights = super(ServiceRegressor, self).fit(scaledData, targetPrices)
        np.savetxt('data/training.csv', trainingLosses, delimiter=',')

    # I had naming difficulties calling this function 'predict' as the fit function in the parent class calls the parent predict via self.predict
    def format_and_predict(self, inputFeatures):
        # Select and scale simple numeric features
        scaledData = self.featureScaler.transform(inputFeatures[:,range(0,8)+[10]].astype(float))
        # Load the 3 categorical features, pass them through a one-hot encoder, and append the resulting columns to our dataset
        scaledData = np.concatenate((scaledData, self.monthEncoder.transform(inputFeatures[:,11].reshape(-1,1)),
            self.typeEncoder.transform(inputFeatures[:,8].reshape(-1,1)), 
            self.regionEncoder.transform(inputFeatures[:,9].reshape(-1,1))), axis=1)

        return super(ServiceRegressor, self).predict(scaledData)

         