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

import math
import sys

class Entro:
	def __init(self):
		pass

	#Minimum Description Length
	#Reference: http://homepages.cwi.nl/~pdg/ftp/mdlintro.ps
	#If the text comprises standard ASCII or Unicode alphabet of size 256 or 512
	#MDL = -log p1^n1 * p2^n2 * .... p256^n256 .... * p512^n512
	#where each pi is probability of occurence of the alphabet
	#and ni is number of occurrences of the alphabet - sigma(ni)=size of the text
	#Thus the entire text is minimum-describable as Bernoulli trials
	def MDL(self, text):
		occurdict={}
		for i in text:
			if i not in occurdict:
				occurdict[i]=1
			else:
				occurdict[i]=occurdict[i] + 1
	
		probdict={}
		for k,v in occurdict.items():
			if k not in occurdict:
				probdict[k]=0.0
			else:
				probdict[k] = float(v)/float(len(text))

		print probdict
		
		mdl=1.0
		for k,v in probdict.items():
			print "v=",v,"; occurdict[k]=",occurdict[k]
			if v != 0.0:
				proboccur=math.pow(v,occurdict[k])
				if mdl * proboccur > 0.0:
					mdl  = mdl * proboccur
		print "mdl:",abs(mdl)
		return -1 * math.log(abs(mdl)) 

	def entropy(self, text):
		occurdict={}
		for i in text:
			if i not in occurdict:
				occurdict[i]=1
			else:
				occurdict[i]=occurdict[i] + 1
	
		probdict={}
		for k,v in occurdict.items():
			if k not in occurdict:
				probdict[k]=0.0
			else:
				probdict[k] = float(v)/float(len(text))

		entropy=0.0
		sumprob=0.0
		print probdict
		for k,v in probdict.items():
			if v != 0.0:
				entropy = entropy - (v * math.log(v))
			sumprob=sumprob+v
		print "sumprob (must be 1)", sumprob
		return entropy


if __name__=="__main__":
	e=Entro()
	entr = e.entropy(sys.argv[1])
	print "Entropy of text [",sys.argv[1],"]= " + str(entr) 
