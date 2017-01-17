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

#Backpropagation on a Multilayered Neural Network example - Reference: http://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/

import math

class BackPropagation(object):
	def __init__(self,i1,i2,i3,h1,h2,h3,expected_o1,expected_o2,expected_o3,weights):
		self.input_layer=[i1,i2,i3]
		self.hidden_layer=[h1,h2,h3]
		self.output_layer=[0.0,0.0,0.0]
		self.expected_output_layer=[expected_o1,expected_o2,expected_o3]
		w1=weights[0]
		w2=weights[1]
		w3=weights[2]
		w4=weights[3]
		w5=weights[4]
		w6=weights[5]
		w7=weights[6]
		w8=weights[7]
		w9=weights[8]
		w10=weights[9]
		w11=weights[10]
		w12=weights[11]
		w13=weights[12]
		w14=weights[13]
		w15=weights[14]
		w16=weights[15]
		w17=weights[16]
		w18=weights[17]
		self.weights=[w1,w2,w3,w4,w5,w6,w7,w8,w9,w10,w11,w12,w13,w14,w15,w16,w17,w18]
		self.weight_input_neuron_map={0:0,1:1,2:2,3:0,4:1,5:2,6:0,7:1,8:2,9:0,10:1,11:2,12:0,13:1,14:2,15:0,16:1,17:2}
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
		doe_error_weight=self.doeError_doeOutput_all(output_index) * self.doeOutput_doeInput(output_index) * self.doeInput_doeWeight(weight_index)
		self.weights[weight_index]=self.weights[weight_index] - doe_error_weight
		
	def doeError_doeOutput_all(self, index):
		return self.doeErrorOut1_doeOutput(index) + self.doeErrorOut2_doeOutput(index) + self.doeErrorOut3_doeOutput(index)

	def doeErrorOut1_doeOutput(self,input_index):
		return self.doeError_doeOutput(0) * self.doeOutput_doeInput(0) * self.output_layer[0] / self.hidden_layer[0]

	def doeErrorOut2_doeOutput(self,input_index):
		return self.doeError_doeOutput(1) * self.doeOutput_doeInput(1) * self.output_layer[1] / self.hidden_layer[0]

	def doeErrorOut3_doeOutput(self,input_index):
		return self.doeError_doeOutput(2) * self.doeOutput_doeInput(2) * self.output_layer[2] / self.hidden_layer[0]

	def compute_neural_network(self):
		self.hidden_layer[0]=self.input_layer[0]*self.weights[0] + self.input_layer[1]*self.weights[1] + self.input_layer[2]*self.weights[2] + self.bias
		self.hidden_layer[1]=self.input_layer[0]*self.weights[3] + self.input_layer[1]*self.weights[4] + self.input_layer[2]*self.weights[5] + self.bias
		self.hidden_layer[2]=self.input_layer[0]*self.weights[6] + self.input_layer[1]*self.weights[7] + self.input_layer[2]*self.weights[8] + self.bias
		self.output_layer[0]=self.hidden_layer[0]*self.weights[9] + self.hidden_layer[1]*self.weights[10] + self.input_layer[2]*self.weights[11] + self.bias
		self.output_layer[1]=self.hidden_layer[0]*self.weights[12] + self.hidden_layer[1]*self.weights[13] + self.input_layer[2]*self.weights[14] + self.bias
		self.output_layer[2]=self.hidden_layer[0]*self.weights[15] + self.hidden_layer[1]*self.weights[16] + self.input_layer[2]*self.weights[17] + self.bias

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

#######################################################################################################
#Software Analytics with Backpropagation - Example learning from top output for CPU and Memory usage:
#---------------------------------------------------------------------------------------------------
#top - 14:34:33 up  4:46,  2 users,  load average: 0.25, 0.26, 0.41
#Tasks: 212 total,   1 running, 211 sleeping,   0 stopped,   0 zombie
#%Cpu(s):  5.1 us,  3.9 sy,  0.0 ni, 89.4 id,  1.7 wa,  0.0 hi,  0.0 si,  0.0 st
#KiB Mem:   2930068 total,  2803660 used,   126408 free,   156176 buffers
#KiB Swap:  3103740 total,   166656 used,  2937084 free.  1017176 cached Mem
#
#  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
# 4273 shriniv+   9 -11  231168   7592   6412 S   4.6  0.3   6:18.91 pulseaudio
#-----------------------------------------------------------------------------------------
#In above %CPU=4.6 and %MEM=0.3 are used as input to backpropagation as below with expected outputs
#for 2 neurons in output layers being 0.09 and 0.01.
#4.6% is converted to 0.046 and 0.3% to 0.003.
#######################################################################################################

if __name__=="__main__":
	iter=0
	weights=[0.01,0.023,0.056,0.043,0.099,0.088,0.033,0.021,0.12,0.23,0.34,0.45,0,11,0.56,0.77,0.21,0.88,0.92]
	#parameters - initial conditions - input1,input2,input3,hidden1,hidden2,hidden2,expected_output1,expected_output2,expected_output3,weights_array
	bpnn=BackPropagation(0.046,0.003,0.1,0.8,0.9,0.3,0.09,0.01,0.21,weights)
	bpnn.compute_neural_network()
	bpnn.print_layers()
	print "Error before Backpropagation:"
	print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
	while iter < 3000000:
		bpnn.backpropagation_pde_update_hidden_to_output(0,9)
		bpnn.backpropagation_pde_update_hidden_to_output(0,10)
		bpnn.backpropagation_pde_update_hidden_to_output(0,11)
		bpnn.backpropagation_pde_update_hidden_to_output(1,12)
		bpnn.backpropagation_pde_update_hidden_to_output(1,13)
		bpnn.backpropagation_pde_update_hidden_to_output(1,14)
		bpnn.backpropagation_pde_update_hidden_to_output(2,15)
		bpnn.backpropagation_pde_update_hidden_to_output(2,16)
		bpnn.backpropagation_pde_update_hidden_to_output(2,17)
		bpnn.backpropagation_pde_update_input_to_hidden(0,0)
		bpnn.backpropagation_pde_update_input_to_hidden(0,1)
		bpnn.backpropagation_pde_update_input_to_hidden(0,2)
		bpnn.backpropagation_pde_update_input_to_hidden(1,3)
		bpnn.backpropagation_pde_update_input_to_hidden(1,4)
		bpnn.backpropagation_pde_update_input_to_hidden(1,5)
		bpnn.backpropagation_pde_update_input_to_hidden(2,6)
		bpnn.backpropagation_pde_update_input_to_hidden(2,7)
		bpnn.backpropagation_pde_update_input_to_hidden(2,8)
		print "Recomputing Neural Network after backpropagation weight update"
		bpnn.compute_neural_network()
		print "Error after Backpropagation- iteration :",iter
		print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
		print "Layers in this iteration:"
		bpnn.print_layers()
		print "Weights updated in this iteration:"
		print bpnn.weights
		iter=iter+1
