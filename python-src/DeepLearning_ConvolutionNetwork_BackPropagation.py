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
# function (or error from expected output) are learnt through backpropagation implementation .
# Convolution is deep in the sense that hidden structure in  input is learnt. Has some similarities to construction of a hologram.
# Reference: http://neuralnetworksanddeeplearning.com
############################################################################################################################

import math
from PIL import Image
import numpy
import pprint
import random
import DeepLearning_BackPropagation
import ImageToBitMatrix 

class DeepLearningConvolution(object):
	def __init__(self,input_bitmap):
		self.sigmoidPerceptron=False
	        self.input_bitmap = input_bitmap
		self.max_pooling_inference = []
		self.weight=[[[0.07,0.07,0.07,0.07,0.07],
			      [0.07,0.07,0.07,0.07,0.07],
			      [0.07,0.07,0.07,0.07,0.07],
			      [0.07,0.07,0.07,0.07,0.07],
			      [0.07,0.07,0.07,0.07,0.07],
			      [0.07,0.07,0.07,0.07,0.07]],
			     [[0.08,0.08,0.08,0.08,0.08],
			      [0.08,0.08,0.08,0.08,0.08],
			      [0.08,0.08,0.08,0.08,0.08],
			      [0.08,0.08,0.08,0.08,0.08],
			      [0.08,0.08,0.08,0.08,0.08],
			      [0.08,0.08,0.08,0.08,0.08]],
			     [[0.09,0.09,0.09,0.09,0.09],
			      [0.09,0.09,0.09,0.09,0.09],
			      [0.09,0.09,0.09,0.09,0.09],
			      [0.09,0.09,0.09,0.09,0.09],
			      [0.09,0.09,0.09,0.09,0.09],
			      [0.09,0.09,0.09,0.09,0.09]]]
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
			if i+p < len(self.input_bitmap[0]) and j+q < len(self.input_bitmap[0]):
			   #dynamic_weight=self.weight[convolution_map_index][p][q]*self.input_bitmap[i+p][j+q]*(p+q+1)/(p*q+1)
			   rfw = rfw + self.input_bitmap[i+p][j+q]*self.weight[convolution_map_index][p][q]
			   #rfw = rfw + self.input_bitmap[i+p][j+q]*dynamic_weight
		return rfw

	def convolution(self,stride):
		for convolution_map_index in xrange(3):
			for i in xrange(10):
		   		 for j in xrange(10):
					self.convolution_map[convolution_map_index][i][j] = self.bias+self.receptive_field_window(i,j,stride,convolution_map_index)
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

	#Connects all points in all max pooling layers into a single neural activation function and does
	#backpropagation iterations to recompute weights
	def infer_from_max_pooling(self,max_pooling_map,maxpool_map_width):
		weights=[]
		for convmap in xrange(3):
			weights.append([])
		for convmap in xrange(3):
			for k in xrange(maxpool_map_width*maxpool_map_width*maxpool_map_width*maxpool_map_width*2):
				weights[convmap].append(0.01)
		inputlayer=[]
		hiddenlayer=[]
		expectedoutput=[]
        	#parameters - initial conditions - inputlayer,hiddenlayer,expectedoutputlayer,weights_array - for arbitrary number of variables
		self.max_pooling_inference=[]
		for convmap in xrange(3):
			for p in xrange(maxpool_map_width):
				for q in xrange(maxpool_map_width):
        				inputlayer.append(max_pooling_map[convmap][p][q])
        				hiddenlayer.append(0.1)
					expectedoutput.append(0.1*max_pooling_map[convmap][p][q])
        		bpnn=DeepLearning_BackPropagation.BackPropagation(inputlayer,hiddenlayer,expectedoutput,weights[convmap])
        		bpnn.compute_neural_network()
			#bpnn.print_layers()
			iter=0
		        while iter < 10:
               			 for m in xrange(len(inputlayer)):
		                        for l in xrange(len(inputlayer)):
                		               bpnn.backpropagation_pde_update_hidden_to_output(m,len(weights)/2 + len(inputlayer)*m + l)

			         for m in xrange(len(inputlayer)):
		                        for l in xrange(len(inputlayer)):
               			               bpnn.backpropagation_pde_update_input_to_hidden(m,len(inputlayer)*m+l)

		                 #print "Recomputing Neural Network after backpropagation weight update"
               			 bpnn.compute_neural_network()
                		 #print "Error after Backpropagation- iteration :",iter
		                 #print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
		                 #print "Layers in this iteration:"
               			 #bpnn.print_layers()
		                 #print "Weights updated in this iteration:"
		                 #print bpnn.weights
	   	                 iter=iter+1

			weighted_sum=0.0
			for p in xrange(maxpool_map_width):
				for q in xrange(maxpool_map_width):
					weighted_sum = weighted_sum + max_pooling_map[convmap][p][q]*(bpnn.weights[p*(maxpool_map_width)+q])
			if self.sigmoidPerceptron==True:
				self.max_pooling_inference.append(self.sigmoid(weighted_sum+self.bias))
			else:
				self.max_pooling_inference.append((weighted_sum+self.bias))
			inputlayer=[]
			hiddenlayer=[]
			expectedoutput=[]
		return self.max_pooling_inference

if __name__=="__main__":
	#An example input picture bitmap with '0' inscribed as set of 1s
	input_bitmap11=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

	input_bitmap12=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,1,1,1,1,1,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,1,1,1,1,1,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	#An example input picture bitmap with '8' inscribed as set of 1s
	input_bitmap21=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

	input_bitmap22=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,1,1,1,1,1,1,1,1,1,1,0,0],
		[0,0,1,0,0,0,0,0,0,0,0,1,0,0],
		[0,0,1,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,0,1,0,0,0,0,0,1,0,0,0,0],
		[0,0,0,0,1,0,0,0,1,0,0,0,0,0],
		[0,0,0,0,1,1,1,1,1,0,0,0,0,0],
		[0,0,0,1,1,0,0,0,0,1,0,0,0,0],
		[0,0,1,0,0,0,0,0,0,0,1,0,0,0],
		[0,0,1,0,0,0,0,0,0,0,0,1,0,0],
		[0,0,1,0,0,0,0,0,0,0,0,1,0,0],
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

	#An example input picture bitmap with pattern X inscribed with 1s
	input_bitmap41=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

	input_bitmap42=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[1,1,0,0,0,0,0,0,0,0,0,0,1,1],
		[1,1,0,0,0,0,0,0,0,0,0,1,1,0],
		[0,1,1,0,0,0,0,0,0,0,1,1,0,0],
		[0,0,1,1,0,0,0,0,0,1,1,0,0,0],
		[0,0,0,1,1,0,0,0,1,1,0,0,0,0],
		[0,0,0,0,1,1,0,1,1,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,0,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,1,1,0,0,1,1,0,0,0,0],
		[0,0,0,1,1,0,0,0,0,1,1,0,0,0],
		[0,0,1,1,0,0,0,0,0,0,1,1,0,0],
		[0,1,1,0,0,0,0,0,0,0,0,1,1,0],
		[1,1,0,0,0,0,0,0,0,0,0,0,1,1]]


	#An example input picture bitmap with pattern 1 inscribed with 1s
	input_bitmap51=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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

	input_bitmap52=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,1,0,0,0,0,0],
		[0,0,0,0,0,0,0,1,1,0,0,0,0,0],
		[0,0,0,0,0,1,1,1,1,1,1,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

	input_image1 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141138.jpg")
	input_image2 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141144.jpg")
	input_image3 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141152.jpg")
	input_image4 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_131709.jpg")
	input_image5 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg")
	input_image6 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_2.jpg")
	input_image7 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf2_1.jpg")
	input_image8 = ImageToBitMatrix.image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf8_1.jpg")

	dlim1=DeepLearningConvolution(input_image1)
	dlim2=DeepLearningConvolution(input_image2)
	dlim3=DeepLearningConvolution(input_image3)
	dlim4=DeepLearningConvolution(input_image4)
	dlim5=DeepLearningConvolution(input_image5)
	dlim6=DeepLearningConvolution(input_image6)
	dlim7=DeepLearningConvolution(input_image7)
	dlim8=DeepLearningConvolution(input_image8)

	dlc11=DeepLearningConvolution(input_bitmap11)
	dlc12=DeepLearningConvolution(input_bitmap12)
	dlc21=DeepLearningConvolution(input_bitmap21)
	dlc22=DeepLearningConvolution(input_bitmap22)
	dlc3=DeepLearningConvolution(input_bitmap3)
	dlc41=DeepLearningConvolution(input_bitmap41)
	dlc42=DeepLearningConvolution(input_bitmap42)
	dlc51=DeepLearningConvolution(input_bitmap51)
	dlc52=DeepLearningConvolution(input_bitmap52)

	convolution_stride=5
	conv_dlim1=dlim1.convolution(convolution_stride)
	conv_dlim2=dlim2.convolution(convolution_stride)
	conv_dlim3=dlim3.convolution(convolution_stride)
	conv_dlim4=dlim4.convolution(convolution_stride)
	conv_dlim5=dlim5.convolution(convolution_stride)
	conv_dlim6=dlim6.convolution(convolution_stride)
	conv_dlim7=dlim7.convolution(convolution_stride)
	conv_dlim8=dlim8.convolution(convolution_stride)

	conv_map11=dlc11.convolution(convolution_stride)
	conv_map12=dlc12.convolution(convolution_stride)
	conv_map21=dlc21.convolution(convolution_stride)
	conv_map22=dlc22.convolution(convolution_stride)
	conv_map3=dlc3.convolution(convolution_stride)
	conv_map41=dlc41.convolution(convolution_stride)
	conv_map42=dlc42.convolution(convolution_stride)
	conv_map51=dlc51.convolution(convolution_stride)
	conv_map52=dlc52.convolution(convolution_stride)

	pool_slidewindow_width=2
	pool_dlim1=dlim1.max_pooling(pool_slidewindow_width)
	pool_dlim2=dlim2.max_pooling(pool_slidewindow_width)
	pool_dlim3=dlim3.max_pooling(pool_slidewindow_width)
	pool_dlim4=dlim4.max_pooling(pool_slidewindow_width)
	pool_dlim5=dlim5.max_pooling(pool_slidewindow_width)
	pool_dlim6=dlim6.max_pooling(pool_slidewindow_width)
	pool_dlim7=dlim7.max_pooling(pool_slidewindow_width)
	pool_dlim8=dlim8.max_pooling(pool_slidewindow_width)

	pool_map11=dlc11.max_pooling(pool_slidewindow_width)
	pool_map12=dlc12.max_pooling(pool_slidewindow_width)
	pool_map21=dlc21.max_pooling(pool_slidewindow_width)
	pool_map22=dlc22.max_pooling(pool_slidewindow_width)
	pool_map3=dlc3.max_pooling(pool_slidewindow_width)
	pool_map41=dlc41.max_pooling(pool_slidewindow_width)
	pool_map42=dlc42.max_pooling(pool_slidewindow_width)
	pool_map51=dlc51.max_pooling(pool_slidewindow_width)
	pool_map52=dlc52.max_pooling(pool_slidewindow_width)

	print "##########################################"
	print "Set of Convolution Maps"
	print "##########################################"
	print conv_dlim1
	print conv_dlim2
	print conv_dlim3
	print conv_dlim4
	print conv_dlim5
	print conv_dlim6
	print conv_dlim7
	print conv_dlim8

	#print "Example 11:"
	#print "###########"
	#pprint.pprint(conv_map11)
	#print "###########"
	#print "Example 12:"
	#print "###########"
	#pprint.pprint(conv_map12)
	#print "###########"
	#print "Example 21:"
	#print "###########"
	#pprint.pprint(conv_map21)
	#print "###########"
	#print "Example 22:"
	#print "###########"
	#pprint.pprint(conv_map22)
	#print "###########"
	#print "Example 3:"
	#print "###########"
	#pprint.pprint(conv_map3)
	#print "###########"
	#print "Example 41:"
	#print "###########"
	#pprint.pprint(conv_map41)
	#print "###########"
	#print "Example 42:"
	#print "###########"
	#pprint.pprint(conv_map42)
	#print "###########"
	#print "Example 51:"
	#print "###########"
	#pprint.pprint(conv_map51)
	#print "###########"
	#print "Example 52:"
	#print "###########"
	#pprint.pprint(conv_map52)

	print "##########################################"
	print "Max Pooling Map"
	print "##########################################"
	print pool_dlim1
	print pool_dlim2
	print pool_dlim3
	print pool_dlim4
	print pool_dlim5
	print pool_dlim6
	print pool_dlim7
	print pool_dlim8

	#print "Example 11:"
	#print "###########"
	#pprint.pprint(pool_map11)
	#print "###########"
	#print "Example 12:"
	#print "###########"
	#pprint.pprint(pool_map12)
	#print "###########"
	#print "Example 21:"
	#print "###########"
	#pprint.pprint(pool_map21)
	#print "###########"
	#print "Example 22:"
	#print "###########"
	#pprint.pprint(pool_map22)
	#print "###########"
	#print "Example 3:"
	#print "###########"
	#pprint.pprint(pool_map3)
	#print "###########"
	#print "Example 41:"
	#print "###########"
	#pprint.pprint(pool_map41)
	#print "###########"
	#print "Example 42:"
	#print "###########"
	#pprint.pprint(pool_map42)
	#print "###########"
	#print "Example 51:"
	#print "###########"
	#pprint.pprint(pool_map51)
	#print "###########"
	#print "Example 52:"
	#print "###########"
	#pprint.pprint(pool_map52)

	maxpool_map_width=5
	
	print "###########################################################################################"
	print "Final Layer of Inference from Max Pooling Layer - BackPropagation on Max Pooling Layer Neurons"
	print "###########################################################################################"
	dlim1infer=dlim1.infer_from_max_pooling(pool_dlim1,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim1infer
	dlim2infer=dlim2.infer_from_max_pooling(pool_dlim2,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim2infer
	dlim3infer=dlim3.infer_from_max_pooling(pool_dlim3,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim3infer
	dlim4infer=dlim4.infer_from_max_pooling(pool_dlim4,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim4infer
	dlim5infer=dlim5.infer_from_max_pooling(pool_dlim5,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim5infer
	dlim6infer=dlim6.infer_from_max_pooling(pool_dlim6,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim6infer
	dlim7infer=dlim7.infer_from_max_pooling(pool_dlim7,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim7infer
	dlim8infer=dlim8.infer_from_max_pooling(pool_dlim8,maxpool_map_width)
	print "Inference from Max Pooling Layer - Image:",dlim8infer

	#print "Example 11:"
	#print "###########"
	dlc11infer=dlc11.infer_from_max_pooling(pool_map11,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 11:",dlc11infer)
	#print "###########"
	#print "Example 12:"
	#print "###########"
	dlc12infer=dlc12.infer_from_max_pooling(pool_map12,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 12:",dlc12infer)
	#print "###########"
	#print "Example 21:"
	#print "###########"
	dlc21infer=dlc21.infer_from_max_pooling(pool_map21,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 21:",dlc21infer)
	#print "###########"
	#print "Example 22:"
	#print "###########"
	dlc22infer=dlc22.infer_from_max_pooling(pool_map22,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 22:",dlc22infer)
	#print "###########"
	#print "Example 3:"
	#print "###########"
	dlc3infer=dlc3.infer_from_max_pooling(pool_map3,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 3:",dlc3infer)
	#print "###########"
	#print "Example 41:"
	#print "###########"
	dlc41infer=dlc41.infer_from_max_pooling(pool_map41,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 41:",dlc41infer)
	#print "###########"
	#print "Example 42:"
	#print "###########"
	dlc42infer=dlc42.infer_from_max_pooling(pool_map42,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 42:",dlc42infer)
	#print "###########"
	#print "Example 51:"
	#print "###########"
	dlc51infer=dlc51.infer_from_max_pooling(pool_map51,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 51:",dlc51infer)
	#print "###########"
	#print "Example 52:"
	#print "###########"
	dlc52infer=dlc52.infer_from_max_pooling(pool_map52,maxpool_map_width)
	print("Inference from Max Pooling Layer - Example 52:",dlc52infer)