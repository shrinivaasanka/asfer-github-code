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
# Copyleft (Copyright+):
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


import sys
import pickle

from pyspark import SparkContext, SparkConf
import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
#from nltk.book import FreqDist
from nltk.corpus import stopwords
import networkx as nx
import matplotlib.pyplot as plt
import queue
import operator
import TreeWidth
from pymemcache.client import base 
import InterviewAlgorithmWithIntrinisicMerit_SparkMapReducer

parents_computation_spark = True

#########################################################################################################
# Intrinsic Merit computation and Interview Algorithm
# For publications:
# 1. http://arxiv.org/abs/1006.4458
# 2. http://www.nist.gov/tac/publications/2010/participant.papers/CMI_IIT.proceedings.pdf
#
# Constructs wordnet subgraph from documents.
# This takes as input a scrapy crawled text from WebSpider-HTML.out from python-src/webspider/
# Adds some visualizations and a graph theoretic intrinsic merit based on connectivity.
#########################################################################################################

required_none_vertices = False

#function - compute_idf()


def compute_idf(corpus, keyword):
    import math
    total_occur = 0
    keyword_occur = 0
    for file in corpus:
        raw = open(file).read()
        tokens = nltk.word_tokenize(raw.decode("utf-8"))
        total_occur = total_occur + len(tokens)
        keyword_occur = keyword_occur + \
            len([w for w in tokens if w == keyword])
    return math.log(total_occur / (keyword_occur))

# parents (at level i-1) of a given vertex at level i
# arguments are a keyword at present level and all disambiguated synsets of previous level


def parents(keyword, prevlevelsynsets):
    parents = []
    print("parents(): prevlevelsynsets:", prevlevelsynsets)
    for syn in prevlevelsynsets:
        print("type(syn):", type(syn))
        if type(syn) is nltk.corpus.reader.wordnet.Synset:
            syndef_tokens = set(nltk.word_tokenize(syn.definition()))
            print("parents(): syndef_tokens:", syndef_tokens)
            if keyword in syndef_tokens:
                print("parents(): keyword :", keyword, " in syndef, adding to parents:")
                parents = parents + [syn]
    print("parents(): returning parents:", parents)
    return parents

# parents (at level i-1) of a given vertex at level i
# arguments are a keyword at present level and all disambiguated synsets of previous level


def parents_tokens(keyword, prevleveltokens):
    parents = []
    print("parents_tokens(): prevleveltokens:", prevleveltokens)
    for prevleveltoken in prevleveltokens:
       #syn=best_matching_synset(prevleveltokens, wn.synsets(prevleveltoken))
        syns = wn.synsets(prevleveltoken)
        syn = syns[0]
        print("type(syn):", type(syn))
        if type(syn) is nltk.corpus.reader.wordnet.Synset:
            syndef_tokens = set(nltk.word_tokenize(syn.definition()))
            print("parents_tokens(): syndef_tokens:", syndef_tokens)
            if keyword in syndef_tokens:
                print("parents_tokens(): keyword :", keyword, " in syndef, adding to parents:")
                parents = parents + [syn]
    print("parents_tokens(): returning parents:", parents)
    return parents

#function - best_matching_synset()


def best_matching_synset(doc_tokens, synsets):
    maxmatch = -1
    retset = []
    for synset in synsets:
        def_tokens = set(nltk.word_tokenize(synset.definition()))
        intersection = def_tokens.intersection(doc_tokens)
        if len(intersection) > maxmatch:
            maxmatch = len(intersection)
            retset = synset
    return retset

#function - get_context()


def get_context(query, documents):
    file1 = open(documents[0])
    file_contents = file1.read()
    file_tokens = nltk.word_tokenize(file_contents)
    try:
        first_occur = file_tokens.index(query)
    except ValueError:
        return ""
    context = ''
    for i in file_tokens[first_occur-5:first_occur+5]:
        context = context + ' ' + i
    return context


def filter_none_vertices(nxg):
    for e in nx.edges(nxg):
        if e[0] == "None" or e[1] == "None":
            nxg.remove_edge(e[0], e[1])
    # nxg.remove_vertex("None")

#function - get_jaccard_coefficient()
# def get_jaccard_coefficient(refanswer, candidanswer):
#	total = len(set(shingles(refanswer) + shingles(candidanswer)))
#	intersect = len(set(shingles(refanswer)).intersection(set(shingles(candidanswer))))
#	return (intersect + 1) / (total + 1)

# get shingles
# def shingles(phrase):
#	return bigrams(nltk.word_tokenize(phrase))


def InterviewAlgorithm_main(argv1):
    # ----------------------------------------------
    # 1.Get the input documents
    # ----------------------------------------------

    corpus = [argv1]
    # get keywords

    files = [argv1]

    # ----------------------------------------------
    # 2.Initialize MemCached Client
    # ----------------------------------------------
    graphcache = base.Client(["127.0.0.1:11211"], debug=1)
    InterviewAlgorithmWithIntrinisicMerit_SparkMapReducer.flushCache(
        graphcache)

    # ---------------------------------------------------------------------------------
    # 3.Compute intrinsic merit (either using linear or quadratic overlap)
    # ---------------------------------------------------------------------------------

    definitiongraphedges = defaultdict(list)
    definitiongraphedgelabels = defaultdict(list)
    weight_str_map = defaultdict()

    for filestr in files:
        outputfile = 'Output-Webspider-HTML.out'
        output = open(outputfile, 'w')
        file1 = open(filestr)
        raw1 = file1.read()
        doc1 = nltk.word_tokenize(raw1.decode("utf-8"))
        #fdist1 = FreqDist(doc1)
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords = stopwords + [' ', 'or', 'and', 'who', 'he', 'she', 'whom', 'well', 'is', 'was', 'were', 'are', 'there', 'where', 'when', 'may', 'The',
                                 'the', 'In', 		'in', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        puncts = [' ', '.', '"', ',', '{', '}', '+', '-', '*', '/', '%',
                  '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';', '\'s']
        #freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w))]
        freqterms1 = [
            w for w in doc1 if w not in stopwords and w not in puncts]

        current_level = 1
        nodewithmaxparents = ''
        noofparents = 0
        maxparents = 0
        relatedness = 0
        first_convergence_level = 1
        tokensofthislevel = []
        convergingterms = []
        convergingparents = []
        tokensofprevlevel = []
        prevlevelsynsets = []
        commontokens = []
        vertices = 0
        edges = 0
        overlap = 0
        iter = 0
        # recurse down to required depth and update intrinsic merit score
        # relatedness is either sum(overlaps) or sum((overlapping_parents)*(overlaps)^2) also called convergence factor
        while current_level < 3:
            # crucial - gather nodes which converge/overlap (have more than 1 parent)
            if current_level > 1:
                print(current_level)
                prevlevelsynsets_tokens = []
                for s in prevlevelsynsets:
                    s_lemma = s.lemma_names()
                    prevlevelsynsets_tokens.append(s_lemma[0])
                for x in freqterms1:
                    # prevlevelsynsets_tokens=[]
                    # for s in prevlevelsynsets:
                    #	s_lemma=s.lemma_names()
                    #	prevlevelsynsets_tokens.append(s_lemma[0])
                    if parents_computation_spark:
                        parents_x = InterviewAlgorithmWithIntrinisicMerit_SparkMapReducer.Spark_MapReduce_Parents(
                            x, prevlevelsynsets_tokens, graphcache)
                        if len(parents_x) > 1:
                            convergingterms.append(x)
                    else:
                        #parents_x = parents(x,prevlevelsynsets)
                        parents_x = parents_tokens(x, prevlevelsynsets_tokens)
                        if len(parents_x) > 1:
                            convergingterms.append(x)
                    convergingparents = convergingparents + \
                        ([w for w in parents_x if len(parents_x) > 1])
                    noofparents = len(parents_x)
                    if noofparents > maxparents:
                        maxparents = noofparents
                        nodewithmaxparents = x
                    for y in parents_x:
                        if parents_computation_spark:
                            definitiongraphedges[x].append(y)
                        else:
                            y_lemma_names = y.lemma_names()
                            definitiongraphedges[x].append(y_lemma_names[0])
                output.write(
                    'converging terms(terms with more than 1 parent):\n ')
                output.write('converging parents :\n')

            print("InterviewAlgorithmWithIntrinisicMerit_Crawl_Visual_Spark.py:freqterms1=", freqterms1)
            tokensofthislevel = InterviewAlgorithmWithIntrinisicMerit_SparkMapReducer.Spark_MapReduce(
                current_level, freqterms1, graphcache).tokensatthislevel
            print("InterviewAlgorithmWithIntrinisicMerit_Crawl_Visual_Spark.py:tokensofthislevel:", tokensofthislevel)
            picklef = open(
                "RecursiveGlossOverlap_MapReduce_Persisted.txt", "r")
            prevlevelsynsets = InterviewAlgorithmWithIntrinisicMerit_SparkMapReducer.asfer_pickle_load(
                picklef)
            print("prevlevelsynsets:", prevlevelsynsets)
            picklef = open(
                "RecursiveGlossOverlap_MapReduce_Persisted.txt", "w")
            picklef.seek(0)
            picklef.truncate()
            output.write('At level:\n')
            output.write(str(current_level))
            output.write('\n')
            output.write('tokens grasped at this level:\n')
            #pickle.dump(tokensofthislevel, output)
            output.write('\n')
            listcount = len(tokensofthislevel)
            setcount = len(set(tokensofthislevel))
            overlap = listcount-setcount
            if overlap > 0 and iter == 0:
                first_convergence_level = current_level
                iter = 1
            # choose between two relatedness/convergence criteria :-
            # 1) simple linear overlap or 2) zipf distributed quadratic overlap
            #relatedness = relatedness + len(convergingparents)*overlap
            relatedness = relatedness + overlap + len(convergingparents)
            #relatedness = relatedness + ((len(convergingparents)*overlap*overlap) + 1)
            # find out common tokens of this and previous level so that same token does not get grasped again -
            # relatedness must be increased since repetition of keywords in two successive levels is a sign of
            # interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 					#corresponding to common tokens
            commontokens = set(tokensofthislevel).intersection(
                set(tokensofprevlevel))
            tokensofthislevel = list(
                set(tokensofthislevel).difference(commontokens))
            relatedness = relatedness + len(commontokens)
            output.write('removing tokens already grasped:\n')
            # pickle.dump(commontokens,output)
            output.write('\n')
            output.write('Relatedness:\n')
            output.write(str(relatedness))
            output.write('\n')
            # decrease the vertices count to address common tokens removed above - edges should remain same since they
            # would just point elsewhere
            vertices = vertices + setcount - len(commontokens)
            output.write('Vertices:\n')
            output.write(str(vertices))
            output.write('\n')
            edges = edges + listcount
            output.write('Edges:\n')
            output.write(str(edges))
            output.write('\n')
            current_level = current_level + 1
            freqterms1 = tokensofthislevel
            tokensofprevlevel = tokensofthislevel
            tokensofthislevel = []

        intrinsic_merit = vertices*edges*relatedness / first_convergence_level
        output.write('Intrinsic merit of this document is:\n')
        output.write(str(intrinsic_merit))
        output.write('\n')
        output.write(
            'Node with maximum parents (and hence the most likely class of document) is:\n')
        output.write(nodewithmaxparents)
        output.write('\n')

    print(definitiongraphedges)

    nxg = nx.DiGraph()
    pos = nx.spectral_layout(nxg)
    for k, v in definitiongraphedges.items():
        for l in v:
            nxg.add_edge(k, l)
            nxg.add_edge(l, k)
            ksynset = wn.synsets(k)
            lsynset = wn.synsets(l)
            if ksynset and lsynset:
                print("ksynset=", ksynset[0])
                print("lsynset=", lsynset[0])
                hypoksynsets = set(
                    [i for i in ksynset[0].closure(lambda n:n.hyponyms())])
                hyperlsynsets = set(
                    [i for i in lsynset[0].closure(lambda n:n.hypernyms())])
                for m in hypoksynsets:
                    try:
                        mlemmanames = m.lemma_names()
                        weight_str_map[k+" - "+l] = weight_str_map[k +
                                                                   " - "+l]+" contains "+mlemmanames[0]
                    except KeyError:
                        weight_str_map[k+" - "+l] = ""
                for n in hyperlsynsets:
                    try:
                        nlemmanames = n.lemma_names()
                        weight_str_map[l+" - "+k] = weight_str_map[l +
                                                                   " - "+k]+" is part of "+nlemmanames[0]
                    except KeyError:
                        weight_str_map[l+" - "+k] = ""
    if not required_none_vertices:
        filter_none_vertices(nxg)

    nx.draw_networkx(nxg)
    try:
        nx.write_dot(
            nxg, "InterviewAlgorithmWithIntrinisicMerit_Crawl_Visual_RGOGraph.dot")
    except:
        pass
    plt.show()
    nxg.remove_edges_from(nxg.selfloop_edges())
    #print "Core number =",nx.core_number(nxg)
    sorted_core_nxg = sorted(list(nx.core_number(
        nxg).items()), key=operator.itemgetter(1), reverse=True)
    print("Core number (sorted) :", sorted_core_nxg)
    print("=============================================================================================================")
    print("Unsupervised Classification based on top percentile Core numbers of the definition graph(subgraph of WordNet)")
    print("=============================================================================================================")
    no_of_classes = len(nx.core_number(nxg))
    top_percentile = 0
    max_core_number = 0
    for n in sorted_core_nxg:
        print("This document belongs to class:", n[0], ",core number=", n[1])
        if top_percentile < no_of_classes*0.10:
            top_percentile += 1
        else:
            break
        if n[1] > max_core_number:
            max_core_number = n[1]
    print("max_core_number", max_core_number)

    print("===================================================================")
    print("Page Rank of the vertices of RGO Definition Graph")
    print("===================================================================")
    print(sorted(list(nx.pagerank(nxg).items()),
                 key=operator.itemgetter(1), reverse=True))

    try:
        print("==========================================================================================================")
        print("Alternative Quantitative Intrinsic Merit  - connectivity of RGO Definition Graph - Mengers Theorem")
        print("==========================================================================================================")
        print(nx.node_connectivity(nxg))
    except:
        pass
    try:
        print("==========================================================================================================")
        print("Alternative Quantitative Intrinsic Merit  - Maxflow-Mincut of RGO Definition Graph - Minimum Edge Cut")
        print("==========================================================================================================")
        print(nx.minimum_edge_cut(nxg))
    except:
        pass
    try:
        print("==========================================================================================================")
        print("Alternative Quantitative Intrinsic Merit  - Maxflow-Mincut of RGO Definition Graph - Stoer-Wagner")
        print("==========================================================================================================")
        print(nx.stoer_wagner(nxg))
    except:
        pass
    try:
        print("==========================================================================================================")
        print("Alternative Quantitative Intrinsic Merit  - Average Clustering Coefficient")
        print("==========================================================================================================")
        print(nx.average_clustering(nxg))
    except:
        pass
    # try:
    #print "=========================================================================================================="
    #print "Alternative Quantitative Intrinsic Merit  - Junction Tree Width"
    #print "=========================================================================================================="
    #print TreeWidth.tree_width(nxg,3)
    # except:
    #	pass


if __name__ == "__main__":
    InterviewAlgorithm_main(sys.argv[1])
