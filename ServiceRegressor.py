from LinearRegressor import LinearRegressor
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import numpy as np

class ServiceRegressor(LinearRegressor, object):
    def __init__(self):
        self.featureScaler = MinMaxScaler()
        self.monthEncoder = OneHotEncoder(sparse=False)
        self.typeEncoder = OneHotEncoder(sparse=False)
        self.regionEncoder = OneHotEncoder(sparse=False)
        super(ServiceRegressor, self).__init__()

    def fit(self, dataFilepath):
        #dataset = np.loadtxt(dataFilepath, delimiter=',')
        
        # Select and scale simple numeric features
        scaledData = self.featureScaler.fit_transform(np.loadtxt(dataFilepath, delimiter=',', usecols=range(1,9)+[11]))
        # Quite a lot going on here. We load the 3 categorical features, pass them through a one-hot encoder, and append the resulting columns to our dataset
        scaledData = np.concatenate((scaledData, self.monthEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[12]).reshape(-1,1)),
            self.typeEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[9]).reshape(-1,1)), 
            self.regionEncoder.fit_transform(np.loadtxt(dataFilepath, delimiter=',', dtype='|S20', usecols=[10]).reshape(-1,1))), axis=1)
        
        targetPrices =  np.loadtxt(dataFilepath, delimiter=',', usecols=[0]).reshape(-1,1)
        print(targetPrices[0])
        super(ServiceRegressor, self).fit(scaledData, targetPrices)


