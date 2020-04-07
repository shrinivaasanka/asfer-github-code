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
# Personal website(research): https://sites.google.com/site/kuja27/
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

fig, ax = plt.subplots(1, 1)


class ChaoticHMM(object):
    def __init__(self, Lambda, states, start_probs, transition_probs, emission_probs, observ):
        self.Lambda = Lambda
        self.states = states
        self.start_probabilities = start_probs
        # State Transition Probabilities
        self.transition_probabilities = transition_probs
        self.observations = observ
        self.emission_probabilities = emission_probs

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

        print("============================")
        print("Chaotic HMM Viterbi computation")
        print("============================")
        pprint.pprint(Viterbi)
        print("============================")
        print("Chaotic HMM Viterbi path computation")
        print("============================")
        pprint.pprint(Viterbi_path)


if __name__ == "__main__":
    chaotichmmf=open("SocialNetworkAnalysis_PeopleAnalytics_ChaoticHMM.json")
    chaotichmmjson=json.loads(chaotichmmf.read())
    print("chaotichmmjson:",chaotichmmjson)
    #states = ["PSGTech", "BaaN-SSAGlobal", "SunMicrosystems-Oracle", "Krishna-iResearch", "Verizon",
    #          "webMethods-SoftwareAG", "CMI-IIT-IMSc", "GlobalAnalytics", "Clockwork-PiQube", "CloudEnablers"]
    #start_probabilities={'noun':0.3, 'verb':0.2, 'object':0.2, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.2}
    #start_probabilities = {"PSGTech": 1.0, "BaaN-SSAGlobal": 1.0, "SunMicrosystems-Oracle": 1.0, "Krishna-iResearch": 0.0, "Verizon": 0.0,
    #                       "webMethods-SoftwareAG": 0.0, "CMI-IIT-IMSc": 0.0, "GlobalAnalytics": 0.0, "Clockwork-PiQube": 0.0, "CloudEnablers": 0.0}
    # transition_probabilities={ 'noun':{'noun':0.0, 'verb':0.3, 'object':0.2, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.3},
    #		   'verb':{'noun':0.1, 'verb':0.0, 'object':0.4, 'adjective':0.2, 'adverb':0.1,'conjunction':0.3},
    #		   'object':{'noun':0.0, 'verb':0.1, 'object':0.4, 'adjective':0.1, 'adverb':0.1,'conjunction':0.3},
    #		   'adjective':{'noun':0.4, 'verb':0.2, 'object':0.2, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.1},
    #		   'adverb':{'noun':0.1, 'verb':0.4, 'object':0.1, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.3},
    #		   'conjunction':{'noun':0.2, 'verb':0.4, 'object':0.1, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.1}
    #		 }
    #transition_probabilities = {"PSGTech": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "BaaN-SSAGlobal": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "SunMicrosystems-Oracle": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "Krishna-iResearch": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "Verizon": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "webMethods-SoftwareAG": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "CMI-IIT-IMSc": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "GlobalAnalytics": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "Clockwork-PiQube": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1},
    #                            "CloudEnablers": {"PSGTech": 0.1, "BaaN-SSAGlobal": 0.1, "SunMicrosystems-Oracle": 0.1, "Krishna-iResearch": 0.1, "Verizon": 0.1, "webMethods-SoftwareAG": 0.1, "CMI-IIT-IMSc": 0.1, "GlobalAnalytics": 0.1, "Clockwork-PiQube": 0.1, "CloudEnablers": 0.1}}
    # observations=obs_file.read().split()
    #observations = ["Graduation", "AssociateSoftwareEngineer", "MemberTechStaff", "Founder-Architect", "SystemAnalyst",
    #                "Specialist", "PostGraduation-ResearchScholar", "Consultant-Architect", "Consultant", "Architect"]
    # emission_probabilities={ 'noun':{'noun':0.0, 'verb':0.3, 'object':0.2, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.3},
    #		   'verb':{'noun':0.1, 'verb':0.0, 'object':0.4, 'adjective':0.2, 'adverb':0.1,'conjunction':0.3},
    #		   'object':{'noun':0.0, 'verb':0.1, 'object':0.4, 'adjective':0.1, 'adverb':0.1,'conjunction':0.3},
    #		   'adjective':{'noun':0.4, 'verb':0.2, 'object':0.2, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.1},
    #		   'adverb':{'noun':0.1, 'verb':0.4, 'object':0.1, 'adjective':0.0, 'adverb':0.1, 'conjunction':0.3},
    #		   'conjunction':{'noun':0.2, 'verb':0.4, 'object':0.1, 'adjective':0.1, 'adverb':0.1, 'conjunction':0.1}
    #		 }
    #emission_probabilities = {"PSGTech": {"Graduation": 1.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "BaaN-SSAGlobal": {"Graduation": 0.0, "AssociateSoftwareEngineer": 1.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "SunMicrosystems-Oracle": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 1.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "Krishna-iResearch": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 1.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "Verizon": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 1.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "webMethods-SoftwareAG": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 1.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "CMI-IIT-IMSc": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 1.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "GlobalAnalytics": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 1.0, "Consultant": 0.0, "Architect": 0.0},
    #                          "Clockwork-PiQube": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 1.0, "Architect": 0.0},
    #                          "CloudEnablers": {"Graduation": 0.0, "AssociateSoftwareEngineer": 0.0, "MemberTechStaff": 0.0, "Founder-Architect": 0.0, "SystemAnalyst": 0.0, "Specialist": 0.0, "PostGraduation-ResearchScholar": 0.0, "Consultant-Architect": 0.0, "Consultant": 0.0, "Architect": 1.0}}
    chaotichmm = ChaoticHMM(3.7, chaotichmmjson["states"], chaotichmmjson["start_probabilities"],
                            chaotichmmjson["transition_probabilities"], chaotichmmjson["emission_probabilities"], chaotichmmjson["observations"])
    chaotichmm.chaotic_HMM_viterbi()
