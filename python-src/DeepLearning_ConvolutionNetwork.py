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
#Copyleft (Copyright+):
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
		self.sigmoidPerceptron=False
	        self.input_bitmap = input_bitmap
		self.max_pooling_inference = []
		self.weight=[[[2.05,2.05,2.05,2.05,2.05],
			      [2.05,2.09,2.09,2.09,2.05],
			      [2.05,2.09,2.09,2.09,2.05],
			      [2.05,2.09,2.09,2.09,2.05],
			      [2.05,2.09,2.09,2.09,2.05],
			      [2.05,2.05,2.05,2.05,2.05]],
			     [[2.06,2.06,2.06,2.06,2.06],
			      [2.06,2.09,2.09,2.09,2.06],
			      [2.06,2.09,2.09,2.09,2.06],
			      [2.06,2.09,2.09,2.09,2.06],
			      [2.06,2.09,2.09,2.09,2.06],
			      [2.06,2.06,2.06,2.06,2.06]],
			     [[2.07,2.07,2.07,2.07,2.07],
			      [2.07,2.09,2.09,2.09,2.07],
			      [2.07,2.09,2.09,2.09,2.07],
			      [2.07,2.09,2.09,2.09,2.07],
			      [2.07,2.09,2.09,2.09,2.07],
			      [2.07,2.07,2.07,2.07,2.07]]]
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
		return float(1.0/(1.0+math.exp(-1.0*perceptron)))

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

	def max_pooling(self,pooling_slidewindow_width):
		for convolution_map_index in xrange(3):
			row=col=0
			k=l=0
			while row < len(self.convolution_map[convolution_map_index])-1:
		   		while col < len(self.convolution_map[convolution_map_index])-1:
					maximum = self.find_maximum(self.convolution_map[convolution_map_index][row][col], self.convolution_map[convolution_map_index][row+1][col], self.convolution_map[convolution_map_index][row][col+1], self.convolution_map[convolution_map_index][row+1][col+1])
					self.max_pooling_map[convolution_map_index][k][l]=maximum
					col=col+pooling_slidewindow_width
					l=l+1
		   		col=0
		   		l=0
				row=row+pooling_slidewindow_width
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

	#Connects all points in all max pooling layers into a single neural activation function
	def infer_from_max_pooling(self,max_pooling_map,pooling_neuron_weight,maxpool_map_width):
		weighted_sum=0.0
		self.max_pooling_inference=[]
		for p in xrange(maxpool_map_width):
			for q in xrange(maxpool_map_width):
				for convolution_map_index in xrange(3):
					weighted_sum = weighted_sum + max_pooling_map[convolution_map_index][p][q]*(self.weight[convolution_map_index][p][q])
		if self.sigmoidPerceptron==True:
			self.max_pooling_inference.append(self.sigmoid(weighted_sum+self.bias))
		else:
			self.max_pooling_inference.append((weighted_sum+self.bias))
		return self.max_pooling_inference
                       
			
if __name__=="__main__":
	#An example input picture bitmap with '0' inscribed as set of 1s
	input_bitmap1=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,1,1,1,1,1,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,1,1,1,1,1,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	#An example input picture bitmap with '8' inscribed as set of 1s
	input_bitmap2=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,1,1,1,1,1,1,1,1,1,1,0,0],
		[0,0,1,1,1,1,1,1,1,1,1,1,0,0],
		[0,0,1,1,1,0,0,0,1,1,1,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0,0,0,0,0],
		[0,0,1,1,1,0,0,0,1,1,1,0,0,0],
		[0,0,1,1,1,0,0,0,1,1,1,1,0,0],
		[0,0,1,1,1,1,1,1,1,1,1,1,0,0],
		[0,0,1,1,1,1,1,1,1,1,1,1,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	#An example input picture bitmap with no patterns
	input_bitmap3=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	#An example input picture bitmap with no patterns
	input_bitmap4=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[1,1,1,0,0,0,0,0,0,0,0,1,1,1],
		[0,1,1,0,0,0,0,0,0,0,1,1,1,0],
		[0,1,1,1,0,0,0,0,0,1,1,1,0,0],
		[0,0,1,1,1,0,0,1,1,1,1,0,0,0],
		[0,0,0,1,1,1,1,1,1,1,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,0,0,0,0,0,0],
		[0,0,0,0,1,1,1,1,0,0,0,0,0,0],
		[0,0,0,1,1,1,1,1,1,0,0,0,0,0],
		[0,0,1,1,1,0,0,1,1,1,0,0,0,0],
		[0,1,1,1,0,0,0,0,1,1,1,0,0,0],
		[1,1,1,0,0,0,0,0,0,1,1,1,0,0],
		[1,1,0,0,0,0,0,0,0,0,1,1,1,0]]

	#An example input picture bitmap with no patterns
	input_bitmap5=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,1,0,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,0,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	dlc1=DeepLearningConvolution(input_bitmap1)
	dlc2=DeepLearningConvolution(input_bitmap2)
	dlc3=DeepLearningConvolution(input_bitmap3)
	dlc4=DeepLearningConvolution(input_bitmap4)
	dlc5=DeepLearningConvolution(input_bitmap5)

	#maximum stride is 5
	convolution_stride=2
	conv_map1=dlc1.convolution(convolution_stride)
	conv_map2=dlc2.convolution(convolution_stride)
	conv_map3=dlc3.convolution(convolution_stride)
	conv_map4=dlc4.convolution(convolution_stride)
	conv_map5=dlc5.convolution(convolution_stride)

	#maximum pool sliding window width is 5
	pool_slidewindow_width=2
	pool_map1=dlc1.max_pooling(pool_slidewindow_width)
	pool_map2=dlc2.max_pooling(pool_slidewindow_width)
	pool_map3=dlc3.max_pooling(pool_slidewindow_width)
	pool_map4=dlc4.max_pooling(pool_slidewindow_width)
	pool_map5=dlc5.max_pooling(pool_slidewindow_width)

	print "##########################################"
	print "Set of Convolution Maps"
	print "##########################################"
	print "Example 1:"
	print "###########"
	pprint.pprint(conv_map1)
	print "###########"
	print "Example 2:"
	print "###########"
	pprint.pprint(conv_map2)
	print "###########"
	print "Example 3:"
	print "###########"
	pprint.pprint(conv_map3)
	print "###########"
	print "Example 4:"
	print "###########"
	pprint.pprint(conv_map4)
	print "###########"
	print "Example 5:"
	print "###########"
	pprint.pprint(conv_map5)
	print "##########################################"
	print "Max Pooling Map"
	print "##########################################"
	print "Example 1:"
	print "###########"
	pprint.pprint(pool_map1)
	print "###########"
	print "Example 2:"
	print "###########"
	pprint.pprint(pool_map2)
	print "###########"
	print "Example 3:"
	print "###########"
	pprint.pprint(pool_map3)
	print "###########"
	print "Example 4:"
	print "###########"
	pprint.pprint(pool_map4)
	print "###########"
	print "Example 5:"
	print "###########"
	pprint.pprint(pool_map5)
	print "####################################################################################################"
	print "Final layer that connects all neurons in max pooling map into set of 10 neurons"
	print "####################################################################################################"
	maxpool_map_width=5
	for w in xrange(10):
		print "###########################################################################################"
		print "Inference from Max Pooling Layer - Neuron ",w
		print "###########################################################################################"
		print "Example 1:"
		print "###########"
		pprint.pprint(dlc1.infer_from_max_pooling(pool_map1,float(random.randint(1,w+1))/float(w+1),maxpool_map_width))
		print "###########"
		print "Example 2:"
		print "###########"
		pprint.pprint(dlc2.infer_from_max_pooling(pool_map2,float(random.randint(1,w+1))/float(w+1),maxpool_map_width))
		print "###########"
		print "Example 3:"
		print "###########"
		pprint.pprint(dlc3.infer_from_max_pooling(pool_map3,float(random.randint(1,w+1))/float(w+1),maxpool_map_width))
		print "###########"
		print "Example 4:"
		print "###########"
		pprint.pprint(dlc4.infer_from_max_pooling(pool_map4,float(random.randint(1,w+1))/float(w+1),maxpool_map_width))
		print "###########"
		print "Example 5:"
		print "###########"
		pprint.pprint(dlc5.infer_from_max_pooling(pool_map5,float(random.randint(1,w+1))/float(w+1),maxpool_map_width))
