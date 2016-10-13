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
#--------------------------------------------------------------------------------------------------------

#GSpan Algorithm implementation for mining subgraph patterns in Graph Datasets
#Reference: http://www.cs.ucsb.edu/~xyan/papers/gSpan-short.pdf

import networkx as nx
import operator
from collections import defaultdict

class GSpan(object):
	def __init__(self,graphs):
		self.graph_dataset=graphs
		self.graph_dataset_dfs=[]
		self.graph_dataset_graph2dfscodes={}
		self.graphset_SLeast={}
		self.mined_graphs=[]
		self.Ds=[]
		self.S=[]

	def DepthFirstTrees(self):
		for g in self.graph_dataset:
			dfstree=nx.dfs_tree(g,1)	
			self.graph_dataset_dfs.append(dfstree)

	def Graph2DFSCodes(self):
		for t in self.graph_dataset:
			self.graph_dataset_graph2dfscodes[self.DFSCode(t)]=t
		print self.graph_dataset_graph2dfscodes

	def DFSCode(self,t):
		tdfs=nx.dfs_tree(t,1)
		sorted_edges=sorted(tdfs.edges(),key=operator.itemgetter(0), reverse=False)
		dfscode=""
		for s in sorted_edges:
			dfscode = dfscode + "#" + str(s[0]) + "-" + str(s[1])
		return dfscode

	def FindSmallestGraphs(self):
		print self.graph_dataset_graph2dfscodes
		sortedbydfscode=sorted(self.graph_dataset_graph2dfscodes.items(), key=operator.itemgetter(0), reverse=False)
		print "sortedbydfscode:",sortedbydfscode
		smallest=[]
		for k,v in sortedbydfscode[:2]:
			smallest.append(v)
		print "smallest:",smallest
		return smallest

	def SearchGraphs(self,e):
		containinggraphs=[]
		for g in self.graph_dataset:
			for edge in g.edges():
				if edge[0]==e[0] and edge[1]==e[1]:
					containinggraphs.append(g)
		return containinggraphs

	def FindChildren(self,s):
		children=[]
		sstr=str(s[0])+"-"+str(s[1])
		for k,v in self.graph_dataset_graph2dfscodes.items():
			if k.find(sstr) != -1 :
				children.append(self.DFSCode(v))
		return children

	def GraphSet_Projection(self):
		self.DepthFirstTrees()
		self.Graph2DFSCodes()
		graphset_SLeast=self.FindSmallestGraphs()
		self.S=graphset_SLeast
		for n in xrange(len(graphset_SLeast)):
			g=graphset_SLeast[n]	
			for e in g.edges():
				print "e:",e
				s=e
				self.Ds=self.SearchGraphs(e)
				self.iteration = 0
				self.Subgraph_Mining(self.graph_dataset, self.S, s)
			for r in graphset_SLeast:
				try:
					if len(self.graph_dataset) > 0:
						self.graph_dataset.remove(r)
				except:
					pass
		print "Mined Frequent Subgraph Edges:",set(self.S)

	def Subgraph_Mining(self,dataset,S,s):
		print "Subgraph_Mining:",dataset
		self.S.append(s)
		if s :
			children=self.FindChildren(s)
		print "children:",children
		for n in xrange(len(children)):
			print "n:",n
			print "s:",children[n]
			if self.iteration < 10:
				self.Subgraph_Mining(self.Ds, self.S, children[n])
		self.iteration += 1

if __name__=="__main__":
	G1=nx.Graph()
	G2=nx.Graph()
	G3=nx.Graph()
	G4=nx.Graph()
	G5=nx.Graph()
	G1.add_edges_from([(1,2),(2,3),(2,4),(1,5),(2,5)])
	G2.add_edges_from([(1,3),(4,3),(5,4),(2,5),(1,5)])
	G3.add_edges_from([(1,4),(5,3),(5,2),(4,5),(1,2)])
	G4.add_edges_from([(1,5),(2,3),(4,2),(2,5),(3,2),(1,6)])
	G5.add_edges_from([(1,4),(2,1),(5,4),(4,1),(4,2),(5,6),(7,1)])
	dataset=[G1,G2,G3,G4,G5]
	gspan=GSpan(dataset)
	gspan.GraphSet_Projection()	
			 
