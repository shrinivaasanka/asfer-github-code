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

class UnsortedSearch:
	def __init__(self,numarray):
		self.maxnumberdigits=5
		self.unsortedarray=[]
		self.digithashtables=[]
		for n in numarray:
			nstr=str(n)
			if len(nstr) < self.maxnumberdigits:
				hashpadding=""
				for z in xrange(self.maxnumberdigits - len(nstr)):
					hashpadding += "#"
			nstr = hashpadding+nstr	
			ntuple=[]
			for digit in nstr:
				ntuple.append(digit)
			self.unsortedarray.append(ntuple)

	def create_digit_hashtables(self):
		for d in xrange(self.maxnumberdigits):
			digitdict=LSH()
			for ntuple in self.unsortedarray:
				digitdict.add(ntuple[d])
			self.digithashtables.append(digitdict)

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
				hashpadding += "#"
			nstr = hashpadding+nstr	
		print "search_number(): padded n = ",nstr
		ntuple=[]
		cnt=0
		exists=True
		digitmatch=False
		for digit in nstr:
			if digit != "#":
				print "digit=",digit
				match=self.digithashtables[cnt].query_nearest_neighbours(digit)
				print "search_number(): match = ",match[0]
				for x in match[0][1]:
					if x == digit:
						print "digitmatch=True"
						digitmatch=True
				exists=exists & digitmatch 
				digitmatch=False
			cnt += 1
		return exists 

if __name__=="__main__":
	primes=[2,3,5,7,11,13,17,19,23,29,31,35,37,41,43]
	unsorted=UnsortedSearch(primes)
	unsorted.create_digit_hashtables()
	unsorted.print_unsorted_ntuples_hash()
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
