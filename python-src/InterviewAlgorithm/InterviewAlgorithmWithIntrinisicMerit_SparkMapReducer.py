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

#Apache Spark RDD MapReduce Transformations script for Recursive Gloss Overlap. Also creates a SparkSQL DataFrame temp table.
#Following recursive graph construction is map-reduced in Spark
                #for keyword in freqterms1:
                #       #WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset()
                #       disamb_synset = best_matching_synset(freqterms1, wn.synsets(keyword))
                #       prevlevelsynsets = prevlevelsynsets + [disamb_synset]
                #       if len(wn.synsets(keyword)) != 0:
                #               disamb_synset_def = disamb_synset.definition()
                #               tokens = nltk.word_tokenize(disamb_synset_def)
                #               fdist_tokens = FreqDist(tokens)
                #               tokensofthislevel = tokensofthislevel + ([w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts and fdist_tokens.freq(w)])

#Example pyspark RDD mapreduce code at: http://www.mccarroll.net/blog/pyspark2/

from __future__ import division
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row 
import operator
import pickle
import sys

import nltk
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.book import FreqDist 
from nltk.corpus import stopwords
from collections import namedtuple

#rgo_object=namedtuple("rgo_object", "tokensatthislevel prevlevelsynsets")
rgo_object=namedtuple("rgo_object", "tokensatthislevel")

def asfer_pickle_dump(prevlevelsynsets,picklef):
     for s in prevlevelsynsets:
	picklef.write(repr(s)+",")

def asfer_pickle_load(picklef):
     line=picklef.readline()
     synsets=[]
     stringsynsets=line.split(",")
     for s in stringsynsets:
         s_synset_tokens=s.split("'")
	 #print "s_synset_tokens:",s_synset_tokens
	 if len(s_synset_tokens) == 3:
	     s_synset_word_tokens=s_synset_tokens[1].split(".")
	     #print "s_synset_word_tokens:",s_synset_word_tokens
	     s_synsets=wn.synsets(s_synset_word_tokens[0])
	     #print "s_synsets:",s_synsets
             synsets.append(s_synsets[0])	
     #print "asfer_pickle_load(): synsets=",synsets
     return synsets

def mapFunction(freqterms1):
     prevlevelsynsets=[]
     stopwords = nltk.corpus.stopwords.words('english')
     stopwords = stopwords + [' ','or','and','who','he','she','whom','well','is','was','were','are','there','where','when','may', 'The', 'the', 'In','in','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
     puncts = [' ','.', '"', ',', '{', '}', '+', '-', '*', '/', '%', '&', '(', ')', '[', ']', '=', '@', '#', ':', '|', ';','\'s']
     mapped_object=()
     print "mapFunction(): freqterms1:",freqterms1
     for keyword in [freqterms1]:
       	 #WSD - invokes Lesk's algorithm adapted to recursive gloss overlap- best_matching_synset()
         disamb_synset = best_matching_synset(freqterms1, wn.synsets(keyword))
     	 #print "mapFunction(): keyword = ",keyword,"; disamb_synset=",disamb_synset
         prevlevelsynsets = prevlevelsynsets + [disamb_synset]
         if len(wn.synsets(keyword)) != 0:
      		         disamb_synset_def = disamb_synset.definition()
      			 tokens = nltk.word_tokenize(disamb_synset_def)
             		 fdist_tokens = FreqDist(tokens)
         		 fdist_tokens=[w for w in fdist_tokens.keys() if w not in stopwords and w not in puncts and fdist_tokens.freq(w)]
	 		 #mapped_object=rgo_object(fdist_tokens.keys(),prevlevelsynsets)
	 		 mapped_object=rgo_object(fdist_tokens)
     #print "mapFunction(): prevlevelsynsets=",prevlevelsynsets
     picklef=open("RecursiveGlossOverlap_MapReduce_Persisted.txt","ab")
     asfer_pickle_dump(prevlevelsynsets,picklef)
     return (1,mapped_object)
 
def reduceFunction(mapped_object1,mapped_object2):
    reduced_rgo_object=()
    #print "reduceFunction():mapped_object1: ",mapped_object1
    #print "reduceFunction():mapped_object2: ",mapped_object2
    #reduced_rgo_object=rgo_object(mapped_object1.tokensatthislevel+mapped_object2.tokensatthislevel,mapped_object1.prevlevelsynsets+mapped_object2.prevlevelsynsets) 
    if (not mapped_object1):	
    	reduced_rgo_object=rgo_object(mapped_object2.tokensatthislevel) 
    if (not mapped_object2):
    	reduced_rgo_object=rgo_object(mapped_object1.tokensatthislevel) 
    if (mapped_object1 and mapped_object2):
    	reduced_rgo_object=rgo_object(mapped_object1.tokensatthislevel+mapped_object2.tokensatthislevel) 
    print "reduceFunction():returns : ",reduced_rgo_object
    return reduced_rgo_object

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

def Spark_MapReduce(level, wordsatthislevel):
        spcon=SparkContext() 
	print "Spark_MapReduce(): wordsatthislevel:",wordsatthislevel
	paralleldata=spcon.parallelize(wordsatthislevel)
	#k=paralleldata.map(lambda wordsatthislevel: mapFunction(wordsatthislevel)).reduceByKey(reduceFunction)
	k=paralleldata.map(mapFunction).reduceByKey(reduceFunction)

	#dict_k=k.collect()
	#s = sorted(dict_k.items(),key=operator.itemgetter(1), reverse=True)
	#print "Spark MapReduce results:"
	#print s
	############################
	sqlContext=SQLContext(spcon)
	recursiveglossoverlap_schema=sqlContext.createDataFrame(k.collect())
	recursiveglossoverlap_schema.registerTempTable("Interview_RecursiveGlossOverlap")
	query_results=sqlContext.sql("SELECT * FROM Interview_RecursiveGlossOverlap")
	dict_query_results=dict(query_results.collect())
	print "Spark_MapReduce() - SparkSQL DataFrame query results:"
	print dict_query_results[1]
	spcon.stop()
	return dict_query_results[1]

#Following parents computation from prevlevel synsets is map-reduced in Spark
#parents (at level i-1) of a given vertex at level i
#arguments are a keyword at present level and all disambiguated synsets of previous level
#def parents(keyword, prevlevelsynsets):
#        parents = []
#        for syn in prevlevelsynsets:
#                if type(syn) is nltk.corpus.reader.wordnet.Synset:
#                        syndef_tokens = set(nltk.word_tokenize(syn.definition()))
#                        if keyword in syndef_tokens:
#                                parents = parents + [syn]
#        return parents

def mapFunction_Parents(keyword,prevleveltokens):
	parents=[]
	print "mapFunction_Parents(): keyword = ",keyword,";prevleveltokens:",prevleveltokens
	for prevleveltoken in prevleveltokens:
	   syn=best_matching_synset(prevleveltokens, wn.synsets(prevleveltoken))
	   #syns=wn.synsets(prevleveltoken)
	   #syn=syns[0]
           if type(syn) is nltk.corpus.reader.wordnet.Synset:
                   syndef_tokens = set(nltk.word_tokenize(syn.definition()))
	           #print "mapFunction_Parents(): syndef_tokens=",syndef_tokens
       	           if keyword in syndef_tokens:
				parents = parents + [prevleveltoken]
	print "mapFunction_Parents(): returns=",parents
	return (1,parents)


def reduceFunction_Parents(parents1, parents2):
	print "reduceFunction_Parents(): returns=", parents1 + parents2
	return parents1 + parents2

def Spark_MapReduce_Parents(keyword, tokensofprevlevel):
	spcon = SparkContext()
	paralleldata = spcon.parallelize(tokensofprevlevel)
	k=paralleldata.map(lambda keyword: mapFunction_Parents(keyword,tokensofprevlevel)).reduceByKey(reduceFunction_Parents)
	sqlContext=SQLContext(spcon)
	parents_schema=sqlContext.createDataFrame(k.collect())
	parents_schema.registerTempTable("Interview_RecursiveGlossOverlap_Parents")
	query_results=sqlContext.sql("SELECT * FROM Interview_RecursiveGlossOverlap_Parents")
	dict_query_results=dict(query_results.collect())
	print "Spark_MapReduce_Parents() - SparkSQL DataFrame query results:"
	spcon.stop()
	print "Spark_MapReduce_Parents(): dict_query_results[1]=",dict_query_results[1]
	return dict_query_results[1]
	
