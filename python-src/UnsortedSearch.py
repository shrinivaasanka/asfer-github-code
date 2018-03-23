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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

from LocalitySensitiveHashing import LSH
import Streaming_AbstractGenerator

class UnsortedSearch:
	def __init__(self,streamiterator):
		self.maxnumberdigits=10
		self.unsortedarray=[]
		self.substringhashtables=[]
		for n in streamiterator:
			nstr=str(n)
			if len(nstr) < self.maxnumberdigits:
				hashpadding=""
				for z in xrange(self.maxnumberdigits - len(nstr)):
					hashpadding += "0"
			nstr = hashpadding+nstr	
			print "nstr=",nstr
			self.unsortedarray.append(nstr)

	def create_prefix_suffix_hashtables(self):
		for prefix in xrange(self.maxnumberdigits):
			substringdict=LSH()
			self.substringhashtables.append(substringdict)
		for prefix in xrange(self.maxnumberdigits):
			for nstr in self.unsortedarray:
				self.substringhashtables[prefix].add(nstr[:prefix])
		for suffix in xrange(self.maxnumberdigits):
			substringdict=LSH()
			self.substringhashtables.append(substringdict)
		for suffix in range(self.maxnumberdigits,self.maxnumberdigits*2):
			for nstr in self.unsortedarray:
				self.substringhashtables[suffix-self.maxnumberdigits].add(nstr[(suffix-self.maxnumberdigits):])

	def print_digit_hashtables(self):
		for substringhashtable in self.substringhashtables:
			substringhashtable.dump_contents()

	def print_unsorted_ntuples_hash(self):
		print "============================================"
		print "Unsorted N-tuple array"
		print "============================================"
		print self.unsortedarray
		print "============================================"
		print "Digit Hashtables"
		print "============================================"
		print self.digithashtables

	def search_number(self,n):
		print "search_number(): n= ",n
		nstr=str(n)
		if len(nstr) < self.maxnumberdigits:
			hashpadding=""
			for z in xrange(self.maxnumberdigits - len(nstr)):
				hashpadding += "0"
			nstr = hashpadding+nstr	
		print "search_number(): padded n = ",nstr
		ntuple=[]
		cnt=0
		exists=True
		substringmatch=False
		for prefix in xrange(self.maxnumberdigits):
			match=self.substringhashtables[prefix].query_nearest_neighbours(nstr[:prefix])
			print "match=",match
			for x in match[0][1]:
				if x == nstr[:prefix]:
					print "substringmatch=True"
					substringmatch=True
			exists=exists & substringmatch 
			substringmatch=False
			cnt += 1
		for suffix in range(self.maxnumberdigits,self.maxnumberdigits*2):
			match=self.substringhashtables[suffix-self.maxnumberdigits].query_nearest_neighbours(nstr[(suffix-self.maxnumberdigits):])
			print "match=",match
			for x in match[0][1]:
				if x == nstr[(suffix-self.maxnumberdigits):]:
					print "substringmatch=True"
					substringmatch=True
			exists=exists & substringmatch 
			substringmatch=False
			cnt += 1
		return exists 

if __name__=="__main__":
	#primesf=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
	primesf=Streaming_AbstractGenerator.StreamAbsGen("file","First100Primes.txt")
	unsorted=UnsortedSearch(primesf)
	unsorted.create_prefix_suffix_hashtables()
	#unsorted.print_unsorted_ntuples_hash()
	unsorted.print_digit_hashtables()
	print "======================================================"
	exists=unsorted.search_number(99455)
	print "Is Queried integer 99455 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(43)
	print "Is Queried integer 43 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(31)
	print "Is Queried integer 31 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(17)
	print "Is Queried integer 17 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(3278)
	print "Is Queried integer 3278 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(333)
	print "Is Queried integer 333 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(29)
	print "Is Queried integer 29 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(327)
	print "Is Queried integer 327 in unsorted array:",exists
	print "======================================================"
	exists=unsorted.search_number(115)
	print "Is Queried integer 115 in unsorted array:",exists
