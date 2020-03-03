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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

#Apache Spark RDD MapReduce Transformations script for parsing the most frequent Source IP in 
#Uncompilcated Firewall logs in /var/log/kern.log. This can be a key-value config in the
#/etc/virgo_kernel_analytics.conf file for VIRGO kernel_analytics module.

#Example pyspark RDD mapreduce code at: http://www.mccarroll.net/blog/pyspark2/

from pyspark import SparkContext, SparkConf

def mapFunction(patternline):
     for i in patternline.split():
          return (i,1)
 
def reduceFunction(value1,value2):
     return value1+value2

def log_mapreducer(logfilename, pattern):
	spcon=SparkContext() 
	input=open(logfilename,'r')
	paralleldata=spcon.parallelize(input.readlines())
	patternlines=paralleldata.filter(lambda patternline: pattern in patternline)
	matches=patternlines.map(mapFunction).reduceByKey(reduceFunction)
	matches_collected=matches.collect()
	print "--------------------------------------------------------------"
	print "log_mapreducer(): pattern [",pattern,"] in [",logfilename,"]"
	print "--------------------------------------------------------------"
	print matches_collected
	return matches_collected
