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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

import numpy as np
import random
import math
import sys
from collections import defaultdict

def prob_dist(freq):
        prob=[]
        sumfreq=0
        for x,y in freq.iteritems():
                sumfreq=sumfreq + y
        #print "sumfreq=",sumfreq
        for x,y in freq.iteritems():
                #print "y=",y
                prob.append(float(y)/float(sumfreq))
        return prob

if __name__=="__main__":
	numvars=10
	nuvariables=defaultdict(int)
	iterations=0
	alpha=3
	literal=[]
	extendedvariables=[]
	while iterations < 100:
		variables=np.random.choice(numvars, numvars, replace=True)
		for x in variables:
			extendedvariables.append(x)
		for x in xrange(int(alpha*len(variables))):
			extendedvariables.append(int(math.sqrt(alpha)*len(variables)))
		literal=np.random.choice(len(extendedvariables),1,replace=True)
		print "variable=",extendedvariables[literal[0]]
		while extendedvariables[literal[0]] == int(math.sqrt(alpha)*len(variables)):
			literal=np.random.choice(len(extendedvariables),1,replace=True)
			print "variable=",extendedvariables[literal[0]]
			nuvariables[extendedvariables[literal[0]]] = nuvariables[extendedvariables[literal[0]]] + 1
		nuvariables[extendedvariables[literal[0]]] = nuvariables[extendedvariables[literal[0]]] + 1
		print "per literal average probability:",prob_dist(nuvariables)
		iterations += 1
