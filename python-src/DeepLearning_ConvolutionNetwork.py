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
class DeepLearningConvolution(object):
	def __init__(self,input_bitmap):
	        self.input_bitmap = input_bitmap
		self.weight=0.2
		self.convolution_map=[[0,0,0,0,0,0,0,0,0,0],
 	      			      [0,0,0,0,0,0,0,0,0,0],
	     			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0],
	      			      [0,0,0,0,0,0,0,0,0,0]]
		self.max_pooling_map=[[0,0,0,0,0],
				      [0,0,0,0,0],
		                      [0,0,0,0,0],
		                      [0,0,0,0,0],
		                      [0,0,0,0,0]]
		self.bias=0.05

	def sigmoid(self, perceptron):
		# 1/(1+e^(-z))
		return 1/(1+math.exp(-1*perceptron))

	def receptive_field_window(self,i,j,stride):
		rfw=0.0
		for p in xrange(stride):
		   for q in xrange(stride):
			if i+p < 10 and j+q < 10:
			   rfw = rfw + self.input_bitmap[i+p][j+q]	
		return rfw	

	def convolution(self,stride):
		for i in xrange(10):
		    for j in xrange(10):
                        self.convolution_map[i][j] = self.sigmoid(self.bias+self.receptive_field_window(i,j,stride))
		return self.convolution_map	

	def max_pooling(self,conv_map,pooling_width):
		row=col=0
		k=l=0
		while row < 10:
		   while col < 10:
			maximum = self.find_maximum(self.convolution_map[row][col], self.convolution_map[row+1][col],
				     self.convolution_map[row][col+1], self.convolution_map[row+1][col+1])
			self.max_pooling_map[k][l]=maximum
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

	def infer_from_max_pooling(self,max_pooling_map,weight):
		bias=0.1
		weighted_sum=0.0
		for p in xrange(5):
		   for q in xrange(5):
			weighted_sum = weighted_sum + max_pooling_map[p][q]*weight
		return self.sigmoid(weighted_sum+bias)	
                       
			

#An example input picture with '0' inscribed as set of 1s
input_bitmap=[[0,0,0,0,0,0,0,0,0,0],
 	      [0,0,0,0,0,0,0,0,0,0],
	      [0,0,0,1,1,1,1,0,0,0],
	      [0,0,0,1,0,0,1,0,0,0],
	      [0,0,0,1,0,0,1,0,0,0],
	      [0,0,0,1,0,0,1,0,0,0],
	      [0,0,0,1,0,0,1,0,0,0],
	      [0,0,0,1,1,1,1,0,0,0],
	      [0,0,0,0,0,0,0,0,0,0],
	      [0,0,0,0,0,0,0,0,0,0]]
dlc=DeepLearningConvolution(input_bitmap)
conv_map1=dlc.convolution(2)
pool_map1=dlc.max_pooling(conv_map1,2)
print "##########################################"
print "Convolution Map"
print "##########################################"
print conv_map1
print "##########################################"
print "Max Pooling Map"
print "##########################################"
print pool_map1
print "####################################################################################################"
print "Percentage probability - Final layer that connects all neurons in max pooling map into set of 5 neurons"
print "####################################################################################################"
for w in xrange(5):
	print dlc.infer_from_max_pooling(pool_map1,w*0.265) * 100


