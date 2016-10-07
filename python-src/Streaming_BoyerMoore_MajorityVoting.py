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

#This class implements Streaming Majority Algorithm of Boyer-Moore for streaming sequence.

import Streaming_AbstractGenerator

class BoyerMoore_MajorityVoting(object):
	def __init__(self):
		self.inputstream = Streaming_AbstractGenerator.StreamAbsGen("file","file")
		self.counter=0
		self.element=""

	def majority_voting(self):
		for e in self.inputstream:	
			if self.counter==0:
				self.element=e
				self.counter=1
			else:
				if e == self.element:
					self.counter += 1
				else:
					self.counter -= 1
		print "Majority Element in Stream:",self.element

if __name__=="__main__":
	bm=BoyerMoore_MajorityVoting()
	bm.majority_voting()
