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

import nltk
import json
from nltk.probability import FreqDist	
englishdict=open("Dictionary.txt","r")
prefixes=[]
suffixes=[]
prefixdict={}
suffixdict={}
prefixprobdict={}
suffixprobdict={}

def computeprefixessuffixes(w):
	for n in xrange(len(w)-1):
		prefixes.append(w[:n].lower())
	for n in xrange(len(w)-1):
		suffixes.append(w[n:].lower())

def wordprefixsuffixprobdist():
	for w in englishdict:
		wtok=w.split()
		if len(wtok) > 0:		
			computeprefixessuffixes(wtok[0])
	#prefixf=open("WordPrefixesProbabilities.txt","w")
	#suffixf=open("WordSuffixesProbabilities.txt","w")
	prefixdict=FreqDist(prefixes)
	suffixdict=FreqDist(suffixes)
	totalprefixes=sum(prefixdict.values())
	totalsuffixes=sum(suffixdict.values())
	for pk,pv in zip(prefixdict.keys(), prefixdict.values()):
		prefixprobdict[pk] = float(pv)/float(totalprefixes)
	for pk,pv in zip(suffixdict.keys(), suffixdict.values()):
		suffixprobdict[pk] = float(pv)/float(totalsuffixes)
	#json.dump(prefixprobdict,prefixf)
	#json.dump(suffixprobdict,suffixf)
	print "prefix probabilities:",prefixprobdict
	print "suffix probabilities:",suffixprobdict
	return (prefixprobdict, suffixprobdict)
	
if __name__=="__main__":
	wordprefixsuffixprobdist()
	
	

