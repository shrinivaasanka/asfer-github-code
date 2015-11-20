#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets
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
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

from __future__ import division
import pickle
import sys

import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import Queue
import operator
from nltk.corpus import sentiwordnet as swn
from nltk.book import *
from nltk.corpus import stopwords

definitiongraphedges=defaultdict(list)
definitiongraphedgelabels=defaultdict(list)
weight_str_map=defaultdict()

#########################################################################################################
#Related to publications:
#1. http://arxiv.org/abs/1006.4458
#2. http://www.nist.gov/tac/publications/2010/participant.papers/CMI_IIT.proceedings.pdf
#
#Constructs wordnet subgraph from documents using Recursive Gloss Overlap and does Sentiment Analysis
#from RGO graph
#########################################################################################################

def SentimentAnalysis_SentiWordNet(text):
        tokens=text.split()
	sumposscore=0.0
	sumnegscore=0.0
	sumobjscore=0.0
        for t in tokens:
                 sset = swn.senti_synsets(t.decode("utf-8"))
		 if len(sset) > 0:
                 	negscore = sset[0].neg_score()
                 	posscore = sset[0].pos_score()
			objscore = sset[0].obj_score()
                 	sumposscore+= posscore
                 	sumnegscore+= negscore
			sumobjscore+= objscore
	return (sumposscore, sumnegscore, sumobjscore)

def get_edge_lambda(f,t,nxg): 
	return " [lambda: " + f + " " + definitiongraphedgelabels[f + " - " + t][0] + " " + t + "]"

def composition_lambda(nxg):
	composition_lambda_str=""
	for k,v in nx.dfs_edges(nxg):
		composition_lambda_str="(" + composition_lambda_str + get_edge_lambda(k,v,nxg) + ")"
	return composition_lambda_str

def SentimentAnalysis_RGO_Belief_Propagation(nxg):
	#Bayesian Pearl Belief Propagation is done by
	#assuming the senti scores as probabilities with positive
	#and negative signs and the Recursive Gloss Overlap
	#definition graph being the graphical model.
	#Sentiment as a belief potential is passed through 
	#the DFS tree of this graph.  
	dfs_positive_belief_propagated=1.0
	core_positive_belief_propagated=1.0
	dfs_negative_belief_propagated=1.0
	core_negative_belief_propagated=1.0
	core_xnegscore=core_xposscore=1.0
	dfs_knegscore=dfs_kposscore=dfs_vposscore=dfs_vnegscore=1.0
	sorted_core_nxg=sorted(nx.core_number(nxg).items(),key=operator.itemgetter(1), reverse=True)
	kcore_nxg=nx.k_core(nxg,6,nx.core_number(nxg))
	for x in sorted_core_nxg:
	      xsset = swn.senti_synsets(x[0])
	      if len(xsset) > 2:
	     		core_xnegscore = float(xsset[0].neg_score())*10.0
	      		core_xposscore = float(xsset[0].pos_score())*10.0
	      if core_xnegscore == 0.0:
			core_xnegscore = 1.0
	      if core_xposscore == 0.0:
			core_xposscore = 1.0
	      core_positive_belief_propagated *= float(core_xposscore)
	      core_negative_belief_propagated *= float(core_xnegscore)
	print "Core Number: RGO_sentiment_analysis_belief_propagation: %f, %f" % (float(core_positive_belief_propagated), float(core_negative_belief_propagated))
	#for k,v in nx.dfs_edges(nxg):
	for k,v in nx.dfs_edges(kcore_nxg):
	      ksynset = swn.senti_synsets(k)
	      vsynset = swn.senti_synsets(v)
	      if len(ksynset) > 2:
	     		dfs_knegscore = float(ksynset[0].neg_score())*10.0
	      		dfs_kposscore = float(ksynset[0].pos_score())*10.0
	      if len(vsynset) > 2:
			dfs_vnegscore = float(vsynset[0].neg_score())*10.0
			dfs_vposscore = float(vsynset[0].pos_score())*10.0
	      dfs_kposscore_vposscore = float(dfs_kposscore*dfs_vposscore)
	      dfs_knegscore_vnegscore = float(dfs_knegscore*dfs_vnegscore)
	      if dfs_kposscore_vposscore == 0.0:
		dfs_kposscore_vposscore = 1.0
	      if dfs_knegscore_vnegscore == 0.0:
		dfs_knegscore_vnegscore = 1.0
	      dfs_positive_belief_propagated *= float(dfs_kposscore_vposscore)
	      dfs_negative_belief_propagated *= float(dfs_knegscore_vnegscore)
	print "K-Core DFS: RGO_sentiment_analysis_belief_propagation: %f, %f" % (float(dfs_positive_belief_propagated),float(dfs_negative_belief_propagated))
	return (dfs_positive_belief_propagated, dfs_negative_belief_propagated, core_positive_belief_propagated, core_negative_belief_propagated)
		

#function - compute_idf()
def compute_idf(corpus, keyword):
	import math
	total_occur = 0
	keyword_occur = 0
	for file in corpus:
		raw = open(file).read()
		tokens = nltk.word_tokenize(raw)
		total_occur = total_occur + len(tokens)
		keyword_occur = keyword_occur + len([w for w in tokens if w == keyword])
	return math.log(total_occur / (keyword_occur))

#parents (at level i-1) of a given vertex at level i
#arguments are a keyword at present level and all disambiguated synsets of previous level
def parents(keyword, prevlevelsynsets):
	parents = []
	for syn in prevlevelsynsets:
		if type(syn) is nltk.corpus.reader.wordnet.Synset:
			syndef_tokens = set(nltk.word_tokenize(syn.definition()))
			if keyword in syndef_tokens:
				parents = parents + [syn]
	#output.write('Parents of ' + keyword + ' are:\n')
	#pickle.dump(parents,output)
	#output.write('\n')
	return parents
	

#function - best_matching_synset()
def best_matching_synset(doc_tokens, synsets):
	#output.write('best_matching_synset():\n')
	maxmatch = -1
	retset = []
	for synset in synsets:
		def_tokens = set(nltk.word_tokenize(synset.definition()))
		intersection = def_tokens.intersection(doc_tokens)
		#output.write('--------------------')
		#output.write('intersection:\n')
		#pickle.dump(intersection, output)	
		#output.write('\n')
		#output.write('--------------------')
		if len(intersection) > maxmatch:
			maxmatch = len(intersection)
			retset = synset
	#output.write(retset.definition)
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
	intersect = len(set(shingles(refanswer)).intersection(set(shingles(candidanswer))))	
	return (intersect + 1) / (total + 1)

#get shingles
def shingles(phrase):
	return bigrams(nltk.word_tokenize(phrase))


def SentimentAnalysis_RGO(text,output):
	#---------------------------------------------------------------------------------
	#2.Compute intrinsic merit (either using linear or quadratic overlap)
	#---------------------------------------------------------------------------------
	tokenized = nltk.word_tokenize(text)
	fdist1 = FreqDist(tokenized)
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords = stopwords + [u'why',u'be',u'what',u' ',u'or',u'and',u'who',u'he',u'she',u'whom',u'well',u'is',u'was',u'were',u'are',u'there',u'where',u'when',u'may',u'might',u'would',u'shall',u'will',u'should',u'The', u'the', u'In',u'in',u'A',u'B',u'C',u'D',u'E',u'F',u'G',u'H',u'I',u'J',u'K',u'L',u'M',u'N',u'O',u'P',u'Q',u'R',u'S',u'T',u'U',u'V',u'W',u'X',u'Y',u'Z']
	puncts = [u' ',u'.', u'"', u',', u'{', u'}', u'+', u'-', u'*', u'/', u'%', u'&', u'(', ')', u'[', u']', u'=', u'@', u'#', u':', u'|', u';',u'\'s']
	#at present tfidf filter is not applied
	#freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w))]
	freqterms1 = [w.decode("utf-8") for w in fdist1.keys() if w not in stopwords and w not in puncts]
	
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

	#recurse down to required depth and update intrinsic merit score
	#relatedness is either sum(overlaps) or sum((overlapping_parents)*(overlaps)^2) also called convergence factor
	while current_level < 3:
		#crucial - gather nodes which converge/overlap (have more than 1 parent)
		if current_level > 1:
			print current_level
			for x in freqterms1:
				for y in parents(x,prevlevelsynsets):
					ylemmanames=y.lemma_names()
					for yl in ylemmanames:
						definitiongraphedges[x].append(yl)
						definitiongraphedgelabels[x + " - " + yl].append(" is a subinstance of ")
						definitiongraphedgelabels[yl + " - " + x].append(" is a superinstance of ")
						
			convergingterms = [w for w in freqterms1 if len(parents(w,prevlevelsynsets)) > 1]
			for kw in freqterms1:
				convergingparents = convergingparents + ([w for w in parents(kw, prevlevelsynsets) if len(parents(kw, prevlevelsynsets)) > 1])
			for kw in freqterms1:
				noofparents = len(parents(kw, prevlevelsynsets))
				if noofparents > maxparents:
					maxparents = noofparents
					nodewithmaxparents = kw
			output.write('converging terms(terms with more than 1 parent):\n ')
			#pickle.dump(convergingterms,output)
			output.write('\n')
			output.write('converging parents :\n')
			#pickle.dump(convergingparents,output)
			output.write('\n')
		for keyword in freqterms1:
			#WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset() 
			output.write('===============================================\n')
			#output.write('keyword : ' + keyword.decode("utf-8"))
			#output.write('\n')
			#disamb_synset = best_matching_synset(set(doc1), wn.synsets(keyword))
			disamb_synset = best_matching_synset(freqterms1, wn.synsets(keyword))
			prevlevelsynsets = prevlevelsynsets + [disamb_synset]
			output.write('prevlevelsynsets:\n')
			#pickle.dump(prevlevelsynsets, output)
			output.write('\n')
			output.write('matching synset:\n')
			#pickle.dump( disamb_synset,output)
			output.write('\n')
			if len(wn.synsets(keyword)) != 0:
				disamb_synset_def = disamb_synset.definition()
				tokens = nltk.word_tokenize(disamb_synset_def) 
				fdist_tokens = FreqDist(tokens)
				#at present frequency filter is not applied
				#if keyword in convergingterms:
				tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])
		output.write('At level:\n')
		output.write(str(current_level))
		output.write('\n')
		output.write('tokens grasped at this level:\n')
		#pickle.dump(tokensofthislevel, output)
		output.write('\n')
		listcount = len(tokensofthislevel)
		setcount = len(set(tokensofthislevel))
		overlap =  listcount-setcount
		if overlap > 0 and iter == 0 :
			first_convergence_level = current_level
			iter = 1
		#choose between two relatedness/convergence criteria :- 
		#1) simple linear overlap or 2) zipf distributed quadratic overlap
		#relatedness = relatedness + len(convergingparents)*overlap 
		relatedness = relatedness + overlap + len(convergingparents)
		#relatedness = relatedness + ((len(convergingparents)*overlap*overlap) + 1) 
		#find out common tokens of this and previous level so that same token does not get grasped again - 	
		#relatedness must be increased since repetition of keywords in two successive levels is a sign of 
		#interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 					#corresponding to common tokens
		commontokens = set(tokensofthislevel).intersection(set(tokensofprevlevel))
		tokensofthislevel = set(tokensofthislevel).difference(commontokens)
		relatedness = relatedness + len(commontokens)
		output.write('removing tokens already grasped:\n')
		#pickle.dump(commontokens,output)
		output.write('\n')
		output.write('Relatedness:\n')
		output.write(str(relatedness))
		output.write('\n')
		#decrease the vertices count to address common tokens removed above - edges should remain same since they 
		#would just point elsewhere
		vertices = vertices + setcount - len(commontokens)
		output.write('Vertices:\n')
		output.write(str(vertices))
		output.write('\n')
		edges = edges + listcount
		output.write('Edges:\n')
		output.write(str(edges))
		output.write('\n')
		current_level = current_level + 1
		freqterms1 = set(tokensofthislevel)
		tokensofprevlevel = tokensofthislevel
		tokensofthislevel = []
	
	intrinsic_merit = vertices*edges*relatedness / first_convergence_level
	output.write('Intrinsic merit of this document is:\n')
	output.write(str(intrinsic_merit))
	output.write('\n')
	output.write('Node with maximum parents (and hence the most likely class of document) is:\n')
	output.write(nodewithmaxparents)
	output.write('\n')

	print definitiongraphedges

	nxg=nx.DiGraph()
	#pos=nx.spring_layout(nxg)
	#pos=nx.shell_layout(nxg)
	#pos=nx.random_layout(nxg)
	#weight_str_map={}
	pos=nx.spectral_layout(nxg)
	for k,v in definitiongraphedges.iteritems():
		for l in v:
			nxg.add_edge(k,l)
			nxg.add_edge(l,k)
			ksynset=wn.synsets(k)
			lsynset=wn.synsets(l)
			if ksynset and lsynset:
				print "ksynset=",ksynset[0]
				print "lsynset=",lsynset[0]
				hypoksynsets=set([i for i in ksynset[0].closure(lambda n:n.hyponyms())])
				hyperlsynsets=set([i for i in lsynset[0].closure(lambda n:n.hypernyms())])
				for m in hypoksynsets:
					try:
						mlemmanames=m.lemma_names()
						weight_str_map[k+" - "+l]=weight_str_map[k+" - "+l]+" contains "+mlemmanames[0]
					except KeyError:
						weight_str_map[k+" - "+l]=""
				for n in hyperlsynsets:
					try:
						nlemmanames=n.lemma_names()
						weight_str_map[l+" - "+k]=weight_str_map[l+" - "+k]+" is part of "+nlemmanames[0]
					except KeyError:
						weight_str_map[l+" - "+k]=""
	
	#nx.dra	w_graphviz(nxg,prog="neato")
	nx.draw_networkx(nxg)
	plt.show()
	nxg.remove_edges_from(nxg.selfloop_edges())
	#print "Core number =",nx.core_number(nxg)
	sorted_core_nxg=sorted(nx.core_number(nxg).items(),key=operator.itemgetter(1), reverse=True)
	print "Core number (sorted) :",sorted_core_nxg
	print "============================================================================================================="
	print "Unsupervised Classification based on top percentile Core numbers of the definition graph(subgraph of WordNet)"
	print "============================================================================================================="
	no_of_classes=len(nx.core_number(nxg))
	top_percentile=0
	max_core_number=0
	for n in sorted_core_nxg:
		print "This document belongs to class:",n[0],",core number=",n[1]
		if top_percentile < no_of_classes*0.10:
			top_percentile+=1
		else:	
			break
		if n[1] > max_core_number:
			max_core_number=n[1]
	print "	max_core_number",max_core_number
	
	print "==================================================================="
	print "Page Rank of the vertices of RGO Definition Graph"
	print "==================================================================="
	print sorted(nx.pagerank(nxg).items(),key=operator.itemgetter(1),reverse=True)

	#print "================================================================================"
	#print "A primitive text generated from traversal of the k-core closure of RGO Definition Graph"
	#print "================================================================================"
	#kcore_nxg=nx.k_core(nxg,10,nx.core_number(nxg))
	#kcore_nxg=nx.k_core(nxg)
	#for k,v in kcore_nxg.edges():
	#	print k, weight_str_map[k+" - "+v], v, ".",

	#print "\n"
	#print "=============================================================================="
	#print "Lambda Composition Closure with Depth First Search of RGO graph edges as relations"
	#print "=============================================================================="
	#print definitiongraphedgelabels
	#lambda_vertex_map={}
	#lambda_edge_map={}

	#print composition_lambda(nxg)

	print "=============================================================================="
	print "Sentiment Analysis (Applying SentiWordNet to the tokenized text) of the text"
	print "=============================================================================="
	pos,neg,obj = SentimentAnalysis_SentiWordNet(text)
	print "Positivity = ", pos
	print "Negativity = ", neg
	print "Objectivity = ",obj

	print "=========================================================================================================="
	print "Sentiment Analysis (Applying SentiWordNet to the top core-numbered words in RGO graph of text) of the text"
	print "=========================================================================================================="
	for x in sorted_core_nxg:
	      xsset = swn.senti_synsets(x[0])
	      if len(xsset) > 2:
	     		xnegscore = xsset[0].neg_score()
	      		xposscore = xsset[0].pos_score()
      			print "negscore of ", x[0], ": ", xnegscore
		        print "posscore of ", x[0], ": ", xposscore
	
	return nxg

if __name__=="__main__":
	#----------------------------------------------
	#1.Get the input documents
	#----------------------------------------------
	corpus = [sys.argv[1]]
	#get keywords
	files = [sys.argv[1]]
	outputfile = 'Output-SentimentAnalyzer-WebSpider.txt'
	output = open(outputfile, 'w')
	file1 = open(files[0])
	text = file1.read()
	nxg=SentimentAnalysis_RGO(text,output)
	print "=========================================================================================================="
	print "Sentiment Analysis (Belief Propagation of Sentiment in the RGO graph) of the text"
	print "=========================================================================================================="
	dfs_belief_propagated_posscore, dfs_belief_propagated_negscore, core_belief_propagated_posscore, core_belief_propagated_negscore = SentimentAnalysis_RGO_Belief_Propagation(nxg)
	print "DFS belief_propagated_posscore:",float(dfs_belief_propagated_posscore)
	print "DFS belief_propagated_negscore:",float(dfs_belief_propagated_negscore)
	print "Core Number belief_propagated_posscore:",float(core_belief_propagated_posscore)
	print "Core Number belief_propagated_negscore:",float(core_belief_propagated_negscore)

