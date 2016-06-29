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

#This code creates the ThoughtNet HyperGraph Database on Neo4j reading the contents of the thoughtnet edges and hypergraph text file 
#storage. Python interface to Neo4j requires py2neo Neo4j python client.

from py2neo import Node, Relationship, Graph
import ast

g=Graph(bolt=False)
#thoughtnet_hypergraph_file=open("ThoughtNet_Hypergraph.txt","r")
thoughtnet_hypergraph_file=open("ThoughtNet_Hypergraph_Generated.txt","r")
thoughtnet_hypergraph=ast.literal_eval(thoughtnet_hypergraph_file.read())
thoughtnet_edges_file=open("ThoughtNet_Edges.txt","r")
thoughtnet_edges=ast.literal_eval(thoughtnet_edges_file.read())

print "======================================================"
print "ThoughtNet Hypergraph Edges"
print "======================================================"
cnt=0
for e in thoughtnet_edges:
	print "HyperEdge"+str(cnt), ":", e
	cnt+=1	
print "======================================================"
print "ThoughtNet classes "
print "======================================================"
print thoughtnet_hypergraph.keys()
print "========================================================================="
print "ThoughtNet Hypergraph after classification of edges onto previous classes"
print "========================================================================="
print thoughtnet_hypergraph

hypergraph=[]
for n in xrange(len(thoughtnet_edges)):
	hyperedge=[]
	for k,v in thoughtnet_hypergraph.iteritems():
		if n in v:
			hyperedge.append(k)
	hypergraph.append(hyperedge)

tx = g.begin()
neo4j_thoughtnet_nodes={}
neo4j_thoughtnet_relationships=[]
for category in thoughtnet_hypergraph.keys():
	neo4j_thoughtnet_nodes[category]=Node("Thought",name=category)
	tx.create(neo4j_thoughtnet_nodes[category])
tx.commit()

tx = g.begin()
hyperedge_index=0
for e in hypergraph:
	hyperedge_traversal=0
	while hyperedge_traversal < len(e)-1:
		r=Relationship(neo4j_thoughtnet_nodes[e[hyperedge_traversal]],"HyperEdge"+str(hyperedge_index),neo4j_thoughtnet_nodes[e[hyperedge_traversal+1]])
		neo4j_thoughtnet_relationships.append(r)
		tx.create(r)
		hyperedge_traversal+=1
	hyperedge_index+=1

tx.commit()

print "============================================================================"
print "Neo4j ThoughtNet Nodes"
print "============================================================================"
print neo4j_thoughtnet_nodes
print "============================================================================"
print "Neo4j ThoughtNet HyperEdge Relationships"
print "============================================================================"
print neo4j_thoughtnet_relationships	
