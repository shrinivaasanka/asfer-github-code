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
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

#Locality Sensitive Hashing based Text Indexing Implementation :
#--------------------------------------------------------------
#A random hash function polynomial of very high degree is created by concatenation of monomials. There are multiple replicated hash tables. 
#Each key is hashed onto each of the hash tables by randomly chosen hash function polynomial. For nearest neighbour query q, all redis_index
#are lookedup with random hash polynomial function,and bucket contents are returned. Redis is a distributed key-value store.

from collections import defaultdict
import jellyfish
import random
import sys
import operator
import pprint
import redis
import ast
import hashlib

class LSHIndex(object):
	def __init__(self,size=10,number_of_functions=5):
		self.datasource="webcrawler"
		self.hashfunctions=[]
		for k in range(1,number_of_functions):
			self.hashfunctions.append("x**" + str(k) + "*" + str(k))
		self.redis_index=redis.StrictRedis(host="localhost",port=6379,db=0)
		self.size=size
		self.randomhashfunctions=[]
		reload(sys)
		sys.setdefaultencoding("utf8")
		self.nearest_neighbours=defaultdict(list)
		self.usemd5hash=True

	def add(self,element):
		self.add_to_table(element)

	def query_nearest_neighbours(self,e):
		hashcode=self.hash(e)
		bucket=self.redis_index.get(hashcode % self.size)
		if bucket != None:
			self.nearest_neighbours=ast.literal_eval(bucket)
                	sorted_nearest_neighbours = sorted(self.nearest_neighbours)
			print "#####################################################################"
			print "Nearest Neighbours for Query - ",e,":"
			pprint.pprint(sorted_nearest_neighbours)
			print "#####################################################################"
			print "Top Nearest Neighbour Ranked for Query - ",e,":"
			pprint.pprint(self.find_nearest_neighbour(e,sorted_nearest_neighbours))

	def find_nearest_neighbour(self, e, neighbours):
		minneighbour=""
		mindistance=100000000000.0
		d=0
		for n in neighbours:
            		d=jellyfish.levenshtein_distance(unicode(e),unicode(n))
			if d < mindistance:
				mindistance=d
				minneighbour=n
		return minneighbour,mindistance 
	
	def add_to_table(self,element):
		hashcode=self.hash(element)
		bucket=self.redis_index.get(hashcode % self.size)
		if bucket==None:
			print "bucket does not exist, creating"
			newbucket=[element]
			self.redis_index.set(hashcode % self.size,newbucket)
		else:
			print "bucket exists, appending"
			newbucket=ast.literal_eval(bucket)
			newbucket.append(element)
			self.redis_index.set(hashcode % self.size,newbucket)

	def hash(self,e):
		hashcode=0
		randomhashfunction=""
		for i in range(1,len(self.hashfunctions)):
			randomhashfunction=randomhashfunction + "+" + self.hashfunctions[random.randint(0,len(self.hashfunctions)-1)]
		randomhashfunction=randomhashfunction[1:]
		if self.usemd5hash==True:
	        	h=hashlib.new("ripemd160")
       			h.update(e)
       			md5hash=int(h.hexdigest(),16)
			hashcode=md5hash
		else:
			sumhash=0
                	for c in e:
                       		 sumhash += ord(c) * (2)
                	x=sumhash
			hashcode=eval(randomhashfunction)
			self.randomhashfunctions.append(randomhashfunction)
                return hashcode

	def print_index(self):
		print "##################################################"
		print "Slot -------------------- Buckets"
		print "##################################################"
		for k in self.redis_index.scan_iter():
			print k,"<==============>",self.redis_index.get(k)

	def delete_index(self):
		self.redis_index.flushdb()

if __name__=="__main__":
	lsh=LSHIndex(50,50)
	crawled=open("../webspider/WebSpider-HTML.out","r")
	for sentence in crawled:
		lsh.add(sentence)
	#lsh.query_nearest_neighbours("Chennai Metropolitan Area Expansion")
	lsh.query_nearest_neighbours(sys.argv[1])
	lsh.print_index()
	#lsh.delete_index()

