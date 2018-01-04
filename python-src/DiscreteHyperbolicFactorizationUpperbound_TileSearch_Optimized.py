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


def tilesearch(tileintervalstr):
	global number_to_factorize
	if(len(tileintervalstr) > 1):
		tileinterval=eval(tileintervalstr)
		#print "tilesearch(): tileinterval=",tileinterval
		xleft=tileinterval[0]
		yleft=tileinterval[1]
		xright=tileinterval[2]
		yright=tileinterval[3]
		binary_search_interval(xleft,yleft,xright,yright)

def binary_search_interval(xl,yl,xr,yr):
	intervalmidpoint = int((xr-xl)/2)
	if intervalmidpoint >= 0:
		factorcandidate=(xl+intervalmidpoint)*yl
		#print "factorcandidate = ",factorcandidate
		if factorcandidate == number_to_factorize:
			print "================================================="
			print "Factor is = ", yl 
			print "================================================="
		else:
			if factorcandidate >  number_to_factorize:
			        binary_search_interval(xl, yl, xl+int((xr-xl)/2), yr)
               		else:
               		        binary_search_interval(xl+int((xr-xl)/2)+1, yl, xr, yr)


def SearchTiles_and_Factorize(n): 
	global globalmergedtiles
	global globalcoordinates

	spcon = SparkContext("local[2]","Spark_TileSearch_Optimized")

        tileintervalsf=open("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.tileintervals","r")

        tileintervalslist=tileintervalsf.read().split("\n")
	#print "tileintervalslist=",tileintervalslist
        tileintervalslist_accum=spcon.accumulator(tileintervalslist, VectorAccumulatorParam())

	paralleltileintervals=spcon.parallelize(tileintervalslist)
	paralleltileintervals.foreach(tilesearch)

if __name__=="__main__":
	number_to_factorize=toint(sys.argv[1])
	SearchTiles_and_Factorize(number_to_factorize)

