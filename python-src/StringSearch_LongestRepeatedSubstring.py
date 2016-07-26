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
#-----------------------------------------------------------------------------------------------------------------------------------

#String Pattern Search - to find the repeated substrings within a string
#Suffix Tree Implementation is done indirectly with combination of Suffix Arrays and Longest Common Prefix (LCP) datastructures
#Longest Repeated Substring is searched with LCP and position information in Suffix Arrays
#References: http://algs4.cs.princeton.edu/63suffix/, http://webglimpse.net/pubs/suffix.pdf

import operator

class SuffixArray(object):
	def __init__(self):
		self.pattern_file=open("StringSearch_Pattern.txt","r")
		self.pattern=self.pattern_file.read()
		print "String Pattern: ", self.pattern
		self.suffix_dict={}
		self.suffix_array=[]

	def construct_suffix_array(self):
		for n in xrange(len(self.pattern)-1):
			suffix=self.pattern[n:len(self.pattern)-1]
			self.suffix_dict[suffix]=n
                self.suffix_array = sorted(self.suffix_dict.items(),key=operator.itemgetter(0), reverse=False)
		print "Suffix Array with Position Info:",self.suffix_array

	def longest_common_prefix(self,index):
		first_len=len(self.pattern)-self.suffix_array[index][1]
		second_len=len(self.pattern)-self.suffix_array[index-1][1]
		n=min(first_len,second_len)
		for i in xrange(n-1):
			if self.suffix_array[index][0][i] != self.suffix_array[index-1][0][i]:
				return i
		return n

	def longest_repeated_substring(self,text):
		lrs=""
		length=0
		for i in range(1,len(text)-1):
			length=self.longest_common_prefix(i)
			print "Repeated Substring:",text[self.suffix_array[i][1]:self.suffix_array[i][1]+length]
			if length > len(lrs):
				lrs=text[self.suffix_array[i][1]:self.suffix_array[i][1]+length]
		print "========================================================="
		print "Longest Repeated Substring=",lrs
		print "========================================================="
			
if __name__=="__main__":
	suff_array=SuffixArray()
	suff_array.construct_suffix_array()
	suff_array.longest_repeated_substring(suff_array.pattern)					

