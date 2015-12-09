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
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#Apache Spark RDD MapReduce Transformations script for parsing Streamed Data. This can be a key-value config in the
#/etc/virgo_kernel_analytics.conf file for VIRGO kernel_analytics module. Also creates a SparkSQL DataFrame temp table.

#Example pyspark RDD mapreduce code at: http://www.mccarroll.net/blog/pyspark2/

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row 
import operator

def mapFunction(printbufferline):
     #for i in printbufferline.split(":"):
     return (printbufferline,1)
 
def reduceFunction(value1,value2):
     return value1+value2


spcon=SparkContext() 
#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
input=open('StreamingData.txt','r')
paralleldata=spcon.parallelize(input.readlines())
printbuflines=paralleldata.filter(lambda printbufline: printbufline)
k=printbuflines.map(mapFunction).reduceByKey(reduceFunction)
dict_k=dict(k.collect())
s = sorted(dict_k.items(),key=operator.itemgetter(1), reverse=True)
print "Spark MapReduce results:"
print s

############################
sqlContext=SQLContext(spcon)
bytes_stream_schema=sqlContext.createDataFrame(k.collect())
bytes_stream_schema.registerTempTable("USBWWAN_bytes_stream")
query_results=sqlContext.sql("SELECT * FROM USBWWAN_bytes_stream")
dict_query_results=dict(query_results.collect())
print "SparkSQL DataFrame query results:"
print dict_query_results
print "Cardinality of Stream Dataset:"
print len(dict_query_results)
no_of_elements=0
for key,value in dict_k.items():
	no_of_elements += value
print "Number of elements in Stream Dataset:"
print no_of_elements
