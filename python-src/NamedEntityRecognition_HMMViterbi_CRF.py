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

#CRF - mixture of HMM and Maximum Entropy Markov Models(Logistic Regression)

#---------------------------
#CRF - Viterbi Algorithm
#---------------------------
#arg max Pr[transitions from State(1) to State(t-1) with observations from O1 to O(t-1)] and observing O[t] at State(t) ] usually drawn as all possible paths in trellis graph 

import pprint
import math
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(1,1)

states=["noun","conjunction","verb","adjective","adverb","object"]

start_probabilities={'noun':0.3, 'verb':0.2, 'object':0.2, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.2}

#State Transition Probabilities
transition_probabilities={ 'noun':{'noun':0.0, 'verb':0.3, 'object':0.2, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.3},
			   'verb':{'noun':0.1, 'verb':0.0, 'object':0.4, 'adjective':0.2, 'adverb':0.1,'conjunction':0.3},
			   'object':{'noun':0.0, 'verb':0.1, 'object':0.4, 'adjective':0.1, 'adverb':0.1,'conjunction':0.3},
			   'adjective':{'noun':0.4, 'verb':0.2, 'object':0.2, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.1},
			   'adverb':{'noun':0.1, 'verb':0.4, 'object':0.1, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.3},
			   'conjunction':{'noun':0.2, 'verb':0.4, 'object':0.1, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.1}
			 }


#Part of Speech Tagging - Named Entity Recognition
obs_file=open("NamedEntityRecognition_HMMViterbi_CRF.observations","r")
observations=obs_file.read().split()

emission_probabilities={}
cnt=len(states)

for s in states:
	emissionsdict={}
	x = np.linspace(skewnorm.ppf(0.01,5,cnt*0.5,1),skewnorm.ppf(0.99,5,loc=cnt,scale=1),len(observations))
	sknormpdf = skewnorm.pdf(x,5,loc=cnt,scale=1)
	print "sknormpdf:",sknormpdf
	ax.plot(x, sknormpdf,'r-', lw=5, alpha=0.6, label='skewnorm pdf')
	obs_cnt=0
	for o in observations:
		emissionsdict[o]=sknormpdf[obs_cnt]/sum(sknormpdf)
		obs_cnt += 1
	emission_probabilities[s]=emissionsdict
	cnt=(cnt-1)
plt.show()

for s in states:
	emissiondict=emission_probabilities[s]
	sumprob = 0.0
	for k,v in emissiondict.iteritems():
		sumprob += v
	for k,v in emissiondict.iteritems():
		emissiondict[k] = float(v)/float(sumprob)

print "Emission Probabilities:",emission_probabilities
Viterbi=[{}]
Viterbi_path={}

for s in states:
	print "s=",s,"; observation=",observations[0]
	Viterbi[0][s] = start_probabilities[s]*emission_probabilities[s][observations[0]]
	Viterbi_path[s] = [s]

print "Viterbi initialised to:"
print Viterbi
print len(observations)

for x in range(1,len(observations)):
	Viterbi.append({})
	path2={}
	for y in states:
 		(probability, state) = max((Viterbi[x-1][t]*transition_probabilities[t][y], t) for t in states)
		Viterbi[x][y] = probability
		path2[y] = Viterbi_path[state] + [y]
	Viterbi_path=path2	

print "============================"
print "CRF Viterbi computation"
print "============================"
pprint.pprint(Viterbi) 
print "============================"
print "CRF Viterbi path computation"
print "============================"
pprint.pprint(Viterbi_path)

#---------------------
#Standard CRF equation
#---------------------
#arg max [Pr(State=S/Obs) = exp(weight*F(S,Obs)) / Sigma_X(exp(weight*F(X,Obs))]
# (or)
#arg max [Pr(State=S/Obs) is directly proportional to exp(weight*F(S,Obs))]

print "============================"
print "PoS tagging with CRF"
print "============================"

#Above equation is computed for finding hidden state label 
#observations=['PoSTagging', 'is', 'used', 'to', 'annotate', 'complex', 'sentences', 'with','PoS'] 
#PoS_CRF_states=['noun','verb','?','conjunction','?','verb','object','?','object'] 

poscrffile=open("NamedEntityRecognition_HMMViterbi_CRF.states","r")
PoS_CRF_states=poscrffile.read().split()
PoS_probabilities={}

weight=0.01
k=0.2
maximum=0
feature={}
i=0
missing_PoS=[]
prev_PoS_tag=[]

for n in PoS_CRF_states:
	if n == '?':
		missing_PoS.append(observations[i])
		prev_PoS_tag.append(PoS_CRF_states[i-1])
	i+=1

print "Sentence to be PoS tagged", observations
print "Previous tagged PoS",prev_PoS_tag
print "PoS tagged words in previous sentence", PoS_CRF_states
print "words missing PoS tag:",missing_PoS

for t in zip(missing_PoS, prev_PoS_tag):
	label=""
	maximum=0
	for s in states:
		#Compute Feature function for missing PoS - definition of Feature function is subjective
		#Here the feature function to find argmax() is the conditional probability product - discriminative model:
		#	probability of transition from a previous labelled state * probability of observation in the state 
		feature[s]=emission_probabilities[s][t[0]]*transition_probabilities[t[1]][s]
		PoS_probabilities[s]=k*math.exp(weight*feature[s])
		print "argmax() computation for observations missing PoS tags: emission(s=",s,",t[0]=",t[0],")*transition(t[1]=",t[1],",s=",s,") - feature[s]=",feature[s],", PoS_probabilities[s] =",PoS_probabilities[s]
		if PoS_probabilities[s] > maximum:
		#if feature[s] > maximum:
			maximum = PoS_probabilities[s]
			#maximum = feature[s]
			label=s
	print " \"",t[0],"\" PoS tagged using CRF as: ",label
