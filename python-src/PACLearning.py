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

#Python implementation for PAC Learning a Boolean Conjunction for five boolean variables
#Reference: http://www.cis.temple.edu/~giorgio/cis587/readings/pac.html

dataset={"10001":True, "11100":False, "11101":True, "10101":True, "00101":False, "11011":False, "11000":False, "00001":True, "10000":False, "00100":False,"00010":False}

hypothesis={"x1":1, "notx1":1, "x2":2, "notx2":2, "x3":3, "notx3":3, "x4":4, "notx4":4, "x5":5, "notx5":5}

for k,v in dataset.items():
	print "key=",k,";value=",v
	if v==True:
		index=0
		for i in k:
			if i=="1":	
				try:
					hypothesis.pop("notx"+str(index+1))
				except:
					pass
			if i=="0":	
				try:
					hypothesis.pop("x"+str(index+1))
				except:
					pass
			index=index+1				

hypolen=len(hypothesis)
for i in xrange(hypolen):
	if hypothesis.has_key("x"+str(i+1)) and hypothesis.has_key("notx"+str(i+1)):
		hypothesis.pop("x"+str(i+1))
		hypothesis.pop("notx"+str(i+1))
	
		
print "Boolean conjunction hypothesis approximating the dataset:",dataset
print "=================================================================="
hypostr=""
for k,v in hypothesis.items():
	hypostr= hypostr + k + " /\ "
print hypostr[:-3]

