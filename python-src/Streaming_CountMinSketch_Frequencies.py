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
# CountMinSketch Algorithm for Frequencies in Stream
#----------------------------------------------------
# a matrix of m-rows*n-columns where each value in the stream is hashed to some grid cell on 
# every row (the cell value is incremented). For each row different hash function is applied. 
# Each row is an estimator and minimum of counters in the hashed cells in all rows is an
# estimate of frequency of the value in input stream.

import binascii

def getHash(inp, row):
	hash=int(binascii.hexlify(inp),16)*row % columns 
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

inputf=open("StreamingData.txt","r")
#add and populate sketch
for i in inputf:
	for row in xrange(rows):
		countminsketch[row][getHash(i,row)]+=1	
print countminsketch

inputf=open("StreamingData.txt","r")
#frequencies of each input - minimum of all hashed cells 
for i in inputf:
	maximum=10000000000
	for row in xrange(rows):
		minsketch=min(maximum, getHash(i,row))	
	print "minsketch for [",i,"] :",minsketch
