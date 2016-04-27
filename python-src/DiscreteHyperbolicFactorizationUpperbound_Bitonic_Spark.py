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

#Reference for global state modified within local worker node:
#http://fossies.org/linux/spark/python/pyspark/accumulators.py

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
globalcoordinates=[]
bitoniclock=threading.Lock()
upglobal=True

def bitonic_sort(up, mergedtiles):
	upglobal=up
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
		if (up==True):
			bitonic_compare_true(mergedtiles)
		else:
			bitonic_compare_false(mergedtiles)
		firsthalf = bitonic_merge(up, mergedtiles[:int(len(mergedtiles)/2)])
		secondhalf = bitonic_merge(up, mergedtiles[int(len(mergedtiles)/2):])
		print "bitonic_merge: firsthalf: ", firsthalf
		print "bitonic_merge: secondhalf: ", secondhalf
		return firsthalf+secondhalf

'''
#####################################################
Parallelizes:
        midpoint = int(len(mergedtiles)/2)
        print "bitonic_compare_true(): up= True"
        for i in range(midpoint):
                if (mergedtiles[i] > mergedtiles[i+midpoint]) == True:
                        temp = mergedtiles[i+midpoint]
                        mergedtiles[i+midpoint] = mergedtiles[i]
                        mergedtiles[i] = temp
#####################################################
'''

def bitonic_compare_true(mergedtiles):
	#bitoniclock.acquire()
	midpoint = int(len(mergedtiles)/2)
	#bitoniclock.release()
	midpointlist=[]
	spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
	for l in xrange(midpoint):
		midpointlist.append(mergedtiles[l+midpoint])
	mergedtilesmidpointlist=zip(mergedtiles[:midpoint],midpointlist)

        #paralleldata = spcon.parallelize(mergedtilesmidpointlist)
        paralleldata = spcon.parallelize(mergedtilesmidpointlist).cache()
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduceByKey(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduce(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare)
	#bitoniclock.acquire()
       	k=paralleldata.map(Foreach_BitonicCompare_True)

	mergedtiles_comparators=[]
	if k is not None:
		mergedtiles_comparators=k.collect()
		print "bitonic_compare_true() collected:",mergedtiles_comparators
	mergedtilesmidpointlist_new=[]
	cnt=0
	print "bitonic_compare_true(): mergedtiles_comparators:",mergedtiles_comparators
	for comparator in mergedtiles_comparators:
		print "bitonic_compare_true(): comparator=",comparator 
		mergedtilesmidpointtuple=mergedtilesmidpointlist[cnt]
		if comparator:
			mergedtilesmidpointlist_new.append((mergedtilesmidpointtuple[1], mergedtilesmidpointtuple[0]))
		else:
			mergedtilesmidpointlist_new.append((mergedtilesmidpointtuple[0], mergedtilesmidpointtuple[1]))
		cnt+=1
	if len(mergedtilesmidpointlist_new) > 0:
		mergedtilesmidpointlist=mergedtilesmidpointlist_new
		print "mergedtilesmidpointlist=", mergedtilesmidpointlist
		shuffled_firsthalf, shuffled_secondhalf = zip(*mergedtilesmidpointlist)
		mergedtiles=shuffled_firsthalf+shuffled_secondhalf
	
	print "bitonic_compare_true(): mergedtiles=",mergedtiles
	#bitoniclock.release()
        #sqlContext=SQLContext(spcon)
        #parents_schema=sqlContext.createDataFrame(k.collect())
        #parents_schema.registerTempTable("Spark_MapReduce_Bitonic")
        #query_results=sqlContext.sql("SELECT * FROM Spark_MapReduce_Bitonic")
        #dict_query_results=dict(query_results.collect())
        spcon.stop()

'''
#####################################################
Parallelizes:
        midpoint = int(len(mergedtiles)/2)
        print "bitonic_compare_true(): up= False"
        for i in range(midpoint):
                if (mergedtiles[i] > mergedtiles[i+midpoint]) == False:
                        temp = mergedtiles[i+midpoint]
                        mergedtiles[i+midpoint] = mergedtiles[i]
                        mergedtiles[i] = temp
#####################################################
'''

def bitonic_compare_false(mergedtiles):
	#bitoniclock.acquire()
	midpoint = int(len(mergedtiles)/2)
	#bitoniclock.release()
	midpointlist=[]
	spcon = SparkContext("local[2]","Spark_MapReduce_Bitonic")
	for l in xrange(midpoint):
		midpointlist.append(mergedtiles[l+midpoint])
	mergedtilesmidpointlist=zip(mergedtiles[:midpoint],midpointlist)

        #paralleldata = spcon.parallelize(mergedtilesmidpointlist)
        paralleldata = spcon.parallelize(mergedtilesmidpointlist).cache()
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduceByKey(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare_False).reduce(reduceFunction_BitonicCompare)
        #k=paralleldata.map(mapFunction_BitonicCompare)
	#bitoniclock.acquire()
       	k=paralleldata.map(Foreach_BitonicCompare_False)

	mergedtiles_comparators=[]
	if k is not None:
		mergedtiles_comparators=k.collect()
		print "bitonic_compare_true() collected:",mergedtiles_comparators
	mergedtilesmidpointlist_new=[]
	cnt=0
	print "bitonic_compare_false(): mergedtiles_comparators:",mergedtiles_comparators
	for comparator in mergedtiles_comparators:
		print "bitonic_compare_false(): comparator=",comparator 
		mergedtilesmidpointtuple=mergedtilesmidpointlist[cnt]
		if comparator:
			mergedtilesmidpointlist_new.append((mergedtilesmidpointtuple[1], mergedtilesmidpointtuple[0]))
		else:
			mergedtilesmidpointlist_new.append((mergedtilesmidpointtuple[0], mergedtilesmidpointtuple[1]))
		cnt+=1
	if len(mergedtilesmidpointlist_new) > 0:
		mergedtilesmidpointlist=mergedtilesmidpointlist_new
		print "mergedtilesmidpointlist=", mergedtilesmidpointlist
		shuffled_firsthalf, shuffled_secondhalf = zip(*mergedtilesmidpointlist)
		mergedtiles=shuffled_firsthalf+shuffled_secondhalf
	
	print "bitonic_compare_false(): mergedtiles=",mergedtiles
	#bitoniclock.release()
        #sqlContext=SQLContext(spcon)
        #parents_schema=sqlContext.createDataFrame(k.collect())
        #parents_schema.registerTempTable("Spark_MapReduce_Bitonic")
        #query_results=sqlContext.sql("SELECT * FROM Spark_MapReduce_Bitonic")
        #dict_query_results=dict(query_results.collect())
        spcon.stop()

def Foreach_BitonicCompare_True(tileelement):
	global globalmergedtiles
	print "##################################################################################"
	print "Foreach_BitonicCompare_True():"
	midpoint=tileelement[1]
	if (tileelement[0] > tileelement[1]) == True:
		print "Comparing mergedtiles[i] and mergedtiles[i+midpoint] ...: tileelement[0]=", tileelement[0], "; tileelement[1]=", tileelement[1]
		return True
	else:
		return False

def Foreach_BitonicCompare_False(tileelement):
	global globalmergedtiles
	print "##################################################################################"
	print "Foreach_BitonicCompare_False():"
	if (tileelement[0] > tileelement[1]) == False:
		print "Comparing mergedtiles[i] and mergedtiles[i+midpoint] ...: tileelement[0]=", tileelement[0], "; tileelement[1]=", tileelement[1]
		return True
	else:
		return False

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
	mergedtilesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles","r")
	coordinatesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates","r")
	#mergedtiles=[10, 3, 5, 71, 30, 11, 20, 4, 330, 21, 110, 7, 33, 9, 39, 46]
	cnt=1
	#try:
	mergedtileslist=mergedtilesf.read().split("\n")
	print mergedtileslist
	while cnt <= 16384:
	#while cnt <= 128:
		print "cnt=",cnt
		globalmergedtiles[cnt-1]=toint(mergedtileslist[cnt])
		cnt+=1
	#except:
	#	print "Exception:"
	#	pass

	cnt=1
	#try:
	coordinateslist=coordinatesf.read().split("\n")
	while cnt <= 16384:
	#while cnt <= 128:
		globalcoordinates.append(toint(coordinateslist[cnt]))
		cnt+=1
	#except:
	#	print "Exception:"
	#	pass

	print "unsorted=",globalmergedtiles
	upglobal=False
	sorted=bitonic_sort(False, globalmergedtiles.values())
	print "sorted=",globalmergedtiles
	print "globalcoordinates=",globalcoordinates

if __name__=="__main__":
	bitoniccache=memcache.Client(["127.0.0.1:11211"], debug=1)
	MergedTiles_BitonicSort()
