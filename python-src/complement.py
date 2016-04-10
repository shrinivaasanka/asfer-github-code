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

################################################################################################
# Test python script written in March 2011 While at CMI as JRF for
# "Decidability of Existence and Construction of a Complement of a given Function" :
# http://arxiv.org/abs/1106.4102 and
# https://sites.google.com/site/kuja27/ComplementOfAFunction_earlier_draft.pdf?attredirects=0
# Added to repository for numerical pattern analysis mentioned in:
# https://sourceforge.net/p/asfer/code/HEAD/tree/asfer-docs/AstroInferDesign.txt
# --------------------------
# Updated on 10 April 2016:
# --------------------------
# Function for Ihara Identity and Complement Function extended draft in :
# - https://github.com/shrinivaasanka/asfer-github-code/blob/master/asfer-docs/AstroInferDesign.txt
# - https://sourceforge.net/p/asfer/code/HEAD/tree/asfer-docs/AstroInferDesign.txt
################################################################################################

import math
import string
import decimal

#Lf=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
Lf=[]
cosvalues=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

def getgofx(x):
    u=0
    z=-1
    while True:
        if u in Lf:
            u=u+1
        if u not in Lf:
            z=z+1
            if (z==x):
                return u
            else:
                u=u+1

def toint(primestr):
	print int(decimal.Decimal(primestr))
	return int(decimal.Decimal(primestr))

def IharaIdentity():
	#Imaginary(s) = b = arccos(float(q+1.0)/float(2.0*sqrt(q)))/float(log(q)) for prime q
	for eigen_scaling in cosvalues:
		print "#####################################################################"
		for primestr in Lf:
			if primestr != '':
				prime=toint(primestr)
				num2=2.0*math.sqrt(float(prime))
				num1=(float(2*eigen_scaling*math.sqrt(prime)))/num2
				den=float(math.log(prime))
				imaginary=math.acos(num1)/den
				print "eigen_scaling=",eigen_scaling,"; imaginary(s) for prime ",prime,": ",imaginary
		print "#####################################################################"

if __name__=="__main__":
	primesf=open("First10000Primes.txt","r")
	for line in primesf:
		primes=line.split(" ")
		Lf=Lf+primes[:-1]
	print Lf

	for i in range(10):
		print "g(",i,")=",getgofx(i)
	IharaIdentity()
