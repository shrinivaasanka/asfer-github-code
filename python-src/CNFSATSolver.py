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
#from scipy.linalg import solve
from scipy.linalg import lstsq
from numpy.linalg import solve
from numpy.linalg import inv 
#from numpy.linalg import lstsq
from scipy.sparse.linalg import lsqr
from scipy.sparse.linalg import lsmr
from scipy.sparse.linalg import dsolve
from scipy.sparse.linalg import bicgstab 
from scipy.sparse.linalg import gmres 
from scipy.sparse.linalg import lgmres 
from scipy.sparse.linalg import minres 
from scipy.sparse.linalg import bicg 
from scipy.sparse.linalg import cg 
from scipy.sparse.linalg import cgs 
from scipy.sparse import csc_matrix
from scipy.linalg import pinv
from scipy.linalg import pinv2
from numpy import matmul
#from scipy.sparse import csr_matrix 
from numpy import polyfit
from scipy.optimize import lsq_linear
from scipy.fftpack import fft

variables=defaultdict(int)
negations=defaultdict(int)

nuvariables=defaultdict(int)
rounding_threshold="Static"
#rounding_threshold="Randomized"

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

	def satisfy(self, assignment, fractional_assignment):
		#print "CNF Formula:", self.cnfparsed
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
		

	def solve_SAT(self,cnf,number_of_variables,number_of_clauses):
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
			#dnfclause1=[]
			#dnfclause2=[]
			#for i in xrange(n):
			#	dnfclause1.append("1")
			#	dnfclause2.append("0")
			for l in clauseliterals:
				lstrip=l.strip()
				if lstrip[0]=="(":
					lstrip=lstrip[1:] 
				if lstrip[len(lstrip)-1]==")":
					lstrip=lstrip[:len(lstrip)-1]
				cnfclause.append(lstrip)

			#	print "lstrip:",lstrip
			#	if lstrip[0] != "!":
			#		print "lstrip[1:]:",int(lstrip[1:])
			#		dnfclause1[int(lstrip[1:])-1] = "0"
			#		dnfclause2[int(lstrip[1:])-1] = "0"
			#	else:
			#		#print "lstrip[2:]:",lstrip[2:]
			#		dnfclause1[int(lstrip[2:])-1] = "1"
			#		dnfclause2[int(lstrip[2:])-1] = "1"
			#dnfclauses1.append(dnfclause1)
			#dnfclauses2.append(dnfclause2)
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
		#Solves CNFSAT by a Polynomial Time Approximation scheme:
		#	- Encode each clause as a linear equation in n variables: missing variables and negated variables are 0, others are 1
		#	- Solve previous system of equations by least squares algorithm to fit a line
		#	- Variable value above 0.5 is set to 1 and less than 0.5 is set to 0
		#	- Rounded of assignment array satisfies the CNFSAT with high probability
		#Returns: a tuple with set of satisfying assignments
		satass=[]
		x=[]
		self.solve_SAT(cnf,number_of_variables,number_of_clauses)
		for clause in self.cnfparsed:
			equation=[]
			for n in xrange(number_of_variables):
				equation.append(0)
			#print "clause:",clause
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
		init_guess = []
		for n in xrange(number_of_variables):
			init_guess.append(0.00000000001)
		initial_guess = np.array(init_guess)
		self.A=a
		self.B=b
		#print "a:",a
		#print "b:",b
                #print "a.shape:",a.shape
                #print "b.shape:",b.shape

		x=None
		if number_of_variables == number_of_clauses:
			#x = np.dot(np.linalg.inv(a),b)
			#x = gmres(a,b) 
			#x = lgmres(a,b) 
			#x = minres(a,b) 
			#x = bicg(a,b) 
			#x = cg(a,b) 
			#x = cgs(a,b) 
			#x = bicgstab(a,b)
                	#x = lsqr(a,b,atol=0,btol=0,conlim=0,show=True)
                	x = lsmr(a,b,atol=0,btol=0,conlim=0,show=True,x0=initial_guess)
		else:
			if self.Algorithm=="solve()":
                		x = solve(a,b)
			if self.Algorithm=="lstsq()":
                		x = lstsq(a,b,lapack_driver='gelsy')
			if self.Algorithm=="lsqr()":
                		x = lsqr(a,b,atol=0,btol=0,conlim=0,show=True)
			if self.Algorithm=="lsmr()":
                		#x = lsmr(a,b,atol=0.1,btol=0.1,maxiter=5,conlim=10,show=True)
                		x = lsmr(a,b,atol=0,btol=0,conlim=0,show=True,x0=initial_guess)
			if self.Algorithm=="spsolve()":
				x = dsolve.spsolve(csc_matrix(a),b)
			if self.Algorithm=="pinv2()":
				x=[]
				#pseudoinverse_a=pinv(a)
				pseudoinverse_a=pinv2(a,check_finite=False)
				x.append(matmul(pseudoinverse_a,b))
			if self.Algorithm=="lsq_linear()":
				x = lsq_linear(a,b,lsq_solver='exact')

		print "solve_SAT2(): ",self.Algorithm,": x:",x
		cnt=0
		binary_parity=0
		real_parity=0.0
		if rounding_threshold == "Randomized":
			randomized_rounding_threshold=float(random.randint(1,100000))/100000.0
		else:
			min_assignment=min(x[0])
			max_assignment=max(x[0])
			randomized_rounding_threshold=(min_assignment + max_assignment)/2
		print "randomized_rounding_threshold = ", randomized_rounding_threshold
		print "approximate assignment :",x[0]
		for e in x[0]:
			if e > randomized_rounding_threshold:
				satass.append(1)
				binary_parity += 1
			else:
				satass.append(0)
				binary_parity += 0
			real_parity += e
			cnt+=1
		print "solve_SAT2(): real_parity = ",real_parity
		print "solve_SAT2(): binary_parity = ",binary_parity
		return (satass,real_parity,binary_parity,x[0])
	
	def nonuniform_choice(self, literal_selection, numvars, numclauses):
		randarrayclauses=np.random.choice(numclauses, int(math.sqrt(numclauses)), replace=True)
		randarrayvars=np.random.choice(numvars, int(math.sqrt(numvars)), replace=True)
		randclausevarpairs=[]
		for rc in randarrayclauses:
			for rv in randarrayvars:
				randclausevarpairs.append((rc,rv))
		if literal_selection=="sequential":
			randclausevarpair1=randclausevarpairs[np.random.choice(len(randclausevarpairs),1,replace=True)]
			randclausevarpair2=randclausevarpairs[np.random.choice(len(randclausevarpairs),1,replace=True)]
			randclausevarpair3=randclausevarpairs[np.random.choice(len(randclausevarpairs),1,replace=True)]
			#print "sequential: nonuniform_choice(): random clause = [",randclausevarpair1,",",randclausevarpair2,",",randclausevarpair3,"]"
			nuvariables[randarrayvarpair1[1]] = nuvariables[randarrayvarpair1[1]] + 1
			nuvariables[randarrayvarpair2[1]] = nuvariables[randarrayvarpair2[1]] + 1
			nuvariables[randarrayvarpair3[1]] = nuvariables[randarrayvarpair3[1]] + 1
			return [randclausevarpair1[1],randclausevarpair2[1],randclausevarpair3[1]]
		else:
			if literal_selection=="simultaneous":
				literals=np.random.choice(len(randclausevarpairs),3,replace=True)
				#print "simultaneous: nonuniform_choice(): random clause = [",randclausevarpairs[literals[0]][1],",",randclausevarpairs[literals[1]][1],",",randclausevarpairs[literals[2]][1],"]"
				nuvariables[randclausevarpairs[literals[0]][1]] = nuvariables[randclausevarpairs[literals[0]][1]] + 1
				nuvariables[randclausevarpairs[literals[1]][1]] = nuvariables[randclausevarpairs[literals[1]][1]] + 1
				nuvariables[randclausevarpairs[literals[2]][1]] = nuvariables[randclausevarpairs[literals[2]][1]] + 1
				return [randclausevarpairs[literals[0]][1],randclausevarpairs[literals[1]][1],randclausevarpairs[literals[2]][1]]

	def nonuniform_choice2(self,literal_selection,numvars,numclauses):
		alpha=float(numclauses/numvars)
		valid=False
		randarrayvars1=np.random.choice(numvars, numvars, replace=True)
		#randarrayvars2=np.random.choice(numvars, int(alpha*numvars), replace=True)
		randarrayvars=[]
		for v in randarrayvars1:
			randarrayvars.append(v)
		for v in xrange(int(alpha*numvars*numvars)):
			randarrayvars.append(numvars*2)
		#print "nonuniform_choice2(): randarrayvars = ",randarrayvars
		while not valid:
			if literal_selection=="sequential":
				literal1=np.random.choice(len(randarrayvars),1,replace=True)	
				literal2=np.random.choice(len(randarrayvars),1,replace=True)	
				literal3=np.random.choice(len(randarrayvars),1,replace=True)	
				#print "sequential: nonuniform_choice2(): random clause =[",randarrayvars[literal1[0]],",",randarrayvars[literal2[0]],",",randarrayvars[literal3[0]],"]"
				if randarrayvars[literal1[0]] != numvars*2 and randarrayvars[literal2[0]] != numvars*2 and randarrayvars[literal3[0]] != numvars*2:
					#print "valid clause"
					valid=True
				if valid:
					nuvariables[randarrayvars[literal1[0]]] = nuvariables[randarrayvars[literal1[0]]] + 1
					nuvariables[randarrayvars[literal2[0]]] = nuvariables[randarrayvars[literal2[0]]] + 1
					nuvariables[randarrayvars[literal3[0]]] = nuvariables[randarrayvars[literal3[0]]] + 1
					return [randarrayvars[literal1[0]],randarrayvars[literal2[0]],randarrayvars[literal3[0]]]
			else:
				if literal_selection=="simultaneous":
					literals=np.random.choice(len(randarrayvars),3,replace=True)	
				#print "simultaneous: nonuniform_choice2(): random clause =[",randarrayvars[literals[0]],",",randarrayvars[literals[1]],",",randarrayvars[literals[2]],"]"
				if randarrayvars[literals[0]] != numvars*2 and randarrayvars[literals[1]] != numvars*2 and randarrayvars[literals[2]] != numvars*2:
					#print "valid clause"
					valid=True
				if valid:
					nuvariables[randarrayvars[literals[0]]] = nuvariables[randarrayvars[literals[0]]] + 1
					nuvariables[randarrayvars[literals[1]]] = nuvariables[randarrayvars[literals[1]]] + 1
					nuvariables[randarrayvars[literals[2]]] = nuvariables[randarrayvars[literals[2]]] + 1
					return [randarrayvars[literals[0]],randarrayvars[literals[1]],randarrayvars[literals[2]]]

	def nonuniform_choice3(self,literal_selection,numvars,numclauses):
		variables=np.random.choice(numvars, numvars, replace=True)
		alpha=float(numclauses)/float(numvars)
		damp=1.09
		constant=math.sqrt(alpha)-damp
		skewvariable=int(constant*len(variables))
		extendedvariables=[]
	        for x in variables:
                	extendedvariables.append(x)
        	for x in xrange(int(constant*len(variables))):
               		extendedvariables.append(skewvariable)
		#print "variables=",variables
		#print "extendedvariables =",extendedvariables

        	literal1=np.random.choice(len(extendedvariables),1,replace=True)
        	#print "variable1=",extendedvariables[literal1[0]]
        	while extendedvariables[literal1[0]] == skewvariable:
               		 literal1=np.random.choice(len(extendedvariables),1,replace=True)
               		 #print "variable1=",extendedvariables[literal1[0]]
               		 nuvariables[extendedvariables[literal1[0]]] = nuvariables[extendedvariables[literal1[0]]] + 1
        	nuvariables[extendedvariables[literal1[0]]] = nuvariables[extendedvariables[literal1[0]]] + 1

        	literal2=np.random.choice(len(extendedvariables),1,replace=True)
        	#print "variable2=",extendedvariables[literal2[0]]
        	while extendedvariables[literal2[0]] == skewvariable:
               		 literal2=np.random.choice(len(extendedvariables),1,replace=True)
               		 #print "variable2=",extendedvariables[literal2[0]]
               		 nuvariables[extendedvariables[literal2[0]]] = nuvariables[extendedvariables[literal2[0]]] + 1
        	nuvariables[extendedvariables[literal2[0]]] = nuvariables[extendedvariables[literal2[0]]] + 1

        	literal3=np.random.choice(len(extendedvariables),1,replace=True)
        	#print "variable3=",extendedvariables[literal3[0]]
        	while extendedvariables[literal3[0]] == skewvariable:
               		 literal3=np.random.choice(len(extendedvariables),1,replace=True)
               		 #print "variable3=",extendedvariables[literal3[0]]
               		 nuvariables[extendedvariables[literal3[0]]] = nuvariables[extendedvariables[literal3[0]]] + 1
        	nuvariables[extendedvariables[literal3[0]]] = nuvariables[extendedvariables[literal3[0]]] + 1
		return [extendedvariables[literal1[0]],extendedvariables[literal2[0]],extendedvariables[literal3[0]]]

	def createRandom3CNF(self,distribution,literal_selection,numclauses,numvars):
		cnf=""
		clauses=[]
		for i in xrange(numclauses):
			randarray=np.random.permutation(numvars)
			if distribution=="Uniform":
				randarray=np.random.choice(numvars,3,replace=True)
			else:
				if distribution=="Non-Uniform":
					if literal_selection=="sequential":
						#randarray=self.nonuniform_choice("sequential",numvars,numclauses)
						#randarray=self.nonuniform_choice2("sequential",numvars,numclauses)
						randarray=self.nonuniform_choice3("sequential",numvars,numclauses)
					if literal_selection=="simultaneous":
						#randarray=self.nonuniform_choice("simultaneous",numvars,numclauses)
						#randarray=self.nonuniform_choice2("simultaneous",numvars,numclauses)
						randarray=self.nonuniform_choice3("simultaneous",numvars,numclauses)
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
	#print "sumfreq=",sumfreq
	for x,y in freq.iteritems():
		#print "y=",y
		prob.append(float(y)/float(sumfreq))
	return prob


if __name__=="__main__":
	#cnf="(!x1 + !x2 + !x3 + x4) * (x1 + x2 + !x3 + !x4) * (!x1 + x2 + !x3 + x4) * (x1 + !x2 + x3 + !x4) * (x1 + !x2 + x3 + x4)"
	#cnf="(x1 + !x4 + !x5) * (!x1 + x3 + x4) * (x2 + !x3 +  !x4) * (x3 + !x4 + !x5) * (!x1 + x4 + !x5)"

	cnt=0
	satiscnt=0
	average_percentage_of_clauses_satisfied = 0.0
	number_of_variables=int(sys.argv[1])
	alpha=float(sys.argv[2])
	number_of_clauses=int(number_of_variables*alpha)
	#number_of_clauses=1000
	while(cnt < 1000000):
		print "--------------------------------------------------------------"
		print "Iteration :",cnt
		print "--------------------------------------------------------------"
		print "Number of variables = ",number_of_variables,"; Number of clauses = ",number_of_clauses,"; Alpha = ",float(number_of_clauses)/float(number_of_variables),"; Verifying satisfying assignment computed ....."
		print "--------------------------------------------------------------"
		satsolver=SATSolver("lsmr()")
		#satsolver=SATSolver("solve()")
		#satsolver=SATSolver("pinv2()")
		#satsolver=SATSolver("lstsq()")
		#satsolver=SATSolver("lsqr()")
		#satsolver=SATSolver("lsq_linear()")
		cnf=None
		if number_of_clauses==number_of_variables:
			cnf=satsolver.createRandom3CNF("Uniform","simultaneous",number_of_clauses,number_of_variables)
		else:
			#cnf=satsolver.createRandom3CNF("Non-Uniform","sequential",number_of_clauses,number_of_variables)
			cnf=satsolver.createRandom3CNF("Non-Uniform","simultaneous",number_of_clauses,number_of_variables)
		ass2=satsolver.solve_SAT2(cnf,number_of_variables,number_of_clauses)
		print "Random 3CNF:",cnf
		print "Assignment computed from least squares:",ass2
		satis=satsolver.satisfy(ass2[0],ass2[3])
		print "Assignment satisfied:",satis[0]
		average_percentage_of_clauses_satisfied += satis[1]

		print "Discrete Fourier Transform of the real assignment:",fft(ass2[0])

		cnt += 1
		satiscnt += satis[0]
		prob_dist_variables=prob_dist(variables)
		prob_dist_negations=prob_dist(negations)
		prob_dist_nuvariables=prob_dist(nuvariables)
		avg_prob=0.0
		avg_nu_prob=0.0
		for x in prob_dist_variables:
			avg_prob += x
		for x in prob_dist_negations:
			avg_prob += x
		for x in prob_dist_nuvariables[:-1]:
			avg_nu_prob += x
		#print "Frequencies of Variables chosen in CNFs so far:",variables
		#print "Moving Average - Probability of Variables chosen in CNFs so far:",prob_dist_variables
		#print "Frequencies of Negations chosen in CNFs so far:",negations
		#print "Moving Average - Probability of Negations chosen in CNFs so far:",prob_dist_negations
		#print "Moving Average - Probability of Non-Uniform Choice Variables:",prob_dist_nuvariables
		observed_avg_prob = avg_prob/float(2.0*number_of_variables)
		observed_avg_nu_prob = avg_nu_prob/float(2*number_of_variables)
		print "========================================================================================="
		#print "Observed - Unaveraged Probabilities of Non-Uniformly chosen literal (has one heavily skewed variable, all other probabilities should almost match random matrix probability 1/sqrt(m*n)  :",prob_dist_nuvariables
		if number_of_clauses != number_of_variables:
			print "Observed - Average Probability of Non-Uniformly chosen literal (minus one heavily skewed variable, all other probabilities should almost match random matrix probability 1/sqrt(m*n) if m != n)  :",observed_avg_nu_prob
		print "Percentage of clauses satisfied in this random 3SAT:",satis[1]
		if number_of_clauses == number_of_variables:
			print "Observed - Average probability of a variable or negation :", observed_avg_prob 
		print "Theoretical - Probability per literal from Random Matrix Analysis of Least Squared (1/sqrt(mn)):",1.0/math.sqrt(float(number_of_variables)*float(number_of_clauses))
		if number_of_clauses == number_of_variables:
			print "Theoretical - MAXSAT-APPROXIMATION Ratio - Observed Average Probability substituted in Random Matrix Analysis of Least Squared (m^2*n^2*p^4):",float(number_of_variables*number_of_variables)*float(number_of_clauses*number_of_clauses)*float(observed_avg_prob*observed_avg_prob*observed_avg_prob*observed_avg_prob)*100.0
		else:
			print "Theoretical - MAXSAT-APPROXIMATION Ratio - Observed Average Probability substituted in Random Matrix Analysis of Least Squared (m^2*n^2*p^4):",float(number_of_variables*number_of_variables)*float(number_of_clauses*number_of_clauses)*float(observed_avg_nu_prob*observed_avg_nu_prob*observed_avg_nu_prob*observed_avg_nu_prob)*100.0
		print "Observed - Moving Average Percentage of CNFs satisfied so far:",(float(satiscnt)/float(cnt))*100
		print "Observed - MAXSAT-APPROXIMATION Ratio - Moving Average Percentage of Clauses per CNF satisfied so far:",float(average_percentage_of_clauses_satisfied)/float(cnt)
		print "========================================================================================="
