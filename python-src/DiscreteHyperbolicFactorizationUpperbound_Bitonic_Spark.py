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
#-----------------------------------------------------------------------------------------------------------

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row

from complement import toint
from bidict import bidict

import sys

midpoint=0
globalmergedtiles=bidict()
globalcoordinates=[]

def bitonic_sort(up, mergedtiles):
	if len(mergedtiles) <= 1:
		return mergedtiles
	else:
		firsthalf = bitonic_sort(True, mergedtiles[:int(len(mergedtiles)/2)])
		secondhalf = bitonic_sort(False, mergedtiles[int(len(mergedtiles)/2):])
		print "bitonicsort: firsthalf: ", firsthalf
		print "bitonicsort: secondhalf: ", secondhalf
		return bitonic_merge(up, firsthalf + secondhalf)

def bitonic_merge(up, mergedtiles):
	if len(mergedtiles) == 1:
		return mergedtiles
	else:
		bitonic_compare(up, mergedtiles)
		firsthalf = bitonic_merge(up, mergedtiles[:int(len(mergedtiles)/2)])
		secondhalf = bitonic_merge(up, mergedtiles[int(len(mergedtiles)/2):])
		print "bitonic_merge: firsthalf: ", firsthalf
		print "bitonic_merge: secondhalf: ", secondhalf
		if firsthalf[0] > secondhalf[len(secondhalf)-1]:
			return secondhalf+firsthalf
		else:
			return firsthalf+secondhalf

def bitonic_compare(up, mergedtiles):
	midpoint = int(len(mergedtiles)/2)
	spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
        #paralleldata = spcon.parallelize(mergedtiles)
        paralleldata = spcon.parallelize(mergedtiles).cache()
        #k=paralleldata.map(mapFunction_BitonicCompare).reduceByKey(reduceFunction_BitonicCompare)
        k=paralleldata.map(mapFunction_BitonicCompare).reduce(reduceFunction_BitonicCompare)
        #sqlContext=SQLContext(spcon)
        #parents_schema=sqlContext.createDataFrame(k.collect())
        #parents_schema.registerTempTable("Spark_MapReduce_Bitonic")
        #query_results=sqlContext.sql("SELECT * FROM Spark_MapReduce_Bitonic")
        #dict_query_results=dict(query_results.collect())
        spcon.stop()

def mapFunction_BitonicCompare(tileelement):
	tileelement_index=0
	#for k, v in globalmergedtiles.iteritems():
	#	if v==tileelement:
	#		tileelement_index=k
	tileelement_index=globalmergedtiles.inv[tileelement]
	return tileelement_index
	#return (1,tileelement_index)

def reduceFunction_BitonicCompare(i, k):
	print "##################################################################################"
	print "reduceFunction_BitonicCompare(): i=",i,"; k=",k
	if i is not None and k is not None:
		if (globalmergedtiles[i] > globalmergedtiles[i+midpoint]) == True:
			print "Shuffling mergedtiles and coordinates ..."
			globalmergedtiles[i], globalmergedtiles[i+midpoint] = globalmergedtiles[i+midpoint], globalmergedtiles[i]
			globalcoordinates[i], globalcoordinates[i+midpoint] = globalcoordinates[i+midpoint], globalcoordinates[i]
		if (globalmergedtiles[k] > globalmergedtiles[k+midpoint]) == True:
			print "Shuffling mergedtiles and coordinates ..."
			globalmergedtiles[k], globalmergedtiles[k+midpoint] = globalmergedtiles[k+midpoint], globalmergedtiles[k]
			globalcoordinates[k], globalcoordinates[k+midpoint] = globalcoordinates[k+midpoint], globalcoordinates[k]
	#sys.stdout.flush()

def MergedTiles_BitonicSort():
	mergedtilesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles","r")
	coordinatesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates","r")
	#mergedtiles=[10, 3, 5, 71, 30, 11, 20, 4, 330, 21, 110, 7, 33, 9, 39, 46]
	cnt=1
	try:
		for i in mergedtilesf:
			globalmergedtiles[cnt-1]=toint(i)
			cnt+=1
			if cnt == 16384:
				break

		if cnt < 16384:
			while cnt <= 16384:
				globalmergedtiles[cnt-1]=0
				cnt+=1
	except:
		print "Exception:"
		pass

	try:
		cnt=1
		for i in coordinatesf:
			globalcoordinates.append(toint(i))
			cnt+=1
			if cnt == 16384:
				break

		if cnt < 16384:
			while cnt <= 16384:
				globalcoordinates[cnt-1]=0
				cnt+=1
	except:
		print "Exception:"
		pass
	print "unsorted=",globalmergedtiles
	sorted=bitonic_sort(True, globalmergedtiles.values())
	print "sorted=",globalmergedtiles
	print "globalcoordinates=",globalcoordinates

if __name__=="__main__":
	MergedTiles_BitonicSort()
