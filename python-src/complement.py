# -------------------------------------------------------------------------------------------------------
# ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# -----------------------------------------------------------------------------------------------------------

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
# --------------------------
# Most recent draft updates to complement diophantines (Post Correspondence Problem and MRDP theorem undecidability,Rayleigh-Beatty Theorem,Complementary Sets, Diophantine Analysis,Complementary Equations,Ramsey coloring,Tarski-Sturm decidability,Riemann Zeta Function,Patterns in Primes,Function version of Circuit Range Avoidance (AVOID) and so on) 
# are mentioned in:
# - http://sourceforge.net/p/asfer/code/HEAD/tree/asfer-docs/AstroInferDesign.txt
# - https://github.com/shrinivaasanka/asfer-github-code/blob/master/asfer-docs/AstroInferDesign.txt
# - https://gitlab.com/shrinivaasanka/asfer-github-code/blob/master/asfer-docs/AstroInferDesign.txt
################################################################################################

import math
import string
import decimal
from sympy.solvers.diophantine.diophantine import diop_general_sum_of_squares
from sympy.solvers.diophantine.diophantine import diop_DN
from sympy.abc import a, b, c, d, e, f
from collections import defaultdict
import pprint
import operator
import json
import ast
from networkx.algorithms.approximation.ramsey import ramsey_R2
import numpy as np
from scipy.interpolate import barycentric_interpolate
from scipy.interpolate import lagrange 
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
import inspect

# Lf=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]
Lf = []
cosvalues = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
complement_diophantine_map = {}
unknown_max_limit = 11


def getgofx(x):
    u = 0
    z = -1
    while True:
        if u in Lf:
            u = u+1
        if u not in Lf:
            z = z+1
            if (z == x):
                return u
            else:
                u = u+1

def complement_range_avoid_infinitely_often(function,funcdomain,universalrange):
    print("------------------------------------------------------------")
    funcrange=[]
    print("function to be complemented:",inspect.getsource(function))
    for d in funcdomain:
        funcval=function(d)
        funcrange.append(funcval)
    rangeavoidance=set(universalrange).difference(set(funcrange)) 
    print("universal range:",universalrange)
    print("function domain:",set(funcdomain))
    print("function range:",set(funcrange))
    print("range avoidance:",rangeavoidance)
    complement_diophantine(rangeavoidance,interpol_algorithm="polyfit")
    return rangeavoidance

def toint(primestr):
    if primestr != '' and not None:
        return int(decimal.Decimal(primestr))

def all_possible_unknowns_four_squares():
    all_possible_unknowns = []
    for a in range(unknown_max_limit):
        for b in range(unknown_max_limit):
            for c in range(unknown_max_limit):
                for d in range(unknown_max_limit):
                    tuple_set = set([(a, b, c, d)])
                    all_possible_unknowns.append(str(tuple_set))
    return set(all_possible_unknowns)


def complement_diophantine(enumerableset, interpol_algorithm="barycentric"):
    global complement_diophantine_map
    print("============================================================================")
    print("Complement Diophantine Sum of Four Squares Mapping Constructed for enumerable set:", enumerableset)
    print("============================================================================")
    for e in enumerableset:
        diophantine_sum_of_squares_solve(e)
    pprint.pprint(complement_diophantine_map)
    print("============================================================================")
    print("Complement Diophantine Learning by Polynomial Interpolation - Least Squares Fit")
    print("============================================================================")
    indices=list(map(float,list(range(len(complement_diophantine_map)))))
    print("indices:",indices)
    print("complement_diophantine_map.values():",list(complement_diophantine_map.values()))
    if interpol_algorithm == "polyfit":
        diop_poly=np.polyfit(np.array(indices),np.array(list(complement_diophantine_map.values())),5)
        print("PolyFit Least Squares (Vandermonde) Interpolated Degree 5 Polynomial:",diop_poly)
    elif interpol_algorithm == "barycentric":
        diop_poly = barycentric_interpolate(np.array(indices),np.array(list(complement_diophantine_map.values())),np.array(indices))
        print("Barycentric Interpolated Polynomial:",diop_poly)
    elif interpol_algorithm == "lagrange":
        diop_poly = lagrange(np.array(indices), np.array(list(complement_diophantine_map.values())))

        print("Lagrange Interpolated Polynomial:",diop_poly)
        x = np.arange(0, len(complement_diophantine_map), 1)
        plt.plot(x, Polynomial(diop_poly.coef[::-1])(x), label='Polynomial')
        plt.savefig("testlogs/complement.jpg")
    print("===========================================================================")
    print("Complement Diophantine Map - Unknowns")
    print("===========================================================================")
    unknowns = list(complement_diophantine_map.keys())
    print(unknowns)
    print("===========================================================================")
    print("Complement Diophantine - all possible unknowns")
    print("===========================================================================")
    all_unknowns = all_possible_unknowns_four_squares()
    partial_function_domain_complement = all_unknowns.difference(set(unknowns))
    for k in partial_function_domain_complement:
        complement_diophantine_map[k] = -1

    complement_diophantine_map_sorted = sorted(
        list(complement_diophantine_map.items()), key=operator.itemgetter(0), reverse=True)
    print("============================================================================")
    print("Complement Diophantine Sum of Four Squares Mapping (Sorted by unknown tuples):")
    print("============================================================================")
    pprint.pprint(complement_diophantine_map_sorted)
    complement_diophantine_map_sorted = sorted(
        list(complement_diophantine_map.items()), key=operator.itemgetter(1), reverse=True)
    print("============================================================================")
    print("Complement Diophantine Sum of Four Squares Mapping (Sorted by parameter):")
    print("============================================================================")
    pprint.pprint(complement_diophantine_map_sorted)


def ramsey_text_coloring(text):
    from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlapGraph
    textgraph = RecursiveGlossOverlapGraph(text)
    print("Ramsey coloring of text graph - (maxclique, maxindependentset):", ramsey_R2(
        textgraph[0]))


def diophantine_sum_of_squares_solve(x):
    if x != '':
        unknowntuple = diop_general_sum_of_squares(
            a**2 + b**2 + c**2 + d**2 - toint(x))
        complement_diophantine_map[str(unknowntuple)] = x


def diophantine_factorization_pell_equation(D, N):
    import DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized
    if D == 1 and N >= 1:
        print("==============================================================================")
        print("Pell Diophantine Equation - (exponential time) Factorization by solving Pell's Equation (for D=1 and some N)")
        print("==============================================================================")
        sol = diop_DN(D, N)
        soln = sol[0]
        print("Solution for Pell Equation : x^2 - ", D, "*y^2 = ", N, ":")
        print("(", soln[0], " + ", soln[1], ") * (", soln[0], " - ", soln[1], ") = ", N)
    if D == 1 and N == -1:
        # Invocation of factorization is commented because of Spark Accumulator broadcast issue which
        # probably requires single Spark Context across complementation and factoring. Presently
        # factors are persisted to a json file and read offline by complementation
        # DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.SearchTiles_and_Factorize(N)
        factorsfile = open(
            "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.factors")
        factors = json.load(factorsfile)
        number_to_factorize = 0
        for k, v in factors.items():
            number_to_factorize = k
            factorslist = v
        print("==============================================================================")
        print("Pell Diophantine Equation - (polynomial time) PRAM-NC Factorization solving Pell's Equation (for D=1 and N=", number_to_factorize, ")")
        print("==============================================================================")
        for f in factorslist:
            p = f
            q = int(number_to_factorize)/p
            x = (p+q)/2
            y = (p-q)/2
            print("Solution for Pell Equation : x^2 - ", D, "*y^2 = ", number_to_factorize, ":")
            print("x=", x, "; y=", y)


def IharaIdentity():
    # Imaginary(s) = b = arccos(float(q+1.0)/float(2.0*sqrt(q)))/float(log(q)) for prime q
    primesbinf = open("First10000PrimesBinary.txt", "wa")
    for eigen_scaling in cosvalues:
        print("#####################################################################")
        for primestr in Lf:
            if primestr != '':
                prime = toint(primestr)
                num2 = 2.0*math.sqrt(float(prime))
                num1 = (float(2*eigen_scaling*math.sqrt(prime)))/num2
                den = float(math.log(prime))
                imaginary = math.acos(num1)/den
                print("eigen_scaling=", eigen_scaling, "; imaginary(s) for prime ", prime, ": ", imaginary)
        print("#####################################################################")
    for primestr in Lf:
        if primestr != '':
            print("primestr:", primestr)
            print("Prime in binary:", bin(toint(primestr)))
            primesbinf.write(bin(toint(primestr)))
            primesbinf.write("\n")


if __name__ == "__main__":
    #textfile = open("RecursiveLambdaFunctionGrowth.txt", "r")
    #ramsey_text_coloring(textfile.read())
    #primesf = open("First10000Primes.txt", "r")
    #for line in primesf:
    #    primes = line.split(" ")
    #    primestr = primes[:-1]
    #    Lf = Lf+primestr
    #print(Lf)

    #for i in range(10):
    #    print("g(", i, ")=", getgofx(i))
    # IharaIdentity()
    #nonsquares = [2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19]
    #complement_diophantine(nonsquares,interpol_algorithm="polyfit")
    #complement_diophantine(nonsquares,interpol_algorithm="barycentric")
    #complement_diophantine(nonsquares,interpol_algorithm="lagrange")
    #diophantine_factorization_pell_equation(1, 989295)
    #diophantine_factorization_pell_equation(1, -1)
    #complement_range_avoid_infinitely_often(lambda x: x*x - x + 1,list(range(10)),list(range(50)))
    #complement_range_avoid_infinitely_often(lambda x: x*x,list(range(10)),list(range(50)))
    complement_range_avoid_infinitely_often(lambda x: 2*x,list(range(50)),list(range(50)))
