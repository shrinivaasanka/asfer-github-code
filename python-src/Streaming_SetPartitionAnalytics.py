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
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
from sympy.solvers.diophantine import diop_general_sum_of_squares
from sympy.abc import a, b, c, d, e, f
from complement import toint

def setpartition_to_tilecover(histogram_partition):
	squaretiles_cover=[]
	for hp in histogram_partition:
		tiles=diop_general_sum_of_squares(a**2 + b**2 + c**2 + d**2 - toint(hp))
		print "square tiles for partition ",hp,":",tiles
		for t in list(tiles)[0]:
			squaretiles_cover.append(t*t)
	print "Lagrange Four Square Tiles Cover reduction of Set Partition ",histogram_partition,":",squaretiles_cover
	return squaretiles_cover

def tocluster(histogram,datasource):
	cluster=[]
	if datasource=="Text":
		for tupl in histogram:
			for x in tupl[1][0]:
				cluster.append(tupl[0])
	if datasource=="Dict":
		print "histogram:",histogram
		for k,v in histogram.iteritems():
			for x in v:
				cluster.append(k)
	print "cluster:",cluster
	return cluster

def adjusted_rand_index():
	#The text file is updated by a stream of data
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("file","StreamingData.txt")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("AsFer_Encoded_Strings","NeuronRain")
	#inputf=Streaming_AbstractGenerator.StreamAbsGen("Socket_Streaming","localhost")
	inputf1=Streaming_AbstractGenerator.StreamAbsGen("TextHistogramPartition",["/var/log/kern.log","/var/log/syslog","/var/log/ufw.log","/var/log/dmesg","/var/log/kern.log"])
	histograms=[]
	for p in inputf1:
		histograms.append(p)
	ari=adjusted_rand_score(tocluster(histograms[0],"Text")[:20000],tocluster(histograms[1],"Text")[:20000])
	print "Adjusted Rand Index of first two histogram set partitions(truncated):",ari
	prev=0
	for n in range(1,len(histograms)):
		truncatedlen=int(min(len(histograms[prev]),len(histograms[n]))*0.9)
		ari=adjusted_rand_score(tocluster(histograms[prev],"Text")[:truncatedlen],tocluster(histograms[n],"Text")[:truncatedlen])
		print "Adjusted Rand Index(truncated):",ari
		ami=adjusted_mutual_info_score(tocluster(histograms[prev],"Text")[:truncatedlen],tocluster(histograms[n],"Text")[:truncatedlen])
		print "Adjusted Mutual Info Index(truncated):",ami
		prev=n
	#################################################################
	histograms=[]
	inputf2=Streaming_AbstractGenerator.StreamAbsGen("DictionaryHistogramPartition","Streaming_SetPartitionAnalytics.txt")
	for p in inputf2:
		histograms.append(p)
	prev=0
	print "histograms:",histograms
	for n in range(1,len(histograms)):
		truncatedlen=int(min(len(histograms[prev]),len(histograms[n]))*0.9)
		ari=adjusted_rand_score(tocluster(histograms[prev],"Dict")[:truncatedlen],tocluster(histograms[n],"Dict")[:truncatedlen])
		print "Adjusted Rand Index (truncated):",ari
		ami=adjusted_mutual_info_score(tocluster(histograms[prev],"Dict")[:truncatedlen],tocluster(histograms[n],"Dict")[:truncatedlen])
		print "Adjusted Mutual Info Index (truncated):",ami
		prev=n


if __name__=="__main__":
	ari=adjusted_rand_index()
	setpartition_to_tilecover([11,12,13,14,15])

