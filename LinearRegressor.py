import numpy as np

class LinearRegressor:
    def __init__(self, lRate=0.01, epochCap=100, loggingGap=20):
        self.lRate = lRate # Learning rate for the model
        self.epochCap = epochCap # How may training iterations the model should take
        self.loggingGap = loggingGap

    def cost(self, predictions, targets):
        """Calculate the current cost/loss for the model"""
        # I'm using the absolute rather than squared error to avoid spreading weights across a sparse feature set
        return np.mean(abs(targets - predictions))

    def calculate_gradients(self, samples, predictions, targets):
        """Calculate the gradients for optimising the model parameters"""
        return np.dot(samples.T, (predictions - targets)) / len(targets)

    # This return value is purely to make testing more clean, happy to discuss whether it is correct
    # Same with using weights rather than just self.weights -= ...
    def apply_gradients(self, weights, lRate, gradients):
        """Modify the model to minimise cost"""
        self.weights = weights - lRate * gradients
        return self.weights

    # I'm including the weights as a nullable parameter rather than using self.weights to make testing easier
    # This doesn't feel like the best solution
    def predict(self, samples, weights=None):
        """Make a prediction for a given input"""
        if weights is None:
            weights = self.weights
        # make sure we only add the intercept feature once, again this approach seems awkward
        if samples.shape[1] < self.weights.shape[0]:
            samplesI = np.append(np.ones([len(samples),1]), samples, axis=1)
        else:
            samplesI = samples

        return np.dot(weights, samplesI.T) # take the dot product of input with weights

    def fit(self, samples, targets):
        """Apply gradient decent to train a model given training data"""
        # append a column of ones for the intercept feature
        # if this causes memory issues we can modify the samples variable instead
        samplesI = np.append(np.ones([len(samples),1]), samples, axis=1)
        del samples # delete samples from memory
        self.weights = np.ones(samplesI.shape[1]) # initialise weights to 1, may perform better with some variation

        trainingLoss = []
        for epochCount in range(self.epochCap):
            # predict prices for the training data
            predictions = self.predict(samplesI, self.weights)

            if not epochCount % self.loggingGap or epochCount == self.epochCap-1: # print the loss every 'loggingGap' epochs
                loss = self.cost(predictions, targets)
                trainingLoss.append([epochCount, loss])

            # calculate the gradients given the cost function and modify the weights
            gradients = self.calculate_gradients(samplesI, predictions, targets)
            self.apply_gradients(self.weights, self.lRate, gradients)
        # Might be better to have these written to a log file
        return np.array(trainingLoss), self.weights
