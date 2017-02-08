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

import numpy as np
import random
import math
from scipy.linalg import solve
from scipy.linalg import lstsq

class SATSolver(object):
	def __init__(self):
		self.equationsA=[]
		self.equationsB=[]
		self.cnfparsed=[]

	def difference(self, list1, list2):
		diff=[]
		for l1 in list1:
			if l1 not in list2:
				diff.append(l1)
		return diff

	def satisfy(self, assignment):
		#print "CNF clause:", self.cnfparsed
		#print "assignment:",assignment
		cnfval=1
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
			#print "clause value:",cval
			cnfval = cnfval * cval
		#print "cnf value:",cnfval
		return cnfval
		

	def solve_SAT(self,cnf,number_of_variables):
		cnfclauses=cnf.split("*")
		n=number_of_variables

		dnfclauses1=[]
		dnfclauses2=[]
		clauseliterals=[]
		allstrings=[]

		for i in xrange(int(math.pow(2,n))):
			bini=bin(i)[2:]
			bini=bini.zfill(n)
			allstrings.append(list(bini)) 

		print "cnfclauses:",cnfclauses
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
		print "Parsed CNF clauses:", self.cnfparsed
		print "DNF clauses 1:",dnfclauses1
		print "DNF clauses 2:",dnfclauses2
		print "All strings:",allstrings
		satassignments1=self.difference(allstrings, dnfclauses1)
		satassignments2=self.difference(allstrings, dnfclauses2)
		print "CNF SAT:",cnf
		print "SAT assignments 1:",satassignments1
		print "SAT assignments 2:",satassignments2
		return (satassignments1,satassignments2)

	def solve_SAT2(self,cnf,number_of_variables):
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
		for n in xrange(number_of_variables):
			self.equationsB.append(1)
		a = np.array(self.equationsA)
                b = np.array(self.equationsB)
                print "a:"
		print a
                print "b:"
		print b
                #x = solve(a,b)
                x = lstsq(a,b)
		print "solve_SAT2(): lstsq(): x:",x[0]
		a=[]
		for n in xrange(number_of_variables):
			a.append(0)
		cnt=0
		for e in x[0]:
			if e >= 0.1:
				a[cnt]=1
			else:
				a[cnt]=0
			cnt+=1
		print "solve_SAT2():",a
		return a

	def createRandom3CNF(self,numclauses,numvars):
		cnf=""
		clauses=[]
		for i in xrange(numclauses):
			randarray=np.random.permutation(numvars)
			clause= "("
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[0]+1)
			else:
				clause += "!x"+str(randarray[0]+1)
			clause += " + "
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[1]+1)
			else:
				clause += "!x"+str(randarray[1]+1)
			clause += " + "
			negation=random.randint(1,2)
			if negation==1:
				clause += "x"+str(randarray[2]+1)
			else:
				clause += "!x"+str(randarray[2]+1)
			clause += ")"
			clauses.append(clause)
		cnf=" * ".join(clauses)
		return cnf



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
	while(True):
		satsolver=SATSolver()
		cnf=satsolver.createRandom3CNF(10,10)
		ass2=satsolver.solve_SAT2(cnf,10)
		print "--------------------------------------------------------------"
		print "solve_SAT2(): Verifying satisfying assignment computed ....."
		print "--------------------------------------------------------------"
		satis=satsolver.satisfy(ass2)
		print "Assignment satisfied:",satis
		cnt += 1
		satiscnt += satis
		print "Percentage of CNFs satisfied so far:",(float(satiscnt)/float(cnt))*100
