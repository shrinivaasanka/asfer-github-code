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

#action policy search implemented - random montecarlo choice.

r=[0.5,0.8,0.2,0.9,0.75,0.8]
states=[0,1,2,3,4,5]
actions=[1,2,3,4,5,6]
actions_rewards={1:r[1],2:r[2],3:r[3],4:r[0],5:r[5],6:r[4]}
state_transitions={actions[0]:[0,1],actions[5]:[1,5],actions[2]:[3,6],actions[1]:[6,2],actions[4]:[4,1],actions[3]:[5,4]}

inputf=open("ReinforcementLearning.input.txt","r")
reward=0.0
for obs in inputf.read().split():
	#choose an action - PseudoRandom Monte Carlo
	action_indx=random.randint(0,5)
	print "Policy action index chosen by Monte Carlo:", actions[action_indx]
	print "State transition on observation :", obs, state_transitions[actions[action_indx]]
	reward += actions_rewards[actions[action_indx]]
	print "Reward collected so far:", reward
