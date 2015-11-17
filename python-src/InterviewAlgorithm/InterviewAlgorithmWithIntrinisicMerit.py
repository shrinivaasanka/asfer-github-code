#-------------------------------------------------------------------------`
#ASFER - a ruleminer which gets rules specific to a query and executes them
#
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
#
#-----------------------------------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

#########################################################################################################
#Old version of Example Python code written more than 3 years ago in January 2010 during MSc thesis at IIT Chennai 
#for Intrinsic Merit computation and Interview Algorithm 
#For publications:
#1. http://arxiv.org/abs/1006.4458
#2. http://www.nist.gov/tac/publications/2010/participant.papers/CMI_IIT.proceedings.pdf
#
#Constructs wordnet subgraph from documents and computes similarity measures like edit distance
#########################################################################################################

from __future__ import division
import pickle
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
			syndef_tokens = set(nltk.word_tokenize(syn.definition))
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
		def_tokens = set(nltk.word_tokenize(synset.definition))
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

#----------------------------------------------
#1.Get the input documents
#----------------------------------------------

corpus = ['/media/disk/CMI-related/ThesisDemo-english-test1.txt','/media/disk/CMI-related/ThesisDemo-english-test2.txt','/media/disk/CMI-related/ThesisDemo-english-test3.txt','/media/disk/CMI-related/ThesisDemo-carrace-test1.txt','/media/disk/CMI-related/ThesisDemo-carrace-test2.txt','/media/disk/CMI-related/ThesisDemo-carrace-test3.txt','/media/disk/CMI-related/ThesisDemo-datamining-test1.txt','/media/disk/CMI-related/ThesisDemo-datamining-test2.txt','/media/disk/CMI-related/ThesisDemo-datamining-test3.txt','/media/disk/CMI-related/ThesisDemo-datamining-test4.txt','/media/disk/CMI-related/ThesisDemo-datamining-test5.txt','/media/disk/CMI-related/ThesisDemo-graphtheory-test1.txt','/media/disk/CMI-related/ThesisDemo-graphtheory-test2.txt','/media/disk/CMI-related/ThesisDemo-graphtheory-test3.txt','/media/disk/CMI-related/ThesisDemo-fermatslasttheorem-test16.txt','/media/disk/CMI-related/ThesisDemo-fermatslasttheorem-test17.txt','/media/disk/CMI-related/ThesisDemo-car-test1.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt']
#get keywords

import nltk
files = ['ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt']


"""
#---------------------------------------------------------------------------------
#2.Compute intrinsic merit (either using linear or quadratic overlap)
#---------------------------------------------------------------------------------

for filestr in files:
	filestrtok = filestr.split('-')
	outputfile = 'Output-' + filestrtok[1] + '-' + filestrtok[2]
	output = open(outputfile, 'w')
	file1 = open(filestr)
	raw1 = file1.read()
	doc1 = nltk.word_tokenize(raw1)
	from nltk.book import *
	from nltk.corpus import stopwords
	fdist1 = FreqDist(doc1)
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords = stopwords + ['may', 'The', 'the', 'In', 		'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
	#at present tfidf filter is not applied
	freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w))]

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
			output.write('keyword : ' + keyword)
			output.write('\n')
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
				disamb_synset_def = disamb_synset.definition
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
		#interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 			#corresponding to common tokens
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
"""	
#--------------------------------
#3. Interview Algorithm
#--------------------------------
"""
references = ['ThesisDemo-carrace-test1.txt']
candidate = ['ThesisDemo-carrace-test2.txt']
queries = []
stopwords = nltk.corpus.stopwords.words('english')
stopwords = stopwords + ['may', 'The', 'the', 'In', 		'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
from nltk.book import *
for filestr in references:
	file1 = open(filestr)
	filecontents = file1.read()	
	filetokens = nltk.word_tokenize(filecontents)
	freqdist = FreqDist(filetokens)	
	queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and freqdist.freq(w) * compute_idf(corpus, w) > 0.1]

print 'Most important tokens/ngrams = queries :'
print queries

ref_qandamap={}
candid_qandamap={}
for q in queries:
	ref_qandamap[q] = get_context(q, references)

candid_file = open(candidate[0])
candid_file_contents = candid_file.read()
candid_tokens = nltk.word_tokenize(candid_file_contents)
candid_text = nltk.Text(candid_tokens)
for q in queries:
	#print '--------------------------------'
	#print 'concordance for :' + q
	#candid_text.concordance(q)
	#print '--------------------------------'
	candid_qandamap[q] = get_context(q, candidate)

print 'reference:'
print ref_qandamap
print 'candidate:'
print candid_qandamap

#compute jaccard coefficient score for each question and answer
scores=[]
i=0
for q in queries:
	print 'q = ' + q
	scores.append(get_jaccard_coefficient(ref_qandamap[q], candid_qandamap[q]))

x=0
sumscore = 0
for x in scores:
	sumscore = sumscore + x

print 'Interview score:'
print sumscore
"""
#--------------------------------------------------------------------------------------------------------------------
#4.Compute Value Addition applying edit distance between definition-graph(reference) and definition-graph(candidate)
#at present limited to 1 reference which will be updated after interview algorithm finishes if necessary
#--------------------------------------------------------------------------------------------------------------------
references = ['ThesisDemo-newsmodipranab-test1.txt']
candidate = ['ThesisDemo-newsmodipranab-test2.txt']

ref_file = open(references[0])
candid_file = open(candidate[0])
ref_file_contents = ref_file.read()
candid_file_contents = candid_file.read()
ref_tokens = nltk.word_tokenize(ref_file_contents)
candid_tokens = nltk.word_tokenize(candid_file_contents)
from nltk.book import *
from nltk.corpus import stopwords
reffdist = FreqDist(ref_tokens)
candidfdist = FreqDist(candid_tokens)
stopwords = nltk.corpus.stopwords.words('english')
stopwords = stopwords + ['may', 'The', 'the', 'In', 	'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
#at present tfidf filter is not applied
reffreqterms = [w for w in reffdist.keys() if w not in stopwords and w not in puncts and (reffdist.freq(w) * compute_idf(corpus, w))]
candfreqterms = [w for w in candidfdist.keys() if w not in stopwords and w not in puncts and (candidfdist.freq(w) * compute_idf(corpus, w))]

refkeyword = ''
candkeyword = ''
current_level = 1
editdistance = 0
reftokensofthislevel = []
candtokensofthislevel = []
reftokensofprevlevel = []
candtokensofprevlevel = []
refcommontokens = []
candcommontokens = []
refprevlevelsynsets = []
candprevlevelsynsets = []
ref_definitiongraphedges = []
cand_definitiongraphedges = []
from nltk.corpus import wordnet as wn

#recurse down to required depth and update edit distance between reference and candidate documents
while current_level < 3:
	if current_level > 1:
		for kw in reffreqterms:
				refparents = parents(kw, refprevlevelsynsets)
				for p in refparents:
					ref_definitiongraphedges.append((kw, p))
		for kw in candfreqterms:
				candparents = parents(kw, candprevlevelsynsets)
				for p in candparents:
					cand_definitiongraphedges.append((kw, p))
		print 'Current level:'
		print current_level
		print 'Reference DefGraph:'
		print ref_definitiongraphedges
		print 'Candidate DefGraph:'
		print cand_definitiongraphedges
	#for refkeyword, candkeyword in reffreqterms, candfreqterms:
	reffreqtermscount = 0
	candfreqtermscount = 0
	while reffreqtermscount < len(reffreqterms) or candfreqtermscount < len(candfreqterms):
		#WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset() 
		if reffreqtermscount < len(reffreqterms):
			refdisamb_synset = best_matching_synset(reffreqterms, wn.synsets(list(reffreqterms)[reffreqtermscount]))
			print refdisamb_synset
			refprevlevelsynsets = refprevlevelsynsets + [refdisamb_synset]
		if candfreqtermscount < len(candfreqterms):
			canddisamb_synset = best_matching_synset(candfreqterms, wn.synsets(list(candfreqterms)[candfreqtermscount]))
			print canddisamb_synset
			candprevlevelsynsets = candprevlevelsynsets + [canddisamb_synset]
		if reffreqtermscount < len(reffreqterms) and len(wn.synsets(list(reffreqterms)[reffreqtermscount])) != 0:
			refdisamb_synset_def = refdisamb_synset.definition
			reftokens = nltk.word_tokenize(refdisamb_synset_def)
			reffdist_tokens = FreqDist(reftokens)
			#at present frequency filter is not applied
			#if keyword in convergingterms:
			reftokensofthislevel = reftokensofthislevel + ([w for w in reffdist_tokens.keys() if w not in stopwords and w not in puncts and reffdist_tokens.freq(w)])
		if candfreqtermscount < len(candfreqterms) and len(wn.synsets(list(candfreqterms)[candfreqtermscount])) != 0:
			canddisamb_synset_def = canddisamb_synset.definition
			candtokens = nltk.word_tokenize(canddisamb_synset_def) 
			canddist_tokens = FreqDist(candtokens)
			#at present frequency filter is not applied
			#if keyword in convergingterms:
			candtokensofthislevel = candtokensofthislevel + ([w for w in canddist_tokens.keys() if w not in stopwords and w not in puncts and canddist_tokens.freq(w)])
		reffreqtermscount = reffreqtermscount + 1
		candfreqtermscount = candfreqtermscount + 1
	reflistcount = len(reftokensofthislevel)
	candlistcount = len(candtokensofthislevel)
	refsetcount = len(set(reftokensofthislevel))
	candsetcount = len(set(candtokensofthislevel))
	#find out common tokens of this and previous level so that same token does not get grasped again - 	
	#relatedness must be increased since repetition of keywords in two successive levels is a sign of 
	#interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 		#corresponding to common tokens
	refcommontokens = set(reftokensofthislevel).intersection(set(reftokensofprevlevel))
	candcommontokens = set(candtokensofthislevel).intersection(set(candtokensofprevlevel))
	reftokensofthislevel = set(reftokensofthislevel).difference(refcommontokens)
	candtokensofthislevel = set(candtokensofthislevel).difference(candcommontokens)
	current_level = current_level + 1
	reffreqterms = set(reftokensofthislevel)
	candfreqterms = set(candtokensofthislevel)
	reftokensofprevlevel = reftokensofthislevel
	candtokensofprevlevel = candtokensofthislevel
	reftokensofthislevel = []
	candtokensofthislevel = []
for kw in reffreqterms:
	refparents = parents(kw, refprevlevelsynsets)
	for p in refparents:
		ref_definitiongraphedges.append((kw, p))
for kw in candfreqterms:
	candparents = parents(kw, candprevlevelsynsets)
	for p in candparents:
		cand_definitiongraphedges.append((kw, p))
print 'Current level:'
print current_level
print 'Reference DefGraph:'
print ref_definitiongraphedges
print 'Candidate DefGraph:'
print cand_definitiongraphedges

#value addition - edges present in candidate but not in reference
valueaddition = set(cand_definitiongraphedges).difference(set(ref_definitiongraphedges))
#edit distance - edges added + edges removed
editdistance = editdistance + len(set(cand_definitiongraphedges).difference(set(ref_definitiongraphedges))) + len(set(ref_definitiongraphedges).difference(set(cand_definitiongraphedges)))
print 'Value addition:'
print valueaddition
print 'Edit Distance:'
print editdistance

