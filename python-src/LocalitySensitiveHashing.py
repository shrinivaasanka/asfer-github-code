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

#Locality Sensitive Hashing Implementation - Nearest Neighbour Search:
#---------------------------------------------------------------------
#A random hash function polynomial of very high degree is created by concatenation of monomials. There are multiple replicated hash tables. 
#Each key is hashed onto each of the hash tables by randomly chosen hash function polynomial. For nearest neighbour query q, all hashtables
#are lookedup with random hash polynomial function,and bucket contents are returned. Shortest distance neighbour amongst them is returned as
#nearest neighbour.

from collections import defaultdict
import jellyfish
import random
import sys
import operator
import pprint

class LSH(object):
	def __init__(self,size=10,number_of_tables=50,number_of_functions=50):
		self.datasource="webcrawler"
		self.hashfunctions=[]
		for k in range(1,number_of_functions):
			self.hashfunctions.append("x**" + str(k) + "*" + str(k))
		self.hashtables=[]
		for i in range(1,number_of_tables):
			self.hashtables.append(defaultdict(list))
		self.size=size
		self.randomhashfunctions=[]
		reload(sys)
		sys.setdefaultencoding("utf8")
		self.nearest_neighbours=defaultdict(list)

	def add(self,element):
		for t in range(0,len(self.hashtables)):
			self.add_to_table(element,t)

	def query_nearest_neighbours(self,e):
		for t in range(0,len(self.hashtables)):
			sumhash = 0
			for c in e:
				#print "sumhash=",sumhash
				sumhash += ord(c) * (t+1)
			x=sumhash
			hashcode=eval(self.randomhashfunctions[t])
			#print "Nearest Neighbours in hashtable ",t,":",self.hashtables[t][hashcode % self.size]	
			nearest_neighbour,nearest_distance=self.find_nearest_neighbour(e,self.hashtables[t][hashcode % self.size])
			print "Nearest Neighbour in hashtable ",t," = ",nearest_neighbour,nearest_distance	
			self.nearest_neighbours[nearest_distance].append(nearest_neighbour)
                sorted_nearest_neighbours = sorted(self.nearest_neighbours.items(),key=operator.itemgetter(0), reverse=False)
		print "#####################################################################"
		print "Top Nearest Neighbours Ranked for Query - ",e,":"
		pprint.pprint(sorted_nearest_neighbours)
		return sorted_nearest_neighbours

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
	

	def add_to_table(self,element,t):
		hashcode=self.hash(element,t) 	
		self.hashtables[t][hashcode % self.size].append(element)

	def hash(self,e,t):
		randomhashfunction=""
		sumhash=0
		for i in range(1,10):
			randomhashfunction=randomhashfunction + "+" + self.hashfunctions[random.randint(0,len(self.hashfunctions)-1)]
		randomhashfunction=randomhashfunction[1:]
		for c in e:
			#print "sumhash=",sumhash
			sumhash += ord(c) * (t+1)
		x=sumhash
		#print "x=",x
		#print "randomhashfunction=",randomhashfunction
		hashcode=eval(randomhashfunction)
		#print "hashcode:",hashcode
		self.randomhashfunctions.append(randomhashfunction)
		return hashcode

	def dump_contents(self):
		for t in range(1,len(self.hashtables)):
			print "##################################################"
			print "Slot -------------------- Buckets"
			print "##################################################"
			for k,v in self.hashtables[t].iteritems():
				print k,"<==============>",	
				for i in v:
					print i,"#",
				print 

if __name__=="__main__":
	lsh=LSH()
	if lsh.datasource=="webcrawler":
		crawled=open("webspider/WebSpider-HTML.out","r")
	else:
		crawled=open("LocalitySensitiveHashing.txt","r")
	for sentence in crawled:
		lsh.add(sentence)
	lsh.query_nearest_neighbours("Chennai Metropolitan Area Expansion")
	lsh.dump_contents()

