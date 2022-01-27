# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------
# Social Network Analysis - People Analytics - Chaotic Hidden Markov Model of Tenures - Viterbi Algorithm
# --------------------------------------------------------------------------------------------------------
# arg max Pr[transitions from State(1) to State(t-1) with observations from O1 to O(t-1) and observing O[t] at State(t)] usually drawn as all possible paths in trellis graph

import pprint
import math
from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import wordnet as wn
import networkx as nx
from itertools import product
from collections import Counter
import json
import tensorflow as tf
import tensorflow_io as tfio
from numpy import polyfit

fig, ax = plt.subplots(1, 1)


class ChaoticHMM(object):
    def __init__(self, Lambda, states, start_probs, transition_probs, emission_probs, observ, designations,career_statemachine):
        self.Lambda = Lambda
        self.states = states
        self.start_probabilities = start_probs
        # State Transition Probabilities
        self.transition_probabilities = transition_probs
        self.observations = observ
        self.emission_probabilities = emission_probs
        self.career_transition_score = 0
        self.designations=designations
        self.career_statemachine=career_statemachine

    def career_transition_analytics(self):
        prev_obs=self.observations[0]
        for n in range(1,len(self.observations)-1):
            obs=self.observations[n]
            career_transition=""
            if prev_obs in self.designations["academic"].keys():
                career_transition+="academic-"
                self.career_transition_score += self.designations["academic"][prev_obs]
            if prev_obs in self.designations["startup"].keys():
                career_transition+="startup-"
                self.career_transition_score += self.designations["startup"][prev_obs]
            if prev_obs in self.designations["work"].keys():
                career_transition+="work-"
                self.career_transition_score += self.designations["work"][prev_obs]
            if prev_obs in self.designations["business"].keys():
                career_transition+="business-"
                self.career_transition_score += self.designations["business"][prev_obs]
            if obs in self.designations["academic"].keys():
                career_transition+="academic"
                self.career_transition_score += self.career_statemachine[career_transition]
            if obs in self.designations["startup"].keys():
                career_transition+="startup"
                self.career_transition_score += self.career_statemachine[career_transition]
            if obs in self.designations["work"].keys():
                career_transition+="work"
                self.career_transition_score += self.career_statemachine[career_transition]
            if obs in self.designations["business"].keys():
                career_transition+="business"
                self.career_transition_score += self.career_statemachine[career_transition]
            prev_obs = obs
        if prev_obs in self.designations["academic"].keys():
            self.career_transition_score += self.designations["academic"][prev_obs]
        if prev_obs in self.designations["startup"].keys():
            self.career_transition_score += self.designations["startup"][prev_obs]
        if prev_obs in self.designations["work"].keys():
            self.career_transition_score += self.designations["work"][prev_obs]
        if prev_obs in self.designations["business"].keys():
            self.career_transition_score += self.designations["business"][prev_obs]
        print("career_transition_analytics(): career transition score of the profile = ",self.career_transition_score)
        self.weighted_designations=dict(list(self.designations["academic"].items()) + list(self.designations["work"].items()) + list(self.designations["startup"].items()) + list(self.designations["business"].items()))
        career_polynomial_points=[]
        for o in self.observations:
            career_polynomial_points.append((o,self.weighted_designations[o]))
        print("career_transition_analytics(): career_polynomial_points:",career_polynomial_points)
        career_polynomial=polyfit(list(range(len(career_polynomial_points))),self.second(career_polynomial_points),5)
        print("career_transition_analytics(): career polynomial - based on weighted designations (HMM observations):",career_polynomial)

    def career_polynomial_inner_product_distance(self,poly1,poly2):
        career_polynomial1=polyfit(range(len(poly1)),poly1,5)
        career_polynomial2=polyfit(range(len(poly2)),poly2,5)
        ip_distance=0.0
        for x,y in zip(poly1,poly2):
            ip_distance += x*y
        print("career_polynomial_inner_product_distance(): career_polynomial1 = ",career_polynomial1)
        print("career_polynomial_inner_product_distance(): career_polynomial2 = ",career_polynomial2)
        print("career_polynomial_inner_product_distance(): ip_distance = ",ip_distance)
        return ip_distance

    def second(self,orderedpair):
        values=[]
        for op in orderedpair:
            values.append(op[1])
        return values

    def normalize(self,iterable):
        newx=[]
        for x in iterable:
            newx.append(x/max(iterable))
        return newx

    def chaotic_HMM_viterbi(self):
        Viterbi = [{}]
        Viterbi_path = {}

        for s in self.states:
            #print "s=",s,"; observation=",self.observations[0]
            Viterbi[0][s] = self.start_probabilities[s] * \
                self.emission_probabilities[s][self.observations[0]]
            Viterbi_path[s] = [s]

        print("Viterbi initialised to:")
        print(Viterbi)
        print(len(self.observations))

        for x in range(1, len(self.observations)):
            Viterbi.append({})
            path2 = {}
            for y in self.states:
                #(probability, state) = max((Viterbi[x-1][t]*self.transition_probabilities[t][y], t) for t in self.states)
                (probability, state) = max((Viterbi[x-1][t]*self.Lambda*self.transition_probabilities[t][y]*(
                    1-self.transition_probabilities[t][y])*self.emission_probabilities[y][self.observations[x]], t) for t in self.states)
                #(probability, state) = max((Viterbi[x-1][t]*self.Lambda*self.transition_probabilities[t][y]*(1-self.transition_probabilities[t][y]), t) for t in self.states)
                Viterbi[x][y] = probability
                path2[y] = Viterbi_path[state] + [y]
            Viterbi_path = path2
        ViterbiTrellis=[]
        for vertex in Viterbi:
            maxk=0
            maxv=0
            for k,v in vertex.items():
                if v > maxv:
                    maxk=k
                    maxv=v
            ViterbiTrellis.append(maxk)
        print("============================")
        print("Chaotic HMM Viterbi computation")
        print("============================")
        pprint.pprint(Viterbi)
        print("============================")
        print("Chaotic HMM Viterbi Trellis computation")
        print("============================")
        pprint.pprint(ViterbiTrellis)


if __name__ == "__main__":
    chaotichmmf=open("SocialNetworkAnalysis_PeopleAnalytics_ChaoticHMM.json")
    chaotichmmjson=json.loads(chaotichmmf.read())
    print("chaotichmmjson:",chaotichmmjson)
    piplprofile=open("SocialNetworkAnalysis_PeopleAnalytics_ChaoticHMM.json")
    piplprofilejson=json.load(piplprofile)
    print("piplprofilejson:",piplprofilejson)
    #piplprofiletensor=tf.io.decode_json_example(piplprofilejson["states"])
    piplprofiletensor_states=tf.convert_to_tensor(piplprofilejson["states"])
    print("piplprofiletensor - states:",piplprofiletensor_states)
    chaotichmm = ChaoticHMM(5.0, chaotichmmjson["states"], chaotichmmjson["start_probabilities"], chaotichmmjson["transition_probabilities"], chaotichmmjson["emission_probabilities"], chaotichmmjson["observations"],chaotichmmjson["designations"],chaotichmmjson["career_statemachine"])
    chaotichmm.chaotic_HMM_viterbi()
    chaotichmm.career_transition_analytics()
    designations1=[1,2,3,4,5,6,7]
    remunerations1=[100000,700000,1000000,1300000,200000,1400000,2500000]
    durations1=[0.7,5,0.1,2,3,2,0.5]
    designations2=[2,4,5,7,3,6]
    remunerations2=[10000,70000,1000000,1300,20000,1500000,3500000]
    durations2=[7,5,0.3,2,4,1,0.3]
    print("========================================================")
    print("Career Polynomial Inner Product Distance - Remunerations")
    print("========================================================")
    chaotichmm.career_polynomial_inner_product_distance(chaotichmm.normalize(remunerations1),chaotichmm.normalize(remunerations2))
    print("========================================================")
    print("Career Polynomial Inner Product Distance - Designations")
    print("========================================================")
    chaotichmm.career_polynomial_inner_product_distance(chaotichmm.normalize(designations1),chaotichmm.normalize(designations2))
    print("========================================================")
    print("Career Polynomial Inner Product Distance - Durations")
    print("========================================================")
    chaotichmm.career_polynomial_inner_product_distance(chaotichmm.normalize(durations1),chaotichmm.normalize(durations2))
