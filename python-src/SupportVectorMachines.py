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
import cvxpy 
import numpy
import dccp
import cvxopt
import sys
from collections import defaultdict
import operator
import pprint

class SupportVectorMachines(object):
	def __init__(self,dimensions,bias):
		self.bias=bias
		self.dimensions=dimensions
		self.distvectormap=defaultdict(list)

	def learn_support_vectors_from_dataset(self,training_dataset):
		print "===================================================================================="
		print "learn_support_vectors_from_dataset() - Support Vectors Learnt from Training Dataset:"
		print "===================================================================================="
		for t in training_dataset:
			distance=self.distance_from_separating_hyperplane(t)
			self.distvectormap[distance[0][0]].append(t)
		self.distvectormap=sorted(self.distvectormap.items(), key=operator.itemgetter(0), reverse=False)

	def classify(self,point,training_dataset):
		distance_from_dhp=self.distance_from_separating_hyperplane(point)
		print "================================================="
		print "classify() - Support Vectors:"
		print "================================================="
		for k,v in self.distvectormap:
			print "distance = ",k," : vector = ",v 
		print "================================================="
		print "classify(): distance of ",point," from decision hyperplane = ",distance_from_dhp[0][0]

	def distance_from_separating_hyperplane(self,tple=None):
		no_of_weights=self.dimensions
		no_of_tuple=self.dimensions
		weights=cvxpy.Variable(no_of_weights,1)
		if tple==None:
			tuple=numpy.random.rand(no_of_tuple)
		else:
			tuple=numpy.array(tple)	
		print "weights:",weights
		print "tuple:",tuple

		bias=self.bias
		svm_function = 0.0 

		for i in xrange(no_of_weights):
			svm_function += cvxpy.abs(weights[i,0])

		objective=cvxpy.Minimize(cvxpy.abs(svm_function)*0.5)
		print "============================================"
		print "Objective Function"
		print "============================================"
		print objective

		constraint=0.0
		constraints=[]
		for i,k in zip(xrange(no_of_weights),xrange(no_of_tuple)):
			constraint += weights[i,0]*tuple[k] 
		constraint += bias
		print "constraint:",constraint
		constraints.append(cvxpy.abs(constraint) >= 1)
		
		print "============================================"
		print "Constraints"
		print "============================================"
		print constraints

		problem=cvxpy.Problem(objective,constraints)
		print "====================================="
		print "Installed Solvers:"
		print "====================================="
		print cvxpy.installed_solvers()
		print "Is Problem DCCP:",dccp.is_dccp(problem)
		print "====================================="
		print "CVXPY args:"
		print "====================================="
		result=problem.solve(solver=cvxpy.SCS,verbose=True,method='dccp')
		print "====================================="
		print "Problem value:"
		print "====================================="
		print problem.value
		print "====================================="
		print "Result:"
		print "====================================="
		print result
		return (result,tuple)

if __name__=="__main__":
	cvx=SupportVectorMachines(10,18.0)
	point0=[1,1,1,1,1,1,1,1,1,1]
	point1=[4,3,3,4,4,2,6,2,6,1]
	point2=[-4,-3,-3,-4,-4,-2,-6,-2,-6,-1]
	point3=[5,3,5,6,7,3,6,3,6,7]
	res0=cvx.distance_from_separating_hyperplane(point0)
	res1=cvx.distance_from_separating_hyperplane(point1)
	res2=cvx.distance_from_separating_hyperplane(point2)
	res3=cvx.distance_from_separating_hyperplane(point3)
	res4=cvx.distance_from_separating_hyperplane()
	res5=cvx.distance_from_separating_hyperplane()
	print "======================================================="
	print "distance of Support Vector point0 - ",point0," :",res0[0][0]
	print "distance of Support Vector point1 - ",point1," :",res1[0][0]
	print "distance of Support Vector point2  - ",point2," (diametrically 180 degrees from point1, should be equal to distance of point1):",res2[0][0]
	print "distance of Support Vector point3 - ",point3," :",res3[0][0]
	print "distance of random point :",res4[1],":",res4[0][0]
	print "distance of random point :",res5[1],":",res5[0][0]
	point4=res4[1]
	point5=res5[1]
	training_dataset=[point0,point1,point2,point3,point4,point5]
	cvx.learn_support_vectors_from_dataset(training_dataset)
	point6=eval(sys.argv[1])
	cvx.classify(point6,training_dataset)
