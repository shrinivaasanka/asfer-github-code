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

class SATSolver(object):
	def __init__(self):
		self.cnfparsed=[]

	def difference(self, list1, list2):
		diff=[]
		for l1 in list1:
			if l1 not in list2:
				diff.append(l1)
		return diff

	def satisfy(self, assignment):
		#print "CNF clause", self.cnfparsed
		cnfval=1
		for c in self.cnfparsed:
			cval=0
			for l,v in zip(c,assignment):
				#print "v:",int(v)
				if l[0] == "!":
					cval = cval + (1-int(v))
				else:
					cval = cval + int(v)
				if cval > 1:
					cval=1
				#print "cval:",cval
			cnfval = cnfval * cval
		#print "cnfval:",cnfval
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
			print "clauseliterals:",clauseliterals
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

				print "lstrip:",lstrip
				if lstrip[0] != "!":
					print "lstrip[1:]:",int(lstrip[1:])
					dnfclause1[int(lstrip[1:])-1] = "0"
					dnfclause2[int(lstrip[1:])-1] = "0"
				else:
					print "lstrip[2:]:",lstrip[2:]
					dnfclause1[int(lstrip[2:])-1] = "1"
					dnfclause2[int(lstrip[2:])-1] = "1"
			dnfclauses1.append(dnfclause1)
			dnfclauses2.append(dnfclause2)
			self.cnfparsed.append(cnfclause)
		print "DNF clauses 1:",dnfclauses1
		print "DNF clauses 2:",dnfclauses2
		print "All strings:",allstrings
		satassignments1=self.difference(allstrings, dnfclauses1)
		satassignments2=self.difference(allstrings, dnfclauses2)
		print "CNF SAT:",cnf
		print "SAT assignments 1:",satassignments1
		print "SAT assignments 2:",satassignments2
		return (satassignments1,satassignments2)

if __name__=="__main__":
	satsolver=SATSolver()	
	cnf="(!x1 + !x2 + !x3 + x4) * (x1 + x2 + !x3 + !x4) * (!x1 + x2 + !x3 + x4) * (x1 + !x2 + x3 + !x4) * (x1 + !x2 + x3 + x4)"

	#Parameter1: any k-CNF with all literals in each clause, negations prefixed with !
	#Parameter2: Number of variables
	#Returns: a tuple with set of satisfying assignments (missing literals initialized to 0 and 1 respectively, but 
	#presently both are equal)
	ass=satsolver.solve_SAT(cnf,4)
	print "------------------------------------------------------"
	print "Verifying satisfying assignments computed ....."
	print "------------------------------------------------------"
	for a in ass[0]:	
		print "Assignment (array1) satisfied:",satsolver.satisfy(a)
	for a in ass[1]:	
		print "Assignment (array2) satisfied:",satsolver.satisfy(a)
	print "------------------------------------------------------"
	print "Verifying some non-satisfying assignments ....."
	print "------------------------------------------------------"
	print "Assignment satisfied:",satsolver.satisfy(['0','1','0','0'])
	print "Assignment satisfied:",satsolver.satisfy(['0','1','0','1'])
	print "Assignment satisfied:",satsolver.satisfy(['0','0','1','1'])
