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
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------

#Jensen-Shannon Divergence based on symmetric Kullback-Leibler Divergence for 2 Probability Distributions:
#-----------------------------------------------------------------------------------------------------------
#Jensen-Shannon Divergence = 0.5 * KL(P,Q) + 0.5 * KL(Q,P) where KL is Kullback-Leibler Divergence
#Measures how close two probability distributions are - weighted sum of number of bits required to represent the average distance between two
#probability distributions - a correlation coefficient. Smoothed by weighted average of KL Divergence in both directions.

import math

dataset1=[]
dataset2=[]
sumtotaldataset1=0.0
sumtotaldataset2=0.0

def summation(dataset):
	s=0.0
	for n in dataset:
		s+= -1*float(n)
	return s

def normalize(tuple):
	global dataset1
	global dataset2
	global sumtotaldataset1
	global sumtotaldataset2
	return (float(tuple[0])/float(sumtotaldataset1), float(tuple[1])/float(sumtotaldataset2))	

if __name__=="__main__":
	#f1=open("FFT_classical_1_19July2016_trimmed.txt")
	#f2=open("FFT_classical_2_20July2016_trimmed.txt")
	f1=open("FFT_classical_1_20July2016_trimmed.txt")
	f2=open("FFT_classical_2_19July2016_trimmed.txt")
	i=0
	kld1=0.0
	kld2=0.0
	dataset1=f1.read().split()
	dataset2=f2.read().split()
	sumtotaldataset1=summation(dataset1)
	sumtotaldataset2=summation(dataset2)
	print "sumtotaldataset1 = ",sumtotaldataset1,", sumtotaldataset2 = ",sumtotaldataset2
	unnormalized_dists=zip(dataset1,dataset2)
	normalized_dists=map(normalize, unnormalized_dists)
	#print normalized_dists
	for s in normalized_dists:
		#print "[p[",i,"],q[",i,"]) = [",s[0],",",s[1],"]"
		kld1=kld1 + -1*float(s[0])*math.log((-1*float(s[0]))/(-1*float(s[1])))
		i+=1
	i=0
	for s in normalized_dists:
		#print "[p[",i,"],q[",i,"]) = [",s[1],",",s[0],"]"
		kld2=kld2 + -1*float(s[1])*math.log((-1*float(s[1]))/(-1*float(s[0])))
		i+=1
	print "Jensen-Shannon Distance [ 0.5 * KL(P,Q) + 0.5 * KL(Q,P) ]:", 0.5*kld1 + 0.5*kld2

