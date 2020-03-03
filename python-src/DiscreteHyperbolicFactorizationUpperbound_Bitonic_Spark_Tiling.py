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

import math
import json

alltiles={}
allcoordinates=[]
next=0

def hyperbolic_tiling(number):
	tilesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.mergedtiles","w")
        coordinatesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.coordinates","w")
	no_of_bits=int(math.log(number,2)+1.0) 
	print "number of bits:",no_of_bits
	power_of_two=int(math.pow(2,no_of_bits))

	for z in xrange(power_of_two):
		alltiles[z]=0
		allcoordinates.append(0)

	print len(alltiles)
	print len(allcoordinates)

        xtile_start=float(number/2.0)
        xtile_end=float(number)
        y=1.0
	PADDING=0.0
        while y < number:
                create_tile(int(number),int((xtile_start)-PADDING),int(y),int((xtile_end)+PADDING),int(y))
                xtile_end=xtile_start
                xtile_start=xtile_end-(number/((y+1.0)*(y+2.0)))
		y += 1

	print "alltiles:",alltiles
	print "allcoordinates:",allcoordinates
	json.dump(alltiles,tilesf)
	json.dump(allcoordinates,coordinatesf)


def create_tile(N, xleft, yleft, xright, yright):
	global next
	i=0
	print "create_tile(): xleft=",xleft,"; yleft=",yleft,"; xright=",xright,"; yright=",yright 
        while i <= (xright-xleft) and next < N:
                alltiles[next]=int((xleft+i)*yleft)
                allcoordinates[next]=int(yleft)
		print "next=",next
		print "alltiles[next]=",alltiles[next]
		print "allcoordinates[next]=",allcoordinates[next]
                next += 1
		i += 1

if __name__=="__main__":
	hyperbolic_tiling(723)
