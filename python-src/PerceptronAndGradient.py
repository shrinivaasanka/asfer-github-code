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


#Gradient Descent and Ascent for local minimum and maximum of a cost function
#-------------------------------
#Gradient iterative update rule:
#-------------------------------
#xnew = xold - rho*firstderivative for descent
#xnew = xold + rho*firstderivative for ascent

#Following is a generic approximation written for linear perceptrons of the form wx+b
#Above update rule is discretized as :
#wnew = wold - alpha*deltaw

import rpy2.robjects as robj

#For a linear non-sigmoid perceptron w1*x1+w2*x2+...+wn*xn+b  for which weights have to be updated by Gradient
#the L2 norm of the perceptron is differentiated wrt x1,x2,...,xn and deltaw is computed
def LinearPerceptronGradient(outputs,weights,rho,bias,variables):
	converged=False
	sum=0.0
	iteration=0
	while not converged and iteration < 1000: 
                deltaw=[]
                term=bias
                varnum=0
                sum=0.0
                #Example iteration for two variables:
                #-----------------------------------
        	#for x1,x2,output in zip(x1s, x2s, outputs):
        	#	term = bias + weights[0]*x1 + weights[1]*x2 - output
        	#	term = term * x2
        	#	sum = sum + term	
		#deltaw2 = sum * 2	
                #------------------------------------------------------------------------------
                #Following iteration is generic for arbitrary number of variables
                #generalizing previous example for 2 variables
                #------------------------------------------------------------------------------
                for cnt1 in xrange(len(variables[0])-1):
        	   for cnt2 in xrange(len(variables)-1):
        	       term += weights[cnt2]*variables[cnt2][cnt1]
                   term = term - outputs[cnt1]
        	   term = term * variables[varnum][cnt1]
        	   sum = sum + term	
                   varnum += 1
        	   deltaw.append(sum * 2)
                for cnt in xrange(len(variables[0])-1):
                    if compute_perceptron(weights,variables,outputs) == 1:
	                print "LinearPerceptronGradient() weight update iteration: Descending"
		        weights[cnt] = weights[cnt] - rho * deltaw[cnt]
                    else:
                        print "LinearPerceptronGradient() weight update iteration: Ascending" 
		        weights[cnt] = weights[cnt] + rho * deltaw[cnt]
	            print "LinearPerceptronGradient() weight update iteration: weights[",cnt,"] = ",weights[cnt]
		    print "LinearPerceptronGradient() weight update iteration: deltaw = ",deltaw
		
                for cnt in xrange(len(weights)-1):
		    if deltaw[cnt]*-1.0 < 0.0000001:
			converged=True
                    else:
                        converged=False
		print "weights updated after Gradient : " , weights
		iteration+=1

def compute_perceptron(weights,variables,outputs):
    for o in xrange(len(outputs)-1):
        sum=0
        for w in xrange(len(weights)-1):
            sum = sum + weights[w]*variables[w][o]
        if (outputs[o] - sum) > 10:
            return 1
    return 0
	
if __name__=="__main__":
	outputs=[10.0,25.0,30.0,45.0,275.0]	
	weights=[1.0,1.4,2.5,2.0,5.0]
	rho=-0.8
	bias=0.0
	variables=[[1.0,2.0,5.0,6.0,8.0], [1.0,12.0,5.0,7.0,18.0], [1.0,22.0,35.0,7.0,8.0], [1.0,2.0,5.0,87.0,88.0], [1.0,12.0,5.0,7.0,8.0]]
        LinearPerceptronGradient(outputs,weights,rho,bias,variables)
