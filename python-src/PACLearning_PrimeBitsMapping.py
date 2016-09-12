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
import json
mappings=[]
primebit=0
while primebit < 14:
	primes=open("First10000PrimesBinary.txt","r")
	index=0
	index_to_primebit_dict={}
	for p in primes:
		if len(p) < 17:
			paddinglen=16-len(p)
			p1 = "0b"
			for i in xrange(paddinglen):
				p1 += "0"
			for s in p[2:]:
				p1 += s 
		p=p1
		strbin=str(bin(index))
		if p[primebit]=='0':
			index_to_primebit_dict[strbin[2:]]=True
		else:
			index_to_primebit_dict[strbin[2:]]=False
		index += 1
	mappings.append(index_to_primebit_dict)
	index_to_primebit_dict={}
	primebit += 1
primemappings=open("PACLearning_PrimeBitsMapping.txt","w")
json.dump(mappings,primemappings)
