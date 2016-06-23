#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
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
#Srinivasan Kannan 
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

#Long Term Short Term Memory Recurrent Neural Network - Deep Learning
#LSTM is a graph (with feedback) of alternating product and linear weighted sum gates with following leaf gates:
#	Cell gate (leftmost)
#	Input gate (second from left)
#	Forget gate (third from left)
#	Output gate (rightmost)
# Level 1 product gates (cell * input)
# Level 2 Weighted sum gate ( level1 products - cell*input and forget * level2_sum_feedback)
# Level 3 product gate (level 2 sum gate and output gate)
#
# References: 
# 1. LSTM RNN Architecture Diagram in https://en.wikipedia.org/wiki/Long_short-term_memory
# 2. LSTM RNN resources - http://people.idsia.ch/~juergen/rnn.html
# 3. Schmidhuber-Hochreiter LSTM RNN paper - http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf

import math

class LSTMRecurrentNeuralNetwork(object):
	def __init__(self, cellvars, cellweights, inputvars, inputweights, forgetvars, forgetweights, outputvars, outputweights):
		self.cellout = self.sigmoid(cellvars, cellweights)
		self.inputout = self.sigmoid(inputvars, inputweights)
		self.forgetout = self.sigmoid(forgetvars, forgetweights)
		self.outputout = self.sigmoid(outputvars, outputweights)
		self.cell_input_product1_level1 = 0.0
		self.forget_feedback_product2_level1 = 0.0
		self.product1_product2_sum1_level2 = 0.0005
		self.sum1_output_product1_level3 = 0.0005
		self.sum1_product1_product2_sum1_level2 = 0.0005
		self.level2weights=[0.3,0.6]
	
	def sigmoid(self, vars, weights):
                # 1/(1+e^(-z))
		bias = 0.7
		cnt = 0
		input = 0.0
		while cnt < len(vars):
			input = input + weights[cnt]*vars[cnt]
			cnt+=1
                return 1/(1+math.exp(-1*input))

	def compute_cell_input_product1_level1(self):
		self.cell_input_product1_level1 = self.cellout * self.inputout
		print "self.cell_input_product1_level1 = ", self.cell_input_product1_level1

	def compute_forget_feedback_product2_level1(self):
		self.forget_feedback_product2_level1 = self.forgetout * self.product1_product2_sum1_level2
		print "self.forget_feedback_product2_level1 = ", self.forget_feedback_product2_level1

	def compute_product1_product2_sum1_level2(self):
		self.product1_level1 = self.cell_input_product1_level1 
		self.product2_level1 = self.forget_feedback_product2_level1 
		self.product1_product2_sum1_level2 = self.level2weights[0] * self.product1_level1 + self.level2weights[1] * self.product2_level1
		print "self.product1_product2_sum1_level2 = ", self.product1_product2_sum1_level2

	def compute_sum1_output_product1_level3(self):
		self.sum1_output_product1_level3 = self.outputout * self.product1_product2_sum1_level2
		print self.outputout
		print self.product1_product2_sum1_level2
		print "self.sum1_output_product1_level3 = ", self.sum1_output_product1_level3

if __name__=="__main__":
	cellvars=[0.01,0.2,0.3,0.7]
	cellweights=[0.8,0.4,0.1,0.3]
	inputvars=[0.02,0.3,0.5,0.8]
	inputweights=[0.1,0.2,0.3,0.4]
	forgetvars=[0.01,0.5,0.14,0.45]
	forgetweights=[0.4,0.2,0.5,0.7]
	outputvars=[0.1,0.5,0.2,0.6]
	outputweights=[0.11,0.445,0.24,0.2]
	iteration = 0
	lstmRNN=LSTMRecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights, forgetvars, forgetweights, outputvars, outputweights)
	while iteration < 10000:
		lstmRNN.compute_cell_input_product1_level1()
		lstmRNN.compute_forget_feedback_product2_level1()
		lstmRNN.compute_product1_product2_sum1_level2()
		lstmRNN.compute_sum1_output_product1_level3()
		print "Iteration: ", iteration, " Final LSTM Recurrent Neural Network out value = ", lstmRNN.sum1_output_product1_level3
		print "####################################################################################################################"
		iteration += 1
