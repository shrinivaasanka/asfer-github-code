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

import math
import numpy

class GRURecurrentNeuralNetwork(object):
	def __init__(self,cellvars, cellweights, inputvars, inputweights_c, inputweights_u, inputweights_r, updateweights, resetweights):
		self.cellvars=cellvars
		self.cellweights=cellweights
		self.inputvars=inputvars
		self.inputweights_update=inputweights_u
		self.inputweights_reset=inputweights_r
		self.inputweights_cell=inputweights_c
		self.updateweights=updateweights
		self.resetweights=resetweights
		self.htprev=[]
		self.ht=[]
		for n in xrange(len(self.inputvars)):
			self.htprev.append(0.1)
			self.ht.append(0.1)
		self.update_input_htprev= 0.1
		self.reset_input_htprev=0.1
		self.bias_u=0.02
		self.bias_r=0.03
	
	def sigmoid(self, z):
                # 1/(1+e^(-z))
                return 1/(1+math.exp(-1*z))

	def compute_update_input_htprev_gate(self):
		update_input_htprev=0.0
		for n in xrange(len(self.inputvars)):
			update_input_htprev += self.inputvars[n]*self.inputweights_update[n] + self.htprev[n]*self.updateweights[n]
		update_input_htprev += self.bias_u
		self.update_input_htprev = self.sigmoid(update_input_htprev)

	def compute_reset_input_htprev_gate(self):
		reset_input_htprev=0.0
		for n in xrange(len(self.inputvars)):
			reset_input_htprev += self.inputvars[n]*self.inputweights_reset[n] + self.htprev[n]*self.resetweights[n]
		reset_input_htprev += self.bias_r
		self.reset_input_htprev = self.sigmoid(reset_input_htprev)

	def compute_cell_htprev_reset_product(self):
		for n in xrange(len(self.htprev)):
			self.cellvars[n] = numpy.tanh(self.inputweights_cell[n] * self.inputvars[n] + self.cellweights[n] * self.htprev[n] * self.reset_input_htprev)

	def compute_update_cell_product(self):
		for n in xrange(len(self.cellvars)):
			self.htprev[n] = self.ht[n]
			self.ht[n] = (1.0 - self.update_input_htprev) * self.cellvars[n] + self.update_input_htprev * self.htprev[n]


if __name__=="__main__":
	cellvars=[0.01,0.02,0.3,0.7]
	cellweights=[0.08,0.4,0.1,0.3]
	inputvars=[0.2,0.05,0.6,0.7]
	inputweights_cell=[0.21,0.05,0.7,0.8]
	inputweights_update=[0.1,0.45,0.33,0.23]
	inputweights_reset=[0.4,0.05,0.3,0.2]
	updatevars=[0.02,0.3,0.05,0.8]
	updateweights=[0.1,0.02,0.3,0.4]
	resetvars=[0.01,0.05,0.14,0.45]
	resetweights=[0.04,0.2,0.5,0.7]
	iteration = 0
	GRURNN=GRURecurrentNeuralNetwork(cellvars, cellweights, inputvars, inputweights_cell, inputweights_update, inputweights_reset, updateweights, resetweights)
	while iteration < 10000:
		GRURNN.compute_update_input_htprev_gate()
		GRURNN.compute_reset_input_htprev_gate()
		GRURNN.compute_cell_htprev_reset_product()
		GRURNN.compute_update_cell_product()
		print "####################################################################################################################"
		iteration += 1
		print "Iteration:",iteration
		print "state at time t",GRURNN.ht
		print "Cellvars:",GRURNN.cellvars
		print "Update gate:",GRURNN.update_input_htprev
		print "Reset gate:",GRURNN.reset_input_htprev
