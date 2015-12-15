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

def create_all_subsets(nodes):
	all_subsets=[]
	size=len(nodes)
	for i in xrange(size):
		for s in itertools.combinations(nodes,i):
			all_subsets.append(s)
	return all_subsets

def tree_width(nxg):
	junction_tree=nx.Graph()
	all_subsets=create_all_subsets(nxg.nodes())
	for k in zip(all_subsets, all_subsets):
		if len(set(k[0]).intersection(set(k[1]))) > 0:
			junction_tree.add_edge(k[0],k[1])
	print "Junction Tree :",junction_tree	
