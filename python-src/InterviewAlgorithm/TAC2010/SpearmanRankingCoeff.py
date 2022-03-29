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

from __future__ import division
otherrankingid={}
otherranking=[[]]
intrinsicmeritranking=[[]]

otherrankingid[0] = "Google ranking for \'data mining\'"
otherranking[0] = [1,2,3,9,4,5,7,8,10,6]
intrinsicmeritranking[0] = [1,2,3,4,5,6,7,8,9,10]

otherrankingid[1] = "Google ranking for \'literary\'"
otherranking.append([6,9,1,2,4,8,10,3,7,5])
intrinsicmeritranking.append([1,2,3,4,5,6,7,8,9,10])

otherrankingid[2] = "Google ranking for \'philosophy\'"
otherranking.append([1,4,8,9,10,2,6,5,7,3])
intrinsicmeritranking.append([1,2,3,4,5,6,7,8,9,10])

otherrankingid[3] = "Google ranking for \'haiti earthquake\'"
otherranking.append([1,5,3,6,7,2,4])
intrinsicmeritranking.append([1,2,3,4,5,6,7])

otherrankingid[4] = "Human ranking(2 judges) for \'democracy\'"
otherranking.append([4.5,2,2,3.5,5,5])
intrinsicmeritranking.append([5,3,4,1,6,2])

otherrankingid[5] = "Human ranking(1 judge) for \'soap\'"
otherranking.append([5,1,2,3,4])
intrinsicmeritranking.append([5,1,3,2,4])

i=0
r=0
sigmadisqr=0.0
pearsonnum=0.0
pearsondenom1=0.0
pearsondenom2=0.0
pearsoncoeff=0.0
rho=0.0
n=0
while r < len(otherranking):
	n=len(otherranking[r])
	otherrankmean=sum(otherranking[r])/n
	intrinsicmeritrankmean=sum(intrinsicmeritranking[r])/n
	while i < len(otherranking[r]):
		sigmadisqr = sigmadisqr + (intrinsicmeritranking[r][i] - otherranking[r][i])*(intrinsicmeritranking[r][i] - otherranking[r][i])
		pearsonnum = pearsonnum + (intrinsicmeritranking[r][i] - intrinsicmeritrankmean)*(otherranking[r][i] - otherrankmean)	
		pearsondenom1 = pearsondenom1 + (intrinsicmeritranking[r][i] - intrinsicmeritrankmean)*(intrinsicmeritranking[r][i] - intrinsicmeritrankmean)
		pearsondenom2 = pearsondenom2 + (otherranking[r][i] - otherrankmean)*(otherranking[r][i] - otherrankmean)
		i=i+1
	rho = 1 - ((6 * sigmadisqr)/(n*(n*n - 1)))
	pearsoncoeff = pearsonnum /(pearsondenom1 * pearsondenom2)
	print "##########################################################"
	print "(1) . Spearman ranking coeffiecient for " + otherrankingid[r] +" : ",
	print otherranking[r], 
	print " -----and------",
	print intrinsicmeritranking[r],
	print "-----is : ",
	print str(rho)
	print "(2) . Pearson ranking coeffiecient for " + otherrankingid[r] +" : ",
	print otherranking[r], 
	print " -----and------",
	print intrinsicmeritranking[r],
	print "-----is : ",
	print str(pearsoncoeff)
	rho=0
	i=0
	r=r+1
	sigmadisqr=0.0
	pearsonnum=0.0
	pearsondenom1=0.0
	pearsondenom2=0.0
	pearsoncoeff=0.0

