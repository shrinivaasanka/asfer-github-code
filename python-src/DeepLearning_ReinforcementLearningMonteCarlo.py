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

monte_carlo_policy_search=False
ThoughtNet_policy_search=True

#Two action policy searches have been implemented - one is the random montecarlo choice and the other is a non-trivial ThoughtNet evocation.
#This is an example ThoughtNet storage with hyperedges and multiplanar hypergraph. A practical ThoughtNet storage could be of billions of
#edges based on experiential learning of an individual over a period of lifetime and has to be suitably stored in a medium that mimicks brain.
#Ideally following dictionary has to be in some persistence bigdate storage though it still is just an approximation.
#Hypergraph encodes the edges as numbers - for example, "transactions":[1] and "security":[1] implies that a sentence numbered 1 has been
#pre-classified under transactions and security categories. Also "services":[0,1] implies that there are two sentences encoded as 0 and 1 
#classified in services category with descending order of evocative potentials - 0 is more evocative than 1.
#In an advanced setting the ThoughtNet stores the lambda function composition parenthesized equivalent to the sentence and action taken upon
#evocation is to evaluate the most potent evocative lambda expression.

#ThoughtNet File System Storage - eval()-ed to dict and list
thoughtnet_edges_storage=open("./ThoughtNet/ThoughtNet_Edges.txt","r")
thoughtnet_hypergraph_storage=open("./ThoughtNet/ThoughtNet_Hypergraph_Generated.txt","r")

thoughtnet_edges=ast.literal_eval(thoughtnet_edges_storage.read())
thoughtnet_hypergraph=ast.literal_eval(thoughtnet_hypergraph_storage.read())

r=[0.5,0.8,0.2,0.9,0.75,0.8]
states=[0,1,2,3,4,5]
actions=[1,2,3,4,5,6]
actions_rewards={1:r[1],2:r[2],3:r[3],4:r[0],5:r[5],6:r[4]}
state_transitions={actions[0]:[0,1],actions[5]:[1,5],actions[2]:[3,6],actions[1]:[6,2],actions[4]:[4,1],actions[3]:[5,4]}

inputf=open("ReinforcementLearning.input.txt","r")
reward=0.0
for obs in inputf.read().split():
	if monte_carlo_policy_search == True:
		#choose an action - PseudoRandom Monte Carlo
		action_indx=random.randint(0,5)
		print "Policy action index chosen by Monte Carlo:", actions[action_indx]
		print "State transition on observation :", obs, state_transitions[actions[action_indx]]
		reward += actions_rewards[actions[action_indx]]
		print "Reward collected so far:", reward
	if ThoughtNet_policy_search == True:
		#Evocatives are returned from ThoughtNet storage
		print "==========================================================================================="
		print "Observation:",obs.lower()
		try:
			if thoughtnet_hypergraph[obs.lower()] is not None:
				for s in thoughtnet_hypergraph[obs.lower()]:
					print "evocative thought (reward) returned(in descending order of evocation potential):", thoughtnet_edges[s] 
		except:
			pass

