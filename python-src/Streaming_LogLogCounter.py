#--------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#
#--------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9789346927, 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch):
#http://sourceforge.net/users/ka_shrinivaasan
#https://www.ohloh.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

# Streaming - LogLog counter algorithm - Cardinality Estimation :
#----------------------------------------------------------------
# alpha*no_of_buckets*2^(sigma(buckets)/no_of_buckets) where alpha ~ 0.39701

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
inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
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
print cardinality
	
