#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

import WordSubstringProbabilities

vowels = ['A','E','I','O','U','a','e','i','o','u']

def removevowels(w):
	wcomp=""
	for x in w:
		if x in vowels:
			wcomp = wcomp + "_"
		else:
			wcomp = wcomp + x
	return wcomp

def compute_maximumlikelihood(comp, suggestions):
	maxlikely=""
	maxlikelyprob=0.0
	for x in suggestions:
		#Bayesian 
		#probability=prob(x,comp)	
		#if probability > maxlikelyprob:
		#	maxlikelyprob = probability
		#	maxlikely=x
		maxlikely = HiddenMarkovModel_MLE(comp)
	print "comp=",comp,"; maxlikely=",maxlikely
	return maxlikely 

#def prob(x,comp):
#	if len(x) > len(comp):
#		xptr=0
#		compptr=0
#		print "x=",x,"; comp=",comp
#		while xptr < len(x) and compptr < len(comp):
#			while xptr < len(x):
#				if x[xptr] in vowels and comp[compptr] != x[xptr]:
#					xptr=xptr+1
#			compptr=compptr+1
#		if xptr == len(x) and compptr == len(comp):
#			print "x = ",x,";comp = ",comp,"; return 1"
#			return 1.0
#		else:
#			return 0.0
#

def HiddenMarkovModel_MLE(comp):
	print "#####################################################################################################"
	#This is only a sample MLE using Forward probabilities.
	#Implementing for all words requires precomputed constant read-only hashtable of approximately 
	#500000 substring-probabilites entries or more.	

	#Prior probabilites for "tha", "the", "thi", "tho", "thu" prefixes
	Probabilities_prefixes={"tha":0.4, "the":0.3, "thi":0.1, "tho":0.1, "thu":0.1, "ca":0.3, "ce":0.1, "ci":0.1, "co":0.4, "cu":0.1}

	#Prior probabilites for "at", "et", "it", "ot", "ut" suffixes
	Probabilities_suffixes={"at":0.3, "et":0.2, "it":0.1, "ot":0.2, "ut":0.2, "as":0.1, "es":0.2, "is":0.4, "os":0.2, "us":0.1}
	prefixsuffixprob=WordSubstringProbabilities.wordprefixsuffixprobdist()
	#Probabilities_prefixes=prefixsuffixprob[0]
	#Probabilities_suffixes=prefixsuffixprob[1]
	#print "prefixsuffixprob=",prefixsuffixprob

	maxk1=""
	maxv1=-1.0
	maxk2=""
	maxv2=-1.0

	for k1,v1 in Probabilities_prefixes.items():
		if maxv1 < v1:
			maxv1 = v1
			maxk1 = k1	
			#maxvowel = maxk1[len(maxk1)-1]

	for k2,v2 in Probabilities_suffixes.items():
		if maxv2 < v2:
			maxv2 = v2
			maxk2 = k2 
	
	likelydict={}
	matchinglikelydict={}
	
	#Precomputed read-only Hidden Markov Model Forward probabilities product priors hashtable
	#This is for all substrings in English dictionary and in its full size could have 500000+ entries
	#and has to be read from disk storage
	for k3,v3 in Probabilities_prefixes.items():
		for k4,v4 in Probabilities_suffixes.items():
			#print "k3=",k3,"; k4=",k4
			if len(k3) > 0 and len(k4) > 0 and (k3[len(k3)-1] == k4[0]):
				likelydict[k3[:-1]+k3[len(k3)-1]+k4[1:]] = v3 * v4 

	for k5, v5 in Probabilities_suffixes.items():
		likelydict[k5]=v5
	for k6, v6 in Probabilities_prefixes.items():
		likelydict[k6]=v6

	compsubstrings=comp.split("_")
	print compsubstrings

	#For loop that matches a compressed word to likely candidate words by left-to-right substring comparison
	#between compressed word's substrings and the dictionary entries and populates a matching word dictionary
	start=0
	i=0
	compsubstrindex=-2
	match=False
	for k7, v7 in likelydict.items():
		print "k7=",k7,"; v7=",v7
		while start < len(k7) and i < len(compsubstrings):
			print "finding substring :",compsubstrings[i]," in : ",k7
			compsubstrindex = k7.find(compsubstrings[i],start)
			print "compsubstrindex =",compsubstrindex
			if compsubstrindex == -1:
				match = False
				break
			start = start + len(compsubstrings[i]) 
			i=i+1
		print "compsubstrindex=",compsubstrindex,"; i=",i
		if compsubstrindex > -1 and len(comp)==len(k7):
			match=True
			print "matching; adding to matching likely dict k7 =",k7,"; v7=",v7
			matchinglikelydict[k7] = v7
		match = False
		compsubstrindex = -2
		start=0
		i=0

	#Returns the word with maximum likelihood probability
	#Word returned depends on the HMM priors in the hashtable
	print "matchinglikelydict=",matchinglikelydict	
	maxlikelyretprob=-1.0
	maxlikelyret=""	
	for k7, v7 in matchinglikelydict.items():
		if maxlikelyretprob < v7:
			maxlikelyret = k7	
			maxlikelyretprob = v7

	print "maxlikelyretprob=",maxlikelyretprob, "; maxlikelyret = ",maxlikelyret
	print matchinglikelydict
	return maxlikelyret


def prob(x,comp):
	#Only suggestions with vowels as additional letters are sifted.
	#two pointers in the suggested word and compressed word get incremented
	#and 1 is returned if the compressed word's alphabets are contained in
	#suggested word preserving order from left to right
	print "=============================================="
	setx=set(x)
	setcomp=set(comp)
	#if setcomp.issubset(setx):
	setdiff=setx.difference(setcomp)
	setdiffconso = [y for y in setdiff if y not in vowels]

	if len(setdiffconso)==0 and len(x) > len(comp):
		xptr=0
		compptr=0
		print "x=",x,"; comp=",comp
		while xptr < len(x) and compptr < len(comp):
			while xptr < len(x) and comp[compptr] != x[xptr]:
				print "x[xptr]=",x[xptr],"; comp[compptr]=",comp[compptr]
				xptr=xptr+1
			compptr=compptr+1
		#Both pointers should have reached the end of the respective words
		if xptr == len(x) and compptr == len(comp):
			print "x = ",x,";comp = ",comp,"; return 1"
			return 1.0
		else:
			return 0.0
	

import enchant
f=open("texttocompress.txt","r")
fcomp = open("compressedtext.txt","w")
fdecomp = open("decompressedtext.txt","w")

d = enchant.Dict("en_US")
origfilesize=0
compfilesize=0
compbits=0

wcompcomp=""
#Compression
print "Compression by vowel removal:"
for i in f:
	wcomp = removevowels(i)
	#remove _ in compressed word
	for k in wcomp:
		if k != '_':
			wcompcomp =  wcompcomp + k
		else:
			compbits = compbits+1
	print "wcompcomp = ",wcompcomp
	origfilesize = origfilesize + len(i)
	compfilesize = compfilesize + len(wcompcomp)
	for n in wcomp:
		fcomp.write(n)	
	print "Compression ratio = ", 100*(origfilesize-compfilesize-0.125*compbits)/origfilesize, "%"
	fcomp.close()

fcomp = open("compressedtext.txt","r")
fcompstr = fcomp.read()

#Decompression
print "Decompression using PyEnchant Spellcheck suggest() function:"
for i in fcompstr.split():
	suggestions=d.suggest(i)
	print i, suggestions
	#midpoint=len(suggestions)
	maximumlikelihoodword=compute_maximumlikelihood(i,suggestions)	
	fdecomp.write(maximumlikelihoodword)
	fdecomp.write(" ")
