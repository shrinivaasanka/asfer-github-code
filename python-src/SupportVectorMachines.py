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
#--------------------------------------------------------------------------------------------------------

import math
from cvxpy import * 
import numpy
import dccp
import cvxopt

class SupportVectorMachines(object):
	def distance_from_separating_hyperplane(self,no_of_tuple,no_of_weights,tple=None):
		weights=Variable(no_of_weights,1)
		if tple==None:
			tuple=numpy.random.rand(no_of_tuple)
		else:
			tuple=numpy.array(tple)	
		print "weights:",weights
		print "tuple:",tuple

		bias=10.0
		svm_function = 0.0 

		for i in xrange(no_of_weights):
			svm_function += abs(weights[i,0])

		objective=Minimize(abs(svm_function)*0.5)
		print "============================================"
		print "Objective Function"
		print "============================================"
		print objective

		constraint=0.0
		constraints=[]
		for i,k in zip(xrange(no_of_weights),xrange(no_of_tuple)):
			constraint += weights[i,0]*tuple[k] 
		constraint += bias
		constraints.append(abs(constraint) >= 1)
		
		print "============================================"
		print "Constraints"
		print "============================================"
		print constraints

		problem=Problem(objective,constraints)
		print "====================================="
		print "Installed Solvers:"
		print "====================================="
		print installed_solvers()
		print "Is Problem DCCP:",dccp.is_dccp(problem)
		print "====================================="
		print "CVXPY args:"
		print "====================================="
		result=problem.solve(solver=SCS,verbose=True,method='dccp')
		print "====================================="
		print "Problem value:"
		print "====================================="
		print problem.value
		print "====================================="
		print "Result:"
		print "====================================="
		print result
		return result

if __name__=="__main__":
	cvx=SupportVectorMachines()
	point1=[4,3,3,4,4,2,6,2,6,1]
	point2=[-4,-3,-3,-4,-4,-2,-6,-2,-6,-1]
	res1=cvx.distance_from_separating_hyperplane(len(point1),len(point1),point1)
	res2=cvx.distance_from_separating_hyperplane(len(point2),len(point2),point2)
	res3=cvx.distance_from_separating_hyperplane(10,10)
	print "======================================================="
	print "distance of Support Vector point1 - ",point1," :",res1
	print "distance of Support Vector point2  - ",point2," (diametrically 180 degrees from point1, should be equal to distance of point1):",res2
	print "distance of random point :",res3
