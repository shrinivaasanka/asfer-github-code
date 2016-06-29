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

from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlap_Classify
from collections import defaultdict
import ast
import json

thoughtnet_edges_file=open("ThoughtNet_Edges.txt","r")
thoughtnet_hypergraph_file=open("ThoughtNet_Hypergraph_Generated.txt","w")
thoughtnet_hypergraph=defaultdict(list)
edge_number=0
contents=thoughtnet_edges_file.read()
lines=ast.literal_eval(contents)
while edge_number < len(lines):
	print "line=",lines[edge_number]
	classification=RecursiveGlossOverlap_Classify(lines[edge_number])
	for k in range(0,len(classification[0])-1):
		#at present edge numbers are just appended without sorting based on evocation potential
		#assigning evocation potential looks non trivial for each edge for a class than a plain sentiment scoring,
		#because it requires some simulation of human brain EEG electric signal responses on uttering a word.
		#This deficiency has already been mentioned in AstroInferDesign.txt
		thoughtnet_hypergraph[classification[0][k][0]].append(edge_number)
	edge_number += 1
print thoughtnet_hypergraph
json.dump(thoughtnet_hypergraph,thoughtnet_hypergraph_file)
