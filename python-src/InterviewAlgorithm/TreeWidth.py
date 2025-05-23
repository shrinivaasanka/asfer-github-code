# -------------------------------------------------------------------------------------------------------
# ASFER - Software for Mining Large Datasets
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
# Copyright (C):
# Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
# Ph: 9791499106, 9003082186
# Krishna iResearch Open Source Products Profiles:
# http://sourceforge.net/users/ka_shrinivaasan,
# https://github.com/shrinivaasanka,
# https://www.openhub.net/accounts/ka_shrinivaasan
# Personal website(research): https://sites.google.com/site/kuja27/
# emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
# kashrinivaasan@live.com
# --------------------------------------------------------------------------------------------------------


import pickle
import sys

import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import itertools


def hash_graph(edges):
    hash = "Set"
    for e in edges:
        hash += "#"+str(e)
    return hash


def create_all_subgraphs(edges, size_edges):
    all_subgraphs = []
    for i in range(size_edges):
        all_subgraphs += itertools.combinations(edges, i)
    return all_subgraphs


def tree_width(nxg, i):
    maxsize = 1000000000
    junction_tree = nx.Graph()
    max_junction_tree_node = junction_tree
    all_subgraphs = create_all_subgraphs(nxg.edges(), i)
    print("All subgraphs:", all_subgraphs)
    print("============================================")
    for k0 in all_subgraphs:
        for k1 in all_subgraphs:
            hash_graph_k0 = hash_graph(k0)
            hash_graph_k1 = hash_graph(k1)
            if (hash_graph_k0 != hash_graph_k1) and len(set(k0).intersection(set(k1))) > 0:
                junction_tree.add_edge(hash_graph_k0, hash_graph_k1)
                if len(k0) < maxsize:
                    max_junction_tree_node = k0
                    maxsize = len(k0)
                if len(k1) < maxsize:
                    max_junction_tree_node = k1
                    maxsize = len(k1)
    print("============================================")
    print("Junction Tree (with subgraphs of size less than", i, ") :")
    nx.draw_networkx(junction_tree)
    plt.show()
    print("============================================")
    print("Junction Tree Width for subgraphs of size less than ", i, " - size of largest node set:", maxsize)
