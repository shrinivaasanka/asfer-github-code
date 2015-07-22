#---------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#---------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------


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
			if v != 0.0:
				mdl  = mdl * (math.pow(v,occurdict[k]))
		return -1 * math.log(mdl) 

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




print sys.argv[1]
e=Entro()
entr = e.entropy(sys.argv[1])
print "Entropy of text [",sys.argv[1],"]= " + str(entr) 
