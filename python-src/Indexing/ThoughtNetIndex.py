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
#---------------------------------------------------------------------------------------------------------

from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlap_Classify
import json

class ThoughtNetIndex(object):
	def __init__(self):
		self.thoughtnet_hypergraph_storage=open("../ThoughtNet/ThoughtNet_Hypergraph_Generated.txt","r")
		self.thoughtnet_hypergraph_edges_storage=open("../ThoughtNet/ThoughtNet_Edges.txt","r")
		self.thoughtnet_hypergraph=json.loads(self.thoughtnet_hypergraph_storage.read())
		self.thoughtnet_hypergraph_edges=json.loads(self.thoughtnet_hypergraph_edges_storage.read())

	def query_index(self,query):
		print "##############################################################"
		print "Querying ThoughtNet Hypergraph Index for query:",query
		print "##############################################################"
		classification=RecursiveGlossOverlap_Classify(query)
                for k in range(0,len(classification[0])-1):
			print "######################################"
                        print "searching class:",classification[0][k][0]
			print "######################################"
			for edges in self.thoughtnet_hypergraph[classification[0][k][0]]:
				print self.thoughtnet_hypergraph_edges[edges].encode('utf-8')

if __name__=="__main__":
	index=ThoughtNetIndex()
	index.query_index("Human Development")
