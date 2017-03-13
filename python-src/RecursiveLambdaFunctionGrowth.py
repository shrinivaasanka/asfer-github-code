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
		self.tensor_intrinsic_merit=0.0

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
		while len(self.lambda_expression) > 2 :
			operand2=self.lambda_expression.pop()
			function=self.lambda_expression.pop()
			operand1=self.lambda_expression.pop()
			self.tensor_intrinsic_merit += self.tensor_neuron_weight(operand1, function, operand2)
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

	def tensor_neuron_weight(self, e1, r, e2):
		relation=r
		if e1[0]=="(":
			e1_parsed=e1.split("(")
			#print "operand1:", e1_parsed[1]
			synset_e1 = wn.synsets(e1_parsed[1])
		else:
			synset_e1 = wn.synsets(e1)
			#print "operand1:", e1

		if e2[0]=="(":
			e2_parsed=e2.split("(")
			#print "operand2:", e2_parsed[1]
			synset_e2 = wn.synsets(e2_parsed[1])
		else:
			#print "operand2:", e2
			synset_e1 = wn.synsets(e2)

		similarity = 0.0
		for s1, s2 in product(synset_e1, synset_e1):
			smt=wn.wup_similarity(s1,s2)
			if smt > similarity:
				similarity = smt
		return similarity

	def randomwalk_lambda_function_composition_tree(self,randomwalk):
		randomwalk_lambdacomposition=self.grow_lambda_function2(randomwalk)
		return randomwalk_lambdacomposition

	def grow_lambda_function3(self):
		text=open("RecursiveLambdaFunctionGrowth.txt","r")
		stpairs=[]
		definitiongraph=RecursiveGlossOverlap_Classifier.RecursiveGlossOverlapGraph(text.read())
		apsp=nx.all_pairs_shortest_path(definitiongraph)
		for a in definitiongraph.nodes():
			for b in definitiongraph.nodes():
				stpairs.append((a,b))
		rw_ct=""
		for k,v in stpairs:
			try:
				print "Random Walk between :",k," and ",v,":",apsp[k][v]
				rw_ct=self.randomwalk_lambda_function_composition_tree(apsp[k][v])
				print "Random Walk Composition Tree for walk between :",k," and ",v,":",rw_ct
			except KeyError:
				pass
			print
			rw_ct=""
		print "Tensor Neuron Intrinsic Merit :",self.tensor_intrinsic_merit


if __name__=="__main__":
	lambdafn=RecursiveLambdaFunctionGrowth()
	lambdafn.grow_lambda_function3()
