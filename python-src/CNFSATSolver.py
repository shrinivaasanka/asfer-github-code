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
from collections import defaultdict
#from scipy.linalg import solve
from scipy.linalg import lstsq
from numpy.linalg import solve
#from numpy.linalg import lstsq
from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from scipy.sparse.linalg import dsolve
from scipy.sparse import csc_matrix
from scipy.linalg import pinv
from scipy.linalg import pinv2
from numpy import matmul
#from scipy.sparse import csr_matrix 

variables=defaultdict(int)
negations=defaultdict(int)

class SATSolver(object):
	def __init__(self,algorithm):
		self.equationsA=[]
		self.equationsB=[]
		self.cnfparsed=[]
		self.Algorithm=algorithm

	def difference(self, list1, list2):
		diff=[]
		for l1 in list1:
			if l1 not in list2:
				diff.append(l1)
		return diff

	def satisfy(self, assignment):
		print "CNF Formula:", self.cnfparsed
		#print "assignment:",assignment
		cnfval=1
		number_of_clauses_satisfied=0.0
		for c in self.cnfparsed:
			varass=[]
			for l in c:
				if l[0] != "!":
					varass.append((l,assignment[int(l[1:])-1]))
				else:
					varass.append((l,assignment[int(l[2:])-1]))

			cval=0
			for l,v in varass:
				#print "v:",int(v)
				if l[0] == "!":
					cval = cval + (1-int(v))
				else:
					cval = cval + int(v)
				if cval > 1:
					cval=1
			if cval == 1:
				number_of_clauses_satisfied+=1.0
			#print "clause value:",cval
			cnfval = cnfval * cval
		#print "cnf value:",cnfval
		print "Number of clauses satisfied:",number_of_clauses_satisfied
		print "Number of clauses :",len(self.cnfparsed)
		percentage_clauses_satisfied=number_of_clauses_satisfied/float(len(self.cnfparsed))*100.0
		if percentage_clauses_satisfied > 100.0:
			print "percentage > 100"
		return (cnfval,percentage_clauses_satisfied)
		

	def solve_SAT(self,cnf,number_of_variables):
		cnfclauses=cnf.split("*")
		n=number_of_variables

		dnfclauses1=[]
		dnfclauses2=[]
		clauseliterals=[]
		allstrings=[]

		#for i in xrange(int(math.pow(2,n))):
		#	bini=bin(i)[2:]
		#	bini=bini.zfill(n)
		#	allstrings.append(list(bini)) 

		#print "cnfclauses:",cnfclauses
		for c in cnfclauses:
			cnfclause=[]
			clauseliterals=c.strip().split("+")
			#print "clauseliterals:",clauseliterals
			dnfclause1=[]
			dnfclause2=[]
			for i in xrange(n):
				dnfclause1.append("1")
				dnfclause2.append("0")
			for l in clauseliterals:
				lstrip=l.strip()
				if lstrip[0]=="(":
					lstrip=lstrip[1:] 
				if lstrip[len(lstrip)-1]==")":
					lstrip=lstrip[:len(lstrip)-1]
				cnfclause.append(lstrip)

				#print "lstrip:",lstrip
				if lstrip[0] != "!":
					#print "lstrip[1:]:",int(lstrip[1:])
					dnfclause1[int(lstrip[1:])-1] = "0"
					dnfclause2[int(lstrip[1:])-1] = "0"
				else:
					#print "lstrip[2:]:",lstrip[2:]
					dnfclause1[int(lstrip[2:])-1] = "1"
					dnfclause2[int(lstrip[2:])-1] = "1"
			dnfclauses1.append(dnfclause1)
			dnfclauses2.append(dnfclause2)
			self.cnfparsed.append(cnfclause)
		#print "Parsed CNF clauses:", self.cnfparsed
		#print "DNF clauses 1:",dnfclauses1
		#print "DNF clauses 2:",dnfclauses2
		#print "All strings:",allstrings
		#satassignments1=self.difference(allstrings, dnfclauses1)
		#satassignments2=self.difference(allstrings, dnfclauses2)
		#print "CNF SAT:",cnf
		#print "SAT assignments 1:",satassignments1
		#print "SAT assignments 2:",satassignments2
		#return (satassignments1,satassignments2)

	def solve_SAT2(self,cnf,number_of_variables,number_of_clauses):
		satass=[]
		x=[]
		self.solve_SAT(cnf,number_of_variables)
		for clause in self.cnfparsed:
			equation=[]
			for n in xrange(number_of_variables):
				equation.append(0)
			for literal in clause:
				if literal[0] != "!":
					equation[int(literal[1:])-1]=1
				else:
					equation[int(literal[2:])-1]=0
			self.equationsA.append(equation)
		for n in xrange(number_of_clauses):
			self.equationsB.append(1)
		a = np.array(self.equationsA)
                b = np.array(self.equationsB)
		self.A=a
		self.B=b
		#print "a:",a
		#print "b:",b
                #print "a.shape:",a.shape
                #print "b.shape:",b.shape

		x=None
		if self.Algorithm=="solve()":
                	x = solve(a,b)
		if self.Algorithm=="lstsq()":
                	x = lstsq(a,b,lapack_driver='gelsy')
		if self.Algorithm=="lsqr()":
                	x = lsqr(a,b,atol=0,btol=0,conlim=0,show=True)
		if self.Algorithm=="lsmr()":
                	x = lsmr(a,b,atol=0.1,btol=0.1,maxiter=1,conlim=100,show=True)
		if self.Algorithm=="spsolve()":
			x = dsolve.spsolve(csc_matrix(a),b)
		if self.Algorithm=="pinv2()":
			x=[]
			#pseudoinverse_a=pinv(a)
			pseudoinverse_a=pinv2(a,check_finite=False)
			x.append(matmul(pseudoinverse_a,b))

		print "solve_SAT2(): ",self.Algorithm,": x:",x
		cnt=0
		for e in x[0]:
			if e >= 0.5:
				satass.append(1)
			else:
				satass.append(0)
			cnt+=1
		#print "solve_SAT2():",a
		return satass

	def createRandom3CNF(self,numclauses,numvars):
		cnf=""
		clauses=[]
		for i in xrange(numclauses):
			#randarray=np.random.permutation(numvars)
			randarray=np.random.choice(numvars,3,replace=False)
			clause= "("
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[0]+1)
				variables[randarray[0]+1] = variables[randarray[0]+1] + 1
			else:
				clause += "!x"+str(randarray[0]+1)
				negations[randarray[0]+1] = negations[randarray[0]+1] + 1
			clause += " + "
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[1]+1)
				variables[randarray[1]+1] = variables[randarray[1]+1] + 1
			else:
				clause += "!x"+str(randarray[1]+1)
				negations[randarray[1]+1] = negations[randarray[1]+1] + 1
			clause += " + "
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[2]+1)
				variables[randarray[2]+1] = variables[randarray[2]+1] + 1
			else:
				clause += "!x"+str(randarray[2]+1)
				negations[randarray[2]+1] = negations[randarray[2]+1] + 1
			clause += ")"
			clauses.append(clause)
		cnf=" * ".join(clauses)
		return cnf

def prob_dist(freq):
	prob=[]
	sumfreq=0
	for x,y in freq.iteritems():
		sumfreq=sumfreq + y
	for x,y in freq.iteritems():
		#print "y=",y
		#print "sumfreq=",sumfreq
		prob.append(float(y)/float(sumfreq))
	return prob


if __name__=="__main__":
	#cnf="(!x1 + !x2 + !x3 + x4) * (x1 + x2 + !x3 + !x4) * (!x1 + x2 + !x3 + x4) * (x1 + !x2 + x3 + !x4) * (x1 + !x2 + x3 + x4)"
	#cnf="(x1 + !x4 + !x5) * (!x1 + x3 + x4) * (x2 + !x3 +  !x4) * (x3 + !x4 + !x5) * (!x1 + x4 + !x5)"


	#Parameter1: any k-CNF with all literals in each clause, negations prefixed with !
	#Parameter2: Number of variables
	#Solves CNFSAT by a Polynomial Time Approximation scheme:
	#	- Encode each clause as a linear equation in n variables: missing variables and negated variables are 0, others are 1
	#	- Solve previous system of equations by least squares algorithm to fit a line
	#	- Variable value above 0.5 is set to 1 and less than 0.5 is set to 0
	#	- Rounded of assignment array satisfies the CNFSAT with high probability
	#Returns: a tuple with set of satisfying assignments
	#ass=satsolver.solve_SAT(cnf,5)
	cnt=0
	satiscnt=0
	average_percentage_of_clauses_satisfied = 0.0
	number_of_variables=2500
	number_of_clauses=2500
	while(cnt < 1000000):
		print "--------------------------------------------------------------"
		print "Iteration :",cnt
		print "--------------------------------------------------------------"
		print "Verifying satisfying assignment computed ....."
		print "--------------------------------------------------------------"
		#satsolver=SATSolver("lsmr()")
		satsolver=SATSolver("pinv2()")
		#satsolver=SATSolver("lstsq()")
		cnf=satsolver.createRandom3CNF(number_of_clauses,number_of_variables)
		ass2=satsolver.solve_SAT2(cnf,number_of_variables,number_of_clauses)
		print "Random 3CNF:",cnf
		print "Assignment computed from least squares:",ass2
		satis=satsolver.satisfy(ass2)
		print "Assignment satisfied:",satis[0]
		print "Percentage of clauses satisfied in this random 3SAT:",satis[1]
		average_percentage_of_clauses_satisfied += satis[1]
		cnt += 1
		satiscnt += satis[0]
		prob_dist_variables=prob_dist(variables)
		prob_dist_negations=prob_dist(negations)
		avg_prob=0.0
		for x in prob_dist_variables:
			avg_prob += x
		for x in prob_dist_negations:
			avg_prob += x
		#print "Frequencies of Variables chosen in CNFs so far:",variables
		print "Moving Average - Probability of Variables chosen in CNFs so far:",prob_dist_variables
		#print "Frequencies of Negations chosen in CNFs so far:",negations
		print "Moving Average - Probability of Negations chosen in CNFs so far:",prob_dist_negations
		observed_avg_prob = avg_prob/float(2.0*number_of_variables)
		print "Observed - Average probability of a variable or negation:", observed_avg_prob 
		print "Theoretical - Probability per literal from Random Matrix Analysis of Least Squared (1/sqrt(mn)):",1.0/math.sqrt(float(number_of_variables)*float(number_of_clauses))
		print "Observed - Average Probability substituted in Random Matrix Analysis of Least Squared (m^2*n^2*p^4):",float(number_of_variables*number_of_variables)*float(number_of_clauses*number_of_clauses)*float(observed_avg_prob*observed_avg_prob*observed_avg_prob*observed_avg_prob)*100.0
		print "========================================================================================="
		print "Moving Average Percentage of CNFs satisfied so far:",(float(satiscnt)/float(cnt))*100
		print "*****MAXSAT-APPROXIMATION*****Moving Average Percentage of Clauses per CNF satisfied so far:",float(average_percentage_of_clauses_satisfied)/float(cnt)
		print "========================================================================================="
