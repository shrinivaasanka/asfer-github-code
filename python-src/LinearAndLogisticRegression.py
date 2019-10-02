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
from numpy import array 

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

def EconomicMerit(NationFitnesses,distances):
    print "GDPFitnesses:",NationFitnesses
    print "distances:",distances
    linkprobabilities=[]
    gravitymodel=[]
    xindx=0
    for z1 in NationFitnesses:
        yindx=0
        for z2 in NationFitnesses:
           #print "xindx:",xindx,", yindx:",yindx
           #print "distance:",distances[xindx][yindx]
           linkprobabilities.append((float(z1*z2))/(1.0+float(z1*z2))) 
           gravitymodel.append(float(z1*z2)/float(distances[xindx][yindx]))
           yindx+=1
        xindx+=1
    print "Trade Link probabilities between Nations in Economic Networks based on per nation GDP Fitness e.g ITN :",linkprobabilities
    print "Volume of Trade predicted between Nations in Economic Networks based on per nation GDP Fitness e.g ITN :",gravitymodel
    return (linkprobabilities,gravitymodel)

if __name__=="__main__":
    weights=[2.0,1.0,2.3,3.2,5.0]
    bias=0.03
    variables=[1.0,2.0,5.0,7.0,8.0]
    GDPFitnesses=[2.3,2.1,4.1,5.2,6.1]
    distances=[[1,2,4,4,6],[1,1,4,4,6],[1,2,5,4,6],[1,5,4,4,6],[1,2,5,5,6]]
    print "##################"
    print "Linear Regression:"
    print "##################"
    LinearRegression(bias,weights,variables)
    print "##################"
    print "Logistic Regression:"
    print "##################"
    LogisticRegression(bias,weights,variables)
    EconomicMerit(GDPFitnesses,distances)
