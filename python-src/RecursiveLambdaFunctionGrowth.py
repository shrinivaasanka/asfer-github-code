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


from bintrees import AVLTree
from bintrees import BinaryTree
import random
import networkx as nx
from itertools import product
import RecursiveGlossOverlap_Classifier
from nltk.corpus import wordnet as wn
import math
import operator
import difflib
from ConceptNet5Client import ConceptNet5Client
from WordNetPath import path_between
import SentimentAnalyzer
from networkx.drawing.nx_pydot import write_dot

#Graph Tensor Neuron Network (Graph Neural Network + Tensor Neuron) evaluation of lambda composition tree of a random walk of
#Recursive Gloss Overlap graph of a text

class RecursiveLambdaFunctionGrowth(object):
	def __init__(self):
		self.lambda_comp_tree=AVLTree()
		self.index_tree=BinaryTree()
		self.word_list=[]
		self.word_dict={}
		self.index_dict={}
		self.index_list=[]
		self.lambda_expression=[]
		self.lambda_composition=""
		self.graph_tensor_neuron_network_intrinsic_merit=1.0
		self.entropy=10000000000.0
		self.conceptnet=ConceptNet5Client()
		#self.Similarity="ConceptNet"
		self.Similarity="WordNet"
		self.ClosedPaths=True

	def get_next_tree_traversal_id(self,x,y):
		if y-x == 1 or x-y == 1:
			return 1 
		print "x,y:",x,y
		self.index_list.append((x+y)/2)
		self.get_next_tree_traversal_id(x,(x+y)/2)
		self.get_next_tree_traversal_id((x+y)/2,y)

	def build_lambda_expression(self,key,value):
		#print value,
		self.lambda_expression.append(value)

	def build_lambda_comp_tree(self,k,v):
		if k < len(self.word_list):
			self.word_dict[k]=self.word_list[k]

	def return_next(self,k,v):
		return (k,v)

	def grow_lambda_function2(self, wordlist):
		self.word_list=wordlist
		self.word_dict={}
		
		cnt=0
		while cnt < len(self.word_list):
			self.index_dict[cnt]=cnt
			cnt+=1

		self.index_tree=BinaryTree(self.index_dict)
		self.index_tree.foreach(self.build_lambda_comp_tree,0)
		
		self.lambda_comp_tree=AVLTree(self.word_dict)
		print "==========================================================================="
		print "Lambda Composition AVL Tree (inorder traversed) is the original text itself:"
		print "==========================================================================="
		self.lambda_expression=[]
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 0)
		print self.lambda_expression
		print "==========================================================================="
		print "Lambda Composition AVL Tree (postorder traversed - Postfix expression):"
		print "Every parenthesis has two operands,operated by function outside:"
		print "==============================================================="
		self.lambda_expression=[]
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 1)
		self.lambda_composition=[]
		cnt=0

		per_random_walk_graph_tensor_neuron_network_intrinsic_merit = 0 
		#recursively evaluate the Graph Tensor Neuron Network for random walk composition tree bottom up as Graph Neural Network
		#having Tensor Neuron activations for each subtree.
		while len(self.lambda_expression) > 2 :
			operand2=self.lambda_expression.pop()
			operand1=self.lambda_expression.pop()
			function=self.lambda_expression.pop()
			subtree_graph_tensor_neuron_network_wght = self.subtree_graph_tensor_neuron_network_weight(operand1, function, operand2)
			self.graph_tensor_neuron_network_intrinsic_merit += subtree_graph_tensor_neuron_network_wght
			per_random_walk_graph_tensor_neuron_network_intrinsic_merit += subtree_graph_tensor_neuron_network_wght
			self.lambda_composition="("+function+"("+operand1+","+operand2+"))" 
			self.lambda_expression.append(self.lambda_composition)
			cnt+=1
		if len(self.lambda_expression) > 1:
			return (self.lambda_expression[0] + "("+self.lambda_expression[1]+")", per_random_walk_graph_tensor_neuron_network_intrinsic_merit)
		else:
			return (self.lambda_expression[0], per_random_walk_graph_tensor_neuron_network_intrinsic_merit)
			
	def grow_lambda_function1(self):
		text=open("RecursiveLambdaFunctionGrowth.txt","r")
		word_dict={}
		index_dict={}
		words_evaluated=0
		word_list=text.read().split()

		for cnt in range(1,len(word_list)):
			index_dict[cnt-1] = len(word_list)/cnt

		index_tree=AVLTree(index_dict)
		print "Index AVL Tree:", repr(index_tree)
		#index_tree.foreach(print_node,1)
	
		try:
			while words_evaluated < len(word_list):
				#word_dict[words_evaluated]=word_list[random.randint(0,len(word_list)-1)]
				#print word_list[index_tree.pop_min()[0]]
				word_dict[words_evaluated]=word_list[index_tree.pop_min()[0]]
				words_evaluated+=1
		except:
			pass
	
		self.lambda_comp_tree=AVLTree(word_dict)
		print "Lambda Composition AVL Tree:"
		self.lambda_comp_tree.foreach(print_node)
		iteration=0
		while iteration < len(word_list):
			k=self.lambda_comp_tree.get(iteration)
			print "k:",k
			try:
				prev=self.lambda_comp_tree.prev_key(iteration)
				prevk=self.lambda_comp_tree.get(prev)
				print "prevk:",prevk
			except:
				pass
			try:
				succ=self.lambda_comp_tree.succ_key(iteration)
				succk=self.lambda_comp_tree.get(succ)
				print "succk:",succk
			except:
				pass
			iteration+=1

	def get_tensor_neuron_potential_for_relation(self,synset_vertex,synset_r):
		smt=0.0
		similarity=0.0
		for s1, s2 in product(synset_vertex, synset_r):
			if self.Similarity=="WordNet":
				smt=wn.wup_similarity(s1,s2)
			if self.Similarity=="ConceptNet":
				s1_lemma_names=s1.lemma_names()
				s2_lemma_names=s2.lemma_names()
				smt=self.conceptnet.conceptnet_distance(s1_lemma_names[0], s2_lemma_names[0])
			#print "similarity=",smt
			if smt > similarity and smt != 1.0:
				similarity = float(smt)
		return similarity

	def subtree_graph_tensor_neuron_network_weight(self, e1, r, e2):
		#relation_tensor_neuron_potential=self.get_tensor_neuron_potential_for_relation(r)
		if e1[0]=="(":
			e1_parsed=e1.split("(")
			#print "operand1:", e1_parsed[1]
			synset_e1 = wn.synsets(e1_parsed[1])
		else:
			synset_e1 = wn.synsets(e1)
			#print "operand1:", e1

		#print "Relation: ",r
		synset_r = wn.synsets(r)
		if e2[0]=="(":
			e2_parsed=e2.split("(")
			#print "operand2:", e2_parsed[1]
			synset_e2 = wn.synsets(e2_parsed[1])
		else:
			#print "operand2:", e2
			synset_e2 = wn.synsets(e2)

		similarity1 = 0.0
		similarity2 = 0.0

		#Children of each subtree are the Tensor Neuron inputs to the subtree root
		#Each subtree is evaluated as a graph neural network with weights for
		#each neural input to the subtree root. WordNet similarity is computed
		#between each child and subtree root and is presently assumed as Tensor Neuron
		#relation potential for the lack of better metric to measure word-word EEG potential.
		#If a dataset for tensor neuron potential
		#is available, it has to to be looked-up and numeric
		#potential has to be returned from here.

		similarity1 = self.get_tensor_neuron_potential_for_relation(synset_e1,synset_r)
		similarity2 = self.get_tensor_neuron_potential_for_relation(synset_e2,synset_r)

		if similarity1 == 0.0:
			similarity1 = 1.0
		if similarity2 == 0.0:
			similarity2 = 1.0

		weight1=0.5
		weight2=0.5
		bias=0.1

		#Finally a neuron activation function (simple 1-dimensional tensor) is computed and
		#returned to the subtree root for next level.
		return (weight1*similarity1 + weight2*similarity2 + bias)

	def randomwalk_lambda_function_composition_tree(self,randomwalk):
		randomwalk_lambdacomposition=self.grow_lambda_function2(randomwalk)
		return randomwalk_lambdacomposition

	def create_summary(self,text,corenumber=3,pathsimilarity=0.8,graphtraversedsummary=False,shortestpath=True):
		if graphtraversedsummary==True:
			definitiongraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(text)
			#This has to be replaced by a Hypergraph Transversal but NetworkX does not have Hypergraphs yet.
			#Hence approximating the transversal with a k-core which is the Graph counterpart of
			#Hypergraph transversal. Other measures create a summary too : Vertex Cover is NP-hard while Edge Cover is Polynomial Time.
			richclubcoeff=nx.rich_club_coefficient(definitiongraph.to_undirected())
			print "Rich Club Coefficient of the Recursive Gloss Overlap Definition Graph:",richclubcoeff
			kcore=nx.k_core(definitiongraph,corenumber)
			print "Text Summarized by k-core(subgraph having vertices of degree atleast k) on the Recursive Gloss Overlap graph:"
			print "=========================="
			print "Dense subgraph edges:"
			print "=========================="
			print kcore.edges()
			print "=========================="
			if shortestpath == False:
				for e in kcore.edges():
					for s1 in wn.synsets(e[0]):
						for s2 in wn.synsets(e[1]):
								if s1.path_similarity(s2) > pathsimilarity:
									lowestcommonhypernyms=s1.lowest_common_hypernyms(s2)
									for l in lowestcommonhypernyms:
										for ln in l.lemma_names():
											print e[0]," and ",e[1]," are ",ln,".",
			else:
				#Following is the slightly modified version of shortest_path_distance() function
				#in NLTK wordnet - traverses the synset path between 2 synsets instead of distance
				summary={}
				intermediates=[]
				for e in kcore.edges():
					for s1 in wn.synsets(e[0]):
						for s2 in wn.synsets(e[1]):
							s1dict = s1._shortest_hypernym_paths(False)
							s2dict = s2._shortest_hypernym_paths(False)
							s2dictkeys=s2dict.keys()
							for s,d in s1dict.iteritems():
								if s in s2dictkeys:
									slemmanames=s.lemma_names()
									if slemmanames[0] not in intermediates:
										intermediates.append(slemmanames[0])
					if len(intermediates) > 3:
						sentence1=e[0] + " is a " + intermediates[0]
						summary[sentence1]=self.relevance_to_text(sentence1,text) 
						for i in xrange(len(intermediates)-2):
							sentence2= intermediates[i] + " is a " + intermediates[i+1] + "."
							if sentence2 not in summary:
								summary[sentence2]=self.relevance_to_text(sentence2,text)
						sentence3=intermediates[len(intermediates)-1] + " is a " + e[1]
						summary[sentence3]=self.relevance_to_text(sentence3,text)
						intermediates=[]
				sorted_summary=sorted(summary,key=operator.itemgetter(1), reverse=True)
				print "==================================================================="
				print "Sorted summary created from k-core dense subgraph of text RGO"
				print "==================================================================="
				for s in sorted_summary:
					print s,
			return (sorted_summary, len(sorted_summary))
		else:
			definitiongraph_merit=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(text)
			definitiongraph=definitiongraph_merit[0]
			richclubcoeff=nx.rich_club_coefficient(definitiongraph.to_undirected(),normalized=False)
			print "Rich Club Coefficient of the Recursive Gloss Overlap Definition Graph:",richclubcoeff
			textsentences=text.split(".")
			lensummary=0
			summary=[]
			definitiongraphclasses=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(text)
			print "Text Summarized based on the Recursive Gloss Overlap graph classes the text belongs to:"
			prominentclasses=int(len(definitiongraphclasses[0])/2)
			print "Total number of classes:",len(definitiongraphclasses[0])
			print "Number of prominent classes:",prominentclasses
			for c in definitiongraphclasses[0][:prominentclasses]:
				if len(summary) > len(textsentences) * 0.5:
					return (summary,lensummary)
				for s in textsentences:
					classsynsets=wn.synsets(c[0])
					for classsynset in classsynsets:
						if self.relevance_to_text(classsynset.definition(), s) > 0.41:
							if s not in summary:
								summary.append(s)
								lensummary += len(s)
								print s,
			return (summary,lensummary)

	def relevance_to_text(self, sentence, text):
		#Ratcliff/Obershelp gestalt string pattern matching 
		textset=set(text.split("."))
		relevancescore=0.0
		for t in textset:
			rs=difflib.SequenceMatcher(None,sentence,t).ratio()
			relevancescore=max(rs,relevancescore)
		return relevancescore 

	def instrument_relations(self, rw_words_list):
		word_list_len=len(rw_words_list)
		instrumented_rw_words_list=[]
		if word_list_len==2:
			path=path_between(rw_words_list[0], rw_words_list[1])
			for p in path:
				instrumented_rw_words_list.append(p)
		else:
			for n in range(0,word_list_len-2): 
				path=path_between(rw_words_list[n], rw_words_list[n+1])
				for p in path:
					instrumented_rw_words_list.append(p)
		if len(instrumented_rw_words_list) > 0:
			return instrumented_rw_words_list
		else:
			return rw_words_list

	def grow_lambda_function3(self,text,level=3):
		stpairs=[]
		maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit=("",0.0)
		definitiongraph_merit=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(text,level)
		definitiongraph=definitiongraph_merit[0]
		sentiment=SentimentAnalyzer.SentimentAnalysis_RGO_Belief_Propagation_MarkovRandomFields(definitiongraph)
		apsp=nx.all_pairs_shortest_path(definitiongraph)
		for a in definitiongraph.nodes():
			for b in definitiongraph.nodes():
				stpairs.append((a,b))
		rw_ct=""
		if self.ClosedPaths==False:
			for k,v in stpairs:
				try:
					print "==================================================================="
					print "Random Walk between :",k," and ",v,":",apsp[k][v]
					instrumented_apspkv=self.instrument_relations(apsp[k][v])
					rw_ct=self.randomwalk_lambda_function_composition_tree(instrumented_apspkv)
					print "Random Walk Composition Tree for walk between :",k," and ",v,":",rw_ct
					print "maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit=",maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit
					print "==================================================================="
					if rw_ct[1] > maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit[1]:
						maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit=rw_ct
				except KeyError:
					pass
				rw_ct=""
		if self.ClosedPaths==True:
			allsimplecycles=nx.simple_cycles(definitiongraph)
			#allsimplecycles=nx.cycle_basis(definitiongraph)
			number_of_cycles=0
			for cycle in allsimplecycles:
				number_of_cycles += 1
				if number_of_cycles > 500:
					break
				try:
					print "==================================================================="
					print "Cycle :",cycle
					instrumented_cycle=self.instrument_relations(cycle)
					print "instrumented_cycle:",instrumented_cycle
					rw_ct=self.randomwalk_lambda_function_composition_tree(instrumented_cycle)
					print "Cycle Composition Tree for this cycle :",rw_ct
					print "maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit=",maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit
					print "==================================================================="
					if rw_ct[1] > maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit[1]:
						maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit=rw_ct
				except KeyError:
					pass
				rw_ct=""
		intrinsic_merit_dict={}
		print "grow_lambda_function3(): Graph Tensor Neuron Network Intrinsic Merit for this text:",self.graph_tensor_neuron_network_intrinsic_merit

		self.korner_entropy(definitiongraph)
		print "grow_lambda_function3(): Korner Entropy Intrinsic Merit for this text:",self.entropy

		density = self.density(definitiongraph)
		print "grow_lambda_function3(): Graph Density (Regularity Lemma):",density

		bose_einstein_intrinsic_fitness=self.bose_einstein_intrinsic_fitness(definitiongraph)
		print "grow_lambda_function3(): Bose-Einstein Intrinsic Fitness:",bose_einstein_intrinsic_fitness

		print "grow_lambda_function3(): Maximum Per Random Walk Graph Tensor Neuron Network Intrinsic Merit :",maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit

		print "grow_lambda_function3(): Recursive Gloss Overlap Classifier classes for text:",RecursiveGlossOverlap_Classifier.RecursiveGlossOverlap_Classify(text)

		intrinsic_merit_dict["graph_tensor_neuron_network_intrinsic_merit"]=self.graph_tensor_neuron_network_intrinsic_merit
		intrinsic_merit_dict["maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit"]=maximum_per_random_walk_graph_tensor_neuron_network_intrinsic_merit
		intrinsic_merit_dict["korner_entropy"]=self.entropy
		intrinsic_merit_dict["density"]=density
		intrinsic_merit_dict["bose_einstein_intrinsic_fitness"]=bose_einstein_intrinsic_fitness
		intrinsic_merit_dict["recursive_gloss_overlap_intrinsic_merit"]=definitiongraph_merit[1]
		intrinsic_merit_dict["empath_sentiment"]=sentiment

		write_dot(definitiongraph,"RecursiveLambdaFunctionGrowth.dot")

		self.graph_tensor_neuron_network_intrinsic_merit=1.0
		print "intrinsic_merit_dict:",intrinsic_merit_dict
		return intrinsic_merit_dict 

	#KornerEntropy(G) = minimum [- sum_v_in_V(G) {1/|V(G)| * log(Pr[v in Y])}] for each independent set Y
	def korner_entropy(self, definitiongraph):
		nodes=definitiongraph.nodes()
		stable_sets=[]
		for v in nodes:
			stable_sets.append(nx.maximal_independent_set(definitiongraph.to_undirected(),[v]))
		print "korner_entropy(): Stable Independent Sets:",stable_sets
		entropy=0.0
		prob_v_in_stableset=0.0
		for v in nodes:
			for s in stable_sets:
				if v in s:
					prob_v_in_stableset=math.log(0.999999)
				else:
					prob_v_in_stableset=math.log(0.000001)
				entropy += (-1.0) * float(1.0/len(nodes)) * prob_v_in_stableset
			if entropy < self.entropy:
				self.entropy = entropy
			entropy=0.0
		return self.entropy

	#Graph Density - Regularity Lemma
	def density(self, definitiongraph):
		dty=nx.classes.function.density(definitiongraph)
		return dty

	#Bose-Einstein Bianconi intrinsic fitness 
	def bose_einstein_intrinsic_fitness(self, definitiongraph):
		#Bose-Einstein fitness presently assumes energy of a document vertex in a link graph to be
		#the entropy or extent of chaos in the definition graph of document text 
		#This has to be replaced by a more suitable fitness measure
		#Bose-Einstein Condensation function value is hardcoded
		entropy = self.korner_entropy(definitiongraph)
		becf = 0.3
		bei_fitness = math.pow(2, -1 * becf * entropy)
		return bei_fitness

if __name__=="__main__":
	lambdafn=RecursiveLambdaFunctionGrowth()
	text=open("RecursiveLambdaFunctionGrowth.txt","r")
	textread=text.read()
	lambdafn.grow_lambda_function3(textread)
	summary=lambdafn.create_summary(textread)
	print
	print summary
	print "=========================================================="
	print "Ratio of summary to text:", float(summary[1])/float(len(textread))
