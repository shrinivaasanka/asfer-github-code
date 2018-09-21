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

import sys
import math
import random
import Streaming_AbstractGenerator

def probabilistic_increment(k):
	randint1=random.randint(1,math.pow(2,k))
	randint2=random.randint(1,math.pow(2,k))
	if randint1==randint2:
		return 1 
	else:
		return 0 
		 
def approximate_counting(pattern):
	#The text file is updated by a stream of data
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
	inputf=Streaming_AbstractGenerator.StreamAbsGen("file","StreamingData.txt")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Socket_Streaming","localhost")
	k=0
	for i in inputf:
		if pattern.strip() == i.strip() :
			k += probabilistic_increment(k)
	count=math.pow(2,k) - 1
	print "approximate_counting(): count = ",count
	return count 

if __name__=="__main__":
	approxcount=approximate_counting(sys.argv[1])
	print "Approximate count of pattern [",sys.argv[1],"] in stream:",approxcount
