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

#Apache Spark RDD MapReduce Transformations script for parsing the number of edges and vertices 
#in SATURN generated .dot graph files for program control flow. Cyclomatic Complexity which is a 
#basic function point estimator for complexity of a software is determined as Edges - Vertices + 2. 

#Example pyspark RDD mapreduce code at: http://www.mccarroll.net/blog/pyspark2/

from pyspark import SparkContext, SparkConf
from GraphMining_GSpan import GSpan
import networkx as nx
from networkx.drawing.nx_pydot import read_dot
from networkx.classes.function import edges
from graphframes import *
from pyspark.sql import SQLContext, Row

GraphXFrames=True

def reduceFunction(value1,value2):
     return value1+value2

def mapFunction(line):
     for i in line.split():
	   return (i,1)

def graph_mining(dotfiles):
	dataset=[]
	for dotf in dotfiles:
		dotnx=nx.Graph(read_dot(dotf))
		dataset.append(dotnx)
	gsp=GSpan(dataset)
	gsp.GraphSet_Projection()	

if __name__=="__main__":
	spcon=SparkContext() 
	sqlcon=SQLContext(spcon)
	input_dot_files=['/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/virgo64-linux-github-code/linux-kernel-extensions/drivers/virgo/saturn_program_analysis/saturn_program_analysis_trees/cfg_read_virgo_kernel_analytics_config.dot','/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/virgo64-linux-github-code/linux-kernel-extensions/drivers/virgo/saturn_program_analysis/saturn_program_analysis_trees/memory_skbuff_h_skb_header_pointer_cfg.dot','/media/Krishna_iResearch_/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/software_analytics/kcachegrind_callgraph_DiscreteHyperbolicFactorization_TileSearch_Optimized.dot']
	if GraphXFrames == True:
		for dot_file in input_dot_files:
			nxg=nx.Graph(read_dot(dot_file))
			nxgnodes=[[]]
			nxgedges=[[]]
			cnt=0
			for n in nxg.nodes():
				cnt += 1
				nxgnodes[0].append((str(cnt),str(n),str(n)))
			for e in nxg.edges():	
				nxgedges[0].append((str(e[0]),str(e[1]),"causes"))
			print "nxgnodes:",nxgnodes
			print "nxgedges:",nxgedges
			ndf=sqlcon.createDataFrame(nxgnodes,["id","name","label"])
			vdf=sqlcon.createDataFrame(nxgedges,["src","dst","relationship"])
			print "ndf:",ndf
			print "vdf:",vdf
			gf=GraphFrame(ndf,vdf)
			print "Indegrees:",gf.inDegrees.show()
			print "Strongly Connected Components:",gf.stronglyConnectedComponents(1)
			print "Triangle count:",gf.triangleCount()
	else:
		for dot_file in input_dot_files:
			input=open(dot_file,'r')
			paralleldata=spcon.parallelize(input.readlines())
			node_edge_lines=paralleldata.filter(lambda nodeedge: "node" in nodeedge)
			k1=node_edge_lines.map(mapFunction).reduceByKey(reduceFunction)
			edgesplusvertices=k1.collect()
	
			edge_lines=paralleldata.filter(lambda nodeedge: "->" in nodeedge)
			k2=edge_lines.map(mapFunction).reduceByKey(reduceFunction)
			vertices=k2.collect()
			print "Edges + Vertices:",edgesplusvertices
			print "Vertices:",vertices
			print "Cyclomatic Complexity: E-V+2 = ",abs(len(edgesplusvertices)-2*len(vertices)+2)
			#l=k.map(lambda src: src).reduce(lambda x,y: x if (x[1] > y[1]) else y)
			#print l
	graph_mining(input_dot_files)
