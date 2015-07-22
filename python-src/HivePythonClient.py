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

#Python client (modified from https://cwiki.apache.org/confluence/display/Hive/HiveClient with some
#fixes for hive modules imports)
#(and pyhs2 client from https://github.com/BradRuderman/pyhs2)
#for Apache Hive which has the movielens data (one field) as a streaming dataset
#--------------------------
#MovieLens Data Downloaded from: http://files.grouplens.org/datasets/movielens/ml-100k.zip
#and loaded into hive with hive CLI in table stream_data
#This requires hiveserver2 to be started which listens on port 10000
#(The hive schema has been added to repository in bigdata_analytics/)
#--------------------------
#PYTHONPATH has to be exported with path /usr/local/apache-hive-1.0.0-bin/lib/py
#This script is a datasource to be added in Stream Abstract Generator with datastorage in Hive.
#pyhs2 Requires SASL and python-dev packages to be installed.



#client_protocol="thrift"
client_protocol="pyhs2"

if client_protocol=="thrift":
	import sys
	from hive_service import ThriftHive
	from hive_service.ttypes import HiveServerException
	from thrift import Thrift
	from thrift.transport import TSocket
	from thrift.transport import TTransport
	from thrift.protocol import TBinaryProtocol
	try:
		transport = TSocket.TSocket('localhost', 10000)
		print transport
		transport = TTransport.TBufferedTransport(transport)
		print transport
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		print protocol
		client = ThriftHive.Client(protocol)
		print client
		transport.open()
		client.execute("SELECT * FROM stream_data")
		#client.execute("SELECT * FROM stream_dat WHERE alphanum=\"882399156\"")
		#client.execute("DESCRIBE stream_data")
		while (1):
			row = client.fetchOne()
			if (row == None):
				break
			print row
		print client.fetchAll()
		transport.close()
	except Thrift.TException, tx:
		print '%s' % (tx.message)
else:
	import pyhs2
	#pyhs2 client - requires SASL
	conn=pyhs2.connect(host='localhost',
                   port=10000,
                   authMechanism="PLAIN",
	                   user='root',
	                   password='test',
	                   database='default') 
	cur=conn.cursor()
	#Show databases
	print cur.getDatabases()

	#Execute query
	#cur.execute("CREATE TABLE stream_data (alphanum STRING)")
	cur.execute("select * from stream_data")

	#Return column info from query
	print cur.getSchema()

	#Fetch table results
	for i in cur.fetch():
       		 print i

