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

from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlap_Classify
from RecursiveLambdaFunctionGrowth import RecursiveLambdaFunctionGrowth
from collections import defaultdict
import ast
import json
import operator
import SentimentAnalyzer

Merit_Criterion="GraphTensorNeuronNetworkIntrinsicMerit"

def sort_evocative_sentiments_per_class(edges, edge_senti_dict):
	edge_senti_subset_dict={}
	for e in edges: 
		edge_senti_subset_dict[e]=edge_senti_dict[e]
        sorted_edge_senti=sorted(edge_senti_subset_dict.items(),key=operator.itemgetter(1),reverse=True)
	sorted_edge_senti_first=[x for x,y in sorted_edge_senti]
	return sorted_edge_senti_first

def nett_sentiment(senti_tuple):
	return senti_tuple[0] - senti_tuple[1] + senti_tuple[2]

if __name__=="__main__":
	edge_sentiment_dict=defaultdict()
	#recommendersystems_edges_file=open("RecommenderSystems_Edges.txt","r")
	#recommendersystems_edges_file=open("RecommenderSystems_Edges.shoppingcart.txt","r")
	#recommendersystems_edges_file=open("RecommenderSystems_Edges.shoppingcart2.txt","r")
	recommendersystems_edges_file=open("RecommenderSystems_Edges.shoppingcart3.txt","r")
	#recommendersystems_hypergraph_file=open("RecommenderSystems_Hypergraph_Generated.txt","w")
	#recommendersystems_hypergraph_file=open("RecommenderSystems_Hypergraph_Generated.shoppingcart.txt","w")
	#recommendersystems_hypergraph_file=open("RecommenderSystems_Hypergraph_Generated.shoppingcart2.txt","w")
	recommendersystems_hypergraph_file=open("RecommenderSystems_Hypergraph_Generated.shoppingcart3.txt","w")
	recommendersystems_hypergraph=defaultdict(list)
	recommendersystems_hypergraph_sorted=defaultdict(list)
	edge_number=0
	contents=recommendersystems_edges_file.read()
	lines=ast.literal_eval(contents)
	while edge_number < len(lines):
		print "line=",lines[edge_number]
		if Merit_Criterion == "Sentiment": 
			edge_sentiment_dict[edge_number]=nett_sentiment(SentimentAnalyzer.SentimentAnalysis_SentiWordNet(lines[edge_number]))
		if Merit_Criterion == "GraphTensorNeuronNetworkIntrinsicMerit":
                        recursivelambdafunctiongrowth=RecursiveLambdaFunctionGrowth()
                        intrinsic_merit_dict=recursivelambdafunctiongrowth.grow_lambda_function3(lines[edge_number])
                        edge_sentiment_dict[edge_number]=intrinsic_merit_dict["maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit"]

		classification=RecursiveGlossOverlap_Classify(lines[edge_number])
		for k in range(0,len(classification[0])-1):
			#at present edge numbers are just appended by sorting based on sentiment scoring per hyperedge. 
			#assigning evocation potential looks non trivial for each edge for a class than a plain sentiment scoring,
			#because it requires some simulation of human brain EEG electric signal responses on uttering a word.
			#This deficiency has already been mentioned in AstroInferDesign.txt
			recommendersystems_hypergraph[classification[0][k][0]].append(edge_number)
		edge_number += 1

	for k,v in recommendersystems_hypergraph.iteritems():
		sorted_edge_senti_per_class=sort_evocative_sentiments_per_class(v, edge_sentiment_dict)
		recommendersystems_hypergraph_sorted[k]=sorted_edge_senti_per_class

	print recommendersystems_hypergraph_sorted
	json.dump(recommendersystems_hypergraph_sorted,recommendersystems_hypergraph_file)
	print "edge_sentiment_dict = ",edge_sentiment_dict
