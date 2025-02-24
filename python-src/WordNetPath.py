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

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.book import *
from nltk.corpus import stopwords

def path_between(w1,w2):
	try:
		path_lemmas=[]
		synset1 = wn.synset(w1+".n.01")
		synset2 = wn.synset(w2+".n.01")
		#print synset1.common_hypernyms(synset2) 
		dist_dict1 = synset1._shortest_hypernym_paths(False)
		dist_dict2 = synset2._shortest_hypernym_paths(False)
		inf = float('inf')
		path_distance = inf
		synset1_path=list(dist_dict1.keys())
		synset2_path=list(dist_dict2.keys())
		kcnt=lcnt=0
		for k in synset1_path:
			kcnt += 1
			for l in synset2_path:
				lcnt += 1
				if k==l:
					if path_distance > kcnt+lcnt:
						path_distance = kcnt+lcnt
						path = synset1_path[:kcnt] + synset2_path[:lcnt] 
			lcnt=0
		for p in path:
			plemmanames = p.lemma_names()
			path_lemmas.append(plemmanames[0])
		#print(path_lemmas)
	except:	
		pass
	return path_lemmas
				
if __name__=="__main__":
	path_between("man","city")
