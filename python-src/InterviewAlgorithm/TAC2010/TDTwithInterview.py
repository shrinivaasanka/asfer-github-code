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

#function - compute_idf()
def compute_idf(corpus, keyword):
	import math
	total_occur = 0
	keyword_occur = 0
	for file in corpus:
		raw = open(file).read()
		tokens = nltk.word_tokenize(raw)
		total_occur = total_occur + 1
		keyword_occur = keyword_occur + len(set([w for w in tokens if w == keyword]))
	if keyword_occur == 0:
		keyword_occur = 1
	return math.log(total_occur / (keyword_occur))

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
	file1 = open(documents[0])
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

corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt','ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt','ThesisDemo-telengana-test1.txt','ThesisDemo-telengana-test2.txt','ThesisDemo-sukhna-test1.txt','ThesisDemo-lufthansa-test1.txt','ThesisDemo-sukhna-test2.txt','ThesisDemo-sukhna-test3.txt','ThesisDemo-lufthansa-test2.txt','ThesisDemo-bangalorefire-test1.txt','ThesisDemo-bangalorefire-test2.txt','ThesisDemo-bangalorefire-test3.txt','ThesisDemo-indopak-test1.txt','ThesisDemo-indopak-test2.txt']

#news = ['ThesisDemo-telengana-test1.txt','ThesisDemo-telengana-test2.txt','ThesisDemo-sukhna-test1.txt','ThesisDemo-lufthansa-test1.txt','ThesisDemo-sukhna-test2.txt','ThesisDemo-sukhna-test3.txt','ThesisDemo-lufthansa-test2.txt','ThesisDemo-bangalorefire-test1.txt','ThesisDemo-bangalorefire-test2.txt','ThesisDemo-bangalorefire-test3.txt','ThesisDemo-indopak-test1.txt','ThesisDemo-indopak-test2.txt']

#news = ['ThesisDemo-sukhna-test1.txt','ThesisDemo-lufthansa-test1.txt','ThesisDemo-sukhna-test2.txt']
news = ['ThesisDemo-sukhna-test1.txt','ThesisDemo-lufthansa-test1.txt','ThesisDemo-sukhna-test2.txt','ThesisDemo-dantewada-test1.txt','ThesisDemo-ipad-test1.txt']


distance_map = {}
references = []
candidate = []

for nx in news:
	for ny in news:
		references=[]
		candidate=[]
		print '###########################################################################'
		#------------------------------------------------------------------
		# 1.Topic Link Detection - check if 2 news stories discuss same topic and print the topics
		#-------------------------------------------------------------------
		# 1a.Interview one member of the pair (Nx, Ny) with the other
		#------------------------------------------------------------------
		print 'Reference == ' + str(nx) + '; Candidate == ' + str(ny)
		import nltk
		references.append(nx)
		candidate.append(ny)
		queries = []
		stopwords = nltk.corpus.stopwords.words('english')
		stopwords = stopwords + ['may', 'The', 'the', 'In', 				'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', ',', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
		from nltk.book import *
		for filestr in references:
			file1 = open(filestr)
			filecontents = file1.read()	
			filetokens = nltk.word_tokenize(filecontents)
			freqdist = FreqDist(filetokens)	
			queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and (freqdist.freq(w) * compute_idf(corpus, w)) > 0.01]
			#queries = queries + [w for w in freqdist.keys() if w not in stopwords and w not in puncts and freqdist.freq(w) * reuters_compute_idf(corpus, w) > 0.1]

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
			print 'x = ' + str(x)
			sumscore = sumscore + x
		print 'Interview score:'
		print sumscore
		print 'Interview score(in percentage correctness):',
		print (sumscore / len(queries)) * 100
		#--------------------------------------------------------------------------------------------------------------------
		#1b.Compute Value Addition applying edit distance between definition-graph(reference) and definition-graph(candidate)
		#at present limited to 1 reference which will be updated after interview algorithm finishes if necessary
		#--------------------------------------------------------------------------------------------------------------------
		references.append(nx)
		candidate.append(ny)
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
		stopwords = stopwords + ['may', 'The', 'the', 'In', 				'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', ',', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
		#at present tfidf filter is applied
		reffreqterms = [w for w in reffdist.keys() if w not in stopwords and w not in puncts and (reffdist.freq(w) * compute_idf(corpus, w))]
		candfreqterms = [w for w in candidfdist.keys() if w not in stopwords and w not in puncts and (candidfdist.freq(w) * compute_idf(corpus, w))]
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
		from nltk.corpus import wordnet as wn
		refnoofparents = 0
		refmaxparents = 1
		refnodewithmaxparents = []
		candnoofparents = 0
		candmaxparents = 1
		candnodewithmaxparents = []
		#recurse down to required depth and update edit distance between reference and candidate documents
		while current_level < 3:
			if current_level > 1:
				for kw in reffreqterms:
					refparents = parents(kw, refprevlevelsynsets)
					for p in refparents:
						ref_definitiongraphedges.append((kw, p))
					refnoofparents = len(parents(kw, refprevlevelsynsets))
					if refnoofparents > refmaxparents:
						#refmaxparents = refnoofparents
						refnodewithmaxparents.append(kw)
				for kw in candfreqterms:
					candparents = parents(kw, candprevlevelsynsets)
					for p in candparents:
						cand_definitiongraphedges.append((kw, p))
					candnoofparents = len(parents(kw, candprevlevelsynsets))
					if candnoofparents > candmaxparents:
						#candmaxparents = candnoofparents
						candnodewithmaxparents.append(kw)
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
		distance_map[(nx,ny)] = editdistance
		print 'Value addition:'
		print valueaddition
		print 'Edit Distance:'
		print editdistance
		print 'Edit Distance (as percentage value addition from reference):'
		print 100 - (len(set(cand_definitiongraphedges).intersection(set(ref_definitiongraphedges)))/len(set(ref_definitiongraphedges))) * 100
		#------------------------------------------------------------------------------------------------------
		# 1c. If interview score is above threshold1 and edit distance is below threshold2, then stories Nx and Ny discuss same topic
		# Print the most voted keywords(topic) for reference and candidate - 
		# these keywords are likely topics of this news story
		#------------------------------------------------------------------------------------------------------
		interview_threshold = 30
		editdistance_threshold = 50
		w1 = 1
		w2 = 1
		if (w1 * (sumscore / len(queries)) * 100) > interview_threshold and (w2 * (100 - (len(set(cand_definitiongraphedges).intersection(set	(ref_definitiongraphedges)))/len(set(ref_definitiongraphedges))) * 100)) < editdistance_threshold:
			print '1. Topic Link Detection - ' + candidate[0] + ' and ' + references[0] + ' discuss same topic '
		else:
			print '1. Topic Link Detection - ' + candidate[0] + ' and ' + references[0] + ' do not discuss same topic '
		#---------------------------------------------------------------------------------------------------------
		# 2. Topic tracking
		#---------------------------------------------------------------------------------------------------------
		print '2. Topic tracking - Nodes with maximum parents in ' + references[0] + ' is(and hence likely topics of this news story): ',
		print set(refnodewithmaxparents)
		print '2. Topic tracking - Nodes with maximum parents in ' + candidate[0] + ' is(and hence likely topics of this news story): ',
		print set(candnodewithmaxparents)
		print '2. Topic tracking - Intersection of maxparents of' + references[0] + ' and ' + candidate[0] + ': ',
		print  set(refnodewithmaxparents).intersection(set(candnodewithmaxparents))

#------------------------------------------------------------------------------------------------------
# 3. Topic Detection
#------------------------------------------------------------------------------------------------------
maxeditdistance = 0
outlier=''
for nx in news:
	for ny in news:
		if distance_map[(nx,ny)] > maxeditdistance:
			maxeditdistance = distance_map[(nx,ny)]
			outlier = ny
	maxeditdistance = 0
	print '3.Topic Detection - News story ' + outlier + ' has largest pairwise editdistance from ' + nx + ' and least likely to be in this topic'

