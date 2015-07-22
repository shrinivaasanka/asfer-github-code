#------------------------------------------------------------------------------------------------------------
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
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9789346927, 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch):
#http://sourceforge.net/users/ka_shrinivaasan
#https://www.ohloh.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

import rpy2.robjects as robj

#non-linearity starts from k=3.8 and below 3.8 there are periods
k=3.8
x=0.7
chaos_seq=[]
input_seq=[]
#correlation_flag="linear"
correlation_flag="chaotic"

def plotGraph(x):
	no_of_hashes=x*100
	for i in xrange(int(no_of_hashes)):
		print "#",
	print "\n"

#Read input sequence
#f=open("ChaosAttractorInputSequence.txt")
f=open("ChaosAttractorInputSequence_DJIA.txt")
f_str=f.read()
input_seq=f_str.split(",")

#A sample attractor
while True:
	xnext = k*x*(1-x)	
	print "x: ",x,", xnext: ",xnext
	#plotGraph(xnext)
	chaos_seq.append(float(x))
	x=xnext
	if len(chaos_seq) == 19449:
		break

#using rpy2.objects and compute R correlation coefficient
if correlation_flag == "chaotic":
	chaosx = robj.FloatVector(chaos_seq)
if correlation_flag == "linear":
	chaosx = robj.FloatVector(xrange(19449))
print input_seq
inputstreamy = robj.FloatVector(input_seq[0:19449])
print len(chaosx)
print len(inputstreamy)
corfn = robj.r['cor']
corfn(chaosx,inputstreamy)
ret=corfn(chaosx,inputstreamy)
print "correlation coefficient of the two sequences is:", (ret.r_repr())
