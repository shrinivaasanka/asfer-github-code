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

#Kullback-Leibler Divergence for 2 Probability Distributions:
#------------------------------------------------------------
#Measures how close two probability distributions are - weighted sum of number of bits required to represent the average distance between two
#probability distributions - a correlation coefficient

import math
f1=open("KLDivergence_Dataset1.txt")
f2=open("KLDivergence_Dataset2.txt")
i=0
kld=0.0
dists=zip(f1.read().split(),f2.read().split())
for s in dists:
	print "[p[",i,"],q[",i,"]) = [",s[0],",",s[1],"]"
	kld=kld + float(s[0])*math.log(float(s[0])/float(s[1]))
	i+=1
print kld	
