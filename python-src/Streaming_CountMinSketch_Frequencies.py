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

#----------------------------------------------------
# CountMinSketch Algorithm for Frequencies in Stream
#----------------------------------------------------
# a matrix of m-rows*n-columns where each value in the stream is hashed to some grid cell on 
# every row (the cell value is incremented). For each row different hash function is applied. 
# Each row is an estimator and minimum of counters in the hashed cells in all rows is an
# estimate of frequency of the value in input stream.

import binascii
import hashlib
import Streaming_AbstractGenerator

def getHash(str):
        h=hashlib.new("ripemd160")
        h.update(str)
        hash=int(h.hexdigest(),16)
        print "hash for string [",str,"] :",hash
        return hash

rows=3
columns=30

countminsketch=[]
rowvector=[]
for n in xrange(columns):
	rowvector.append(0)
for m in xrange(rows):
	countminsketch.append(rowvector)
print countminsketch

#inputf=open("StreamingData.txt","r")
inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#add and populate sketch
for i in inputf:
	for row in xrange(rows):
		countminsketch[row][getHash(i)%columns]+=1	
print countminsketch

#inputf=open("StreamingData.txt","r")
inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
#frequencies of each input - minimum of all hashed cells 
for i in inputf:
	maximum=10000000000
	for row in xrange(rows):
		minsketch=min(maximum, countminsketch[row][getHash(i)%columns])	
		maximum=minsketch
	print "minsketch for [",i,"] :",minsketch
