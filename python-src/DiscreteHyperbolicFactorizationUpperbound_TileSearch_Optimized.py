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
persisted_tiles=False

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row 
import operator
import sys
import json
import threading
from complement import toint
import DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark_Tiling
import math

from pyspark.accumulators import AccumulatorParam
class VectorAccumulatorParam(AccumulatorParam):
     def zero(self, value):
         return [0.0] * len(value)
     def addInPlace(self, val1, val2):
         for i in range(len(val1)):
              val1[i] += val2[i]
         return val1

####################################################################################################################################
#long double pixelated_hyperbolic_arc(long double n)
#{
#        long double sumoflogs=0.0;
#        long double temp=0.0;
#        long double xtile_start=n/2.0;
#        long double xtile_end=n;
#        long double xtile_sum=n/2.0;
#        long double y=1.0;
#        do
#        {
#                if(log2l(n/(y*(y+1.0))) < 0)
#                        temp = 0.0; // tile has length 1
#                else
#                        temp = log2l(n/(y*(y+1.0)));
#                cout<<"create_tiles("<<(int)n<<","<<(int)xtile_start<<","<<(int)y<<","<<(int)(xtile_end)<<","<<(int)y<<")"<<endl;
#                factor=create_tiles((int)n,(int)(xtile_start)-PADDING,(int)y,(int)(xtile_end)+PADDING,(int)y);
#                xtile_end=xtile_start;
#                xtile_start=xtile_end-(n/((y+1.0)*(y+2.0)));
#                xtile_sum += (n/(y*(y+1.0)));
#                sumoflogs += temp;
#        }
#        while(y++ < (n));
#
#        return sumoflogs;
#}
####################################################################################################################################
# xtile_start = n - y*n/((y+1)*(y+2))
# xtile_end = xtile_start - n/((y+1)*(y+2)) 
# interval/segment = (xtile_start,y,xtile_end,y)
####################################################################################################################################

def tilesearch_nonpersistent(y):
	global number_to_factorize
	n = number_to_factorize
	xtile_start = int(n/y) 
	xtile_end = int(n/(y+1)) 
	#print "tilesearch_nonpersistent(): (",xtile_start,",",y,",",xtile_end,",",y,")"
	binary_search_interval_nonpersistent(xtile_start,y,xtile_end,y)

def binary_search_interval_nonpersistent(xl,yl,xr,yr):
	intervalmidpoint = abs(int((xr-xl)/2))
	#print "intervalmidpoint = ",intervalmidpoint
	if intervalmidpoint > 0:
		factorcandidate=(xl+intervalmidpoint)*yl
		#print "factorcandidate = ",factorcandidate
		if factorcandidate == number_to_factorize or xl*yl == number_to_factorize:
			print "================================================="
			print "Factor is = ", yl 
			print "================================================="
		else:
			if factorcandidate  >  number_to_factorize:
			        binary_search_interval_nonpersistent(xl, yl, xl+intervalmidpoint, yr)
               		else:
               		        binary_search_interval_nonpersistent(xl+intervalmidpoint, yl, xr, yr)

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
		print "factorcandidate = ",factorcandidate
		if factorcandidate == number_to_factorize:
			print "================================================="
			print "Factor is = ", yl 
			print "================================================="
		else:
			if factorcandidate >  number_to_factorize:
			        binary_search_interval(xl, yl, xl+int((xr-xl)/2), yr)
               		else:
               		        binary_search_interval(xl+int((xr-xl)/2)+1, yl, xr, yr)

def hardy_ramanujan_ray_shooting_queries(n):
	#Shoots Ray Queries to Find Approximate Factors by Hardy-Ramanujan Normal Order O(loglogN) for number of factors of N
	#Approximate Factors are y(m) = SquareRoot(N/(tan(m*pi)/2kloglogN)) - 1 , m=1,2,...,kloglogN
	k=2.0
	normal_order_n=int(k*math.log(math.log(n,2),2))
	print "============================================================================================================="
	print "Hardy-Ramanujan Ray Shooting Queries - Approximate Factors of ",n," are:"
	print "============================================================================================================="
	print "normal_order_n(loglogN) = ",normal_order_n
	for m in xrange(1,normal_order_n):
		m_pi=float(m)*math.pi
		tan_m_pi=math.tan(m_pi/(2.0*normal_order_n))
		#print "tan_m_pi=",tan_m_pi
		approximate_factor=float(n)/(tan_m_pi)
		if approximate_factor > 2:
			approximate_factor=math.sqrt(approximate_factor) - 1
			print "approximate_factor(",m,") = ",approximate_factor
	print "============================================================================================================="

def SearchTiles_and_Factorize(n): 
	global globalmergedtiles
	global globalcoordinates

	spcon = SparkContext("local[2]","Spark_TileSearch_Optimized")

	if persisted_tiles == True:
        	tileintervalsf=open("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.tileintervals","r")

        	tileintervalslist=tileintervalsf.read().split("\n")
		#print "tileintervalslist=",tileintervalslist
        	tileintervalslist_accum=spcon.accumulator(tileintervalslist, VectorAccumulatorParam())

		paralleltileintervals=spcon.parallelize(tileintervalslist)
		paralleltileintervals.foreach(tilesearch)
	else:
		hardy_ramanujan_ray_shooting_queries(n)
		spcon.parallelize(xrange(1,n)).foreach(tilesearch_nonpersistent)

if __name__=="__main__":
	number_to_factorize=toint(sys.argv[1])
	SearchTiles_and_Factorize(number_to_factorize)

