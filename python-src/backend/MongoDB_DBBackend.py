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

import Streaming_AbstractGenerator
from pymongo.collection import Collection 
from pymongo import MongoClient
import MongoDB_Configuration
import sys
from injector import Module, provides, Injector, inject, singleton

class MongoDB_DBBackend(Module):
	def __init__(self):
		self.database = 'asfer_backend' 
		self.collection = 'asfer_collection'
		self.client=MongoClient('localhost',27017)

	@singleton
	@provides(Collection)
	@inject(configuration=MongoDB_Configuration.Configuration)
	def connect(self,configuration):
		print "MongoDB_DBBackend.connect():",configuration
		self.database = self.client[configuration['database']]
		self.collection = self.database[configuration['collection']]
		inputf=Streaming_AbstractGenerator.StreamAbsGen("USBWWAN_stream","USBWWAN")
		for line in inputf:
			document={ "text": line }
			document_id=self.collection.insert_one(document).inserted_id
		print type(self.collection)
		return self.collection

	def execute_query(self,query=None):	
		print "MongoDB_DBBackend.execute_query():"
		try:
			documents=self.collection.find()
			for document in documents:
				print document 
		except e:
			print "Error :",e

if __name__=="__main__":
	backend=MongoDB_DBBackend()
	backend.connect()
	backend.execute_query("")
