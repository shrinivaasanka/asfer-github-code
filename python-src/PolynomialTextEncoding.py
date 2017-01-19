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
#---------------------------------------------------------------------------------------------------------

from nltk.metrics.distance import edit_distance
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import polynomial as P
import math

text1="wfffffffffdlkldddeeeeeeeeerrrrrrrrsdsd"
text2="wfffffffffdlkldddeeeeeeeeerrrrrrrrsdsd"
text3="The Chennai Metropolitan Area is the fourth most populous, and the fourth largest metropolitan The CMA has an area of 1,189 km spread over three districts. It includes the whole of the Chennai District, along with the Ambattur"
text4="Chennai is the capital of the Indian state of Tamil Nadu. Located on the Coromandel Coast off The Chennai Metropolitan Area is one of the largest city economies of India. In January 2015, it was ranked third in terms of per capita GDP."
text5="jfkdjkervnnkdnfiujw9ukdkjksjkjskjdkjwijeijijwekjkdjksdjk"
text6="kxkjkfjejriicxnlkkjdjsk;eisldklklsklksdklskdlskdklskdlkl"
text7="fdjfdkfjkjeiurudnjkeuruue9ur9weijdns9uuq9wei9wuiuencjndjnfjdjhfifeu3esopksokoa"
text8="kwu9e2iejjdjiwue9u29ieodjosjdijsidj93ueumknkncjvnjbdubvufuiejiwjidjw9ue2i9wdow"
text9="fdjfjkkkkkkkkkkkkkfjjjjjjjjjjjskwwwwwwwwwwwwwwwwwwiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
text10="wjejwejwkjekwjkejkwjekjwkjekwjjoisjdiwidoiweiwie0iw0eio0wie0wie0iw0ei0cndknfndnfndnfkdjfkjdfkjd"


class PolynomialTextEncoding(object):
	def __init__(self):
		self.xaxis=[]
		self.yaxis=[]
		self.polynomialfit=[]

	def strpoints(self,s):
		index=0
		axis=[]
		for x in s:
			axis.append(ord(x))
			index+=1
		return axis

	def text2polynomial(self,str):
		index=0
		self.xaxis=[]
		self.yaxis=[]
		strpts=self.strpoints(str)
		self.xaxis=xrange(len(str))
		self.yaxis=self.strpoints(str)
		print "X-axis:",self.xaxis
		print "Y-axis:",self.yaxis	 
		self.polynomialfit=P.polyfit(self.xaxis,self.yaxis,5)
		print "Coefficients of fitting polynomial of degree 5:",self.polynomialfit
		plt.plot(self.xaxis, self.yaxis) 
		#plt.show()
		return self.yaxis

	def polynomial_jensenshannon_edit_distance(self,str1,str2):
		str1yaxis=self.strpoints(str1)
		str2yaxis=self.strpoints(str2)
	        str1str2_tuple=zip(str1yaxis,str2yaxis)
		if len(str1yaxis) > len(str2yaxis):
			for i in str1yaxis[len(str2yaxis):]:
				str1str2_tuple.append((i,1))	
		else:
			if len(str1yaxis) < len(str2yaxis):
				for i in str2yaxis[len(str1yaxis):]:
					str1str2_tuple.append((1,i))	
			
		#print "str1str2_tuple:",str1str2_tuple
		kld1=kld2=0.0
	        i=0
	        for s in str1str2_tuple:
                	kld1=kld1 + -1*float(s[0])*math.log((-1*float(s[0]))/(-1*float(s[1])))
                	i+=1
	        i=0
       		for s in str1str2_tuple:
                	kld2=kld2 + -1*float(s[1])*math.log((-1*float(s[1]))/(-1*float(s[0])))
                	i+=1
        	#print "Jensen-Shannon Distance [ 0.5 * KL(P,Q) + 0.5 * KL(Q,P) ]:", 0.5*kld1 + 0.5*kld2
        	return abs(0.5*kld1 + 0.5*kld2)

	def polynomial_l2norm_edit_distance(self,str1,str2):
		#Discrete version of inner product of 2 polynomials 
		str1yaxis=self.strpoints(str1)
		str2yaxis=self.strpoints(str2)
	        str1str2_tuple=zip(str1yaxis,str2yaxis)
		if len(str1yaxis) > len(str2yaxis):
			for i in str1yaxis[len(str2yaxis):]:
				str1str2_tuple.append((i,1))	
		else:
			if len(str1yaxis) < len(str2yaxis):
				for i in str2yaxis[len(str1yaxis):]:
					str1str2_tuple.append((1,i))	
			
		#print "str1str2_tuple:",str1str2_tuple
		l2norm=0.0
		for k,v in str1str2_tuple:
			l2norm = l2norm + (k-v)*(k-v)
		return math.sqrt(l2norm) 

if __name__=="__main__":
	pe=PolynomialTextEncoding()
	str1points=pe.text2polynomial(text1)
	str2points=pe.text2polynomial(text2)
	str3points=pe.text2polynomial(text3)
	str4points=pe.text2polynomial(text4)
	str5points=pe.text2polynomial(text5)
	str6points=pe.text2polynomial(text6)
	str7points=pe.text2polynomial(text7)
	str8points=pe.text2polynomial(text8)
	str9points=pe.text2polynomial(text9)
	str10points=pe.text2polynomial(text10)
	print "##################################################################################"
	print "Wagner-Fischer Edit Distance for text1 and text2:",edit_distance(text1,text2)
	print "Polynomial Encoding Edit Distance (JensenShannon) for text1 and text2:",pe.polynomial_jensenshannon_edit_distance(text1,text2)
	print "Polynomial Encoding Edit Distance (L2 Norm) for text1 and text2:",pe.polynomial_l2norm_edit_distance(text1,text2)
	print "##################################################################################"
	print "Wagner-Fischer Edit Distance for text3 and text4:",edit_distance(text3,text4)
	print "Polynomial Encoding Edit Distance (JensenShannon) for text3 and text4:",pe.polynomial_jensenshannon_edit_distance(text3,text4)
	print "Polynomial Encoding Edit Distance (L2 Norm) for text3 and text4:",pe.polynomial_l2norm_edit_distance(text3,text4)
	print "##################################################################################"
	print "Wagner-Fischer Edit Distance for text5 and text6:",edit_distance(text5,text6)
	print "Polynomial Encoding Edit Distance (JensenShannon) for text5 and text6:",pe.polynomial_jensenshannon_edit_distance(text5,text6)
	print "Polynomial Encoding Edit Distance (L2 Norm) for text5 and text6:",pe.polynomial_l2norm_edit_distance(text5,text6)
	print "##################################################################################"
	print "Wagner-Fischer Edit Distance for text7 and text8:",edit_distance(text7,text8)
	print "Polynomial Encoding Edit Distance (JensenShannon) for text5 and text6:",pe.polynomial_jensenshannon_edit_distance(text7,text8)
	print "Polynomial Encoding Edit Distance (L2 Norm) for text5 and text6:",pe.polynomial_l2norm_edit_distance(text7,text8)
	print "##################################################################################"
	print "Wagner-Fischer Edit Distance for text9 and text10:",edit_distance(text9,text10)
	print "Polynomial Encoding Edit Distance (JensenShannon) for text5 and text6:",pe.polynomial_jensenshannon_edit_distance(text9,text10)
	print "Polynomial Encoding Edit Distance (L2 Norm) for text5 and text6:",pe.polynomial_l2norm_edit_distance(text9,text10)
	print "##################################################################################"
