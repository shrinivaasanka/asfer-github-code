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
#-----------------------------------------------------------------------------------------------------------

from complement import toint

globalmergedtiles=[]

def bitonic_sort(up, mergedtiles):
	if len(mergedtiles) <= 1:
		return mergedtiles
	else:
		firsthalf = bitonic_sort(True, mergedtiles[:int(len(mergedtiles)/2)])
		secondhalf = bitonic_sort(False, mergedtiles[int(len(mergedtiles)/2):])
		print "bitonicsort: firsthalf: ", firsthalf
		print "bitonicsort: secondhalf: ", secondhalf
		return bitonic_merge(up, firsthalf + secondhalf)

def bitonic_merge(up, mergedtiles):
	if len(mergedtiles) == 1:
		return mergedtiles
	else:
		if(up==True):
			bitonic_compare_true(mergedtiles)
		else:
			bitonic_compare_false(mergedtiles)
		firsthalf = bitonic_merge(up, mergedtiles[:int(len(mergedtiles)/2)])
		secondhalf = bitonic_merge(up, mergedtiles[int(len(mergedtiles)/2):])
		print "bitonic_merge: firsthalf: ", firsthalf
		print "bitonic_merge: secondhalf: ", secondhalf
		return firsthalf+secondhalf

def bitonic_compare_true(mergedtiles):
	print "bitonic_compare_true(): 1. mergedtiles=",mergedtiles
	midpoint = int(len(mergedtiles)/2)
	print "bitonic_compare_true(): up= True" 
	for i in range(midpoint):
		if (mergedtiles[i] > mergedtiles[i+midpoint]) == True:
			temp = mergedtiles[i+midpoint]
			mergedtiles[i+midpoint] = mergedtiles[i]
			mergedtiles[i] = temp 
	print "bitonic_compare_true(): 2. mergedtiles=",mergedtiles

def bitonic_compare_false(mergedtiles):
	print "bitonic_compare_false(): mergedtiles=",mergedtiles
	midpoint = int(len(mergedtiles)/2)
	print "bitonic_compare_false(): up= False" 
	for i in range(midpoint):
		if (mergedtiles[i] > mergedtiles[i+midpoint]) == False:
			temp = mergedtiles[i+midpoint]
			mergedtiles[i+midpoint] = mergedtiles[i]
			mergedtiles[i] = temp 
	print "bitonic_compare_true(): 2. mergedtiles=",mergedtiles

if __name__=="__main__":
	mergedtilesf=open("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_Bitonic.mergedtiles","r")
	#mergedtiles=[10, 3, 5, 71, 30, 11, 20, 4, 330, 21, 110, 7, 33, 9, 39, 46]
	cnt=1
	for i in mergedtilesf:
		globalmergedtiles.append(toint(i))			
		cnt+=1
		#if cnt == 16384:
		if cnt == 256:
			break
	if cnt < 16384:
	#if cnt < 256:
		#while cnt <= 256:
		while cnt <= 16384:
			globalmergedtiles.append(0)
			cnt+=1
	sorted=bitonic_sort(False, globalmergedtiles)
	print "Final bitonic sorted=",sorted
