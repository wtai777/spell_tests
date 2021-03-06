# Boltzmann Machiens

import numpy as np 
import pandas as pd 
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable

# Cause you can't print in Spell
file = open("BM_loss.txt","w")

# Importing the Dataset
movies = pd.read_csv('m1-1m/movies.dat',sep="::",header=None,engine='python',encoding='latin-1')
users = pd.read_csv('m1-1m/users.dat',sep="::",header=None,engine='python',encoding='latin-1')
ratings = pd.read_csv('m1-1m/ratings.dat',sep="::",header=None,engine='python',encoding='latin-1')

# Preparing the training set and the test set
training_set = pd.read_csv('m1-100k/u1.base',delimiter='\t')
training_set = np.array(training_set,dtype='int')
test_set = pd.read_csv('m1-100k/u1.test',delimiter='\t')
test_set = np.array(test_set,dtype='int')

# Getting the number of users and movies
nb_users = int(max(max(training_set[:,0]),max(test_set[:,0])))
nb_movies = int(max(max(training_set[:,1]),max(test_set[:,1])))

# Converting the data into an array with users in lines and movies in columns
def convert(data):
	new_data = []
	for id_users in range(1,nb_users+1):
		id_movies = data[:,1][data[:,0] == id_users]
		id_ratings = data[:,2][data[:,0] == id_users]
		ratings = np.zeros(nb_movies)
		ratings[id_movies-1] = id_ratings
		new_data.append(list(ratings))
	return new_data

training_set = convert(training_set)
test_set = convert(test_set)

# Converting the data into Torch tensors
training_set = torch.FloatTensor(training_set)
test_set = torch.FloatTensor(test_set)

# Creating the artchitecture of the Neural Network
class SAE(nn.Module):
	def __init__(self,):
		super(SAE, self).__init__()
		self.fc1 = nn.Linear(nb_movies,20)
		self.fc2 = nn.Linear(20,10)
		self.fc3 = nn.Linear(10,20)
		self.fc4 = nn.Linear(20,nb_movies)
		self.activation = nn.Sigmoid()

	def forward(self,x):
		x = self.activation(self.fc1(x))
		x = self.activation(self.fc2(x))
		x = self.activation(self.fc3(x))
		x = self.fc4(x)
		return x

sae = SAE()
criterion = nn.MSELoss()
optimizer = optim.RMSprop(sae.parameters(),lr=0.01,weight_decay=0.5)

# Training the SAE
nb_epoch = 200
































































