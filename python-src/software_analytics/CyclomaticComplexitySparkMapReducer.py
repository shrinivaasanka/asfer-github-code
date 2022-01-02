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

# Apache Spark RDD MapReduce Transformations script for parsing the number of edges and vertices
# in SATURN generated .dot graph files for program control flow. Cyclomatic Complexity which is a
# basic function point estimator for complexity of a software is determined as Edges - Vertices + 2.

# Example pyspark RDD mapreduce code at: http://www.mccarroll.net/blog/pyspark2/

from pyspark import SparkContext, SparkConf
from GraphMining_GSpan import GSpan
import networkx as nx
from networkx.drawing.nx_pydot import read_dot
from networkx.classes.function import edges
from pyspark.sql import SQLContext, Row
from networkx.drawing.nx_pydot import write_dot
import operator
from graphframes import *
from networkx.algorithms import isomorphism

def reduceFunction(value1, value2):
    return value1+value2


def mapFunction(line):
    for i in line.split():
        return (i, 1)


def ftrace_callgraph_dot(ftracefile):
    callgraph = nx.DiGraph()
    ftracef = open(ftracefile)
    for l in ftracef:
        ltok = l.split(":")
        callgraphedge = ltok[1]
        callgraphedgetok = callgraphedge.split("<-")
        if len(callgraphedgetok) >= 2: 
            callgraph.add_edge(callgraphedgetok[1], callgraphedgetok[0])
    ftracefiletoks=ftracefile.split(".")
    write_dot(callgraph, ftracefiletoks[1]+".ftrace_callgraph.dot")
    sorted_pagerank_nxg = sorted(list(nx.pagerank(
        callgraph).items()), key=operator.itemgetter(1), reverse=True)
    print("Most active kernel code - PageRank of call graph:", sorted_pagerank_nxg)
    sorted_degreecentral_nxg = sorted(list(nx.degree_centrality(
        callgraph).items()), key=operator.itemgetter(1), reverse=True)
    print("Most active kernel code - Degree centrality of call graph:", sorted_degreecentral_nxg)
    print("Simple Cycles in call graph:")
    for cycle in nx.simple_cycles(callgraph):
        print("Cycle:", cycle)
    print("Longest Path (callstack) in call graph:", nx.dag_longest_path(
        callgraph))


def graph_matching(dotfile1, dotfile2, isomorphism_iterations=25,ismagssymmetry=False):
    print(("======== Matching Callgraphs:",dot1," and ",dot2))
    dotnx1 = nx.Graph(read_dot(dotfile1))
    dotnx2 = nx.Graph(read_dot(dotfile2))
    isisomorphic = nx.is_isomorphic(dotnx1, dotnx2)
    print(("Callgraphs of two executables are isomorphic - (True or False):", isisomorphic))
    if isisomorphic:
        print(("Callgraphs of two executables are isomorphic - percentage similarity : 100.0"))
    gm = isomorphism.GraphMatcher(dotnx1, dotnx2)
    issubgraphisomorphic = gm.subgraph_is_isomorphic()
    print(("Callgraphs of two executables are subgraph isomorphic - (True or False):", issubgraphisomorphic))
    cnt = 0
    for sgiso_vf2 in gm.subgraph_isomorphisms_iter():
        print(("VF2 subgraph isomorphisms between two Voronoi facegraphs:", sgiso_vf2))
        print(("VF2 subgraph isomorphisms between two Voronoi facegraphs - percentage similarities - 1:",
              100.0*float(len(sgiso_vf2))/float(len(dotnx1.nodes()))))
        print(("VF2 subgraph isomorphisms between two Voronoi facegraphs - percentage similarities - 2:",
              100.0*float(len(sgiso_vf2))/float(len(dotnx2.nodes()))))
        cnt += 1
        if cnt > isomorphism_iterations:
            break
    cnt = 0
    ismags = isomorphism.ISMAGS(dotnx1, dotnx2)
    for sgiso_ismags_asymmetric in ismags.isomorphisms_iter(ismagssymmetry):
        print(("ISMAGS subgraph isomorphism between two callgraphs - symmetry (",
              ismagssymmetry, "):", sgiso_ismags_asymmetric))
        print(("ISMAGS subgraph isomorphism between two callgraphs - symmetry (", ismagssymmetry,
              ") - percentage similarities - 1 :", 100.0*float(len(sgiso_ismags_asymmetric))/float(len(dotnx1.nodes()))))
        print(("ISMAGS subgraph isomorphism between two callgraphs - symmetry (", ismagssymmetry,
              ") - percentage similarities - 2:", 100.0*float(len(sgiso_ismags_asymmetric))/float(len(dotnx2.nodes()))))
        if cnt > isomorphism_iterations:
            break


def graph_mining(dotfiles):
    dataset = []
    for dotf in dotfiles:
        dotnx = nx.Graph(read_dot(dotf))
        dataset.append(dotnx)
    gsp = GSpan(dataset)
    gsp.GraphSet_Projection()
    for dotf in dotfiles:
        dotnx = nx.Graph(read_dot(dotf))
        dataset.append(dotnx)
    for dot1 in dataset:
        for dot2 in dataset:
            print("=================================")
            gsp.GraphEditDistance(dot1, dot2)


def cyclomatic_complexity(dotfiles):
    for dot_file in input_dot_files:
        nxg = nx.Graph(read_dot(dot_file))
        nxgnodes = [[]]
        nxgedges = [[]]
        cnt = 0
        for n in nxg.nodes():
            cnt += 1
            nxgnodes[0].append((str(cnt), str(n), str(n)))
        for e in nxg.edges():
            nxgedges[0].append((str(e[0]), str(e[1]), "causes"))
        print("nxgnodes:", nxgnodes)
        print("nxgedges:", nxgedges)
        ndf = sqlcon.createDataFrame(nxgnodes, ["id", "name", "label"])
        vdf = sqlcon.createDataFrame(nxgedges, ["src", "dst", "relationship"])
        print("ndf:", ndf)
        print("vdf:", vdf)
        gf = GraphFrame(ndf, vdf)
        print("Indegrees:", gf.inDegrees.show())
        print("Strongly Connected Components:", gf.stronglyConnectedComponents(
            1).show())
        print("Triangle count:", gf.triangleCount().show())
        print("Edges + Vertices:", len(nxgnodes)+len(nxgedges))
        zeroth_betti_number = gf.stronglyConnectedComponents(1).show()
        print("Cyclomatic Complexity: Zeroth Betti Number = ", zeroth_betti_number)
        print("Cyclomatic Complexity: E-V = ", len(nxgedges) - len(nxgnodes))
        if zeroth_betti_number is None:
            zeroth_betti_number = 0
        print("Cyclomatic Complexity: First Betti Number = E-V + <Zeroth-Betti-Number> = ", len(
            nxgedges) - len(nxgnodes) + zeroth_betti_number)


if __name__ == "__main__":
    spcon = SparkContext()
    sqlcon = SQLContext(spcon)
    input_dot_files=['../../../../GitHub/virgo64-linux-github-code/linux-kernel-extensions/drivers/virgo/saturn_program_analysis/saturn_program_analysis_trees/cfg_read_virgo_kernel_analytics_config.dot','../../../../GitHub/virgo64-linux-github-code/linux-kernel-extensions/drivers/virgo/saturn_program_analysis/saturn_program_analysis_trees/memory_skbuff_h_skb_header_pointer_cfg.dot','../../../../GitHub/asfer-github-code/python-src/software_analytics/kcachegrind_callgraph_DiscreteHyperbolicFactorization_TileSearch_Optimized.dot','../../../../GitHub/asfer-github-code/python-src/software_analytics/kcachegrind_callgraph_ls.dot','./kcachegrind_callgraph_DiscreteHyperbolicFactorization_TileSearch_Optimized.dot','CyclomaticComplexitySparkMapReducer.ftrace_callgraph.dot',"pwd.ftrace_callgraph.dot","find.ftrace_callgraph.dot"]
    #ftrace_callgraph_dot("ftrace.pwd.log")
    #ftrace_callgraph_dot("ftrace.find.log")
    #cyclomatic_complexity(input_dot_files)
    #graph_mining(input_dot_files)
    for dot1 in input_dot_files[:4]:
        for dot2 in input_dot_files[:4]:
            graph_matching(dot1, dot2)
