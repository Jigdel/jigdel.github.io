# https://databoys.github.io/Feedforward/
# neural network code provided in "Programming Collective Intelligence"
#
# think of every neuron as having an activation function
# this function determines whether the neuron is 'on' or 'off' - fires or not
# 

import numpy as np

def sigmoid(x):
	return 1/(1+np.exp(-x))

# derivative of sigmoid

# sigmoid(y) * (1.0 - sigmoid(y))

# the way we use this y is already sigmoided
def dsigmoid(y):
	return y*(1.0-y)

# Much like logistic regression, the sigmoid function in a neural 
# network will generate the end point (activation) of inputs multiplied
# by their weights

# Next, we set up the arrays to hold the data for network 
# and initialize some parameters
class MLP_NeuralNetwork(object):

	def __init__(self, input, hidden, output):
		"""
		:param input:  # of input neurons
		:param hidden: # of hidden neurons
		:param output: # of output neurons
		"""
		self.input = input + 1 # add 1 for bias mode
		self.hidden = hidden
		self.output = output

		#set up array of 1s for activations
		self.ai = [1.0]*self.input
		self.ah = [1.0]*self.hidden
		self.ao = [1.0]*self.output

		#create randomized weights
		self.wi = np.random.randn(self.input, self.hidden)
		self.wo = np.random.randn(self.hidden, self.output)

		#create arrays of 0 for changes
		self.ci = np.zeros((self.input, self.hidden))
		self.co = np.zeros((self.hidden, self.output))

		"""
		We are going to do all of these calculations with matricies because they are
		 fast and super easy to read. Our class will take three inputs; the size of the 
		 input layer (# features), the size of the hidden layer (variable parameter to be tuned),
		  and the number of the output layer (# of possible classes). We set up an array of 1s as 
		  a placeholder for the unit activations and an array of 0s as a placeholder for the 
		  layer changes. One important thing to note is that we initialized all of the weights to 
		  random numbers. It's important for the weights to be random otherwise we won't be able to 
		  tune the network. If all of the weights are the same then all of the hidden units will be
		  the same and you'll be screwed.
		"""

		# let's make some predictions
		# feed all of data forward thorugh network w/ random weights &
		# generate some (bad) predictions. we'll fine tune the weights
		# to get better predictions.

		def feedForward(self, inputs):

			if len(inputs) != self.input - 1:
				raise ValueError('Wrong number of inputs you silly goose!')

			# input activations
			for i in range(self.input - 1): # -1 is to avoid the bias
				self.ai[i] = inputs[i]

			# hidden activations
			for j in range(self.hidden):
				sum = 0.0
				for i in range(self.input):
					sum += self.ai[i] * self.wi[i][j]
				self.ah[j] = sigmoid(sum)

			# output activations
			for k in range(self.output):
				sum = 0.0
				for j in range(self.hidden):
					sum += self.ah[j] * self.wo[j][k]
				self.ao[k] = sigmoid(sum)

			return self.ao[:]

		# first pass, predictions bad, will use gradient descent
		# unlike GD for a linear model, we need to use bit of calculus for NN
		# hence the earlier derivative function for sigmoid function

		def backPropogate(self, targets, N):
			"""
			:param targets: y values
			:param N: 		learning rate
			:return: 		updated weights and current error
			"""

			if len(targets) != self.output:
				raise ValueError('Wrong # of targets.')

			#calculate error terms for output
			#the delta will tell you which direction to chnage the weights
			output_deltas = [0.0] * self.output

			for k in range(self.output):
				error = -(targets[k] - self.ao[k])
				output_deltas[k] = dsigmoid(self.ao[k]) * error

			# calculate error terms for hidden
			# delta tells you which direction to change the weight
			hidden_deltas = [0.0] * self.hidden

			for j in range(self.hidden):
				error = 0.0
				for k in range(self.output):
					error += output_deltas[k] * self.wo[j][k]

				hidden_deltas[j] = dsigmoid(self.ah[j]) * error

			# update the weights connecting hidden to output
			for j in range(self.hidden):
				for k in range(self.output):
					change = output_deltas[k]*self.ah[j]
					self.wo[j][k] -= N * change + self.co[j][k]
					self.co[j][k] = change
			
			# update the weights connecting input to hidden
			for i in range(self.input):
				for j in range(self.hidden):
					change = hidden_deltas[j] * self.ai[i]
					self.wi[i][j] -= N * change + self.ai[i]
					self.ci[i][j] = change

			# calculate error
			error = 0.0

			for k in range(len(targets)):
				error += 0.5 * (targets[k] - self.ao[k]) ** 2
			
			return error

			# tie it all together and create training & prediction functions

			def train(self, patterns, iterations = 3000, N = 0.0002):
				
				# N: learning rate

				for i in range(iterations):
					error = 0.0

					for p in patterns:
						inputs = p[0]
						targets = p[1]
						self.feedForward(inputs)
						error = self.backPropogate(targets, N)

					if i % 500 == 0:
						print('error %-.5f' % error)

			# we just simply call the feedForward function
			# will return the activation of the output layer
			# Remember activ. of each layer is a linear combination of the 
			# output of the previous layer * the corresponding weights pushed
			# through sigmoid

			def predict(self, X):
				"""
				return list of predictions after training algorithm
				"""
				predictions = []

				for p in X:
					predictions.append(self.feedForward(p))

				return predictions






