#------------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#
#---------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

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

#For a linear non-sigmoid perceptron w1*x1+w2*x2+b in two variables for which weights have to be updated by Gradient
#the L2 norm of the perceptron is differentiated wrt x1 and x2 and deltaw is computed
def LinearPerceptronGradient():
	outputs=[10.0,25.0,30.0,45.0,275.0]	
	weights=[2.0,5.0]
	converged=False
	rho=-0.8
	sum=0.0
	bias=0.0
	iteration=0
	x1s=[1.0,2.0,5.0,7.0,8.0]
	x2s=[5.0,3.0,6.0,7.0,2.0]
	while not converged: 
		deltaw1=0
		deltaw2=0
		for x1,x2,output in zip(x1s, x2s, outputs):
			term = bias + weights[0]*x1 + weights[1]*x2 - output
			term = term * x1
			sum = sum + term	
		deltaw1 = sum * 2	
		for x1,x2,output in zip(x1s, x2s, outputs):
			term = bias + weights[0]*x1 + weights[1]*x2 - output
			term = term * x2
			sum = sum + term	
		deltaw2 = sum * 2	
		weights[0] = weights[0] - rho * deltaw1	
		weights[1] = weights[1] - rho * deltaw2	
		print "LinearPerceptronGradient() weight update iteration: weights[0] = ",str(weights[0])
		print "LinearPerceptronGradient() weight update iteration: weights[1] = ",str(weights[1])
		print "LinearPerceptronGradient() weight update iteration: deltaw1 = ",str(deltaw1)
		print "LinearPerceptronGradient() weight update iteration: deltaw2 = ",str(deltaw2)
		
		if deltaw1*-1.0 < 0.0000001 and deltaw2*-1.0 < 0.0000001 or iteration==1000:
			converged=True
		print "input 1 to perceptron = " , x1s
		print "input 2 to perceptron = " , x2s
		print "weights updated after Gradient : " , weights
		iteration+=1
	

LinearPerceptronGradient()
