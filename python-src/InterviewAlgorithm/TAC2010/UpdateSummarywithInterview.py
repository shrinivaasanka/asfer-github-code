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

from __future__ import division
import pickle
from nltk.book import *

import os.path
import sys

#function - reuters_compute_idf()
def reuters_compute_idf(corpus, keyword):
	import math
	total_occur = 0
	keyword_occur = 0
	for file in corpus[:250]:
		tokens = reuters.words(file)
		total_occur = total_occur + 1
		keyword_occur = keyword_occur + len(set([w for w in tokens if w == keyword]))
	if keyword_occur == 0:
		keyword_occur = 1
	return math.log(total_occur / (keyword_occur))

#function - compute_idf()
def compute_idf(corpus, keyword):
	basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/"
	import math
	total_occur = 0
	keyword_occur = 0
	for file in corpus:
		raw = open(os.path.join(basepath,file)).read()
		tokens = nltk.word_tokenize(raw)
		total_occur = total_occur + 1
		keyword_occur = keyword_occur + len(set([w for w in tokens if w == keyword]))
	if keyword_occur == 0:
		keyword_occur = 1
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
	#print 'Parents of ' + keyword + ' are:\n 
	#pickle.dump(parents,output)
	#print '\n 
	return parents
	

#function - best_matching_synset()
def best_matching_synset(doc_tokens, synsets):
	#print 'best_matching_synset():\n 
	maxmatch = -1
	retset = []
	for synset in synsets:
		def_tokens = set(nltk.word_tokenize(synset.definition))
		intersection = def_tokens.intersection(doc_tokens)
		#print '-------------------- 
		#print 'intersection:\n 
		#pickle.dump(intersection, output)	
		#print '\n 
		#print '-------------------- 
		if len(intersection) > maxmatch:
			maxmatch = len(intersection)
			retset = synset
	#print retset.definition)
	return retset

#function - get_context()
def get_context(query, documents):
	#basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/d1001a/d1001a-a/"
	basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/"
	file1 = open(os.path.join(basepath,documents[0]))
	file_contents = file1.read()
	file_tokens = nltk.word_tokenize(file_contents)
	try:
		first_occur = file_tokens.index(query)
	except ValueError:
		return ""
	context = ''
	start = first_occur - 5
	finish = first_occur + 5
	if start < 0:
		start = 0
	if finish > len(file_tokens)-1:
		finish = len(file_tokens) - 1
	for i in file_tokens[start:finish]:
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

#update summary with selected candidate
def update_reference_with_candidate(reference,candidate,refdefgraph,canddefgraph,value_addition):
	sentences_with_kw = []
	sentences = []
	kwtfidfmap = {}
	#basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/d1001a/d1001a-a/"
	basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/"
	ref_file = open(os.path.join(basepath,reference[0]))
	candid_file = open(os.path.join(basepath,candidate[0]))
	ref_file_contents = ref_file.read()
	candid_file_contents = candid_file.read()
	ref_tokens = nltk.word_tokenize(ref_file_contents)
	candid_tokens = nltk.word_tokenize(candid_file_contents)
	refdefgraph.extend(list(value_addition))
	#print "after value addition reference definition graph is:"
	#print refdefgraph
	refsentences = ref_file_contents.split(".")
	candsentences = candid_file_contents.split(".")
	all_tokens = ref_tokens + candid_tokens
	fdist = FreqDist(all_tokens)
	for t in all_tokens:
		kwtfidfmap[t] = fdist.freq(t) * compute_idf(corpus, t)
	for kw, p, lev in refdefgraph:
		if lev == 1:
			sentences_with_kw = get_sentences_from_candidate_and_reference(kw, refsentences, candsentences, kwtfidfmap)
			sentences = sentences + sentences_with_kw
	return sentences

#get sentence score
#def sentence_score(x):
#	corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-carrace-test4.txt','ThesisDemo-carrace-test5.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt','ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt','ThesisDemo-hamam-test1.txt','ThesisDemo-hamam-test2.txt','ThesisDemo-hamam-test3.txt','ThesisDemo-hamam-test4.txt','ThesisDemo-hamam-test5.txt','ThesisDemo-sanskrit-test1.txt','ThesisDemo-sanskrit-test2.txt','ThesisDemo-sanskrit-test3.txt','ThesisDemo-sanskrit-test4.txt','ThesisDemo-sanskrit-test5.txt']
#	score = 0
#	tokens = nltk.word_tokenize(x)
#	for t in tokens:
#		score = score + compute_idf(corpus, t)
#	return score

#get sentences containing tokens from the chosen candidate's value-addition list and add to the reference
def get_sentences_from_candidate_and_reference(v, refsentences, candsentences, kwtfidfmap):
	refsentences_with_v = [x for x in refsentences if x.find(v) != -1]
	candsentences_with_v = [x for x in candsentences if x.find(v) != -1]
	refsentences_with_v.extend(candsentences_with_v)
	#print "refsentences=",
	#print refsentences_with_v
	scored_refsentences_with_v = []
	corpus = get_files_list("/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/")
	#corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-carrace-test4.txt','ThesisDemo-carrace-test5.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt','ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt','ThesisDemo-hamam-test1.txt','ThesisDemo-hamam-test2.txt','ThesisDemo-hamam-test3.txt','ThesisDemo-hamam-test4.txt','ThesisDemo-hamam-test5.txt','ThesisDemo-sanskrit-test1.txt','ThesisDemo-sanskrit-test2.txt','ThesisDemo-sanskrit-test3.txt','ThesisDemo-sanskrit-test4.txt','ThesisDemo-sanskrit-test5.txt','ThesisDemo-haiti-test1.txt','ThesisDemo-haiti-test2.txt','ThesisDemo-haiti-test3.txt','ThesisDemo-haiti-test4.txt','ThesisDemo-haiti-test5.txt','ThesisDemo-haiti-test6.txt','ThesisDemo-haiti-test7.txt','ThesisDemo-iceland-test1.txt','ThesisDemo-iceland-test2.txt','ThesisDemo-bangkok-test1.txt','ThesisDemo-bangkok-test2.txt']
	#print "number of refsentences with keyword {" + v + "} is = " + str(len(refsentences_with_v))
	for sen in refsentences_with_v:
		score = 0
		tokens = nltk.word_tokenize(sen)
		for t in tokens:
			try:
				score = score + kwtfidfmap[t]
			except KeyError:
				pass
		#print "adding sentence {" +sen+"} to scoredsentences with " + v + " and score " + str(score)
		scored_refsentences_with_v.append((score, sen))
	return scored_refsentences_with_v	

def get_files_list(root):
	filelist=[]
	os.path.walk(root, corpus_callback, filelist)
	return filelist	

def corpus_callback(arg, dirname, filenames):
	#print "in callback"
	for x in filenames:
		arg.append(x)
	
#----------------------------------------------
#1.Get the input documents
#----------------------------------------------

#corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-datamining-test6.txt','ThesisDemo-datamining-test7.txt','ThesisDemo-datamining-test8.txt','ThesisDemo-datamining-test9.txt','ThesisDemo-datamining-test10.txt','ThesisDemo-maoists-test1.txt','ThesisDemo-maoists-test2.txt','ThesisDemo-maoists-test3.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-english-test4.txt','ThesisDemo-english-test5.txt','ThesisDemo-english-test6.txt','ThesisDemo-english-test7.txt','ThesisDemo-english-test8.txt','ThesisDemo-english-test9.txt','ThesisDemo-english-test10.txt','ThesisDemo-literary-test1.txt','ThesisDemo-literary-test2.txt','ThesisDemo-literary-test3.txt','ThesisDemo-literary-test4.txt','ThesisDemo-literary-test5.txt','ThesisDemo-literary-test6.txt','ThesisDemo-literary-test7.txt','ThesisDemo-literary-test8.txt','ThesisDemo-literary-test9.txt','ThesisDemo-literary-test10.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-carrace-test4.txt','ThesisDemo-carrace-test5.txt']
#corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-carrace-test4.txt','ThesisDemo-carrace-test5.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt','ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt','ThesisDemo-hamam-test1.txt','ThesisDemo-hamam-test2.txt','ThesisDemo-hamam-test3.txt','ThesisDemo-hamam-test4.txt','ThesisDemo-hamam-test5.txt','ThesisDemo-sanskrit-test1.txt','ThesisDemo-sanskrit-test2.txt','ThesisDemo-sanskrit-test3.txt','ThesisDemo-sanskrit-test4.txt','ThesisDemo-sanskrit-test5.txt','ThesisDemo-haiti-test1.txt','ThesisDemo-haiti-test2.txt','ThesisDemo-haiti-test3.txt','ThesisDemo-haiti-test4.txt','ThesisDemo-haiti-test5.txt','ThesisDemo-haiti-test6.txt','ThesisDemo-haiti-test7.txt','ThesisDemo-iceland-test1.txt','ThesisDemo-iceland-test2.txt','ThesisDemo-bangkok-test1.txt','ThesisDemo-bangkok-test2.txt']
corpus=get_files_list("/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/")
#print "corpus:"
#print corpus
#get keywords

import nltk
from nltk.corpus import reuters
#files = ['ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt']
#files = ['ThesisDemo-literary-test1.txt','ThesisDemo-literary-test2.txt','ThesisDemo-literary-test3.txt','ThesisDemo-literary-test4.txt','ThesisDemo-literary-test5.txt','ThesisDemo-literary-test6.txt','ThesisDemo-literary-test7.txt','ThesisDemo-literary-test8.txt','ThesisDemo-literary-test9.txt','ThesisDemo-literary-test10.txt']
#files = ['ThesisDemo-literary-test1.txt','ThesisDemo-literary-test2.txt']
#files = ['ThesisDemo-hamam-test1.txt','ThesisDemo-hamam-test2.txt','ThesisDemo-hamam-test3.txt','ThesisDemo-hamam-test4.txt','ThesisDemo-hamam-test5.txt']
#files = ['ThesisDemo-sanskrit-test1.txt','ThesisDemo-sanskrit-test2.txt','ThesisDemo-sanskrit-test3.txt','ThesisDemo-sanskrit-test4.txt','ThesisDemo-sanskrit-test5.txt']
#files = ['ThesisDemo-haiti-test1.txt','ThesisDemo-haiti-test2.txt','ThesisDemo-haiti-test3.txt','ThesisDemo-haiti-test4.txt','ThesisDemo-haiti-test5.txt']
#files = ['ThesisDemo-haiti-test6.txt','ThesisDemo-haiti-test7.txt']
#files = ['ThesisDemo-iceland-test1.txt','ThesisDemo-iceland-test2.txt']
#basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/d1001a/d1001a-a/"
basepath="/media/disk1/CMI-related-new/TAC2010/GuidedSumm10_test_docs_files/"+sys.argv[1]+"/"+sys.argv[1]+"-"+sys.argv[2]+"/"
#files = get_files_list(basepath)
files=["reference","candidate"]
#print "files list:"
#print files
#Test reuters corpus for first 200 files with 'earn'category
#files = [f for f in (reuters.fileids())[:200] if 'earn' in reuters.categories(f)]



#---------------------------------------------------------------------------------
#2.Compute intrinsic merit (either using linear or quadratic overlap)
#---------------------------------------------------------------------------------
rankingbyintrinsicmerit={}
rankingbyrelatedness={}
rankingbydocumentid={}
for filestr in files[0:3]:
	#print '########################################################################################################'
	#filestrtok = filestr.split('-')
	#outputfile = 'Output-' + filestrtok[1] + '-' + filestrtok[2]
	#output = open(outputfile, 'w') 
	#uncomment next 3 lines and comment the 4th, if not using reuters
	file1 = open(os.path.join(basepath,filestr))
	raw1 = file1.read()
	doc1 = nltk.word_tokenize(raw1)
	#doc1 = reuters.words(filestr)
	from nltk.book import *
	from nltk.corpus import stopwords
	fdist1 = FreqDist(doc1)
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords = stopwords + ['may', 'The', 'the', 'In', 		'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(',')', ',', '#' '[', ']', '=', '@', ':', '|', ';','\'s']
	#at present tfidf filter is applied
	#freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w)) > 0.002]
	#freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * compute_idf(corpus, w)) > 0.02]
	#freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts and (fdist1.freq(w) * reuters_compute_idf(reuters.fileids(), w)) > 0.02]
	freqterms1 = [w for w in fdist1.keys() if w not in stopwords and w not in puncts]
	current_level = 1
	nodewithmaxparents = []
	noofparents = 0
	maxparents = 1
	relatedness = 0
	first_convergence_level = 1
	tokensofthislevel = []
	convergingterms = []
	definitiongraphedges = []
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
				parentslist = parents(kw, prevlevelsynsets)
				convergingparents = convergingparents + ([w for w in parentslist if len(parentslist) > 1])
				for p in parentslist:
					definitiongraphedges.append((kw, p))
			for kw in freqterms1:
				noofparents = len(parents(kw, prevlevelsynsets))
				if noofparents > maxparents:
					#maxparents = noofparents
					nodewithmaxparents.append(kw)
			#print 'converging terms(terms with more than 1 parent):'  
			#pickle.dump(convergingterms,output) 
			#print 'converging parents :'
			#pickle.dump(convergingparents,output)
		for keyword in freqterms1:
			#WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset() 
			#print '==============================================='
			#print 'keyword : ' + keyword
			#disamb_synset = best_matching_synset(set(doc1), wn.synsets(keyword))
			disamb_synset = best_matching_synset(freqterms1, wn.synsets(keyword))
			prevlevelsynsets = prevlevelsynsets + [disamb_synset]
			#print 'prevlevelsynsets:'
			#pickle.dump(prevlevelsynsets, output)
			#print 'matching synset:'
			#print  disamb_synset
			if len(wn.synsets(keyword)) != 0:
				disamb_synset_def = disamb_synset.definition
				tokens = nltk.word_tokenize(disamb_synset_def) 
				fdist_tokens = FreqDist(tokens)
				#at present frequency filter is not applied
				#if keyword in convergingterms:
				#tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])
				tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts])
		#print 'At level:'+ str(current_level)
		#print 'tokens grasped at this level:'
		#pickle.dump(tokensofthislevel, output)
		listcount = len(tokensofthislevel)
		setcount = len(set(tokensofthislevel))
		overlap =  listcount-setcount
		if overlap > 0 and iter == 0 :
			first_convergence_level = current_level
			iter = 1
		#choose between two relatedness/convergence criteria :- 
		#1) simple linear overlap or 2) zipf distributed quadratic overlap
		#relatedness = relatedness + len(convergingparents)*overlap 
		#relatedness = relatedness + overlap
		relatedness = relatedness + ((len(convergingparents)*overlap*overlap)) 
		#find out common tokens of this and previous level so that same token does not get grasped again - 	
		#relatedness must be increased since repetition of keywords in two successive levels is a sign of 
		#interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and edges 
		#corresponding to common tokens
		commontokens = set(tokensofthislevel).intersection(set(tokensofprevlevel))
		tokensofthislevel = set(tokensofthislevel).difference(commontokens)
		relatedness = relatedness + len(commontokens)
		#print 'removing tokens already grasped:' 
		#pickle.dump(commontokens,output)
		#print 'Relatedness:'+ str(relatedness)
		#decrease the vertices count to address common tokens removed above - edges should remain same since they 
		#would just point elsewhere
		vertices = vertices + setcount - len(commontokens)
		#print 'Vertices:'+ str(vertices)
		edges = edges + listcount
		#print 'Edges:'+ str(edges)
		current_level = current_level + 1
		freqterms1 = set(tokensofthislevel)
		tokensofprevlevel = tokensofthislevel
		tokensofthislevel = []
	intrinsic_merit = vertices*edges*relatedness / first_convergence_level
	#print 'Relatedness:'+ str(relatedness)
	#print 'Vertices:'+ str(vertices)
	#print 'Edges:'+ str(edges)
	#print 'Intrinsic merit of this document ' + filestr + ' is:' + str(intrinsic_merit)
	#print 'Nodes with more than ' + str(maxparents) + ' parent (and hence the most likely classes of document) is:',
	#print set(nodewithmaxparents)
	#if reuters print categories this file belongs to
	#print 'Reuter categories of ' + filestr + ' are:', 
	#print reuters.categories(filestr)
	rankingbydocumentid[filestr] = (relatedness, vertices, edges, first_convergence_level)
	rankingbyintrinsicmerit[intrinsic_merit] =(filestr, relatedness, vertices, edges, first_convergence_level)
	rankingbyrelatedness[relatedness] = (filestr, relatedness, vertices, edges, first_convergence_level)
print '##########################################'
print 'Ranking by Intrinsic Merit:',
maxintrinsicmerit = -1
for k in sorted(rankingbyintrinsicmerit.keys()):
	if k > maxintrinsicmerit:
		maxintrinsicmerit = k
	print '(Document,relatedness,vertices,edges,firstconvergencelevel):',
	print rankingbyintrinsicmerit[k],
	print '-------------------IMScore:',
	print k
print '##########################################'
for k in sorted(rankingbyrelatedness.keys()):
	print '(Document,relatedness,vertices,edges,firstconvergencelevel):',
	print rankingbyrelatedness[k],
	print '-------------------Relatedness:',
	print k


#--------------------------------
#3. Interview Algorithm
#--------------------------------
n=0
references = [files[n]]
candidate = [files[n+1]]
#print "################## Interview of " + candidate[0] + " with " + references[0] + "#############################"
queries = []
stopwords = nltk.corpus.stopwords.words('english')
stopwords = stopwords + ['may', 'The', 'the', 'In', 		'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(',  ',', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
from nltk.book import *
for filestr in references:
	file1 = open(os.path.join(basepath,filestr))
	filecontents = file1.read()	
	filetokens = nltk.word_tokenize(filecontents)
	freqdist = FreqDist(filetokens)	
	queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and (freqdist.freq(w) * compute_idf(corpus, w)) > 0.00001]
	#queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and freqdist.freq(w) * compute_idf(corpus, w) > 0.01]
	#queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and freqdist.freq(w) * reuters_compute_idf(corpus, w) > 0.1]

#print 'Most important tokens/ngrams = queries :'
#print queries

ref_qandamap={}
candid_qandamap={}
for q in queries:
	ref_qandamap[q] = get_context(q, references)

candid_file = open(os.path.join(basepath,candidate[0]))
candid_file_contents = candid_file.read()
candid_tokens = nltk.word_tokenize(candid_file_contents)
candid_text = nltk.Text(candid_tokens)
for q in queries:
	#print '--------------------------------'
	#print 'concordance for :' + q
	#candid_text.concordance(q)
	#print '--------------------------------'
	candid_qandamap[q] = get_context(q, candidate)

#print 'reference:'
#print ref_qandamap
#print 'candidate:'
#print candid_qandamap

#compute jaccard coefficient score for each question and answer
scores=[]
i=0
for q in queries:
	#print 'q = ' + q
	scores.append(get_jaccard_coefficient(ref_qandamap[q], candid_qandamap[q]))

x=0
sumscore = 0
for x in scores:
	sumscore = sumscore + x

print 'Interview score:'
print sumscore
print 'Interview score(in percentage correctness):',
print (sumscore / len(queries)) * 100


#--------------------------------------------------------------------------------------------------------------------
#4.Compute Value Addition applying edit distance between definition-graph(reference) and definition-graph(candidate)
#at present limited to 1 reference which will be updated after interview algorithm finishes if necessary
#--------------------------------------------------------------------------------------------------------------------
references = [files[n]]
candidate = [files[n+1]]
print "################## Value addition of " + candidate[0] + " to " + references[0] + "#############################"

ref_file = open(os.path.join(basepath,references[0]))
candid_file = open(os.path.join(basepath,candidate[0]))
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
puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(',  ',', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
#at present tfidf filter is not applied
reffreqterms = [w for w in reffdist.keys() if w not in stopwords and w not in puncts]
candfreqterms = [w for w in candidfdist.keys() if w not in stopwords and w not in puncts]
#reffreqterms = [w for w in reffdist.keys() if w not in stopwords and w not in puncts and (reffdist.freq(w) * compute_idf(corpus, w)) > 0.005]
#candfreqterms = [w for w in candidfdist.keys() if w not in stopwords and w not in puncts and (candidfdist.freq(w) * compute_idf(corpus, w)) > 0.005]
#reffreqterms = [w for w in reffdist.keys() if w not in stopwords and w not in puncts and (reffdist.freq('ThesisDemo-philosophy-test1.txt',w) * reuters_compute_idf(corpus, w))]
#candfreqterms = [w for w in candidfdist.keys() if w not in stopwords and w not in puncts and (candidfdist.freq(w) * reuters_compute_idf(corpus, w))]


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
for i in reffreqterms:
	ref_definitiongraphedges.append((i, nltk.corpus.reader.wordnet.Synset('root.n.01'), 1))
for i in candfreqterms:
	cand_definitiongraphedges.append((i, nltk.corpus.reader.wordnet.Synset('root.n.01'), 1))
from nltk.corpus import wordnet as wn

#recurse down to required depth and update edit distance between reference and candidate documents
while current_level < 3:
	if current_level > 1:
		for kw in reffreqterms:
				refparents = parents(kw, refprevlevelsynsets)
				for p in refparents:
					ref_definitiongraphedges.append((kw, p, current_level))
		for kw in candfreqterms:
				candparents = parents(kw, candprevlevelsynsets)
				for p in candparents:
					cand_definitiongraphedges.append((kw, p, current_level))
		#print 'Current level:'
		#print current_level
		#print 'Reference DefGraph:'
		#print ref_definitiongraphedges
		#print 'Candidate DefGraph:'
		#print cand_definitiongraphedges
	#for refkeyword, candkeyword in reffreqterms, candfreqterms:
	reffreqtermscount = 0
	candfreqtermscount = 0
	while reffreqtermscount < len(reffreqterms) or candfreqtermscount < len(candfreqterms):
		#WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset() 
		if reffreqtermscount < len(reffreqterms):
			refdisamb_synset = best_matching_synset(reffreqterms, wn.synsets(list(reffreqterms)[reffreqtermscount]))
			#print refdisamb_synset
			refprevlevelsynsets = refprevlevelsynsets + [refdisamb_synset]
		if candfreqtermscount < len(candfreqterms):
			canddisamb_synset = best_matching_synset(candfreqterms, wn.synsets(list(candfreqterms)[candfreqtermscount]))
			#print canddisamb_synset
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
	#interrelatedness(a backedge from child-of-one-of-siblings to one-of-siblings). Remove vertices and 
	#edges corresponding to common tokens
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
		ref_definitiongraphedges.append((kw, p, current_level))
for kw in candfreqterms:
	candparents = parents(kw, candprevlevelsynsets)
	for p in candparents:
		cand_definitiongraphedges.append((kw, p, current_level))
#print 'Current level:'
#print current_level
#print 'Reference DefGraph:'
#print ref_definitiongraphedges
#print 'Candidate DefGraph:'
#print cand_definitiongraphedges

#value addition - edges present in candidate but not in reference
valueaddition = set(cand_definitiongraphedges).difference(set(ref_definitiongraphedges))
#edit distance - edges added + edges removed
editdistance = editdistance + len(set(cand_definitiongraphedges).difference(set(ref_definitiongraphedges))) + len(set(ref_definitiongraphedges).difference(set(cand_definitiongraphedges)))
print 'Value addition:'
print valueaddition
print 'Edit Distance:'
print editdistance
print 'Edit Distance (as percentage value addition from reference):'
print 100 - (len(set(cand_definitiongraphedges).intersection(set(ref_definitiongraphedges)))/len(set(ref_definitiongraphedges))) * 100

#------------------------------------------------------------------------------------------------------
# 5. Get the normalized sum (intrinsic merit + interview + value addition) and choose the best
# normalization = score / largest_score (percentage)
# Weighted score = w1(IM) + w2(Interview) + w3(Valueaddition)
#------------------------------------------------------------------------------------------------------
w1 = 1/3
w2 = 1/3
w3 = 1/3
(r,v,e,f) = rankingbydocumentid[candidate[0]]
weighted_score = (w1 * (r * v * e / f) / maxintrinsicmerit) + (w2 * (sumscore / len(queries)) * 100) + (w3 * (100 - (len(set(cand_definitiongraphedges).intersection(set(ref_definitiongraphedges)))/len(set(ref_definitiongraphedges))) * 100))
#weighted_score = (w2 * (sumscore / len(queries)) * 100) + (w3 * (100 - (len(set(cand_definitiongraphedges).intersection(set(ref_definitiongraphedges)))/len(set(ref_definitiongraphedges))) * 100))
print 'Weighted Final score for :' + candidate[0] + ':',
print weighted_score
#-----------------------------------------------------------------------------
# 6. Update reference summary with candidate selected 
#-----------------------------------------------------------------------------
interview_threshold = 20.0
new_reference=[]
if weighted_score > interview_threshold:
	new_reference = update_reference_with_candidate(references, candidate, ref_definitiongraphedges, cand_definitiongraphedges, valueaddition)
print 'New reference summary after update:'
print '##############################################'
new_reference = sorted(list(set(new_reference)),None,None,True)
#choose top 1/20 of total number of sentences
onetwentieth = int(len(new_reference)/20)
top_scoring_sentences = new_reference[0:onetwentieth]
for score, x in top_scoring_sentences:
	print x,
	print ".",



