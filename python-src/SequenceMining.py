#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets 
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
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#This class Implements Sequence Mining for encoded strings - at present Apriori GSP algorithm has been
#implemented - uses Downward Closure - superset is frequent only if subset is frequent

import operator

class SequenceMining(object):
	def __init__(self):
		self.F=[[]]	
		self.candidates=[[]]

	def getNextLengthCandidates(self,length):
		self.candidates.append([])
		for x in self.candidates[length-1]:
			for y in self.candidates[1]:
				#print "x=",x,"y=",y," # adding ",x+y, 'to candidates of length:',length
				self.candidates[length].append(x+y)
		#print "Candidates at length ",length,"=",self.candidates[length]
		return self.candidates[length]

#######################################################################
	def doAprioriGSPSequenceMining(self):
		#inputf=open("asfer.enterprise.encstr.seqmining")
		inputf=open("First10000PrimesBinary.txt")
		input=inputf.readlines()

		self.candidates[0]=[]
		self.candidates.append(['0','1'])

		candidate_support={}

		self.F[0]=set()
		self.F.append(set())
		for cand in self.candidates[1]:
			for x in input:
				if cand in x:
					self.F[1].add(cand)	

		length=1
		maxlength=15
		print self.candidates
		print self.F

		while length < maxlength:
			print "===================================="
			print "iteration (or) length=", length
			print self.candidates[length]
			#C(k) - candidates at iteration k
			for cand in self.candidates[length]:
				for seq in input:
					if cand in seq:
						try:
							candidate_support[cand]+=1
						except KeyError:
							candidate_support[cand]=1
		
			#F(k)- frequent subsequences at iteration k
			self.F.append(set())
			for cand in self.candidates[length]:
				for x in input:
					if cand in x:
						if candidate_support[cand] > len(self.candidates[length])/2:
							self.F[length].add(cand)
			print "Frequent subsequences at length ",length,"=",self.F
			length+=1
			self.candidates[length]=self.getNextLengthCandidates(length)
		print "==================================================="
		print "Sorted Candidate support for all subsequence lengths - gives an approximate pattern in dataset:"
		s = sorted(candidate_support.items(),key=operator.itemgetter(1), reverse=True)
		print s

if __name__=="__main__":
	s=SequenceMining()
	s.doAprioriGSPSequenceMining()
