#--------------------------------------------------------------------------------------------------------
#ASFER - Inference software for Large Datasets
# 
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
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, 
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#HappyBase Python Client for HBase - datasource for Streaming_<algorithm> scripts
#This requires HBase Thrift server to be  started with:
#	bin/hbase-daemon.sh start thrift
#which listens on port 9090


import happybase

connection = happybase.Connection(host='localhost',port=9090,transport='buffered')
table = connection.table('stream_data')
#print table

#HBase table populate code - to be uncommented if rows need to be added
#Presently the table 'stream_data' is populated to 100000+ rows of
#movielens data in textfile movielens_stream.data

index=1
inputf=open("movielens_stream.data","r")
columnname='cf:alphanum'
for i in inputf:
	rowindex="row"+str(index)
	print rowindex,columnname,i
	table.put(rowindex, {columnname:i})	
	index+=1

for data in table.scan():
    print  data  

