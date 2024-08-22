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

######################################################################
# EventNet - a cloudwide event ordering with unique id implementation
# --------------------------------------------------------------------
# EventNet has 2 input files for vertices and edges with partakers and
# writes an output file with ordering of the events

# Input - EventNetVertices.txt has the format:
#	<event vertex> - <csv of partakers> - <tuples of conversations amongst the partakers # separated>
#	partakers could be machine id(s) or IP addresses and thread id(s) and the conversations being the#	 messages to-and-fro across the partakers, which create an IntraEvent Graph of Conversations
#	within each event vertex
#
# Input - EventNetEdges.txt has the format:
#	<event vertex1, event vertex2>
#
# Output - EventNetOrdering.txt has the format:
#	<index in chronologically ascending order> - <event id>
#
# EventNet script thus is run in a central node which has the input files above that is
# updated by all the nodes in cloud.
######################################################################

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write
from pygraph.algorithms.sorting import *

from graphviz import Digraph
import gv
import tensorflow as tf
import networkx as nx

eventsdict = {}


def intraevent_totensor(intraeventedges):
    edges = intraeventedges.split("#")
    nxg = nx.Graph()
    for edge in edges:
        edgestrip=edge.strip()
        edgevertices=edgestrip[1:-1].split(',')
        nxg.add_edge(edgevertices[0],edgevertices[1])
    nxgtensor=tf.convert_to_tensor(nx.adjacency_matrix(nxg).todense())
    print(nxgtensor)
    return nxgtensor 


def EventNet_Tensor_Parser():
    vertices_file = open("EventNetVertices.txt", "r")
    edges_file = open("EventNetEdges.txt", "r")

    gr1 = digraph()
    gr2 = Digraph(engine="neato")

    for vertex in vertices_file:
        print(vertex)
        tokens = vertex.split('-')
        print(tokens)
        gr1.add_nodes([tokens[0].strip()])
        gr2.node(tokens[0], "Event "+tokens[0]+" Partakers -" +
                 tokens[1] + "- IntraEventConversations:"+tokens[2])
        eventsdict[tokens[0].strip()] = intraevent_totensor(tokens[2])

    EventNet_Tensor=nx.Graph()
    for edge in edges_file:
        print(edge)
        tokens = edge.split(',')
        print(tokens)
        edge_tuple = (tokens[0].strip(), tokens[1].strip())
        gr1.add_edge((tokens[0].strip(), tokens[1].strip()))
        # gr1.add_edge(edge_tuple)
        gr2.edge(tokens[0], tokens[1])
        EventNet_Tensor.add_edge(eventsdict[tokens[0].strip()],eventsdict[tokens[1].strip()])
    EventNet_Tensor_tf=tf.convert_to_tensor(nx.to_scipy_sparse_matrix(EventNet_Tensor).todense())
    print("EventNet Tensor - TensorFlow:")
    print(EventNet_Tensor_tf)
    dot = write(gr1)
    gvv = gv.readstring(dot)
    gv.layout(gvv, 'dot')
    gv.render(gvv, 'png', 'EventNet.gv.png')
    gr2.render("EventNet.graphviz")
    print("############################################")
    print("Topological sorting of the graph:")
    print("############################################")
    sortedgr1 = topological_sorting(gr1)
    print(sortedgr1)

    toposortedevents = open("EventNetOrdering.txt", "w")
    index = 1
    for s in sortedgr1:
        toposortedevents.write(str(index) + " - " + s + " \n")
        index += 1


if __name__ == "__main__":
    EventNet_Tensor_Parser()
