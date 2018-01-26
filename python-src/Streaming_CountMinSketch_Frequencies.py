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

#----------------------------------------------------
# CountMinSketch Algorithm for Frequencies in Stream
#----------------------------------------------------
# a matrix of m-rows*n-columns where each value in the stream is hashed to some grid cell on 
# every row (the cell value is incremented). For each row different hash function is applied. 
# Each row is an estimator and minimum of counters in the hashed cells in all rows is an
# estimate of frequency of the value in input stream.
#
# Estimation error epsilon <= 2n/width
# with probability delta = 1 - (1/2)^depth

import binascii
import hashlib
import Streaming_AbstractGenerator
import random

def getHash(str,row,a,b):
        h=hashlib.new("ripemd160")
        h.update(str)
        hash=(int(h.hexdigest(),16)*a[row] + b[row])
        #print "hash for string [",str,"] :",hash
        return hash

#Depth
rows=300

#Width
columns=30000

no_of_elements_added=0
a=b=[]

for x in xrange(rows):
	a.append(random.randint(1,100000))
	b.append(random.randint(1,100000))

countminsketch=[]
rowvector=[]
for n in xrange(columns):
	rowvector.append(0)
for m in xrange(rows):
	countminsketch.append(rowvector)
#print countminsketch

#inputf=open("StreamingData.txt","r")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("file","file")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
#add and populate sketch
for i in inputf:
	for row in xrange(rows):
		column=getHash(i,row,a,b)%columns
		countminsketch[row][column]+=1
		no_of_elements_added+=1
	row=0
print countminsketch

#inputf=open("StreamingData.txt","r")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("file","file")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
#frequencies of each input - minimum of all hashed cells
no_of_elements_estimated=0
no_of_elements_exact=0
minsketch_dict={}

for i in inputf:
	no_of_elements_exact += 1
	minsketch=10000000000
	for row in xrange(rows):
		column=getHash(i,row,a,b)%columns
		minsketch=min(minsketch, countminsketch[row][column])
	print "minsketch frequency estimation for [",i,"] :",minsketch
	if minsketch_dict.get(i,None)==None:
		minsketch_dict[i]=minsketch
	else:
		print "Key already exists"
	row=0

for key,value in minsketch_dict.items():
	no_of_elements_estimated += value

print "CountMinSketch estimate:"
print minsketch_dict
print "Size of CountMinSketch estimate:"
print len(minsketch_dict)
print "Number of Elements Estimated by CountMinSketch:",no_of_elements_estimated
print "Exact number of elements:",no_of_elements_exact
print "Number of Elements added in Sketch:",no_of_elements_added
