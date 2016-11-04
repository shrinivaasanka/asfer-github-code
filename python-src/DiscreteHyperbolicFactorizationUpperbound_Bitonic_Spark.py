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

#Reference for AccumulatorParam and global state modified within local worker node from code documentation of:
#http://fossies.org/linux/spark/python/pyspark/accumulators.py

from pyspark.accumulators import AccumulatorParam
class VectorAccumulatorParam(AccumulatorParam):
     def zero(self, value):
         return [0.0] * len(value)
     def addInPlace(self, val1, val2):
         for i in range(len(val1)):
              val1[i] += val2[i]
         return val1

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row

from complement import toint
from bidict import bidict
import threading
import memcache
from collections import namedtuple

import sys

#globalmergedtiles=bidict()
globalmergedtiles={}
globalmergedtiles_accum=None
globalcoordinates=[]
bitoniclock=threading.Lock()

spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
globalmergedtiles_accum=spcon.accumulator([], VectorAccumulatorParam())

#This thread function assigns the Spark Mapreduce result of Compare and Exchange
#Mulithreading is an alternative for global state mutability in the absence of Spark support
#and it does not require any third party in-memory cacheing products
#Coordinates are also shuffled first few elements of which correspond to number to factor N are
#the factors found finally. Multithreaded assignment maps to a multicore parallelism.
def assign_compareexchange_multithreaded(mergedtiles_comparators, midpoint, i):
	globalmergedtiles_accum.value[mergedtiles_comparators[i][0]]=mergedtiles_comparators[i][2]
	globalmergedtiles_accum.value[mergedtiles_comparators[i][0] + midpoint]=mergedtiles_comparators[i][3]
	globalcoordinates[mergedtiles_comparators[i][0]], globalcoordinates[mergedtiles_comparators[i][0]+midpoint] = globalcoordinates[mergedtiles_comparators[i][0] + midpoint], globalcoordinates[mergedtiles_comparators[i][0]]


def bitonic_sort(spcon, up, mergedtiles, start, end):
	print "##################################################################################"
	if len(mergedtiles) <= 1:
		return mergedtiles
	else:
		firsthalf = bitonic_sort(spcon, True, mergedtiles[:int(len(mergedtiles)/2)], start, start+int(len(mergedtiles)/2))
		secondhalf = bitonic_sort(spcon, False, mergedtiles[int(len(mergedtiles)/2):], start+int(len(mergedtiles)/2), end)
		print "bitonicsort: firsthalf: ", firsthalf
		print "bitonicsort: secondhalf: ", secondhalf
		mergedhalves=bitonic_merge(spcon, up, firsthalf + secondhalf, start, end)
		print "bitonic_sort(): merged sorted halves:", mergedhalves
		return mergedhalves

def bitonic_merge(spcon, up, mergedtiles, start, end):
	if len(mergedtiles) == 1:
		return mergedtiles
	else:
		if (up==True):
			bitonic_compare_true(spcon, mergedtiles, start, end)
		else:
			bitonic_compare_false(spcon, mergedtiles, start, end)
		firsthalf = bitonic_merge(spcon, up, mergedtiles[:int(len(mergedtiles)/2)], start, start+int(len(mergedtiles)/2))
		secondhalf = bitonic_merge(spcon, up, mergedtiles[int(len(mergedtiles)/2):], start+int(len(mergedtiles)/2), end)
		print "bitonic_merge: firsthalf: ", firsthalf
		print "bitonic_merge: secondhalf: ", secondhalf
		return firsthalf+secondhalf

'''
#####################################################
Parallelizes comparator in:
        midpoint = int(len(mergedtiles)/2)
        print "bitonic_compare_true(): up= True"
        for i in range(midpoint):
                if (mergedtiles[i] > mergedtiles[i+midpoint]) == True:
                        temp = mergedtiles[i+midpoint]
                        mergedtiles[i+midpoint] = mergedtiles[i]
                        mergedtiles[i] = temp
#####################################################
'''

def bitonic_compare_true(spcon, mergedtiles, start, end):
	print "bitonic_compare_true(): 1. mergedtiles=",mergedtiles,";start=",start,";end=",end
	midpoint = int(len(mergedtiles)/2)
	midpointlist=[]
	#spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
	for l in range(midpoint):
		midpointlist.append(mergedtiles[l+midpoint])
	#tuple: (globalindex, localindex_per_recursion, firsthalfelement, secondhalfelement)
	mergedtilesmidpointlist=zip(range(start,end),range(midpoint),mergedtiles[:midpoint],midpointlist)

        paralleldata = spcon.parallelize(mergedtilesmidpointlist)
        #paralleldata = spcon.parallelize(mergedtilesmidpointlist).cache()
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduceByKey(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduce(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare)
       	#k=paralleldata.map(Foreach_BitonicCompare_True_map).reduceByKey(Foreach_BitonicCompare_True_reduce)
       	k=paralleldata.map(Foreach_BitonicCompare_True_map)

	mergedtiles_comparators=[]
	if k is not None:
		mergedtiles_comparators=k.collect()
		print "bitonic_compare_true() collected:",mergedtiles_comparators
	print "bitonic_compare_true(): mergedtiles: ",mergedtiles
	print "bitonic_compare_true(): mergedtilesmidpointlist: ",mergedtilesmidpointlist
	print "bitonic_compare_true(): mergedtiles_comparators:",mergedtiles_comparators
	
	threads=[]
	for i in range(midpoint):
                if (mergedtiles_comparators[i][4]):
                        #temp = mergedtiles[mergedtiles_comparators[i][0]]
                        #mergedtiles[mergedtiles_comparators[i][0]] = mergedtiles[mergedtiles_comparators[i][0]+midpoint]
                        #mergedtiles[mergedtiles_comparators[i][0]+midpoint] = temp
			mergedtiles[mergedtiles_comparators[i][1]]=mergedtiles_comparators[i][2]
			mergedtiles[mergedtiles_comparators[i][1] + midpoint]=mergedtiles_comparators[i][3]

			#globalmergedtiles_accum.value[mergedtiles_comparators[i][0]]=mergedtiles_comparators[i][2]
			#globalmergedtiles_accum.value[mergedtiles_comparators[i][0] + midpoint]=mergedtiles_comparators[i][3]
			t=threading.Thread(target=assign_compareexchange_multithreaded, args=(mergedtiles_comparators, midpoint, i))
			threads.append(t)
			t.start()
	
	print "bitonic_compare_true(): 2. mergedtiles=",mergedtiles
	#bitoniclock.release()
        #sqlContext=SQLContext(spcon)
        #parents_schema=sqlContext.createDataFrame(k.collect())
        #parents_schema.registerTempTable("Spark_MapReduce_Bitonic")
        #query_results=sqlContext.sql("SELECT * FROM Spark_MapReduce_Bitonic")
        #dict_query_results=dict(query_results.collect())
        #spcon.stop()

'''
#####################################################
Parallelizes comparator in :
        midpoint = int(len(mergedtiles)/2)
        print "bitonic_compare_true(): up= False"
        for i in range(midpoint):
                if (mergedtiles[i] > mergedtiles[i+midpoint]) == False:
                        temp = mergedtiles[i+midpoint]
                        mergedtiles[i+midpoint] = mergedtiles[i]
                        mergedtiles[i] = temp
#####################################################
'''

def bitonic_compare_false(spcon, mergedtiles, start, end):
	print "bitonic_compare_true(): 1. mergedtiles=",mergedtiles
	midpoint = int(len(mergedtiles)/2)
	midpointlist=[]
	#spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
	for l in range(midpoint):
		midpointlist.append(mergedtiles[l+midpoint])

	#tuple: (globalindex, localindex_per_recursion, firsthalfelement, secondhalfelement)
	mergedtilesmidpointlist=zip(range(start,end),range(midpoint),mergedtiles[:midpoint],midpointlist)

        paralleldata = spcon.parallelize(mergedtilesmidpointlist)
        #paralleldata = spcon.parallelize(mergedtilesmidpointlist).cache()
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduceByKey(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduce(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare)
       	#k=paralleldata.map(Foreach_BitonicCompare_False_map).reduceByKey(Foreach_BitonicCompare_False_reduce)
       	k=paralleldata.map(Foreach_BitonicCompare_False_map)

	mergedtiles_comparators=[]
	if k is not None:
		mergedtiles_comparators=k.collect()
		print "bitonic_compare_false() collected:",mergedtiles_comparators
	print "bitonic_compare_false(): 2. mergedtiles: ",mergedtiles
	print "bitonic_compare_false(): mergedtilesmidpointlist: ",mergedtilesmidpointlist
	print "bitonic_compare_false(): mergedtiles_comparators:",mergedtiles_comparators
        
	threads=[]
	for i in range(midpoint):
                if (mergedtiles_comparators[i][4]):
                        #temp = mergedtiles[mergedtiles_comparators[i][0]]
                        #mergedtiles[mergedtiles_comparators[i][0]] = mergedtiles[mergedtiles_comparators[i][0]+midpoint]
                        #mergedtiles[mergedtiles_comparators[i][0]+midpoint] = temp
			mergedtiles[mergedtiles_comparators[i][1]]=mergedtiles_comparators[i][2]
			mergedtiles[mergedtiles_comparators[i][1] + midpoint]=mergedtiles_comparators[i][3]
			print "globalmergedtiles_accum: ",globalmergedtiles_accum.value
			#globalmergedtiles_accum.value[mergedtiles_comparators[i][0]]=mergedtiles_comparators[i][2]
			#globalmergedtiles_accum.value[mergedtiles_comparators[i][0] + midpoint]=mergedtiles_comparators[i][3]
			t=threading.Thread(target=assign_compareexchange_multithreaded, args=(mergedtiles_comparators, midpoint, i))
			threads.append(t)
			t.start()
	
	print "bitonic_compare_false(): mergedtiles=",mergedtiles
	#bitoniclock.release()
        #sqlContext=SQLContext(spcon)
        #parents_schema=sqlContext.createDataFrame(k.collect())
        #parents_schema.registerTempTable("Spark_MapReduce_Bitonic")
        #query_results=sqlContext.sql("SELECT * FROM Spark_MapReduce_Bitonic")
        #dict_query_results=dict(query_results.collect())
        #spcon.stop()

def Foreach_BitonicCompare_True_map(tileelement):
	print "Foreach_BitonicCompare_True(): Comparing mergedtiles[i] and mergedtiles[i+midpoint] ...: tileelement[2]=", tileelement[2], "; tileelement[3]=", tileelement[3]
	if (tileelement[2] > tileelement[3]) == True:
		#This has to be uncommented when accumulator values are mutable in tasks. Presently Spark does not support
		#distributed synchronized mutables.
                #temp = globalmergedtiles_accum.value[tileelement[0]]
                #globalmergedtiles_accum.value[tileelement[0]] = globalmergedtiles_accum.value[tileelement[0]+midpoint]
                #globalmergedtiles_accum.value[tileelement[0]+midpoint] = temp

		return (tileelement[0], tileelement[1], tileelement[3], tileelement[2], True)
	else:
		return (tileelement[0], tileelement[1], tileelement[2], tileelement[3], False)

def Foreach_BitonicCompare_False_map(tileelement):
	print "Foreach_BitonicCompare_False(): Comparing mergedtiles[i] and mergedtiles[i+midpoint] ...: tileelement[2]=", tileelement[2], "; tileelement[3]=", tileelement[3]
	if (tileelement[2] > tileelement[3]) == False:
		#This has to be uncommented when accumulator values are mutable in tasks. Presently Spark does not support
		#distributed synchronized mutables.
                #temp = globalmergedtiles_accum.value[tileelement[0]]
                #globalmergedtiles_accum.value[tileelement[0]] = globalmergedtiles_accum.value[tileelement[0]+midpoint]
                #globalmergedtiles_accum.value[tileelement[0]+midpoint] = temp

		return (tileelement[0], tileelement[1], tileelement[3], tileelement[2], True)
	else:
		return (tileelement[0], tileelement[1], tileelement[2], tileelement[3], False)

def Foreach_BitonicCompare_True_reduce(flag1, flag2):
	return flag1,flag2

def Foreach_BitonicCompare_False_reduce(flag1, flag2):
	return flag1,flag2

def mapFunction_BitonicCompare_True(tileelement):
	print "##################################################################################"
	print "mapFunction_BitonicCompare(): up=",True
	tileelement_index=0
	for k, v in globalmergedtiles.iteritems():
		if v==tileelement:
			tileelement_index=k
	#tileelement_index=globalmergedtiles.inv[tileelement]
	if (globalmergedtiles[tileelement_index] > globalmergedtiles[tileelement_index+midpoint]) == True:
		print "Shuffling mergedtiles and coordinates ..."
		globalmergedtiles[tileelement_index], globalmergedtiles[tileelement_index+midpoint] = globalmergedtiles[tileelement_index+midpoint], globalmergedtiles[tileelement_index]
		globalcoordinates[tileelement_index], globalcoordinates[tileelement_index+midpoint] = globalcoordinates[tileelement_index+midpoint], globalcoordinates[tileelement_index]
	return tileelement_index
	#return (1,tileelement_index)

def mapFunction_BitonicCompare_False(tileelement):
	print "##################################################################################"
	print "mapFunction_BitonicCompare(): up=",False
	tileelement_index=0
	for k, v in globalmergedtiles.iteritems():
		if v==tileelement:
			tileelement_index=k
	#tileelement_index=globalmergedtiles.inv[tileelement]
	if (globalmergedtiles[tileelement_index] > globalmergedtiles[tileelement_index+midpoint]) == False:
		print "Shuffling mergedtiles and coordinates ..."
		globalmergedtiles[tileelement_index], globalmergedtiles[tileelement_index+midpoint] = globalmergedtiles[tileelement_index+midpoint], globalmergedtiles[tileelement_index]
		globalcoordinates[tileelement_index], globalcoordinates[tileelement_index+midpoint] = globalcoordinates[tileelement_index+midpoint], globalcoordinates[tileelement_index]
	return tileelement_index
	#return (1,tileelement_index)

def reduceFunction_BitonicCompare(i, k):
	print "##################################################################################"
	print "reduceFunction_BitonicCompare(): i=",i,"; k=",k
	#if i is not None and k is not None and i < midpoint and k < midpoint:
	#	if (globalmergedtiles[i] > globalmergedtiles[i+midpoint]) == upglobal:
	#		print "Shuffling mergedtiles and coordinates ..."
	#		globalmergedtiles[i], globalmergedtiles[i+midpoint] = globalmergedtiles[i+midpoint], globalmergedtiles[i]
	#		globalcoordinates[i], globalcoordinates[i+midpoint] = globalcoordinates[i+midpoint], globalcoordinates[i]
	#	if (globalmergedtiles[k] > globalmergedtiles[k+midpoint]) == upglobal:
	#		print "Shuffling mergedtiles and coordinates ..."
	#		globalmergedtiles[k], globalmergedtiles[k+midpoint] = globalmergedtiles[k+midpoint], globalmergedtiles[k]
	#		globalcoordinates[k], globalcoordinates[k+midpoint] = globalcoordinates[k+midpoint], globalcoordinates[k]
	#sys.stdout.flush()

def MergedTiles_BitonicSort():
	global globalmergedtiles_accum
	mergedtilesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles","r")
	coordinatesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates","r")
	#mergedtiles=[10, 3, 5, 71, 30, 11, 20, 4, 330, 21, 110, 7, 33, 9, 39, 46]
	#spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
	cnt=1
	#try:
	mergedtileslist=mergedtilesf.read().split("\n")
	print mergedtileslist
	#while cnt <= 16384:
	while cnt <= 256:
		print "cnt=",cnt
		globalmergedtiles[cnt-1]=toint(mergedtileslist[cnt])
		cnt+=1
	#except:
	#	print "Exception:"
	#	pass

	cnt=1
	#try:
	coordinateslist=coordinatesf.read().split("\n")
	#while cnt <= 16384:
	while cnt <= 256:
		globalcoordinates.append(toint(coordinateslist[cnt]))
		cnt+=1
	#except:
	#	print "Exception:"
	#	pass

	print "unsorted=",globalmergedtiles

	globalmergedtiles_accum=spcon.accumulator(globalmergedtiles.values(), VectorAccumulatorParam())
	print "globalmergedtiles_accum: random element = ",globalmergedtiles_accum.value[3]
	sorted=bitonic_sort(spcon, False, globalmergedtiles.values(), 0, len(globalmergedtiles.values())-1)
	print "sorted=",sorted
	print "globalcoordinates=",globalcoordinates
	print "sorted globalmergedtiles accumulator version:  = ",globalmergedtiles_accum.value
        spcon.stop()

if __name__=="__main__":
	bitoniccache=memcache.Client(["127.0.0.1:11211"], debug=1)
	MergedTiles_BitonicSort()
