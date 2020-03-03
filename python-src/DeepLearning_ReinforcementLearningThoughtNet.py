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

#Reinforcement Learning :
#------------------------
#On environmental observation O(t), agent state changes from S(t) to S(t+1) with action chosen being A(t) and reward R(t).
#Set of Transitions that maximize Sigma(R(t)) is the optimal. 

import random
import ast

#action policy search implemented - non-trivial ThoughtNet evocation:
#This is an example ThoughtNet storage with hyperedges and multiplanar hypergraph. A practical ThoughtNet storage could be of billions of
#edges based on experiential learning of an individual over a period of lifetime and has to be suitably stored in a medium that mimicks brain.
#Ideally ThoughtNet has to be in some persistence bigdata storage though it still is just an approximation. Neo4j backend for ThoughtNet
#has been implemented in ThoughtNet/. ThoughtNet is kind of Evocation WordNet expanded for thoughts represented as sentences (because
#there is no better way to encode thoughts than in a natural language) and classified. Hypergraph encodes the edges as numbers - for example, 
#"transactions":[1] and "security":[1] implies that a sentence numbered 1 has been pre-classified under transactions and security categories. 
#Also "services":[0,1] implies that there are two sentences encoded as 0 and 1 classified in services category with descending order of 
#evocative potentials - 0 is more evocative than 1.  In an advanced setting the ThoughtNet stores the lambda function composition parenthesized
#equivalent to the sentence and action taken upon evocation is to evaluate the most potent evocative lambda expression.
#On an evocative thought, state of "ThoughtNet" mind changes with corresponding action associated with that state 
#(the usual mind-word-action triad). Philosophically, this simulates the following thought experiment:
#	- Word: Sensory receptors perceive stimuli - events
#	- Mind: stimuli evoke thoughts in past
#	- Action: Evocative thought is processed by intellect and inspires action - action is a lambda evaluation of a sentence.
##############################################################################
#
#	Senses(Word) <---------> Mind(Evocation) <---------> Action(Intellect)
#	 ^				                          ^
#	 |<------------------------------------------------------>|
#
#and above is an infinite cycle. Previous schematic maps interestingly to Reinforcement Learning(Agent-Environment-Action-Reward).
##############################################################################
#In this aspect, ThoughtNet is a qualitative experimental inference model compared to quantitative Neural Networks.

from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlap_Classify

#ThoughtNet File System Storage - eval()-ed to dict and list
thoughtnet_edges_storage=open("./ThoughtNet/ThoughtNet_Edges.txt","r")
thoughtnet_hypergraph_storage=open("./ThoughtNet/ThoughtNet_Hypergraph_Generated.txt","r")

thoughtnet_edges=ast.literal_eval(thoughtnet_edges_storage.read())
thoughtnet_hypergraph=ast.literal_eval(thoughtnet_hypergraph_storage.read())

inputf=open("ReinforcementLearning.input.txt","r")
classification=RecursiveGlossOverlap_Classify(inputf.read())
print "classification :"
print classification
creamylayer=int(len(classification[0])*1)
toppercentileclasses=classification[0][:creamylayer]
print "top percentile classes:"
print toppercentileclasses
print "======================================================================================================="
print "ThoughtNet Reinforcement Learning - Contextual Multi Armed Bandit Evocation"
print "======================================================================================================="
for cls, occurrence in toppercentileclasses:
	#Evocatives are returned from ThoughtNet storage
	print "==========================================================================================="
	try:
		#It is assumed in present implementation that every thought edge is a state implicitly, and the action
		#for the state is the "meaning" inferred by recursive lambda evaluation
		if thoughtnet_hypergraph[cls] is not None:
			for s in thoughtnet_hypergraph[cls]:
				print "evocative thought (reward) returned(in descending order of evocation potential) for class [",cls,"] :", thoughtnet_edges[s] 
	except:
		pass

