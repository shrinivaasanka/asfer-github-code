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
#This class implements Streaming Majority Algorithm of Boyer-Moore for streaming sequence.

import Streaming_AbstractGenerator

class BoyerMoore_MajorityVoting(object):
	def __init__(self,datasource,datastorage):
		#self.inputstream = Streaming_AbstractGenerator.StreamAbsGen("file","file")
                #self.inputstream = Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
                self.datasource = datasource
                self.datastorage = datastorage
		self.inputstream = Streaming_AbstractGenerator.StreamAbsGen(datasource,datastorage)
		self.counter=0
		self.element=""

	def majority_voting(self):
                if self.datasource == "DictionaryHistogramPartition":
                    for evm in self.inputstream:
		        self.counter=0
		        self.element=""
                        for k,v in evm.iteritems():
			    if self.counter==0:
			        self.element=(k,v)
			        self.counter=1
			    else:
				if (k,v) == self.element:
				    self.counter += 1
				else:
				    self.counter -= 1
		        print "Majority Element in Stream:",self.element
                else:
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
	bm=BoyerMoore_MajorityVoting("DictionaryHistogramPartition","testlogs/Streaming_SetPartitionAnalytics.EVMs.json")
	bm.majority_voting()
