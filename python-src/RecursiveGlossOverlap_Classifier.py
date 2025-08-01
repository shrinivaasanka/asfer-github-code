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
# Copyleft (Copyright+):
# Srinivasan Kannan
# (also known as: Shrinivaasan Kannan, Shrinivas Kannan)
# Ph: 9791499106, 9003082186
# Krishna iResearch Open Source Products Profiles:
# http://sourceforge.net/users/ka_shrinivaasan,
# https://github.com/shrinivaasanka,
# https://www.openhub.net/accounts/ka_shrinivaasan
# Personal website(research): https://sites.google.com/site/kuja27/
# emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
# kashrinivaasan@live.com
# -----------------------------------------------------------------------------------------------------------------------------------


import pickle
import sys

import nltk
#from pywsd.lesk import simple_lesk
#from pywsd.lesk import extended_lesk
from nltk.wsd import lesk
from collections import defaultdict
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import queue
import operator
from nltk.corpus import sentiwordnet as swn
from nltk.book import *
from nltk.corpus import stopwords
from PyDictionary import PyDictionary
from WordNetPath import path_between

definitiongraphedges = defaultdict(list)
definitiongraphedgelabels = defaultdict(list)
dictionary = PyDictionary()

# reload(sys)
# sys.setdefaultencoding("utf8")

#########################################################################################################
# Related to publications:
# 1. http://arxiv.org/abs/1006.4458
# 2. http://www.nist.gov/tac/publications/2010/participant.papers/CMI_IIT.proceedings.pdf
#
# Constructs wordnet subgraph from documents using Recursive Gloss Overlap and does Sentiment Analysis
# from RGO graph
#########################################################################################################

use_pywsd_lesk = False
use_nltk_lesk = False
#function - compute_idf()

def wordnet_path_meaningfulness(sentence):
    words = sentence.split(" ")
    wordnetpathmeaningfulness=[]
    for w in range(len(words)-1):
        w1 = words[w]
        w2 = words[w+1]
        if len(w1) > 0 and len(w2) > 0:
            wordnet_distance = path_between(w1,w2) 
            print("wordnet_path between ",w1," and ",w2,":",wordnet_distance)
            wordnetpathmeaningfulness = wordnetpathmeaningfulness + wordnet_distance
    return len(wordnetpathmeaningfulness)

def compute_idf(corpus, keyword):
    import math
    total_occur = 0
    keyword_occur = 0
    for file in corpus:
        raw = open(file).read()
        tokens = nltk.word_tokenize(raw)
        total_occur = total_occur + len(tokens)
        keyword_occur = keyword_occur + \
            len([w for w in tokens if w == keyword])
    return math.log(total_occur / (keyword_occur))

# parents (at level i-1) of a given vertex at level i
# arguments are a keyword at present level and all disambiguated synsets of previous level


def parents(keyword, prevlevelsynsets):
    parents = []
    for syn in prevlevelsynsets:
        if type(syn) is nltk.corpus.reader.wordnet.Synset:
            syndef_tokens = set(nltk.word_tokenize(syn.definition()))
            if keyword in syndef_tokens:
                parents = parents + [syn]
    #output.write('Parents of ' + keyword + ' are:\n')
    # pickle.dump(parents,output)
    # output.write('\n')
    return parents


#function - best_matching_synset()
def best_matching_synset(doc_tokens, synsets):
    # output.write('best_matching_synset():\n')
    maxmatch = -1
    retset = []
    for synset in synsets:
        def_tokens = set(nltk.word_tokenize(synset.definition()))
        intersection = def_tokens.intersection(doc_tokens)
        # output.write('--------------------')
        # output.write('intersection:\n')
        #pickle.dump(intersection, output)
        # output.write('\n')
        # output.write('--------------------')
        if len(intersection) > maxmatch:
            maxmatch = len(intersection)
            retset = synset
    # output.write(retset.definition)
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

#function - get_jaccard_coefficient()


def get_jaccard_coefficient(refanswer, candidanswer):
    total = len(set(shingles(refanswer) + shingles(candidanswer)))
    intersect = len(set(shingles(refanswer)).intersection(
        set(shingles(candidanswer))))
    return (intersect + 1) / (total + 1)

# get shingles


def shingles(phrase):
    return bigrams(nltk.word_tokenize(phrase))


def nondictionaryword(w):
    mean = dictionary.meaning(w)
    #print mean
    if mean is not None and len(mean) > 0:
        return False
    else:
        return True


def RecursiveGlossOverlapGraph(text, level=3):
    definitiongraphedges = defaultdict(list)
    definitiongraphedgelabels = defaultdict(list)

    # ---------------------------------------------------------------------------------
    # 2.Compute intrinsic merit (either using linear or quadratic overlap)
    # ---------------------------------------------------------------------------------
    tokenized = nltk.word_tokenize(text)
    fdist1 = FreqDist(tokenized)
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + [' ', 'or', 'and', 'who', 'he', 'she', 'whom', 'well', 'is', 'was', 'were', 'are', 'there', 'where', 'when', 'may', 'The',
                             'the', 'In', 'in', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    puncts = [' ', '.', '"', ',', '{', '}', '+', '-', '*', '/', '%',
              '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';', '\'s']
    # at present tfidf filter is not applied
    #freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w))]
    #freqterms1 = [w.decode("utf-8","ignore") for w in fdist1.keys() if w not in stopwords and w not in puncts and not nondictionaryword(w)]
    #freqterms1 = [w.decode("utf-8","ignore") for w in list(fdist1.keys()) if w not in stopwords and w not in puncts]
    freqterms1 = [w for w in list(fdist1.keys())
                  if w not in stopwords and w not in puncts]

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
    from nltk.corpus import wordnet as wn

    # recurse down to required depth and update intrinsic merit score
    # relatedness is either sum(overlaps) or sum((overlapping_parents)*(overlaps)^2) also called convergence factor
    while current_level < level:
        # crucial - gather nodes which converge/overlap (have more than 1 parent)
        if current_level > 1:
            print(current_level)
            for x in freqterms1:
                for y in parents(x, prevlevelsynsets):
                    ylemmanames = y.lemma_names()
                    # for yl in ylemmanames:
                    #	definitiongraphedges[x].append(yl)
                    definitiongraphedges[x].append(ylemmanames[0])
                    definitiongraphedgelabels[x + " - " +
                                              ylemmanames[0]].append(" is a subinstance of ")
                    definitiongraphedgelabels[ylemmanames[0] +
                                              " - " + x].append(" is a superinstance of ")

            convergingterms = [w for w in freqterms1 if len(
                parents(w, prevlevelsynsets)) > 1]
            for kw in freqterms1:
                convergingparents = convergingparents + \
                    ([w for w in parents(kw, prevlevelsynsets)
                      if len(parents(kw, prevlevelsynsets)) > 1])
            for kw in freqterms1:
                noofparents = len(parents(kw, prevlevelsynsets))
                if noofparents > maxparents:
                    maxparents = noofparents
                    nodewithmaxparents = kw
        for keyword in freqterms1:
            # WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset()
            #disamb_synset = best_matching_synset(set(doc1), wn.synsets(keyword))
            if use_pywsd_lesk:
                disamb_synset = simple_lesk(" ".join(freqterms1), keyword)
            if use_nltk_lesk:
                disamb_synset = lesk(freqterms1, keyword)
            else:
                disamb_synset = best_matching_synset(
                    freqterms1, wn.synsets(keyword))
            prevlevelsynsets = prevlevelsynsets + [disamb_synset]
            if len(wn.synsets(keyword)) != 0:
                disamb_synset_def = disamb_synset.definition()
                tokens = nltk.word_tokenize(disamb_synset_def)
                fdist_tokens = FreqDist(tokens)
                # at present frequency filter is not applied
                # if keyword in convergingterms:
                tokensofthislevel = tokensofthislevel + \
                    ([w for w in list(fdist_tokens.keys(
                    )) if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])
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
        # interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 			#corresponding to common tokens
        commontokens = set(tokensofthislevel).intersection(
            set(tokensofprevlevel))
        tokensofthislevel = set(tokensofthislevel).difference(commontokens)
        relatedness = relatedness + len(commontokens)
        # decrease the vertices count to address common tokens removed above - edges should remain same since they
        # would just point elsewhere
        vertices = vertices + setcount - len(commontokens)
        edges = edges + listcount
        current_level = current_level + 1
        freqterms1 = set(tokensofthislevel)
        tokensofprevlevel = tokensofthislevel
        tokensofthislevel = []

    intrinsic_merit = vertices*edges*relatedness / first_convergence_level

    nxg = nx.DiGraph()
    #pos = nx.spring_layout(nxg)
    # pos=nx.shell_layout(nxg)
    # pos=nx.random_layout(nxg)
    # pos=nx.spectral_layout(nxg)
    # nx.draw_graphviz(nxg,prog="neato")
    for k, v in list(definitiongraphedges.items()):
        for l in v:
            nxg.add_edge(k, l)
            nxg.add_edge(l, k)
    # nx.draw_networkx(nxg)
    # plt.show()

    # nxg.remove_edges_from(nxg.selfloop_edges())
    print("RecursiveGlossOverlapGraph(): textgraph = ",nxg.edges())
    ret=(nxg, intrinsic_merit)
    return ret


def RecursiveGlossOverlap_Classify(text,maxfractionclasses=1):
    print("Text to RecursiveGlossOverlap_Classify:",text)
    definitiongraphedges = defaultdict(list)
    definitiongraphedgelabels = defaultdict(list)

    # ---------------------------------------------------------------------------------
    # 2.Compute intrinsic merit (either using linear or quadratic overlap)
    # ---------------------------------------------------------------------------------
    tokenized = nltk.word_tokenize(text)
    fdist1 = FreqDist(tokenized)
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords + [' ', 'or', 'and', 'who', 'he', 'she', 'whom', 'well', 'is', 'was', 'were', 'are', 'there', 'where', 'when', 'may', 'The',
                             'the', 'In', 'in', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    puncts = [' ', '.', '"', ',', '{', '}', '+', '-', '*', '/', '%',
              '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';', '\'s']
    # at present tfidf filter is not applied
    #freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w))]
    #freqterms1 = [w.decode("utf-8") for w in list(fdist1.keys()) if w not in stopwords and w not in puncts]
    freqterms1 = [w for w in list(fdist1.keys())
                  if w not in stopwords and w not in puncts]

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
    from nltk.corpus import wordnet as wn

    # recurse down to required depth and update intrinsic merit score
    # relatedness is either sum(overlaps) or sum((overlapping_parents)*(overlaps)^2) also called convergence factor
    while current_level < 3:
        # crucial - gather nodes which converge/overlap (have more than 1 parent)
        if current_level > 1:
            print(current_level)
            for x in freqterms1:
                for y in parents(x, prevlevelsynsets):
                    ylemmanames = y.lemma_names()
                    # for yl in ylemmanames:
                    #	definitiongraphedges[x].append(yl)
                    definitiongraphedges[x].append(ylemmanames[0])
                    definitiongraphedgelabels[x + " - " +
                                              ylemmanames[0]].append(" is a subinstance of ")
                    definitiongraphedgelabels[ylemmanames[0] +
                                              " - " + x].append(" is a superinstance of ")

            convergingterms = [w for w in freqterms1 if len(
                parents(w, prevlevelsynsets)) > 1]
            for kw in freqterms1:
                convergingparents = convergingparents + \
                    ([w for w in parents(kw, prevlevelsynsets)
                      if len(parents(kw, prevlevelsynsets)) > 1])
            for kw in freqterms1:
                noofparents = len(parents(kw, prevlevelsynsets))
                if noofparents > maxparents:
                    maxparents = noofparents
                    nodewithmaxparents = kw
        for keyword in freqterms1:
            # WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset()
            #disamb_synset = best_matching_synset(set(doc1), wn.synsets(keyword))
            if use_pywsd_lesk:
                disamb_synset = simple_lesk(" ".join(freqterms1), keyword)
            if use_nltk_lesk:
                disamb_synset = lesk(freqterms1, keyword)
            else:
                disamb_synset = best_matching_synset(
                    freqterms1, wn.synsets(keyword))
            prevlevelsynsets = prevlevelsynsets + [disamb_synset]
            if len(wn.synsets(keyword)) != 0:
                disamb_synset_def = disamb_synset.definition()
                tokens = nltk.word_tokenize(disamb_synset_def)
                fdist_tokens = FreqDist(tokens)
                # at present frequency filter is not applied
                # if keyword in convergingterms:
                tokensofthislevel = tokensofthislevel + \
                    ([w for w in list(fdist_tokens.keys(
                    )) if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])
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
        tokensofthislevel = set(tokensofthislevel).difference(commontokens)
        relatedness = relatedness + len(commontokens)
        # decrease the vertices count to address common tokens removed above - edges should remain same since they
        # would just point elsewhere
        vertices = vertices + setcount - len(commontokens)
        edges = edges + listcount
        current_level = current_level + 1
        freqterms1 = set(tokensofthislevel)
        tokensofprevlevel = tokensofthislevel
        tokensofthislevel = []

    intrinsic_merit = vertices*edges*relatedness / first_convergence_level

    print(definitiongraphedges)

    nxg = nx.DiGraph()
    # pos=nx.spring_layout(nxg)
    # pos=nx.shell_layout(nxg)
    # pos=nx.random_layout(nxg)
    # pos=nx.spectral_layout(nxg)
    # nx.draw_graphviz(nxg,prog="neato")
    for k, v in list(definitiongraphedges.items()):
        for l in v:
            nxg.add_edge(k, l)
            nxg.add_edge(l, k)
    print(("definitiongraph networkx edges:", nxg.edges))
    #nx.draw_networkx(nxg)
    #plt.show()

    nxg.remove_edges_from(nx.selfloop_edges(nxg))
    #print "Core number =",nx.core_number(nxg)
    sorted_core_nxg = sorted(
        list(nx.core_number(nxg).items()), key=operator.itemgetter(1), reverse=True)
    print(("Core number (sorted) :", sorted_core_nxg))
    print("=============================================================================================================")
    print("Unsupervised Classification based on top percentile Core numbers of the definition graph(subgraph of WordNet)")
    print("=============================================================================================================")
    no_of_classes = len(nx.core_number(nxg))
    top_percentile = 0
    max_core_number = 0
    max_core_number_class = ""
    core_meaningfulness = 1
    for n in sorted_core_nxg:
        print(("This document belongs to class:", n[0], ",core number=", n[1]))
        if top_percentile <= no_of_classes*maxfractionclasses:
            top_percentile += 1
        else:
            break
        if n[1] > max_core_number:
            max_core_number = n[1]
            max_core_number_class = n[0]
        core_meaningfulness = core_meaningfulness * n[1]
    print("=============================================================================================================")
    print("Core Meaningfulness of the text:")
    print("=============================================================================================================")
    print("Core meaningfulness of the text:",core_meaningfulness)
    print(("	max_core_number", max_core_number))
    print("=============================================================================================================")
    print("WordNet Path Meaningfulness of the text:")
    print("=============================================================================================================")
    wordnetpathmeaningfulness=wordnet_path_meaningfulness(text)
    print("wordnet path meaningfulness:",wordnetpathmeaningfulness)
    print("===================================================================")
    print("Betweenness Centrality of Recursive Gloss Overlap graph vertices")
    print("===================================================================")
    bc = nx.betweenness_centrality(nxg)
    sorted_bc = sorted(
        list(bc.items()), key=operator.itemgetter(1), reverse=True)
    print(sorted_bc)

    print("===================================================================")
    print("Closeness Centrality of Recursive Gloss Overlap graph vertices")
    print("===================================================================")
    cc = nx.closeness_centrality(nxg)
    sorted_cc = sorted(
        list(cc.items()), key=operator.itemgetter(1), reverse=True)
    print(sorted_cc)

    print("===================================================================")
    print("Degree Centrality of Recursive Gloss Overlap graph vertices")
    print("===================================================================")
    dc = nx.degree_centrality(nxg)
    sorted_dc = sorted(
        list(dc.items()), key=operator.itemgetter(1), reverse=True)
    print(sorted_dc)

    print("===================================================================")
    print("Page Rank of the vertices of RGO Definition Graph (a form of Eigenvector Centrality)")
    print("===================================================================")
    sorted_pagerank_nxg = sorted(
        list(nx.pagerank(nxg).items()), key=operator.itemgetter(1), reverse=True)
    print(sorted_pagerank_nxg)
    return (sorted_core_nxg, sorted_pagerank_nxg)


if __name__ == "__main__":
    # ----------------------------------------------
    # 1.Get the input documents
    # ----------------------------------------------
    corpus = [sys.argv[1]]
    # get keywords
    file1 = open(corpus[0])
    text = file1.read()
    classified = RecursiveGlossOverlap_Classify(text)
    print(("__main__(): This text belongs to classes:", classified))
