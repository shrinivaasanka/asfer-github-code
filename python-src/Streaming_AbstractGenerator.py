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

#An abstraction class that creates an streaming iterable from underlying data which could be
#from any datasource and stored in any bigdata storage(file, Hadoop-HBase, database etc.,)
#This mimicks streaming for the Streaming_<algorithm> scripts. Thus there is a two phase streaming -
#initially the streamed data is populated in storage and streamed later through this generator
#abstracting the source and storage.

import happybase
import pyhs2
from cassandra.cluster import Cluster
from confluent_kafka import Consumer, KafkaError
from pyspark.sql import SparkSession
import json
import socket
from DeepLearning_SchedulerAnalytics import sched_debug_runqueue
from pandas import DataFrame

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
		#self.data_storage="KingCobra"
		#self.data_storage="Spark_Parquet"
		#self.data_storage="AsFer_Encoded_Strings"
		self.data_storage=data_storage

		#Possible datasources:
		#self.data_source="RZF"
		#self.data_source="movielens"
		#self.data_source="USBWWAN"
		#self.data_source="file"
		#self.data_source="KingCobra"
		#self.data_source="Spark_Streaming"
		#self.data_source="NeuronRain"
		self.data_source=data_source

		self.spark=SparkSession.builder.getOrCreate()

		if self.data_storage=="KingCobra":
			self.inputfile=open("/var/log/kingcobra/REQUEST_REPLY.queue")

		if self.data_storage=="AsFer_Encoded_Strings":
			self.inputfile=open("../cpp-src/asfer.enterprise.encstr")

		if self.data_storage=="file":
			self.inputfile=open(data_source,"r")

		if self.data_storage=="USBWWAN_stream":
			self.inputfile=open("../../usb-md-github-code/usb_wwan_modified/testlogs/kern.log.print_buffer_byte")

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

		if self.data_storage=="Kafka":
		        self.c = Consumer({'bootstrap.servers': '0', 'group.id': 'test-consumer-group', 'default.topic.config': {'auto.offset.reset': 'smallest'}})
		        self.c.subscribe(['neuronraindata'])
		if self.data_storage=="Socket_Streaming":
			self.streaming_host=self.data_source
			self.streaming_port=64001
		if self.data_storage=="OperatingSystem":
			self.streaming_host="localhost"
	
	def __iter__(self):
		if self.data_storage=="Spark_Parquet":
			spark_stream_parquet=self.spark.read.parquet("../java-src/bigdata_analytics/spark_streaming/word.parquet")
			#spark_stream_parquet_DS=spark_stream_parquet.rdd.map(lambda row: (row.word))
			spark_stream_parquet_DS=spark_stream_parquet.rdd.filter(lambda row: row.word not in [' ','or','and','who','he','she','whom','well','is','was','were','are','there','where','when','may', 'The', 'the', 'In','in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';','\'s','1','2','3','4','5','6','7','8','9','0'])
			for r in spark_stream_parquet_DS.collect():
				print "StreamiAbsGen(Spark Parquet): iterator yielding %s" % r.word.encode("UTF-8")
				yield r.word.encode("UTF-8")
		if self.data_storage=="KingCobra":
			for i in self.inputfile:
				print "StreamAbsGen(file storage): iterator yielding %s" % i
				yield i
		if self.data_storage=="hbase":
			for key,value in self.hbase_table.scan():
				print "StreamAbsGen(HBase storage): iterator yielding %s" % i
   				yield value['cf:alphanum'] 
		if self.data_storage=="AsFer_Encoded_Strings":
			for i in self.inputfile:
				print "StreamAbsGen(file storage): iterator yielding %s" % i
				yield i
		if self.data_storage=="file":
			for i in self.inputfile:
				words=i.split()
				for word in words:
					print "StreamAbsGen(file storage): iterator yielding %s" % word.strip() 
					yield word.strip() 
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
				#print "StreamAbsGen(USBWWAN byte stream data): iterator yielding %s" % i
				yield i
		if self.data_storage=="Kafka":
			        while True:
				    print "Polling Kafka topic to receive message ..."
			            msg = self.c.poll()
			            if not msg.error() and msg.value():
			                print('Received message: ' , msg.value().encode("utf-8"))
					yield msg
			            else:
			                print(msg.error())
			        self.c.close()
		if self.data_storage=="Socket_Streaming":
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.streaming_host,self.streaming_port))
			print "socket_streaming_client(): host = ",self.streaming_host,"; post=",self.streaming_port
			data=""
			while data != None:
				data=s.recv(100)
				yield data
		if self.data_storage=="OperatingSystem" and self.data_source=="SchedulerRunQueue":
			while True:
				schedrunqueue=sched_debug_runqueue()
				#df=DataFrame(data=schedrunqueue)
				#yield df
				yield schedrunqueue
