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
#--------------------------------------------------------------------------------------------------------

from __future__ import division
import pickle
import sys

import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import itertools

def hash_graph(edges):
	hash="Set"
	for e in edges:
		hash+="#"+str(e)
	return hash

def create_all_subgraphs(edges,size_edges):
	all_subgraphs=[]
	for i in xrange(size_edges):
		all_subgraphs += itertools.combinations(edges,i)
	return all_subgraphs

def tree_width(nxg,i):
	maxsize=1000000000
	junction_tree=nx.Graph()
	max_junction_tree_node=junction_tree
	all_subgraphs=create_all_subgraphs(nxg.edges(),i)
	print "All subgraphs:",all_subgraphs
	print "============================================"
	for k in zip(all_subgraphs, all_subgraphs):
		if len(set(k[0]).intersection(set(k[1]))) > 0:
			junction_tree.add_edge(hash_graph(k[0]),hash_graph(k[1]))
			if len(k[0]) < maxsize:
				max_junction_tree_node=k[0]
				maxsize = len(k[0])
			if len(k[1]) < maxsize:
				max_junction_tree_node=k[1]
				maxsize = len(k[1])
	print "============================================"
	print "Junction Tree (with subgraphs of size less than",i," :",junction_tree.edges()
	print "============================================"
	print "Junction Tree Width for subgraphs of size less than",i," - size of largest node set:",maxsize
