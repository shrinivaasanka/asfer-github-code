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
		#print "==========================================================================="
		#print "Lambda Composition AVL Tree (inorder traversed) is the original text itself:"
		#print "==========================================================================="
		self.lambda_expression=[]
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 0)
		#print
		#print "==========================================================================="
		#print "Lambda Composition AVL Tree (inorder traversed):"
		#print "Every parenthesis has two operands,operated by function outside:"
		#print "==============================================================="
		self.lambda_expression=[]
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 0)
		#print
		#print "=============================================================="
		#print "Lambda Function Composition Infix Evaluation (parenthesized):"
		#print "=============================================================="
		#print self.lambda_expression
		self.lambda_composition=[]
		cnt=0

		#recursively evaluate the Graph Tensor Neuron Network for random walk composition tree bottom up as Graph Neural Network
		#having Tensor Neuron activations for each subtree.
		while len(self.lambda_expression) > 2 :
			operand2=self.lambda_expression.pop()
			function=self.lambda_expression.pop()
			operand1=self.lambda_expression.pop()
			self.graph_tensor_neuron_network_intrinsic_merit += self.subtree_graph_tensor_neuron_network_weight(operand1, function, operand2)
			self.lambda_composition="("+function+"("+operand1+","+operand2+"))" 
			self.lambda_expression.append(self.lambda_composition)
			cnt+=1
		if len(self.lambda_expression) > 1:
			return self.lambda_expression[0] + "("+self.lambda_expression[1]+")"
		else:
			return self.lambda_expression[0]
			
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
			smt=wn.wup_similarity(s1,s2)
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

	def grow_lambda_function3(self,text):
		stpairs=[]
		definitiongraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(text)
		apsp=nx.all_pairs_shortest_path(definitiongraph)
		for a in definitiongraph.nodes():
			for b in definitiongraph.nodes():
				stpairs.append((a,b))
		rw_ct=""
		for k,v in stpairs:
			try:
				#print "Random Walk between :",k," and ",v,":",apsp[k][v]
				rw_ct=self.randomwalk_lambda_function_composition_tree(apsp[k][v])
				#print "Random Walk Composition Tree for walk between :",k," and ",v,":",rw_ct
			except KeyError:
				pass
			rw_ct=""
		print "grow_lambda_function3(): Graph Tensor Neuron Network Intrinsic Merit for this text:",self.graph_tensor_neuron_network_intrinsic_merit
		self.korner_entropy(definitiongraph)
		print "grow_lambda_function3(): Korner Entropy Intrinsic Merit for this text:",self.entropy
		self.graph_tensor_neuron_network_intrinsic_merit=1.0

	#KornerEntropy(G) = minimum [- sum_v_in_V(G) {1/|V(G)| * log(Pr[v in Y])}] for each independent set Y
	def korner_entropy(self, definitiongraph):
		nodes=definitiongraph.nodes()
		stable_sets=[]
		for v in nodes:
			stable_sets.append(nx.maximal_independent_set(definitiongraph,[v]))
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

if __name__=="__main__":
	lambdafn=RecursiveLambdaFunctionGrowth()
	text=open("RecursiveLambdaFunctionGrowth.txt","r")
	#lambdafn.grow_lambda_function3(text.read())
	textread=text.read()
	summary=lambdafn.create_summary(textread)
	print
	print summary
	print "=========================================================="
	print "Ratio of summary to text:", float(summary[1])/float(len(textread))
