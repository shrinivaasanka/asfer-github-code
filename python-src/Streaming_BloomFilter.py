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

#----------------------------------------------------
#Bloom Filter for Streamed Data:
#------------------------------
#Each element is hashed by multiple hash functions into
#the bitmap and location is set to 1. For querying, the
#query is again hashed as above into multiple locations
#in bitset. If atleast 1 location is 0, then the query is
#not member of set, else if all locations are 1 then the
#query may be in the set.
#----------------------------------------------------

import binascii
import Streaming_AbstractGenerator

def getHash(inp, hashfn_index):
	hash=(int(binascii.hexlify(inp),16)*hashfn_index) % bloomfiltersize 
	#print "hash for [",inp,"] :",hash
	return hash

bloomfiltersize=10000
no_of_hashfns=50
bloom_bitset=[]

for i in xrange(bloomfiltersize):
	bloom_bitset.append(0)


#inputf=open("StreamingData.txt","r")
inputf=Streaming_AbstractGenerator.StreamAbsGen()
for i in inputf:
	for k in xrange(no_of_hashfns):
		bloom_bitset[getHash(i,k)]=1
print bloom_bitset

#sample queries from the input stream and not in input stream

#for file storage
#query=["osoioiiee" ,"73885.399249226" ,"2292179968"]

#for HBase storage
query=["osoioiiee" ,"880130065\x0A", "875310463\x0A"]

queryoutput=1
for t in xrange(len(query)):
	for k in xrange(no_of_hashfns):
		queryoutput = queryoutput & bloom_bitset[getHash(query[t],k)]
		if queryoutput == 0:
			print "Element [",query[t],"] is not member of this set"
			break

	if queryoutput==1:
		print "Element [",query[t],"] may be member of this set"
	queryoutput=1
