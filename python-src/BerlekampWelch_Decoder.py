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

ordinaldict={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15,'g':16,'h':17,'i':18,'j':19,'k':20,'l':21,'m':22,'n':23,'o':24,'p':25,'q':26,'r':27,'s':28,'t':29,'u':30,'v':31,'w':32,'x':33,'y':34,'z':35}
alphabetdict={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f',16:'g',17:'h',18:'i',19:'j',20:'k',21:'l',22:'m',23:'n',24:'o',25:'p',26:'q',27:'r',28:'s',29:'t',30:'u',31:'v',32:'w',33:'x',34:'y',35:'z'}

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
	textMessage=True
	#Following is a text with error for "thisissentence" and Berlekamp-Welch algorithm list decodes it with a window for ordinal values
	#This text was automatically generated from a previous execution of Berlekamp-Welch algorithm
	#i.e thisissentence ===> thisisseisdmbd ===> [<list of texts which should be approximately "thisissentence">]
	text="thisisseisdmbd"
	listdecodedtext=["","",""]
	points=[]
	if textMessage==True:
		cnt=1
		for x in text:
			points.append((cnt,ordinaldict[x]))
			cnt+=1
	else:
		points=[(1,4),(2,33),(3,44),(4,17),(5,9),(6,2),(7,10),(8,11),(9,23),(10,12),(11,15),(12,34),(13,11),(14,24),(15,76),(16,21),(17,65)]
	bw=BerlekampWelch_Decoder(points)
	poly=bw.gaussian_elimination_and_extract_polynomial()
	print "polynomial:",poly
	if textMessage:
		print "text (in ordinals):", points
		for x in points:
			ordinal=int(np.polyval(poly[0],x[0]))
			if ordinal >= 0 and ordinal <= 35:
				print "point:",x," ------- values decoded:(",x[0],",",ordinal,")"
				print "ordinal values decoded:",alphabetdict[ordinal]
				listdecodedtext[0]+=alphabetdict[ordinal+1]
				listdecodedtext[1]+=alphabetdict[ordinal]
				listdecodedtext[2]+=alphabetdict[ordinal-1]
			else:
				print "ordinal values not decoded:",ordinal
		print "Decoded text should be most likely one of :",listdecodedtext
	else:
		for x in points:
			print "x:",x," ------- values decoded:(",x[0],",",np.polyval(poly[0],x[0]),")"
