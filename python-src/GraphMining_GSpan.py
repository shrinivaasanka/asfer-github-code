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
import json

numeric=False

class GSpan(object):
	def __init__(self,graphs):
		self.graph_dataset=graphs
		self.graph_dataset_dfs=[]
		self.graph_dataset_graph2dfscodes={}
		self.dfscodes_minimumsupport={}
		self.graphset_SLeast={}
		self.mined_graphs=[]
		self.Ds=[]
		self.S=[]
		self.minsupport=2.8

	def DepthFirstTrees(self):
		for g in self.graph_dataset:
			vertices=g.nodes()
			dfstree=nx.dfs_tree(g,vertices[0])
			self.graph_dataset_dfs.append(dfstree)

	def Graph2DFSCodes(self):
		for t in self.graph_dataset:
			self.graph_dataset_graph2dfscodes[self.DFSCode(t)]=t
		print self.graph_dataset_graph2dfscodes

	def DFSCode(self,t):
		vertices=t.nodes()
		tdfs=nx.dfs_tree(t,vertices[0])
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
			index=k.find(sstr)
			if index != -1 and index < len(k):
				childedges=self.ParseChildren(k[index:])
				for c in childedges:
					children.append(c)
		return children

	def ParseChildren(self,dfscode):
		children=[]
		edges=dfscode.split("#")
		for e in edges:
			vertices=e.split("-")
			if numeric:
				children.append((int(vertices[0]),int(vertices[1])))
			else:
				children.append((vertices[0],vertices[1]))
		print "ParseChildren():",children
		return children

	def DFSCodesMinimumSupport(self):
		for k,v in self.graph_dataset_graph2dfscodes.items():
			self.dfscodes_minimumsupport[k]=0.2*len(k)
		#print "DFSCodesMinimumSupport():",self.dfscodes_minimumsupport

	def GraphSet_Projection(self):
		self.DepthFirstTrees()
		self.Graph2DFSCodes()
		self.DFSCodesMinimumSupport()
		graphset_SLeast=self.FindSmallestGraphs()
		#self.S=graphset_SLeast
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
		self.iteration += 1
		self.S.append(s)
		if s :
			children=self.FindChildren(s)
		print "children:",children
		for n in xrange(len(children)):
			#print "n:",n
			#print "s:",children[n]
			#print "support:",self.dfscodes_minimumsupport
			try:
				if self.dfscodes_minimumsupport[children[n]] > self.minsupport and self.iteration < 10:
					self.Subgraph_Mining(self.Ds, self.S, children[n])
			except:
				pass

if __name__=="__main__":
	G1=nx.Graph()
	G2=nx.Graph()
	G3=nx.Graph()
	G4=nx.Graph()
	G5=nx.Graph()
	G6=nx.Graph()
	G7=nx.Graph()
	G8=nx.Graph()
	G9=nx.Graph()
	G10=nx.Graph()
	G11=nx.Graph()
	G12=nx.Graph()
	G13=nx.Graph()
	G1.add_edges_from([(1,2),(2,3),(2,4),(1,5),(2,5)])
	G2.add_edges_from([(1,3),(4,3),(5,4),(2,5),(1,5)])
	G3.add_edges_from([(1,4),(5,3),(5,2),(4,5),(1,2)])
	G4.add_edges_from([(1,5),(2,3),(4,2),(2,5),(3,2),(1,6)])
	G5.add_edges_from([(1,4),(2,1),(5,4),(4,1),(4,2),(5,6),(7,1)])
	G6.add_edges_from([(5,6),(7,1)])
	G7.add_edges_from([(5,4),(7,1)])
	G8.add_edges_from([(1,4),(5,6),(7,1)])
	rgof=open("./InterviewAlgorithm/graphmining/RecursiveGlossOverlapGraph.WebSpider-HTML.out.1")
	G9edges=json.load(rgof)
	G9.add_edges_from(G9edges)
	print "G9edges:",G9.edges()
	rgof=open("./InterviewAlgorithm/graphmining/RecursiveGlossOverlapGraph.WebSpider-HTML.out.2")
	G10edges=json.load(rgof)
	G10.add_edges_from(G10edges)
	print "G10edges:",G10.edges()
	rgof=open("./InterviewAlgorithm/graphmining/RecursiveGlossOverlapGraph.WebSpider-HTML.out.3")
	G11edges=json.load(rgof)
	G11.add_edges_from(G11edges)
	print "G11edges:",G11.edges()
	rgof=open("./InterviewAlgorithm/graphmining/RecursiveGlossOverlapGraph.WebSpider-HTML.out.4")
	G12edges=json.load(rgof)
	G12.add_edges_from(G12edges)
	print "G11edges:",G12.edges()
	rgof=open("./InterviewAlgorithm/graphmining/RecursiveGlossOverlapGraph.WebSpider-HTML.out.5")
	G13edges=json.load(rgof)
	G13.add_edges_from(G13edges)
	print "G13edges:",G13.edges()
	#dataset=[G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,G13]
	dataset=[G12,G13]
	gspan=GSpan(dataset)
	gspan.GraphSet_Projection()	
