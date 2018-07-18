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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
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
from sympy.solvers.diophantine import diop_general_sum_of_squares
from sympy.solvers.diophantine import diop_DN
from sympy.abc import a, b, c, d, e, f
from collections import defaultdict
import DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized
import pprint
import operator
import json
import ast

#Lf=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
Lf=[]
cosvalues=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
complement_diophantine_map={}
unknown_max_limit=11

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
	if primestr != '' and not None:
		return int(decimal.Decimal(primestr))

def all_possible_unknowns_four_squares():
	all_possible_unknowns=[]
	for a in xrange(unknown_max_limit):
		for b in xrange(unknown_max_limit):
			for c in xrange(unknown_max_limit):
				for d in xrange(unknown_max_limit):
					tuple_set=set([(a,b,c,d)])
					all_possible_unknowns.append(str(tuple_set))
	return set(all_possible_unknowns)

def complement_diophantine(enumerableset):
	global complement_diophantine_map
	print "============================================================================"
	print "Complement Diophantine Sum of Four Squares Mapping Constructed for enumerable set:",enumerableset
	print "============================================================================"
	for e in enumerableset:
		diophantine_sum_of_squares_solve(e)
	pprint.pprint(complement_diophantine_map)

	print "==========================================================================="
	print "Complement Diophantine Map - Unknowns"
	print "==========================================================================="
	unknowns=complement_diophantine_map.keys()
	print unknowns
	print "==========================================================================="
	print "Complement Diophantine - all possible unknowns"
	print "==========================================================================="
	all_unknowns=all_possible_unknowns_four_squares()
	partial_function_domain_complement=all_unknowns.difference(set(unknowns))
	for k in partial_function_domain_complement:
		complement_diophantine_map[k]=-1

	complement_diophantine_map_sorted=sorted(complement_diophantine_map.items(),key=operator.itemgetter(0),reverse=True)
	print "============================================================================"
	print "Complement Diophantine Sum of Four Squares Mapping (Sorted by unknown tuples):" 
	print "============================================================================"
	pprint.pprint(complement_diophantine_map_sorted)
	complement_diophantine_map_sorted=sorted(complement_diophantine_map.items(),key=operator.itemgetter(1),reverse=True)
	print "============================================================================"
	print "Complement Diophantine Sum of Four Squares Mapping (Sorted by parameter):" 
	print "============================================================================"
	pprint.pprint(complement_diophantine_map_sorted)

def diophantine_sum_of_squares_solve(x):
	if x != '':
		unknowntuple=diop_general_sum_of_squares(a**2 + b**2 + c**2 + d**2 - toint(x))
		complement_diophantine_map[str(unknowntuple)]=x

def diophantine_factorization_pell_equation(D,N):
	if D==1 and N >= 1:
		print "=============================================================================="
		print "Pell Diophantine Equation - (exponential time) Factorization by solving Pell's Equation (for D=1 and some N)"
		print "=============================================================================="
		sol=diop_DN(D,N)
		soln=sol[0]
		print "Solution for Pell Equation : x^2 - ",D,"*y^2 = ",N,":"
		print "(",soln[0]," + ",soln[1],") * (",soln[0]," - ",soln[1],") = ",N
	if D==1 and N==-1:
		#Invocation of factorization is commented because of Spark Accumulator broadcast issue which
		#probably requires single Spark Context across complementation and factoring. Presently
		#factors are persisted to a json file and read offline by complementation
		#DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.SearchTiles_and_Factorize(N)
		factorsfile=open("DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.factors")
		factors=json.load(factorsfile)
		number_to_factorize=0
		for k,v in factors.iteritems():
			number_to_factorize=k
			factorslist=v	
		print "=============================================================================="
		print "Pell Diophantine Equation - (polynomial time) PRAM-NC Factorization solving Pell's Equation (for D=1 and N=",number_to_factorize,")"
		print "=============================================================================="
		for f in factorslist:
			p=f
			q=int(number_to_factorize)/p
			x=(p+q)/2
			y=(p-q)/2
			print "Solution for Pell Equation : x^2 - ",D,"*y^2 = ",number_to_factorize,":"
			print "x=",x,"; y=",y

def IharaIdentity():
	#Imaginary(s) = b = arccos(float(q+1.0)/float(2.0*sqrt(q)))/float(log(q)) for prime q
	primesbinf=open("First10000PrimesBinary.txt","wa")
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
	for primestr in Lf:
		if primestr != '':
			print "primestr:",primestr
			print "Prime in binary:",bin(toint(primestr))
			primesbinf.write(bin(toint(primestr)))
			primesbinf.write("\n")

if __name__=="__main__":
	primesf=open("First10000Primes.txt","r")
	for line in primesf:
		primes=line.split(" ")
		primestr=primes[:-1]
		Lf=Lf+primestr
	print Lf

	for i in range(10):
		print "g(",i,")=",getgofx(i)
	#IharaIdentity()
	nonsquares=[2,3,5,6,7,8,9,10,11,12,13,14,15,17,18,19]
	complement_diophantine(nonsquares)
	diophantine_factorization_pell_equation(1,989295)
	diophantine_factorization_pell_equation(1,-1)
