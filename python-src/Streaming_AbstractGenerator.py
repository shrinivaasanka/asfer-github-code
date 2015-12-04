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

#An abstraction class that creates an streaming iterable from underlying data which could be
#from any datasource and stored in any bigdata storage(file, Hadoop-HBase, database etc.,)
#This mimicks streaming for the Streaming_<algorithm> scripts. Thus there is a two phase streaming -
#initially the streamed data is populated in storage and streamed later through this generator
#abstracting the source and storage.

import happybase
import pyhs2
from cassandra.cluster import Cluster

class StreamAbsGen(object):
	def __init__(self,data_storage,data_source):
		#For Apache Cassandra, HBase and Hive, code from HivePythonClient.py for HiveServer2,
		#HBasePythonClient.py and CassandraPythonClient.py has been #replicated in __iter__(). 

		#Possible storages:
		#self.data_storage="file"
		#self.data_storage="hive"
		#self.data_storage="hbase"
		#self.data_storage="cassandra"
		#self.data_storage="USBWWAN_stream"
		self.data_storage=data_storage

		#Possible datasources:
		#self.data_source="RZF"
		#self.data_source="movielens"
		#self.data_source="USBWWAN"
		self.data_source=data_source

		if self.data_storage=="file":
			self.inputfile=open("StreamingData.txt")

		if self.data_storage=="USBWWAN_stream":
			self.inputfile=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/SourceForge/usb-md/usb_wwan_modified/testlogs/kern.log.print_buffer_byte.3December2015")

		if self.data_storage=="hbase":
			self.hbase_connection = happybase.Connection(host='localhost',port=9090,transport='buffered')
			self.hbase_table = self.hbase_connection.table('stream_data')
			print "StreamAbsGen:__init__():connected to HBase table"
	
		if self.data_storage=="hive":	
			#pyhs2 client - requires SASL
			self.hive_conn=pyhs2.connect(host='localhost',
       	        		    port=10000,
			            authMechanism="PLAIN",
       		                     user='root',
       		                     password='test',
       		                     database='default')
			self.hive_cur=self.hive_conn.cursor()
			#Show databases
			print self.hive_cur.getDatabases()

			#Execute query
			self.hive_cur.execute("CREATE TABLE stream_data (alphanum STRING)")
			self.hive_cur.execute("select * from stream_data")

			#Return column info from query
			print self.hive_cur.getSchema()
			print "StreamAbsGen:__init__():connected to Hive table"

		if self.data_storage=="cassandra":
			self.cl=Cluster()
			self.session = self.cl.connect('cassandrakeyspace')
			inputf=open('movielens_stream2.data')
			for line in inputf:
		       		linetoks=line.split(' ')
		       		query='INSERT INTO stream_data(row_id,alphanum) VALUES (\''+linetoks[0]+'\',\''+linetoks[1]+'\');'
		       		print query
		       		session.execute(query)
			self.query='SELECT * FROM stream_data'
			self.resultrows=self.session.execute(self.query)
			print "StreamAbsGen:__init__(): connected to Cassandra"
		
	def __iter__(self):
		if self.data_storage=="hbase":
			for key,value in self.hbase_table.scan():
				print "StreamAbsGen(HBase storage): iterator yielding %s" % i
   				yield value['cf:alphanum'] 
		if self.data_storage=="file":
			for i in self.inputfile:
				print "StreamAbsGen(file storage): iterator yielding %s" % i
				yield i
		if self.data_storage=="hive":
		        #Fetch table results
		        for i in self.hive_cur.fetch():
				print "StreamAbsGen(Hive storage): iterator yielding %s" % i[0]
		                yield i[0]
		if self.data_storage=="cassandra":
			for row in self.resultrows:
			        #print row.row_id,' ',row.alphanum
				print "StreamAbsGen(Cassandra storage): iterator yielding %s" % row.alphanum 
				yield row.alphanum
		if self.data_storage=="USBWWAN_stream":
			for i in self.inputfile:
				print "StreamAbsGen(USBWWAN byte stream data): iterator yielding %s" % i
				yield i

		
