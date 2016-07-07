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

	def get_next_tree_traversal_id(self,x,y):
		if y-x == 1 or x-y == 1:
			return 1 
		print "x,y:",x,y
		self.index_list.append((x+y)/2)
		self.get_next_tree_traversal_id(x,(x+y)/2)
		self.get_next_tree_traversal_id((x+y)/2,y)

	def build_lambda_expression(self,key,value):
		print value,
		self.lambda_expression.append(value)

	def build_lambda_comp_tree(self,k,v):
		self.word_dict[k]=self.word_list[k]

	def return_next(self,k,v):
		return (k,v)

	def grow_lambda_function2(self):
		text=open("RecursiveLambdaFunctionGrowth.txt","r")
		words_evaluated=0
		self.word_list=text.read().split()
		
		#self.get_next_tree_traversal_id(0,len(word_list)-1)
		#print "index list:", self.index_list
		#while words_evaluated < len(self.index_list):
		#	word_dict[words_evaluated]=word_list[self.index_list[words_evaluated]]
		#	words_evaluated+=1
	
		cnt=0
		while cnt < len(self.word_list):
			self.index_dict[cnt]=cnt
			cnt+=1

		self.index_tree=BinaryTree(self.index_dict)
		self.index_tree.foreach(self.build_lambda_comp_tree,0)
		
		self.lambda_comp_tree=AVLTree(self.word_dict)
		self.lambda_expression=[]
		print "==========================================================================="
		print "Lambda Composition AVL Tree (inorder traversed) is the original text itself:"
		print "==========================================================================="
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 0)
		print
		print "==========================================================================="
		print "Lambda Composition AVL Tree (postorder traversed):"
		print "Every parenthesis has two operands,operated by function outside:"
		print "==============================================================="
		self.lambda_expression=[]
		self.lambda_comp_tree.foreach(self.build_lambda_expression, 1)
		print 
		print "=============================================================="
		print "Lambda Function Composition Postfix Evaluation (parenthesized):"
		print "=============================================================="
		#print self.lambda_expression
		self.lambda_composition=[]
		cnt=0
		while len(self.lambda_expression) > 2 :
			function=self.lambda_expression.pop()
			operand1=self.lambda_expression.pop()
			operand2=self.lambda_expression.pop()
			self.lambda_composition="("+function+"("+operand1+","+operand2+"))" 
			self.lambda_expression.append(self.lambda_composition)
			cnt+=1
		print "".join(self.lambda_expression)
		print "==============================================================="	
			

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
	
if __name__=="__main__":
	lambdafn=RecursiveLambdaFunctionGrowth()
	lambdafn.grow_lambda_function2()
