#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

#ConceptNet and WordNet: http://web.media.mit.edu/~havasi/MAS.S60/PNLP10.pdf


import requests
import pprint
from Queue import Queue
from itertools import product
#from rest_client import similar_to_concepts
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path

class ConceptNet5Client:
	def __init__(self):
		print "Init of ConceptNet Client"

	def query_association(self,concept1,concept2):
		conceptjson=requests.get("http://api.conceptnet.io/c/en/"+concept1+"?filter=/c/en/"+concept2).json()
		return conceptjson

	def query_search(self,concept):
		conceptjson=requests.get("http://api.conceptnet.io/search?end=/c/en/"+concept).json()
		return conceptjson

	def query_lookup(self,concept):
		conceptjson=requests.get("http://api.conceptnet.io/c/en/"+concept).json()
		return conceptjson

	def related(self,concept):
		conceptjson=requests.get("http://api.conceptnet.io/related/c/en/"+concept).json()
		return conceptjson

	def query_emotions(self, emoji):
		conceptjson=requests.get("http://api.conceptnet.io/c/mul/"+emoji).json()
		return conceptjson

	def conceptnet_path(self,concept1,concept2):
		conceptjson=requests.get("http://api.conceptnet.io/query?node=/c/en/"+concept1+"&other=/c/en/"+concept2).json()
		return conceptjson

	def conceptnet_least_common_ancestor_distance(self,concept1,concept2):
		pprint.pprint("=======================================================")
		pprint.pprint("Distance and Path between:"+concept1+" and "+concept2)
		pprint.pprint("=======================================================")
		nxg=nx.DiGraph()
		edges=[]
		related1=self.related(concept1)
		related2=self.related(concept2)	
		related1list=[]
		related2list=[]
		for e in related1["related"]:
			if "/en" in e["@id"]:
				related1list.append(e["@id"])
				edges.append((concept1,e["@id"]))
		for e in related2["related"]:
			if "/en" in e["@id"]:
				related2list.append(e["@id"])
				edges.append((e["@id"],concept2))
		#print "related1list: ",related1list
		#print "related2list: ",related2list
		commonancestors=set(related1list).intersection(set(related2list))
		#print "commonancestors: ",commonancestors
		distance=1
		q1=Queue()
		q2=Queue()
		q1.put(set(related1list))
		q2.put(set(related2list))
		while len(commonancestors) == 0 and distance < 1000:
			concept1list=q1.get()
			concept2list=q2.get()
			related1list=related2list=[]
			for c1 in concept1list:
				related1=self.related(c1)
				for e in related1["related"]:
					if "/en" in e["@id"]:
						related1list.append(e["@id"])
						edges.append((c1,e["@id"]))
			for c2 in concept2list:
				related2=self.related(c2) 
				for e in related2["related"]:
					if "/en" in e["@id"]:
						related2list.append(e["@id"])
						edges.append((e["@id"],c2))
			#print "related1list: ",related1list
			#print "related2list: ",related2list
			q1.put(set(related1list))
			q2.put(set(related2list))
			commonancestors=set(related1list).intersection(set(related2list))
			distance = distance + 1
		#print "commonancestors: ",commonancestors
		#print "edges:",edges
		for k,v in edges:
                       	nxg.add_edge(k,v)
		return nxg

if __name__=="__main__":
	conceptnet = ConceptNet5Client()
	print "==================================================="
	print "ConceptNet Emotions "
	print "==================================================="
	conceptjson=conceptnet.query_emotions("😂")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Association"
	print "========================================"
	conceptjson=conceptnet.query_association("chennai","marina")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Search"
	print "========================================"
	conceptjson=conceptnet.query_search("chennai")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Lookup"
	print "========================================"
	conceptjson=conceptnet.query_lookup("chennai")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Related Concepts Ranked Descending by Distance Score"
	print "========================================"
	similarconcepts=conceptnet.related('chennai')
	pprint.pprint("Concepts related to Chennai")
	pprint.pprint(similarconcepts)
	similarconcepts=conceptnet.related('computer science')
	pprint.pprint("Concepts related to computer science")
	pprint.pprint(similarconcepts)
	print "========================================"
	print "ConceptNet Distance - Common Ancestor algorithm"
	print "========================================"
	distance=conceptnet.conceptnet_least_common_ancestor_distance('chennai','delhi')
	sp=shortest_path(distance,'chennai','delhi')
	pprint.pprint("Distance:"+str(len(sp)))
	pprint.pprint("Shortest Path:")
	pprint.pprint(sp)
	distance=conceptnet.conceptnet_least_common_ancestor_distance('fructify','fruitful')
	sp=shortest_path(distance,'fructify','fruitful')
	pprint.pprint("Distance:"+str(len(sp)))
	pprint.pprint("Shortest Path:")
	pprint.pprint(sp)
	distance=conceptnet.conceptnet_least_common_ancestor_distance('medicine','chemical')
	sp=shortest_path(distance,'medicine','chemical')
	pprint.pprint("Distance:"+str(len(sp)))
	pprint.pprint("Shortest Path:")
	pprint.pprint(sp)
	distance=conceptnet.conceptnet_least_common_ancestor_distance('tree','forest')
	sp=shortest_path(distance,'tree','forest')
	pprint.pprint("Distance:"+str(len(sp)))
	pprint.pprint("Shortest Path:")
	pprint.pprint(sp)
	distance=conceptnet.conceptnet_least_common_ancestor_distance('upbraid','anathema')
	sp=shortest_path(distance,'upbraid','anathema')
	pprint.pprint("Distance:"+str(len(sp)))
	pprint.pprint("Shortest Path:")
	pprint.pprint(sp)
	print "========================================="
	print "ConceptNet Path - relations connecting two concepts"
	print "========================================="
	path=conceptnet.conceptnet_path('medicine','chemical')
	pprint.pprint(path)
