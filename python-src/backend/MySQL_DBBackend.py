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


import MySQLdb 
import MySQL_Configuration
import sys
from injector import Module, provides, Injector, inject, singleton

class MySQL_DBBackend(Module):
	def __init__(self):
		self.host = 'localhost'
		self.user = 'asferuser' 
		self.password = 'asferuser' 
		self.database = 'asfer_backend' 

	@singleton
	@provides(MySQLdb.Connection)
	@inject(configuration=MySQL_Configuration.Configuration)
	def connect(self,configuration):
		print configuration
		self.con = MySQLdb.connect(configuration['host'],configuration['user'],configuration['password'],configuration['database'])
		print type(self.con)
		return self.con

	def execute_query(self,query):	
		print "MySQL_DBBackend.execute_query():"
		try:
			cur = self.con.cursor()
			cur.execute(query)
			rows = cur.fetchall()
			for row in rows:
				print row
		except e:
			print "Error :",e
		finally: 
			self.con.close()

#mysqldb = MySQL_DBBackend()
#mysqldb.connect()
#mysqldb.execute_query("SELECT * FROM asfer_table")
