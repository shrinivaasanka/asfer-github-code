# -------------------------------------------------------------------------------------------------------
# NEURONRAIN AI - ASFER - Software for Mining Large Datasets
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
# Krishna iResearch FOSS - http://www.krishna-iresearch.org
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

from collections import defaultdict
import numpy as np
import networkx as nx

def get_majority_label_from_neighbors(node,neighbors,node2labeldict):
    label2freqdict=defaultdict(int)
    for node,label in node2labeldict.items():
        if node in neighbors:
            label2freqdict[label] += 1
    maxfreq=0
    maxlabel=""
    print("label2freqdist:",label2freqdict)
    for label,freq in label2freqdict.items():
        if freq > maxfreq:
            maxlabel = label
            maxfreq = freq
    print("maxlabel:",maxlabel)
    if maxlabel != "":
        return maxlabel
    else:
        return "-1"

def label_propagation(nxgraph,maxiterations=100,convergenceenabled=False):
    node2labeldict=defaultdict()
    prevnode2labeldict=defaultdict()
    label=0
    iterations=0
    for node in nxgraph.nodes():
        node2labeldict[node]="Label-"+str(label)
        label += 1
    print("node2labeldict:",node2labeldict)
    permutednodes=np.random.permutation(nxgraph.nodes())
    while iterations < maxiterations:
        for node in permutednodes:
            neighbors=nxgraph.neighbors(node)
            majoritylabel=get_majority_label_from_neighbors(node,neighbors,node2labeldict)
            if majoritylabel != "-1":
                node2labeldict[node]=majoritylabel
        if convergenceenabled:
            if iterations > 1 and prevnode2labeldict == node2labeldict:
                print("Label propagation iterations have converged ... terminating")
                break
        iterations += 1
        print("Iteration - ",iterations," Label propagated Node-to-Label dictionary:",node2labeldict)
        prevnode2labeldict=node2labeldict
    print("--------------------------------------------------------")
    print("Graph vertices clustered according to Label Propagation:")
    print("--------------------------------------------------------")
    labelclusters=defaultdict(list)
    for node,label in node2labeldict.items():
        labelclusters[label].append(node)
    print(labelclusters)

if __name__=="__main__":
    examplegraph=nx.Graph()
    examplegraph.add_edge("a","b")
    examplegraph.add_edge("f","c")
    examplegraph.add_edge("a","d")
    examplegraph.add_edge("c","b")
    examplegraph.add_edge("c","d")
    examplegraph.add_edge("a","e")
    examplegraph.add_edge("b","f")
    examplegraph.add_edge("e","g")
    examplegraph.add_edge("d","b")
    examplegraph.add_edge("d","c")
    examplegraph.add_edge("d","f")
    examplegraph.add_edge("a","g")
    petersengraph=nx.petersen_graph()
    completegraph=nx.complete_graph(100)
    print("-----------Label Propagation: Example Graph--------------")
    label_propagation(examplegraph,maxiterations=100)
    label_propagation(examplegraph,maxiterations=100,convergenceenabled=True)
    print("-----------Label Propagation: Petersen Graph--------------")
    label_propagation(petersengraph,maxiterations=100)
    print("-----------Label Propagation: Complete Graph--------------")
    label_propagation(completegraph,maxiterations=100)
