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

#-----------------------------------------------------------------
#Linear Regression in n variables:
#y=w1*x1 + w2*x2 + ... + wn*xn + b
#-----------------------------------------------------------------

import rpy2.robjects as robj
import math

def LinearRegression(bias,weights,variables):
        regressed = bias
	for n in xrange(len(variables)-1):
		regressed += weights[n]*variables[n]
	print "Linear Regression for weights ",weights," and variables ",variables,": ",regressed
        return regressed

#-----------------------------------------------------------------
#Logistic Regression in n variables:
#y=1/(1+e^(-(w1*x1 + w2*x2 + ... + wn*xn + b)))
#-----------------------------------------------------------------

def LogisticRegression(bias,weights,variables):
        regressed = bias
	for n in xrange(len(variables)-1):
            weighted_sum = weights[n]*variables[n]
	regressed =  1/(1 + math.pow(2.718, -1*(weighted_sum)))
	print "Logistic Regression for weights ",weights," and variables ",variables,": ",regressed
        return regressed

if __name__=="__main__":
    weights=[2.0,1.0,2.3,3.2,5.0]
    bias=0.03
    variables=[1.0,2.0,5.0,7.0,8.0]
    print "##################"
    print "Linear Regression:"
    print "##################"
    LinearRegression(bias,weights,variables)
    print "##################"
    print "Logistic Regression:"
    print "##################"
    LogisticRegression(bias,weights,variables)
