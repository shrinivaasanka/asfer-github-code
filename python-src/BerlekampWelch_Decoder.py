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
#--------------------------------------------------------------------------------------------------------

import numpy as np
import math
from scipy.linalg import solve
from numpy.polynomial.polynomial import Polynomial

class BerlekampWelch_Decoder(object):
	def __init__(self,points):
		self.equationsA=[]
		self.equationsB=[]
		n=1
		#E(x)=x+e0 and Q=q0+q1*x+q2*x^2+q3*x^3+...
		for x,y in points:
			equation=[1]
			for i in range(1,len(points)-1):
				equation.append(int(math.pow(n,i)))
			equation.append(-1*y)
			self.equationsA.append(equation)
			n+=1
		for x,y in points:
			self.equationsB.append(-1*x*y)

	def gaussian_elimination_and_extract_polynomial(self):
		a = np.array(self.equationsA)
		b = np.array(self.equationsB)
		print "a:",a
		print "b:",b
		x = solve(a,b)
		print "Polynomial :",x
		qslice = x[:-1].tolist()
		print "qslice:",qslice	
		qslice.reverse()
		qslice = map(lambda x: -1 * x, qslice)	
		print "qslice reversed:",qslice	
		q = np.array(qslice)
		e = np.array([1,-1*x[len(x)-1]])
		print "q:",q
		print "e:",e
		return np.polydiv(q,e)

if __name__=="__main__":
	textMessage=False
	text="Th0st0xsjjk0k"
	points=[]
	if textMessage==True:
		cnt=0
		for x in text:
			points.append((cnt,ord(x)))
			cnt+=1
	else:
		points=[(1,4),(2,3),(3,4),(4,1),(5,1),(6,2),(7,10),(8,11),(9,23),(10,12),(11,15),(12,34),(13,11),(14,24)]
	bw=BerlekampWelch_Decoder(points)
	poly=bw.gaussian_elimination_and_extract_polynomial()
	print "polynomial:",poly
	if textMessage:
		for x in points:
			ordinal=int(np.polyval(poly[0],x[0]))
			if ordinal > 0 and ordinal < 255:
				print "ordinal values decoded:",chr(ordinal)
	else:
		for x in points:
			print "x:",x," ------- values decoded:(",x[0],",",np.polyval(poly[0],x[0]),")"
