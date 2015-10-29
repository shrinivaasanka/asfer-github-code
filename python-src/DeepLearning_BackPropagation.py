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

#Backpropagation on a Multilayered Neural Network example - Reference: http://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/

import math

class BackPropagation(object):
	def __init__(self,i1,i2,h1,h2):
		self.input_layer=[i1,i2]	
		self.hidden_layer=[h1,h2]
		self.output_layer=[0.0,0.0]
		self.expected_output_layer=[0.98,0.57]
		w1=w2=w3=w4=w5=w6=w7=w8=0.073
		self.weights=[w1,w2,w3,w4,w5,w6,w7,w8]
		self.weight_input_neuron_map={0:0,1:1,2:0,3:1,4:0,5:1,6:0,7:1}
		self.bias=0.02
	
	def sigmoid(self, input):
                # 1/(1+e^(-z))
                return 1/(1+math.exp(-1*input))

	######################################################################################	
	def backpropagation_pde_update_hidden_to_output(self, output_index, weight_index):
		#From PDE chain rule:
		#doe(error)/doe(weight)=doe(error)/doe(output) * doe(output)/doe(input) * doe(input)/doe(weight)
		doe_error_weight=self.doeError_doeOutput(output_index) * self.doeOutput_doeInput(output_index) * self.doeInput_doeWeight(weight_index)
		self.weights[weight_index]=self.weights[weight_index] - doe_error_weight
		
	def doeError_doeOutput(self, index):
		return -1 * (self.expected_output_layer[index] - self.output_layer[index])
	
	def doeOutput_doeInput(self, index):
		return (self.output_layer[index] * (1 - self.output_layer[index]))

	def doeInput_doeWeight(self, index):
		return self.hidden_layer[self.weight_input_neuron_map[index]]

	######################################################################################	
	def backpropagation_pde_update_input_to_hidden(self, output_index, weight_index):
		#From PDE chain rule:
		#doe(error)/doe(weight)=doe(error)/doe(output) * doe(output)/doe(input) * doe(input)/doe(weight)
		doe_error_weight=self.doeError_doeOutput_both(output_index) * self.doeOutput_doeInput(output_index) * self.doeInput_doeWeight(weight_index)
		self.weights[weight_index]=self.weights[weight_index] - doe_error_weight
		
	def doeError_doeOutput_both(self, index):
		return self.doeErrorOut1_doeOutput(index) + self.doeErrorOut2_doeOutput(index)

	def doeErrorOut1_doeOutput(self,input_index):
		return self.doeError_doeOutput(0) * self.doeOutput_doeInput(0) * self.output_layer[0] / self.hidden_layer[0]

	def doeErrorOut2_doeOutput(self,input_index):
		return self.doeError_doeOutput(1) * self.doeOutput_doeInput(1) * self.output_layer[1] / self.hidden_layer[0]


	def compute_neural_network(self):
		self.hidden_layer[0]=self.input_layer[0]*self.weights[0] + self.input_layer[1]*self.weights[1] + self.bias
		self.hidden_layer[1]=self.input_layer[0]*self.weights[2] + self.input_layer[1]*self.weights[3] + self.bias
		self.output_layer[0]=self.hidden_layer[0]*self.weights[4] + self.hidden_layer[1]*self.weights[5] + self.bias
		self.output_layer[1]=self.hidden_layer[0]*self.weights[6] + self.hidden_layer[1]*self.weights[7] + self.bias

	def print_layers(self):
		print "###############"
		print "Input Layer:"
		print "###############"
		print self.input_layer
		print "###############"
		print "Hidden middle Layer:"
		print "###############"
		print self.hidden_layer
		print "###############"
		print "Output Layer:"
		print "###############"
		print self.output_layer

	def output_error(self,output_layer,expected_output_layer):
		sum_of_squared_error=0.0
		for i in xrange(len(output_layer)):
			sum_of_squared_error=sum_of_squared_error + (output_layer[i]-expected_output_layer[i])*(output_layer[i]-expected_output_layer[i])
		return 0.5*sum_of_squared_error


iter=0
bpnn=BackPropagation(0.01,0.5,0.7,0.38)
bpnn.compute_neural_network()
bpnn.print_layers()
print "Error before Backpropagation:"
print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
while iter < 20000:
	bpnn.backpropagation_pde_update_hidden_to_output(0,4)
	bpnn.backpropagation_pde_update_hidden_to_output(0,6)
	bpnn.backpropagation_pde_update_hidden_to_output(1,5)
	bpnn.backpropagation_pde_update_hidden_to_output(1,7)
	bpnn.backpropagation_pde_update_hidden_to_output(0,0)
	bpnn.backpropagation_pde_update_hidden_to_output(0,1)
	bpnn.backpropagation_pde_update_hidden_to_output(1,2)
	bpnn.backpropagation_pde_update_hidden_to_output(1,3)
	print "Recomputing Neural Network after backpropagation weight update"
	bpnn.compute_neural_network()
	print "Error after Backpropagation- iteration :",iter
	print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
	iter=iter+1

		
		
