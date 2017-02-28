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
#---------------------------------------------------------------------------------------------------------

# Streaming - LogLog counter algorithm - Cardinality Estimation :
#----------------------------------------------------------------
# alpha*no_of_buckets*2^(sigma(buckets)/no_of_buckets) where alpha ~ 0.39701
#
# Each hashed bitstring is split into two substrings [0-k] and [k-n] and there are 2^k estimation buckets. Rank of each hash substring [k-n] is
# computed - number of leading 0s + 1 - which is the cardinality of [k-n] subtring sets. Thus there are two logarithms k and n-k which together # constitute LogLog counting.

import binascii
import hashlib
import math
import Streaming_AbstractGenerator


no_of_buckets=256

def getHash(str):
        h=hashlib.new("ripemd160")
        h.update(str)
	hash=bin(int(h.hexdigest(),16))
	print "hash for string [",str,"] :",hash
	return hash

def getRank(hashstring):
	rank=hashstring.find("1") + 1
	print "rank for hashstring [",hashstring,"] :",rank
	return rank	

estimators={}
for n in xrange(no_of_buckets):
	estimators[n]=0

#The text file is updated by a stream of data
#inputf=open("StreamingData.txt","r")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#inputf=Streaming_AbstractGenerator.StreamAbsGen("file","file")
inputf=Streaming_AbstractGenerator.StreamAbsGen("Spark_Parquet","Spark_Streaming")
for i in inputf:
	print "######################################"
	hashstring=getHash(i)
	hashlen=len(hashstring)
	k=int(math.log(no_of_buckets,2))
	print "k=",k
	bucket=int(hashstring[0:k],2)
	print "bucket=",bucket
	estimators[bucket]=max(estimators[bucket], getRank(hashstring[k+1:]))
	print "estimators[bucket] = ",estimators[bucket]
print estimators


sum=0
for bucket in xrange(no_of_buckets):
	#print estimators[bucket]
	sum = sum + estimators[bucket]

print "sum of buckets : ",sum
cardinality = 0.39701 * no_of_buckets * math.pow(2, float(sum)/float(no_of_buckets))
print "Cardinality of the stream dataset:",cardinality
	
