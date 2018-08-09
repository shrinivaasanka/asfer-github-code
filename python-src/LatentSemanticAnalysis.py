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
from scipy import linalg
import numpy as np
import ast
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import operator
from collections import defaultdict
from numpy.linalg import matrix_rank

class LSA(object):
	def __init__(self,corpus):
		self.corpus = corpus.split()
	
	def compute_svd(self):
		self.svd = linalg.svd(self.tdmatrix)	 
		print "svd:",self.svd

	def create_tdmatrix(self):
		cvec = CountVectorizer("filename")
		print "self.corpus:",self.corpus
		td=cvec.fit_transform(self.corpus)
		df=pd.DataFrame(td.toarray(),columns=cvec.get_feature_names())
		print "tdmatrix - DataFrame:",df
		print "================================="
		self.tdmatrix = df.values
		print "tdmatrix - DataFrame NumPy array:",self.tdmatrix
		print "================================="

	def similarity(self):
		documents=self.svd[0]
		print "documents:",documents
		id1=0
		for d1 in documents.tolist():
			id2=0
			for d2 in documents.tolist():
				s=self.cosine_similarity(d1,d2)
				print "Similarity of Documents [",self.corpus[id1],"] and [",self.corpus[id2],"] :",s 
				id2 += 1
			id1 += 1

	def cosine_similarity(self,d1,d2):
		similarity=0.0
		for x in zip(d1,d2):
			similarity += x[0]*x[1]	
		return similarity	

	def low_rank_approximation(self):
		singular=self.svd[1]
		singularlist=singular.tolist()
		U=self.svd[0]
		V=self.svd[2]
		#lowrank=int(matrix_rank(self.tdmatrix))
		reducedrank=10
		print "singularlist:",singularlist
		for s in xrange(len(singularlist[reducedrank:])):
			singularlist[reducedrank + s] = 0.0
		singular=np.asarray(singularlist)
		sigma = np.zeros((len(singularlist),self.svd[2].shape[0]))
		for e in xrange(len(singularlist)):
			sigma[e][e] = singular[e]
		self.lra = np.dot(U, np.dot(sigma, V))
		print "low rank approximation:",self.lra

if __name__=="__main__":
	tdfile=open("LatentSemanticAnalysis.txt","r")
	lsa=LSA(tdfile.read())
	lsa.create_tdmatrix()
	lsa.compute_svd()
	lsa.similarity()
	lsa.low_rank_approximation()

