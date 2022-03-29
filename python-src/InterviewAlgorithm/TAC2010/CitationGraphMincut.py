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

#Wikipedia Maxflow example code changed for Citation graph - ford-fulkerson algorithm
from __future__ import division
import nltk
import urllib
from sgmllib import SGMLParser
import datetime
from nltk.book import *
import math

##################################################################################
class URLs(SGMLParser):
    def reset(self):
	SGMLParser.reset(self)
	self.urls = []
	self.inside_a_tag = 0
	self.urlcontexts = []
	self.links = []
	self.textsofar = ""

    def start_a(self, attrs):
	self.links = [val for att, val in attrs if att == 'href']
	#print links
	if self.links:
		self.urls.extend(self.links)
		self.inside_a_tag = 1

    def end_a(self):
	self.inside_a_tag = 0
	self.links = []
	
    def handle_data(self, text):
	exclude=['#main','#sidebar']
	#print 'handle_data(): text == ' + text
	if self.inside_a_tag == 1 and self.links[0] not in exclude and self.links[0].find("blogger.com") == -1 and self.links[0].find("http") == -1 and self.links[0].find("mailto:") == -1 and self.links[0].find("javascript:") == -1:
		#print self.links, 
		#print "========",
		#print text
		#print "handle_data :" + self.textsofar[-30:] + " " + text
		self.urlcontexts.append((self.links[0], self.textsofar[-30:] + " " + text))
		#print "url contexts:",
		#print self.urlcontexts
	self.textsofar = self.textsofar + " " + text

##################################################################################################
class SentiWordNet:
    def __init__(self):
	self.lemmas = []
	self.pos = {}
	self.neg = {}
	try:
	    filename = "SentiWordNet_1.0.1.txt"
            fileobj = open(filename)
	    filelines = fileobj.readlines()
	    for fileline in filelines:			
            	if not fileline.startswith('#'):		
	    		filelinetoks = fileline.split('\t')
			#print filelinetoks
	    		#Note offset values can change in the same version of
			#WordNet due to minor edits in glosses.
			#Thus offsets are reported here just for reference, and
			#are not intended for use in applications.
			#Use lemmas instead.
			#String offset = data[0]+data[1]
		        positivity = float(filelinetoks[2])
		        negativity = float(filelinetoks[3])
		        synsetLemmas = nltk.word_tokenize(filelinetoks[4])
			lemmatoks = []
		    	for i in synsetLemmas:
				lemmatoks = i.split('#')
				lemma = lemmatoks[0]
				self.pos[lemma] = positivity
				self.neg[lemma] = negativity
				self.lemmas.append(lemma)
				#print self.pos
				#print self.neg
				#print self.lemmas
	except IOError:
	    pass
	
    def getPositivity(self, lemma):
	print 'getPositivity: ' + lemma
	return self.pos.get(lemma)

    def getNegativity(self, lemma):
	print 'getNegativity: ' + lemma
	return self.neg.get(lemma)

    def getObjectivity(self, lemma):
	return 1-(self.pos.get(lemma) + self.neg.get(lemma))

    def getLemmas(self):
	return self.lemmas


##################################################################################################

class CitationFlowNetwork(object):
    def __init__(self):
        self.adj, self.flow, = {},{}
	self.mincut = []
	self.setofnodes = []
 
    def add_vertex(self, vertex):
        self.adj[vertex] = []

    def print_adjacency(self):
	print self.adj
 
    def get_edges(self, v):
        return self.adj[v]
 
    def add_edge(self, u,v,w=0):
	print 'add_edge():',
	print str(u) + '-----' + str(v) + " with weight: " + str(w)
        self.adj[u].append((v,w))
        #self.adj[v].append((u,0))
        self.flow[(u,v)] = self.flow[(v,u)] = 0
 
    def find_path(self, source, sink,  path):
        if source == sink:
            return path
        for vertex, capacity in self.get_edges(source):
            residual = capacity - self.flow[(source,vertex)]
            edge = (source,vertex,residual)
            if residual > 0 and not edge in path:
                result = self.find_path(vertex, sink, path + [edge]) 
                if result != None:
                    return result

    def find_all_paths_of_radius_from_source(self, source, radius, currentlevel):
        if currentlevel == radius:
            return 
        for vertex, capacity in self.get_edges(source):
            if not vertex in self.setofnodes:
		self.setofnodes.append(vertex)
                self.find_all_paths_of_radius_from_source(vertex, radius, currentlevel + 1) 
                
    def max_flow(self, source, sink):
        path = self.find_path(source, sink, [])
        while path != None:
            flow = min(r for u,v,r in path)
            for u,v,_ in path:
                self.flow[(u,v)] += flow
                #self.flow[(v,u)] -= flow
            path = self.find_path(source, sink, [])
	self.mincut = [vertex for vertex, capacity in self.get_edges(source)]
        return sum(self.flow[(source, vertex)] for vertex, capacity in self.get_edges(source))

    def ylaterthanx(self, xlastmodtok, ylastmodtok):
	monthnum = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
	#4 3 2 5 7 9
	xtime = datetime.datetime(int(xlastmodtok[4]), int(monthnum[xlastmodtok[3]]), int(xlastmodtok[2]), int(xlastmodtok[5]), int(xlastmodtok[7]), int(xlastmodtok[9]))
	print 'xtime: ',
	print xtime
	ytime = datetime.datetime(int(ylastmodtok[4]), int(monthnum[ylastmodtok[3]]), int(ylastmodtok[2]), int(ylastmodtok[5]), int(ylastmodtok[7]), int(ylastmodtok[9]))	
	print 'ytime: ',
	print ytime
	if(ytime-xtime > datetime.timedelta(0,0)):
		print 'y later than x'
		return True
	else:	
		return False
	


##################################################################################
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

#Sentiment Analysis of Link context - apply SentiWordNet
def doSentimentAnalysisWithSentiWordNet(xinpageyctxs):
	total_pos = 0
	total_neg = 0
	total_xcontextiny = ""
	for x in xinpageyctxs:
		total_xcontextiny = total_xcontextiny + " " + x
	print "Total xcontextiny:" + total_xcontextiny
	swn = SentiWordNet()
	ctxtokens = nltk.word_tokenize(total_xcontextiny)
	for t in ctxtokens:	
		pos_t = swn.getPositivity(t)	
		neg_t = swn.getNegativity(t)
		print pos_t
		print neg_t
		if pos_t != None and neg_t != None:
			total_pos = total_pos + pos_t
			total_neg = total_neg + neg_t 
	if total_pos >= (0-total_neg):
		return 1
	else:
		return -1

#Sentiment Analysis of Link context - get link context and do entropy analysis
def doSentimentAnalysisWithEntropy(xinpageyctxs):
	import math
	negativewords = ['bad', 'worse', 'worst', 'sucks', 'poor','shit']
	threshold = 0.2
	total_xcontextiny = ""
	for x in xinpageyctxs:
		total_xcontextiny = total_xcontextiny + " " + x
	print "Total xcontextiny:" + total_xcontextiny
	ctxtokens = nltk.word_tokenize(total_xcontextiny)
	negtokens = [x for x in ctxtokens if x in negativewords]
	posprob = (len(ctxtokens) - len(negtokens))/len(ctxtokens)
	print posprob
	negprob = len(negtokens)/len(ctxtokens)
	print negprob
	if posprob == 0:
		return -1
	if negprob == 0:
		return 1
	entropy = -(posprob * math.log(posprob)) - (negprob * math.log(negprob))
	if entropy < threshold:
		if posprob > 0.5:
			return 1
		else:
			return -1
	else:
		return -1 

#Sentiment Analysis of Link context - get link context and using recursive gloss overlap, get the polarity and accordingly fix sign for weight   
def doSentimentAnalysisWithRecursiveGlossOverlap(xinpageyctxs):
	corpus = ['ThesisDemo-datamining-test1.txt','ThesisDemo-datamining-test2.txt','ThesisDemo-datamining-test3.txt','ThesisDemo-datamining-test4.txt','ThesisDemo-datamining-test5.txt','ThesisDemo-english-test1.txt','ThesisDemo-english-test2.txt','ThesisDemo-english-test3.txt','ThesisDemo-carrace-test1.txt','ThesisDemo-carrace-test2.txt','ThesisDemo-carrace-test3.txt','ThesisDemo-carrace-test4.txt','ThesisDemo-carrace-test5.txt','ThesisDemo-graphtheory-test1.txt','ThesisDemo-graphtheory-test2.txt','ThesisDemo-graphtheory-test3.txt','ThesisDemo-fermatslasttheorem-test16.txt','ThesisDemo-fermatslasttheorem-test17.txt','ThesisDemo-newsmodipranab-test1.txt','ThesisDemo-newsmodipranab-test2.txt','ThesisDemo-philosophy-test1.txt','ThesisDemo-philosophy-test2.txt','ThesisDemo-philosophy-test3.txt','ThesisDemo-philosophy-test4.txt','ThesisDemo-philosophy-test5.txt','ThesisDemo-philosophy-test6.txt','ThesisDemo-philosophy-test7.txt','ThesisDemo-philosophy-test8.txt','ThesisDemo-philosophy-test9.txt','ThesisDemo-philosophy-test10.txt']
	total_xcontextiny = ""
	for x in xinpageyctxs:
		total_xcontextiny = total_xcontextiny + " " + x
	print "Total xcontextiny:" + total_xcontextiny
	doc1 = nltk.word_tokenize(total_xcontextiny)
	#doc1 = reuters.words(filestr)
	from nltk.corpus import stopwords
	fdist1 = FreqDist(doc1)
	stopwords = nltk.corpus.stopwords.words('english')
	stopwords = stopwords + ['may', 'The', 'the', 'In', 		'in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	puncts = ['.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(',')', ',', '#' '[', ']', '=', '@', ':', '|', ';','\'s']
	#at present tfidf filter is not applied
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
	swn = SentiWordNet()
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
					#get all terms in the definition graph which have more than 1 parent i.e involved in gloss overlap
					nodewithmaxparents.append(kw)
			print 'converging terms(terms with more than 1 parent):'  
			#pickle.dump(convergingterms,output) 
			print 'converging parents :'
			#pickle.dump(convergingparents,output)
		for keyword in freqterms1:
			#WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset() 
			print '==============================================='
			print 'keyword : ' + keyword
			#disamb_synset = best_matching_synset(set(doc1), wn.synsets(keyword))
			disamb_synset = best_matching_synset(freqterms1, wn.synsets(keyword))
			prevlevelsynsets = prevlevelsynsets + [disamb_synset]
			print 'prevlevelsynsets:'
			#pickle.dump(prevlevelsynsets, output)
			print 'matching synset:'
			print  disamb_synset
			if len(wn.synsets(keyword)) != 0:
				disamb_synset_def = disamb_synset.definition
				tokens = nltk.word_tokenize(disamb_synset_def) 
				fdist_tokens = FreqDist(tokens)
				#at present frequency filter is not applied
				#if keyword in convergingterms:
				#tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])
				tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts])
		print 'At level:'+ str(current_level)
		print 'tokens grasped at this level:'
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
		print 'removing tokens already grasped:' 
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
	print 'Nodes with more than ' + str(maxparents) + ' parent (and hence the most likely classes of document) is:',
	print set(nodewithmaxparents)
	#negativewords = ['bad', 'worse', 'worst', 'sucks', 'poor', 'shit']
	posmaxparents = []
	negmaxparents = []
	for x in nodewithmaxparents:
		#get positivity/negativity from SentiWordNet for each overlapping parent
		pos_kw = swn.getPositivity(x)	
		neg_kw = swn.getNegativity(x)
		if pos_kw > neg_kw:
			posmaxparents.append(x)
		else:
			negmaxparents.append(x)
	print "negative words:",
	print negmaxparents
	print "positive words:",
	print posmaxparents
	if len(negmaxparents) > len(posmaxparents):
		return -1
	else:
	   	return 1


#################################################################################################################
#Create Citation graph of hyperlinks (Citations are hyperlinks with timestamps - y cites x iff y is later than x)
#################################################################################################################
cfn=CitationFlowNetwork()
xlistofurls=URLs()
ylistofurls=URLs()
urlsiny=[]
xlastmodified=''
ylastmodified=''
xlastmod_tok=[]
ylastmod_tok=[]
i=0
x=0
y=0
#urlroot="file:///media/OS/personal/CMI-related/kuja27/kuja27.blogspot.com/"
#urlroot="file:///media/OS/personal/CMI-related/moviereview/"
#urlroot="file:///media/OS/personal/CMI-related/sulekhamoviereview/"
#urlroot="file:///media/OS/personal/CMI-related/citationtestlocal/"
#urlroot="file:///media/disk/CMI-related/citationtestlocal/"
urlroot="http://reviews.cnet.com/"
usock = urllib.urlopen(urlroot+"index.html")
xlistofurls.feed(usock.read())
xlistofurls.close()
usock.close()
pages=xlistofurls.urls
exclude=['#main','#sidebar']
pages=[l for l in pages if l not in exclude and l.find("blogger.com") == -1 and l.find("http") == -1 and l.find("mailto:") == -1 and l.find("javascript:") == -1]
print pages
#pages = ['./index.html', './movies.sulekha.com/hindi/2006/01/01/reviews.htm', './movies.sulekha.com/hindi/2006/02/01/reviews.htm', './movies.sulekha.com/hindi/2006/03/01/reviews.htm', './movies.sulekha.com/hindi/2006/04/01/reviews.htm', './movies.sulekha.com/hindi/2006/05/01/reviews.htm', './movies.sulekha.com/hindi/2006/06/01/reviews.htm', './movies.sulekha.com/hindi/2006/07/01/reviews.htm', './movies.sulekha.com/hindi/2006/08/01/reviews.htm', './movies.sulekha.com/hindi/2006/09/01/reviews.htm', './movies.sulekha.com/hindi/2006/10/01/reviews.htm', './movies.sulekha.com/hindi/2006/11/01/reviews.htm', './movies.sulekha.com/hindi/2006/12/01/reviews.htm', './movies.sulekha.com/hindi/2007/01/01/reviews.htm', './movies.sulekha.com/hindi/2007/02/01/reviews.htm', './movies.sulekha.com/hindi/2007/03/01/reviews.htm', './movies.sulekha.com/hindi/2007/04/01/reviews.htm', './movies.sulekha.com/hindi/2007/05/01/reviews.htm', './movies.sulekha.com/hindi/2007/06/01/reviews.htm', './movies.sulekha.com/hindi/2007/07/01/reviews.htm', './movies.sulekha.com/hindi/2007/09/01/reviews.htm', './movies.sulekha.com/hindi/2007/10/01/reviews.htm', './movies.sulekha.com/hindi/2007/11/01/reviews.htm', './movies.sulekha.com/hindi/2007/12/01/reviews.htm', './movies.sulekha.com/hindi/2008/01/01/reviews.htm', './movies.sulekha.com/hindi/2008/02/01/reviews.htm', './movies.sulekha.com/hindi/2008/03/01/reviews.htm', './movies.sulekha.com/hindi/atithi-tum-kab-jaoge/default.htm', './movies.sulekha.com/hindi/default.htm', './movies.sulekha.com/hindi/fanaa/default.htm', './movies.sulekha.com/hindi/fanaa/reviews/pageno-1.htm', './movies.sulekha.com/hindi/featured/reviews.htm', './movies.sulekha.com/hindi/gadar-ek-prem-katha/default.htm', './movies.sulekha.com/hindi/gadar-ek-prem-katha/reviews/pageno-1.htm', './movies.sulekha.com/hindi/kabhi-alvida-naa-kehna/default.htm', './movies.sulekha.com/hindi/kabhi-alvida-naa-kehna/reviews/pageno-1.htm', './movies.sulekha.com/hindi/kal-ho-naa-ho/default.htm', './movies.sulekha.com/hindi/kal-ho-naa-ho/reviews/pageno-1.htm', './movies.sulekha.com/hindi/krissh/default.htm', './movies.sulekha.com/hindi/krissh/reviews/pageno-1.htm', './movies.sulekha.com/hindi/main-hoon-na/default.htm', './movies.sulekha.com/hindi/main-hoon-na/reviews/pageno-1.htm', './movies.sulekha.com/hindi/reviews.htm', './movies.sulekha.com/hindi/road-movie/default.htm', './movies.sulekha.com/hindi/road-movie/events/road-movie/picture/default.htm', './movies.sulekha.com/hindi/road-movie/pictures/1.htm', './movies.sulekha.com/hindi/road-movie/reviews/75470.htm', './movies.sulekha.com/hindi/road-movie/reviews/pageno-1.htm', './movies.sulekha.com/hindi/road-movie/trailers/default.htm', './movies.sulekha.com/hindi/road-movie/wallpapers/default.htm' ]
pages = pages[:10]
while i < len(pages):
	cfn.add_vertex(i)
	i = i + 1
 
while x < len(pages):
	y=0
	try:
		xusock=urllib.urlopen(urlroot+pages[x])
		#xlastmodified=xusock.headers.getheader("Last-Modified")
		#print 'xlastmodified: ',
		#print xlastmodified
		#xlastmod_tok = nltk.word_tokenize(xlastmodified)
		xusock.close()
	except IOError:
		pass
	while y < len(pages):
		#if y cites x
		#if pages[y].find('file://') != -1:
		#print pages[y]
		try:
			yusock = urllib.urlopen(urlroot + pages[y])			
			#ylastmodified=yusock.headers.getheader("Last-Modified")
			#print 'ylastmodified: '
			#print ylastmodified
			#ylastmod_tok = nltk.word_tokenize(ylastmodified)
			ylistofurls.feed(yusock.read())
			urlsiny = ylistofurls.urls
			print "ylistofurls.urlcontexts:",
			print ylistofurls.urlcontexts
			if pages[x] in urlsiny:
				#print 'if pages[x] in urlsiny'
				#get the weightage y gives to x when y cites x
				weight = len([l for l in urlsiny if l == pages[x]])
				xurlctxsiny = [ctx for (url, ctx) in ylistofurls.urlcontexts if url == pages[x]]
				#########Do sentiment analysis to get polarity - 1) Recursive gloss overlap or 2) entropy or 3) SentiWordNet#############
				polarity = doSentimentAnalysisWithSentiWordNet(xurlctxsiny)
				#polarity =  doSentimentAnalysisWithRecursiveGlossOverlap(xurlctxsiny)
				#polarity =  doSentimentAnalysisWithEntropy(xurlctxsiny)
				weight = weight * polarity
				#if cfn.ylaterthanx(xlastmod_tok, ylastmod_tok):
				if weight != 0:
					cfn.add_edge(x, y, weight)
					#cfn.add_edge(y, x, weight)
			ylistofurls.reset()
			ylistofurls.close()
			yusock.close()
		except IOError:
			pass
		y=y+1
#		print "y="+str(y)
	x=x+1
#	print "x="+str(x)
#print "########################"
#print "Pages:",
#print pages


########################################################
# 1. Maxflow/Mincut based merit computation
########################################################

print "###########Link Graph Adjacency############"
print cfn.print_adjacency()


m=0
n=0
p=0
averageconceptflowoutofpage = {}	
while p < len(pages):
	averageconceptflowoutofpage[pages[p]] = 0
	p = p + 1

while m < len(pages):
	n=0
	while n < len(pages):
		if m != n:
			print "m= " + str(m) + "; n=" + str(n) + ": Citation graph merit for (source,sink) = (" + pages[m] + ", " + pages[n] + ") ====== " + str(cfn.max_flow(m, n))
			averageconceptflowoutofpage[pages[m]] = averageconceptflowoutofpage[pages[m]] + cfn.max_flow(m,n)
			print 'Mincut for the citation graph maxflow for (source,sink) = ('+ pages[m] + ", " + pages[n] + ') :',
			print cfn.mincut
		n=n+1
	averageconceptflowoutofpage[pages[m]] = averageconceptflowoutofpage[pages[m]] / len(pages)
	m=m+1
print 'Average concept maxflow out of each page: ',
print averageconceptflowoutofpage


#########################################################
# 2. finding number of nodes within radius from a source node in citation graph
#########################################################
p=0
radius = 2
currentlevel = 0
while p < len(pages):
	cfn.find_all_paths_of_radius_from_source(p, radius, currentlevel)
	print 'Set of nodes within radius ' + str(radius) + ' of the source = ' + pages[p] + ' ==== ',
	print  cfn.setofnodes
	print 'Number of nodes within radius ' + str(radius) + ' of the source = ' + pages[p] + ' ==== ',
	print  len(cfn.setofnodes)
	p = p + 1
	cfn.setofnodes = []
