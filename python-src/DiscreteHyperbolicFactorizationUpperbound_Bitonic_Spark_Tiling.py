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

def hyperbolic_tiling(number):
	tiles=[]
	coordinates=[]
	tilesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.mergedtiles","w")
        coordinatesf=open("./DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark.coordinates","w")

	x=1
	y=number
	while x <= number and y > 0:
		print "x,y:",x,y
		coordinates.append(x)
		tiles.append(y*x)
		x=x+1
		y=int(number/(x))
	print "tiles:",tiles
	print "coordinates:",coordinates
	for x in xrange(len(tiles)-1):
		tileelement=tiles[x]
		while tileelement > tiles[x+1]:	
			tilesf.write(str(tileelement))
			tilesf.write("\n")
			coordinatesf.write(str(coordinates[x]))
			coordinatesf.write("\n")
			tileelement = tileelement - 1
	tilesf.write(str(tiles[len(tiles)-1]))
	tilesf.write("\n")
	coordinatesf.write(str(coordinates[len(tiles)-1]))
	coordinatesf.write("\n")
	no_of_bits=int(math.log(number,2) + 1.0) 
	print "number of bits:",no_of_bits
	zero_fill=int(math.pow(2,no_of_bits) - number)
	print zero_fill
	for z in xrange(zero_fill-1):
		tilesf.write(str("0"))
		tilesf.write("\n")
		coordinatesf.write(str("0"))
		coordinatesf.write("\n")
	tilesf.write(str("0"))
	coordinatesf.write(str("0"))

if __name__=="__main__":
	hyperbolic_tiling(15)
		
		
		
