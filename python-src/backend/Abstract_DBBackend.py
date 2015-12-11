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
#-----------------------------------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------
# BigData Backend for Datasets of AsFer Machine Learning Algorithms
#-------------------------------------------------------------------

#An abstraction class for encapsulating access to backends (Both SQL and NoSQL - MySQL, MongoDB, MariaDB etc.,). Product specific
#classes are dependency-injected in here. This is doable without injection also through inheritance.

#Reference : https://pythonhosted.org/injector/ - Google Guice based injector for Python

from injector import Module, provides, Injector, inject, singleton
import MySQLdb
import MySQL_DBBackend
import MySQL_Configuration
import MongoDB_DBBackend
import MongoDB_Configuration
from pymongo.collection import Collection

class Abstract_DBBackend(object):
	@inject(mysqlcon=MySQLdb.Connection)
	@inject(mongodbcollection=Collection)
	def __init__(self,mysqlcon=None,mongodbcollection=None):
		self.mysqlcon = mysqlcon
		self.mongodbcollection = mongodbcollection

	def execute_query(self,query,backend):
		print "Abstract_DBBackend.execute_query():"
		if backend=="MySQL":
			cur = self.mysqlcon.cursor()
			cur.execute(query)
			rows = cur.fetchall()
			for row in rows:
				print row
			return rows
		else:
			print "MongoDB_DBBackend.execute_query():"
			try:
				documents=self.mongodbcollection.find()
				for document in documents:
					print document
			except e:
				print "Error :",e


backend="MongoDB"
if __name__=="__main__":
	if backend=="MySQL":
		mysqldbobj=MySQL_DBBackend.MySQL_DBBackend()
		mysqlconfigobj=MySQL_Configuration.MySQL_Configuration()
		injector=Injector([mysqldbobj,mysqlconfigobj])
		handler=injector.get(Abstract_DBBackend)
		handler.execute_query("SELECT * FROM asfer_table",backend)
	else:
		mongodbobj=MongoDB_DBBackend.MongoDB_DBBackend()
		mongodbconfigobj=MongoDB_Configuration.MongoDB_Configuration()
		injector=Injector([mongodbobj,mongodbconfigobj])
		handler=injector.get(Abstract_DBBackend)
		handler.execute_query("",backend)
