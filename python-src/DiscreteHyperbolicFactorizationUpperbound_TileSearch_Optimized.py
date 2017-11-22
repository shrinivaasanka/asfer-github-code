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

number_to_factorize=0

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row 
import operator
import sys
import json
import threading
from complement import toint
import DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark_Tiling

from pyspark.accumulators import AccumulatorParam
class VectorAccumulatorParam(AccumulatorParam):
     def zero(self, value):
         return [0.0] * len(value)
     def addInPlace(self, val1, val2):
         for i in range(len(val1)):
              val1[i] += val2[i]
         return val1

globalmergedtiles_accum=None
globalcoordinates_accum=None

globalmergedtiles=[]
globalcoordinates=[]
cpp_tiling=True

def tilesearch(tilecoordinatepair):
	global number_to_factorize
	if str(tilecoordinatepair[0]) == str(number_to_factorize):
		print "================================================="
		print "Factor is = ", tilecoordinatepair[1]
		print "================================================="

def SearchTiles_and_Factorize(n): 
	global globalmergedtiles
	global globalcoordinates

	spcon = SparkContext("local[2]","Spark_TileSearch_Optimized")

	if cpp_tiling == True:
                mergedtilesf=open("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles","r")
                coordinatesf=open("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.coordinates","r")
                cnt=0
                mergedtileslist=[]
                coordinateslist=[]
                mergedtileslist=mergedtilesf.read().split("\n")
                while cnt < len(mergedtileslist):
                         globalmergedtiles.append(toint(mergedtileslist[cnt]))
                         cnt+=1

                cnt=0
                coordinateslist=coordinatesf.read().split("\n")
                while cnt < len(coordinateslist):
                         globalcoordinates.append(toint(coordinateslist[cnt]))
                         cnt+=1
        else:
                mergedtilesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.mergedtiles","r")
                coordinatesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.coordinates","r")
                globalmergedtiles=json.load(mergedtilesf)
                globalcoordinates=json.load(coordinatesf)

	globalmergedtiles_accum=spcon.accumulator(globalmergedtiles, VectorAccumulatorParam())
        globalcoordinates_accum=spcon.accumulator(globalcoordinates, VectorAccumulatorParam())

	mergedtilescoordinates=zip(globalmergedtiles,globalcoordinates)
	print "mergedtilescoordinates=",mergedtilescoordinates
	paralleltilescoordinates=spcon.parallelize(mergedtilescoordinates)
	factors=paralleltilescoordinates.foreach(tilesearch)
	#dict_k=dict(k.collect())
	#factors = sorted(dict_k.items(),key=operator.itemgetter(1), reverse=True)
	print "SearchTiles_and_Factorize(): factors = ",factors

if __name__=="__main__":
	number_to_factorize=toint(sys.argv[1])
	if cpp_tiling==False:
		DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark_Tiling.hyperbolic_tiling(number_to_factorize)
	SearchTiles_and_Factorize(number_to_factorize)

