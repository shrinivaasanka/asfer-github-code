#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

############################################################################################################################
# Convolution Networks for Deep Learning:
#----------------------------------------
#  Input bitmap (e.g JPEG image) ===> Hidden Layer Convolution Feature Map ===> Pooling Map (E.g Max Pooling)
# 
# where Convolution is defined as a function that maps a sub-square of bits (receptive field) to a bit in Hidden Layer and sub-square is
# moved across the bitmap (stride or sliding window). Pooling layer condenses the convoluted hidden layer into a smaller map
# by choosing the maximum of bits in a sub-square of convolution.
#
#  bit(k,l) of convoluted layer = sigmoid_perceptron(bias + double-summation(activations-of-bits-in-subsquare*weight))
#
# Following implementation has only one layer in convolution and pooling. The weights and biases that minimize the cost
# function (or error from expected output) might have to be learnt through standard 4 backpropagation 
# partial differential equations which are non-trivial. Convolution is deep in the sense that hidden structure in
# input is learnt. Has some similarities to construction of a hologram.
# Reference: http://neuralnetworksanddeeplearning.com
############################################################################################################################

import math
import pprint
import random

class DeepLearningConvolution(object):
	def __init__(self,input_bitmap):
	        self.input_bitmap = input_bitmap
		self.max_pooling_inference = []
		self.weight=[[[0.1,0.1,0.1,0.1,0.1],
			      [0.1,0.1,0.1,0.1,0.1],
			      [0.1,0.1,0.1,0.1,0.1],
			      [0.1,0.1,0.1,0.1,0.1],
			      [0.1,0.1,0.1,0.1,0.1],
			      [0.1,0.1,0.1,0.1,0.1]],
			     [[0.2,0.2,0.2,0.2,0.2],
			      [0.2,0.2,0.2,0.2,0.2],
			      [0.2,0.2,0.2,0.2,0.2],
			      [0.2,0.2,0.2,0.2,0.2],
			      [0.2,0.2,0.2,0.2,0.2],
			      [0.2,0.2,0.2,0.2,0.2]],
			     [[0.3,0.3,0.3,0.3,0.3],
			      [0.3,0.3,0.3,0.3,0.3],
			      [0.3,0.3,0.3,0.3,0.3],
			      [0.3,0.3,0.3,0.3,0.3],
			      [0.3,0.3,0.3,0.3,0.3],
			      [0.3,0.3,0.3,0.3,0.3]]]
		self.convolution_map=[[[0,0,0,0,0,0,0,0,0,0],
 	      			       [0,0,0,0,0,0,0,0,0,0],
	     			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0]],
				      [[0,0,0,0,0,0,0,0,0,0],
 	      			       [0,0,0,0,0,0,0,0,0,0],
	     			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0]],
				      [[0,0,0,0,0,0,0,0,0,0],
 	      			       [0,0,0,0,0,0,0,0,0,0],
	     			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0],
	      			       [0,0,0,0,0,0,0,0,0,0]]]
		self.max_pooling_map=[[[0,0,0,0,0],
				       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0]],
				      [[0,0,0,0,0],
				       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0]],
				      [[0,0,0,0,0],
				       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0],
		                       [0,0,0,0,0]]]
		self.bias=0.05

	def sigmoid(self, perceptron):
		# 1/(1+e^(-z))
		return 1/(1+math.exp(-1*perceptron))

	def receptive_field_window(self,i,j,stride,convolution_map_index):
		rfw=0.0
		for p in xrange(stride):
		   for q in xrange(stride):
			if i+p < 10 and j+q < 10:
			   rfw = rfw + self.input_bitmap[i+p][j+q]*self.weight[convolution_map_index][p][q]
		return rfw	

	def convolution(self,stride):
		for convolution_map_index in xrange(3):
			for i in xrange(10):
		   		 for j in xrange(10):
                       			 self.convolution_map[convolution_map_index][i][j] = self.sigmoid(self.bias+self.receptive_field_window(i,j,stride,convolution_map_index))
			convolution_map_index+=1
		return self.convolution_map	

	def max_pooling(self,pooling_width):
		for convolution_map_index in xrange(3):
			row=col=0
			k=l=0
			while row < len(self.convolution_map[convolution_map_index])-1:
		   		while col < len(self.convolution_map[convolution_map_index])-1:
					maximum = self.find_maximum(self.convolution_map[convolution_map_index][row][col], self.convolution_map[convolution_map_index][row+1][col], self.convolution_map[convolution_map_index][row][col+1], self.convolution_map[convolution_map_index][row+1][col+1])
					self.max_pooling_map[convolution_map_index][k][l]=maximum
					col=col+pooling_width
					l=l+1
		   		col=0
		   		l=0
		   		row=row+pooling_width
		   		k=k+1
		return self.max_pooling_map
			
	def find_maximum(self,a,b,c,d):
		maximum=a
		if b > maximum:
		   maximum=b
		if c > maximum:
		   maximum=c
		if d > maximum:
		   maximum=d
		return maximum	

	def infer_from_max_pooling(self,max_pooling_map,pooling_neuron_weight,pool_width):
		weighted_sum=[]
		self.max_pooling_inference=[]
		for convolution_map_index in xrange(3):
			weighted_sum.append(0.0)
		for convolution_map_index in xrange(3):
			for p in xrange(pool_width):
		   		for q in xrange(pool_width):
					weighted_sum[convolution_map_index] = weighted_sum[convolution_map_index] + max_pooling_map[convolution_map_index][p][q]*(pooling_neuron_weight*self.weight[convolution_map_index][p][q])
			self.max_pooling_inference.append(self.sigmoid(weighted_sum[convolution_map_index]+self.bias))
		return self.max_pooling_inference
                       
			

#An example input picture with '0' inscribed as set of 1s
input_bitmap1=[[0,0,0,0,0,0,0,0,0,0],
 	      [0,0,0,0,0,0,0,0,0,0],
	      [0,1,1,1,1,1,1,1,1,0],
	      [0,1,1,1,1,1,1,1,1,0],
	      [0,1,1,1,0,0,1,1,1,0],
	      [0,1,1,1,0,0,1,1,1,0],
	      [0,1,1,1,1,1,1,1,1,0],
	      [0,1,1,1,1,1,1,1,1,0],
	      [0,0,0,0,0,0,0,0,0,0],
	      [0,0,0,0,0,0,0,0,0,0]]

#An example input picture with '3' inscribed as set of 1s
input_bitmap2=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
 	      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	      [0,0,1,1,1,1,1,1,1,1,1,0,0,0],
      	      [0,0,1,1,1,1,1,1,1,1,1,0,0,0],
	      [0,0,1,0,0,0,0,0,1,1,0,0,0,0],
	      [0,0,0,0,0,0,0,1,1,0,0,0,0,0],
	      [0,0,0,0,0,0,1,1,1,1,1,0,0,0],
	      [0,0,0,0,0,0,1,1,1,1,1,0,0,0],
	      [0,0,0,0,0,0,0,0,0,1,1,0,0,0],
	      [0,0,1,0,0,0,0,0,0,1,1,0,0,0],
	      [0,0,1,1,1,1,1,1,1,1,1,0,0,0],
	      [0,0,1,1,1,1,1,1,1,1,1,0,0,0],
	      [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	      [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

dlc=DeepLearningConvolution(input_bitmap2)

#maximum stride is 5
convolution_stride=2
conv_map1=dlc.convolution(convolution_stride)

#maximum pool width is 5
pool_width=2
pool_map1=dlc.max_pooling(pool_width)

print "##########################################"
print "Set of Convolution Maps"
print "##########################################"
pprint.pprint(conv_map1)
print "##########################################"
print "Max Pooling Map"
print "##########################################"
print pool_map1
print "####################################################################################################"
print "Final layer that connects all neurons in max pooling map into set of 10 neurons"
print "####################################################################################################"
for w in xrange(10):
	print "###########################################################################################"
	print "Inference from Max Pooling Layer - Neuron ",w
	print "###########################################################################################"
	print dlc.infer_from_max_pooling(pool_map1,float(random.randint(1,w+1))/float(w+1),pool_width)
