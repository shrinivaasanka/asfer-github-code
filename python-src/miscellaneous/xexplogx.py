#ASFER - a ruleminer which gets rules specific to a query and executes them
#Copyright (C) 2009-2013  Ka.ShrinivaasanA

#miscellaneous function plotter

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

#mail to: ka.shrinivaasan@gmail.com (Krishna iResearch)
#-------------------------------------------------------------------------

import math

x=200000000
c=6
while True:
	if x == 20000000000:
		break
	logx = math.log(x)
	explogx = math.pow(math.log(x), c)
	xbyexplogx = x / explogx
	#print "xbyexplogx: ", xbyexplogx
	if logx - xbyexplogx < 0:
		print "sign change point: x = ",x," #### logx - logxbyexplogx: ", logx - xbyexplogx
	x=x+1
	
