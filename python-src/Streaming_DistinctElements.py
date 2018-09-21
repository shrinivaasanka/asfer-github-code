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

def distinct_elements(pattern=None):
	#The text file is updated by a stream of data
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
	inputf=Streaming_AbstractGenerator.StreamAbsGen("file","StreamingData.txt")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Socket_Streaming","localhost")
	supersetsize=0
	randomsubset=[]
	if pattern is None:
		for x in inputf:
			randint=random.randint(1,2)
			supersetsize += 1
			if randint==1:
				randomsubset.append(x)
	else:
		for x in inputf:
			supersetsize += 1
			if x.strip() == pattern.strip():
				randomsubset.append(x)
	minimum=min(randomsubset)
	print "minimum:",minimum
	size=(supersetsize/float(minimum.strip())) - 1
	return size

if __name__=="__main__":
	size=distinct_elements()
	print "Distinct Elements in random subset of the stream:",size
