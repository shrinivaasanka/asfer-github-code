#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# ConceptNet and WordNet: http://web.media.mit.edu/~havasi/MAS.S60/PNLP10.pdf

import nltk
import requests
import pprint
from queue import Queue
from itertools import product
#from rest_client import similar_to_concepts
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from nltk.book import *
import matplotlib.pyplot as plt
import operator
import SentimentAnalyzer
import RecursiveLambdaFunctionGrowth


class ConceptNet5Client:
    def __init__(self):
        self.ClosedPaths = True
        print("Init of ConceptNet Client")

    def query_association(self, concept1, concept2):
        conceptjson = requests.get(
            "http://api.conceptnet.io/c/en/"+concept1+"?filter=/c/en/"+concept2).json()
        return conceptjson

    def query_search(self, concept):
        conceptjson = requests.get(
            "http://api.conceptnet.io/search?end=/c/en/"+concept).json()
        return conceptjson

    def query_lookup(self, concept):
        conceptjson = requests.get(
            "http://api.conceptnet.io/c/en/"+concept).json()
        return conceptjson

    def related(self, concept):
        conceptjson = requests.get(
            "http://api.conceptnet.io/related/c/en/"+concept).json()
        return conceptjson

    def query_emotions(self, emoji):
        conceptjson = requests.get(
            "http://api.conceptnet.io/c/mul/"+emoji).json()
        return conceptjson

    def conceptnet_path(self, concept1, concept2):
        conceptjson = requests.get(
            "http://api.conceptnet.io/query?node=/c/en/"+concept1+"&other=/c/en/"+concept2).json()
        return conceptjson

    def remove_noise(self, cn_sp):
        print(("remove_noise(): cn_sp=", cn_sp))
        print(("remove_noise(): type(cn_sp)=", type(cn_sp)))
        cn_sp.remove('/c/en/\xb0_c')
        return cn_sp

    def conceptnet_textgraph(self, text):
        tokenized = nltk.word_tokenize(text)
        fdist = FreqDist(tokenized)
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords = stopwords + [' ', 'or', 'and', 'who', 'he', 'she', 'whom', 'well', 'is', 'was', 'were', 'are', 'there', 'where', 'when', 'may', 'The',
                                 'the', 'In', 'in', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        puncts = [' ', '.', '"', ',', '{', '}', '+', '-', '*', '/', '%',
                  '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';', '\'s']
        freqterms = [w.decode("utf-8", "ignore") for w in list(fdist.keys())
                     if w not in stopwords and w not in puncts]
        conceptnettg = nx.DiGraph()
        for w1 in freqterms:
            for w2 in freqterms:
                if w1 != w2:
                    cn_distance = self.conceptnet_least_common_ancestor_distance(
                        w1.lower(), w2.lower())
                    try:
                        cn_sp = shortest_path(
                            cn_distance, w1.lower(), w2.lower())
                        print(("conceptnet path:", cn_sp))
                        cn_sp = self.remove_noise(cn_sp)
                        print(("conceptnet path filtered:", cn_sp))
                        # for cn_edge in cn_distance.edges():
                        #    conceptnettg.add_edge(cn_edge[0],cn_edge[1])
                        conceptnettg.add_path(cn_sp)
                    except Exception as e:
                        print(("exception:", e))
        nx.draw_networkx(conceptnettg)
        plt.show()
        conceptnettg.remove_edges_from(conceptnettg.selfloop_edges())
        sorted_core_nxg = sorted(list(nx.core_number(
            conceptnettg).items()), key=operator.itemgetter(1), reverse=True)
        print(("Core number (sorted) :", sorted_core_nxg))
        print("=============================================================================================================")
        print("Unsupervised Classification based on top percentile Core numbers of the definition graph(subgraph of ConceptNet)")
        print("=============================================================================================================")
        no_of_classes = len(nx.core_number(conceptnettg))
        top_percentile = 0
        max_core_number = 0
        max_core_number_class = ""
        for n in sorted_core_nxg:
            if top_percentile < no_of_classes*0.50:
                top_percentile += 1
            else:
                break
            if n[1] > max_core_number:
                max_core_number = n[1]
                max_core_number_class = n[0]
        print(("	max_core_number", max_core_number))

        print("===================================================================")
        print("Betweenness Centrality of Recursive Gloss Overlap graph vertices")
        print("===================================================================")
        bc = nx.betweenness_centrality(conceptnettg)
        sorted_bc = sorted(
            list(bc.items()), key=operator.itemgetter(1), reverse=True)
        print(sorted_bc)

        print("===================================================================")
        print("Closeness Centrality of Recursive Gloss Overlap graph vertices")
        print("===================================================================")
        cc = nx.closeness_centrality(conceptnettg)
        sorted_cc = sorted(
            list(cc.items()), key=operator.itemgetter(1), reverse=True)
        print(sorted_cc)

        print("===================================================================")
        print("Degree Centrality of Recursive Gloss Overlap graph vertices")
        print("===================================================================")
        dc = nx.degree_centrality(conceptnettg)
        sorted_dc = sorted(
            list(dc.items()), key=operator.itemgetter(1), reverse=True)
        print(sorted_dc)

        print("===================================================================")
        print("Page Rank of the vertices of RGO Definition Graph (a form of Eigenvector Centrality)")
        print("===================================================================")
        sorted_pagerank_nxg = sorted(list(nx.pagerank(
            conceptnettg).items()), key=operator.itemgetter(1), reverse=True)
        print(sorted_pagerank_nxg)

        rflg = RecursiveLambdaFunctionGrowth.RecursiveLambdaFunctionGrowth()
        intrinsic_merit_dict = rflg.grow_lambda_function3(
            textgraph=conceptnettg)
        return intrinsic_merit_dict

    def conceptnet_least_common_ancestor_distance(self, concept1, concept2):
        pprint.pprint(
            "=======================================================")
        pprint.pprint("Distance and Path between:"+concept1+" and "+concept2)
        pprint.pprint(
            "=======================================================")
        nxg = nx.DiGraph()
        edges = []
        try:
            related1 = self.related(concept1)
            related2 = self.related(concept2)
            related1list = []
            related2list = []
            for e in related1["related"]:
                if "/en" in e["@id"]:
                    related1list.append(e["@id"])
                    edges.append((concept1, e["@id"]))
            for e in related2["related"]:
                if "/en" in e["@id"]:
                    related2list.append(e["@id"])
                    edges.append((e["@id"], concept2))
            #print "related1list: ",related1list
            #print "related2list: ",related2list
            commonancestors = set(related1list).intersection(set(related2list))
            #print "commonancestors: ",commonancestors
            distance = 1
            q1 = Queue()
            q2 = Queue()
            q1.put(set(related1list))
            q2.put(set(related2list))
            while len(commonancestors) == 0 and distance < 1000:
                concept1list = q1.get()
                concept2list = q2.get()
                related1list = related2list = []
                for c1 in concept1list:
                    related1 = self.related(c1)
                    for e in related1["related"]:
                        if "/en" in e["@id"]:
                            related1list.append(e["@id"])
                            edges.append((c1, e["@id"]))
                for c2 in concept2list:
                    related2 = self.related(c2)
                    for e in related2["related"]:
                        if "/en" in e["@id"]:
                            related2list.append(e["@id"])
                            edges.append((e["@id"], c2))
                #print "related1list: ",related1list
                #print "related2list: ",related2list
                q1.put(set(related1list))
                q2.put(set(related2list))
                commonancestors = set(
                    related1list).intersection(set(related2list))
                distance = distance + 1
                #print "commonancestors: ",commonancestors
        except Exception as e:
            print(("Exception:", e))
        #print "edges:",edges
        for k, v in edges:
            nxg.add_edge(k, v)
        return nxg


if __name__ == "__main__":
    conceptnet = ConceptNet5Client()
    print("==========================================")
    print("ConceptNet Text Graph")
    print("==========================================")
    #conceptnet.conceptnet_textgraph("Madras Day is a festival organized to commemorate the founding of the city of Madras (now Chennai) in Tamil Nadu, India")
    text = open("ConceptNet5Client.txt", "r")
    textread = text.read()
    conceptnet.conceptnet_textgraph(textread)
    print("===================================================")
    print("ConceptNet Emotions ")
    print("===================================================")
    conceptjson = conceptnet.query_emotions("😂")
    pprint.pprint(conceptjson)
    print("========================================")
    print("Association")
    print("========================================")
    conceptjson = conceptnet.query_association("chennai", "marina")
    pprint.pprint(conceptjson)
    print("========================================")
    print("Search")
    print("========================================")
    conceptjson = conceptnet.query_search("chennai")
    pprint.pprint(conceptjson)
    print("========================================")
    print("Lookup")
    print("========================================")
    conceptjson = conceptnet.query_lookup("chennai")
    pprint.pprint(conceptjson)
    print("========================================")
    print("Related Concepts Ranked Descending by Distance Score")
    print("========================================")
    similarconcepts = conceptnet.related('chennai')
    pprint.pprint("Concepts related to Chennai")
    pprint.pprint(similarconcepts)
    similarconcepts = conceptnet.related('computer science')
    pprint.pprint("Concepts related to computer science")
    pprint.pprint(similarconcepts)
    print("========================================")
    print("ConceptNet Distance - Common Ancestor algorithm")
    print("========================================")
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'chennai', 'metropolitan')
    sp = shortest_path(distance, 'chennai', 'metropolitan')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'chennai', 'delhi')
    sp = shortest_path(distance, 'chennai', 'delhi')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'fructify', 'fruitful')
    sp = shortest_path(distance, 'fructify', 'fruitful')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'medicine', 'chemical')
    sp = shortest_path(distance, 'medicine', 'chemical')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'tree', 'forest')
    sp = shortest_path(distance, 'tree', 'forest')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    distance = conceptnet.conceptnet_least_common_ancestor_distance(
        'upbraid', 'anathema')
    sp = shortest_path(distance, 'upbraid', 'anathema')
    pprint.pprint("Distance:"+str(len(sp)))
    pprint.pprint("Shortest Path:")
    pprint.pprint(sp)
    print("=========================================")
    print("ConceptNet Path - relations connecting two concepts")
    print("=========================================")
    path = conceptnet.conceptnet_path('medicine', 'chemical')
    pprint.pprint(path)
