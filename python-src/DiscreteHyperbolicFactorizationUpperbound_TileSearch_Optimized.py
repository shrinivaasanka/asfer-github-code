# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
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
# --------------------------------------------------------------------------------------------------------

from time import gmtime, strftime
from pyspark.sql import SQLContext, Row, SparkSession
from pyspark.accumulators import AccumulatorParam
import decimal
import math
#from . import DiscreteHyperbolicFactorizationUpperbound_Bitonic_Spark_Tiling
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import threading
import json
import sys
import operator
from pyspark import SparkContext, SparkConf
import sys
from decimal import Decimal
import numpy as np
number_to_factorize = 0
persisted_tiles = False
HyperbolicRasterizationGraphicsEnabled = "True"

factors_accum = None
factors_of_n = []
spcon = None


class VectorAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        return [0.0] * len(value)

    def addInPlace(self, val1, val2):
        for i in range(len(val1)):
            val1[i] += val2[i]
        return val1


class FactorsAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        #return [0.0] * len(value)
        return []

    def addInPlace(self, val1, val2):
        #print("val1 =",val1,"; val2 = ",val2)
        factors_of_n = val1
        if type(val2) == list:
            factors_of_n = val1 + val2
        else:
            factors_of_n.append(val2)
        #print("factors_of_n:",factors_of_n)
        return factors_of_n

####################################################################################################################################
# long double pixelated_hyperbolic_arc(long double n)
# {
#        long double sumoflogs=0.0;
#        long double temp=0.0;
#        long double xtile_start=n/2.0;
#        long double xtile_end=n;
#        long double xtile_sum=n/2.0;
#        long double y=1.0;
#        do
#        {
#                if(log2l(n/(y*(y+1.0))) < 0)
#                        temp = 0.0; // tile has length 1
#                else
#                        temp = log2l(n/(y*(y+1.0)));
#                cout<<"create_tiles("<<(int)n<<","<<(int)xtile_start<<","<<(int)y<<","<<(int)(xtile_end)<<","<<(int)y<<")"<<endl;
#                factor=create_tiles((int)n,(int)(xtile_start)-PADDING,(int)y,(int)(xtile_end)+PADDING,(int)y);
#                xtile_end=xtile_start;
#                xtile_start=xtile_end-(n/((y+1.0)*(y+2.0)));
#                xtile_sum += (n/(y*(y+1.0)));
#                sumoflogs += temp;
#        }
#        while(y++ < (n));
#
#        return sumoflogs;
# }
####################################################################################################################################
# xtile_start = n - y*n/((y+1)*(y+2))
# xtile_end = xtile_start - n/((y+1)*(y+2))
# interval/segment = (xtile_start,y,xtile_end,y)
####################################################################################################################################


def toint(primestr):
    if primestr != '' and not None:
        return int(decimal.Decimal(primestr))


def tilesearch_nonpersistent(y):
    global number_to_factorize
    n = number_to_factorize
    xtile_start = int(Decimal(n)/Decimal(y))
    xtile_end = int(Decimal(n)/Decimal(y+1))
    #print "tilesearch_nonpersistent(): (",xtile_start,",",y,",",xtile_end,",",y,")"
    binary_search_interval_nonpersistent(xtile_start, y, xtile_end, y)

def hyperbolic_arc_rasterization(n):
    fig = plt.figure(dpi=100)
    for y in range(1,n):
        xtile_start = int(Decimal(n)/Decimal(y))
        xtile_end = int(Decimal(n)/Decimal(y+1))
        xaxis = []
        yaxis = []
        for x in np.linspace(xtile_start, xtile_end, num=1000):
            xaxis.append(xtile_start+x)
        for n in np.linspace(xtile_start, xtile_end, num=1000):
            yaxis.append(y)
        ax = fig.add_subplot(111)
        ax.plot(xaxis, yaxis, 'r-', rasterized=True, lw=5, alpha=0.6,
                label='rasterized hyperbolic arc bow')
    plt.show()

def binary_search_interval_nonpersistent(xl, yl, xr, yr):
    global factors_accum
    sys.setrecursionlimit(30000)
    intervalmidpoint = abs(int((Decimal(xr)-Decimal(xl))/2))
    #print "intervalmidpoint = ",intervalmidpoint
    if intervalmidpoint > 0:
        factorcandidate = (xl+intervalmidpoint)*yl
        #print "factorcandidate = ",factorcandidate
        if factorcandidate == number_to_factorize or xl*yl == number_to_factorize:
            print("=================================================")
            print("xl + intervalmidpoint = ",xl + intervalmidpoint)
            print("xl = ",xl)
            print("yl = ",yl)
            factorcriterion1=((xl + intervalmidpoint)*yl == number_to_factorize)
            print("Factor point verification: (xl + intervalmidpoint)*yl == number_to_factorize = ",factorcriterion1)
            factorcriterion2=(xl*yl == number_to_factorize)
            print("Factor point verification: xl*yl == number_to_factorize = ",factorcriterion2)
            if factorcriterion1 == True:
                print(("Factors are: (", yl, ",", (xl+intervalmidpoint) , ") (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            if factorcriterion2 == True:
                print(("Factors are: (", yl, ",", xl , ") (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            print("=================================================")
            factors_accum.add(xl)
            factors_accum.add(yl)
        else:
            if factorcandidate > number_to_factorize:
                binary_search_interval_nonpersistent(
                    xl, yl, xl+intervalmidpoint, yr)
            else:
                binary_search_interval_nonpersistent(
                    xl+intervalmidpoint, yl, xr, yr)


def tilesearch(tileintervalstr):
    global number_to_factorize
    if(len(tileintervalstr) > 1):
        tileinterval = eval(tileintervalstr)
        #print "tilesearch(): tileinterval=",tileinterval
        xleft = tileinterval[0]
        yleft = tileinterval[1]
        xright = tileinterval[2]
        yright = tileinterval[3]
        binary_search_interval(xleft, yleft, xright, yright)


def binary_search_interval(xl, yl, xr, yr):
    intervalmidpoint = int((xr-xl)/2)
    if intervalmidpoint >= 0:
        factorcandidate = (xl+intervalmidpoint)*yl
        print(("factorcandidate = ", factorcandidate))
        if factorcandidate == number_to_factorize:
            print("=================================================")
            print(("Factor is = ", yl))
            print("=================================================")
        else:
            if factorcandidate > number_to_factorize:
                binary_search_interval(xl, yl, xl+int((xr-xl)/2), yr)
            else:
                binary_search_interval(xl+int((xr-xl)/2)+1, yl, xr, yr)


def hardy_ramanujan_ray_shooting_queries(n):
    # Shoots Ray Queries to Find Approximate Factors by Hardy-Ramanujan Normal Order O(loglogN) for number of prime factors of N
    # Approximate Prime Factors are y(m) = m*N/kloglogN, m=1,2,3,...,kloglogN
    k = 6.0
    normal_order_n = int(k*math.log(math.log(n, 2), 2))
    print("=============================================================================================================")
    print(("Hardy-Ramanujan Ray Shooting Queries - Approximate Factors of ", n, " are:"))
    print("=============================================================================================================")
    print(("normal_order_n(loglogN) = ", normal_order_n))
    for m in range(1, normal_order_n):
        approximate_prime_factor = int(float(m*n)/float(normal_order_n))
        tan_theta = float(n/math.pow(approximate_prime_factor, 2))
        print("####################################################################")
        print(("approximate ", m, "-th prime factor of ",
               n, ":", approximate_prime_factor))
        print(("tangent of ray shooting query angle :", tan_theta))
        print("####################################################################")
    print("=============================================================================================================")


def hardy_ramanujan_prime_number_theorem_ray_shooting_queries(n):
    # Shoots Ray Queries to Find Approximate Factors by ratio of Prime Number Theorem N/logN and Hardy-Ramanujan Normal Order O(loglogN) for number of prime factors of N
    # Approximate Prime Factors are y(m) = m*N/(logN)(loglogN), m=1,2,3,...,kloglogN
    k = 6.0
    l = 10.0
    normal_order_n = int(k*math.log(math.log(n, 2), 2))
    print("=============================================================================================================")
    print(("Hardy-Ramanujan-Prime Number Theorem Ray Shooting Queries - Approximate Factors of ", n, " are:"))
    print("=============================================================================================================")
    print(("normal_order_n(loglogN) = ", normal_order_n))
    approximate_prime_factor = 2
    prev_approximate_prime_factor = approximate_prime_factor
    for m in range(1, normal_order_n):
        prev_approximate_prime_factor_log_ratio = l * \
            float(prev_approximate_prime_factor) / \
            float(math.log(prev_approximate_prime_factor, 2))
        approximate_prime_factor_log_ratio = prev_approximate_prime_factor_log_ratio + \
            int(l*float(n)/(float(math.log(n, 2))*float(normal_order_n)))

        # Approximately solves x/log(x) = y for x by series expansion of log(x)
        approximate_prime_factor = abs(math.sqrt((2*approximate_prime_factor_log_ratio + 1)*(
            2*approximate_prime_factor_log_ratio + 1) - 4.0) + (2*approximate_prime_factor_log_ratio + 1))/2.0
        tan_theta = float(n/math.pow(approximate_prime_factor, 2))
        print("####################################################################")
        print(("approximate ", m, "-th prime factor of ",
               n, ":", approximate_prime_factor))
        print(("approximate prime factor log ratio - pf/log(pf) :",
               approximate_prime_factor_log_ratio))
        print(("tangent of ray shooting query angle :", tan_theta))
        print("####################################################################")
        prev_approximate_prime_factor = approximate_prime_factor
    print("=============================================================================================================")


def baker_harman_pintz_ray_shooting_queries(n):
    # Shoots Ray Queries based on Baker-Harman-Pintz estimate for Gaps between Primes - p^0.525
    k = 6.0
    l = 0.001
    normal_order_n = int(k*math.log(math.log(n, 2), 2))
    print("=============================================================================================================")
    print(("Baker-Harman-Pintz Theorem Ray Shooting Queries - Approximate Factors of ", n, " are:"))
    print("=============================================================================================================")
    print(("normal_order_n(loglogN) = ", normal_order_n))
    approximate_prime_factor = 2
    # for m in spcon.range(1, normal_order_n).collect():
    for m in range(1, normal_order_n):
        prime_gaps_sum = 0.0
        prev_prime = approximate_prime_factor
        print(("approximate number of primes between two prime factors:", int(
            l*float(n)/(float(math.log(n, 2)*normal_order_n)))))
        # for x in spcon.range(int(l*float(n)/(float(math.log(n, 2)*normal_order_n)))).collect():
        for x in range(int(l*float(n)/(float(math.log(n, 2)*normal_order_n)))):
            next_prime = prev_prime + math.pow(prev_prime, 0.525)
            #print "next_prime: next_prime = ",next_prime
            prime_gaps_sum += math.pow(prev_prime, 0.525)
            prev_prime = next_prime
        approximate_prime_factor = int(
            approximate_prime_factor + prime_gaps_sum)
        tan_theta = float(n/math.pow(approximate_prime_factor, 2))
        if approximate_prime_factor > n:
            break
        print("####################################################################")
        print(("approximate ", m, "-th prime factor of ",
               n, ":", approximate_prime_factor))
        print(("tangent of ray shooting query angle :", tan_theta))
        print("####################################################################")


def cramer_ray_shooting_queries(n):
    # Shoots Ray Queries based on Cramer estimate for Gaps between Primes - p^0.5*log(p)
    k = 6.0
    l = 0.001
    normal_order_n = int(k*math.log(math.log(n, 2), 2))
    print("=============================================================================================================")
    print(("Cramer Ray Shooting Queries - Approximate Factors of ", n, " are:"))
    print("=============================================================================================================")
    print(("normal_order_n(loglogN) = ", normal_order_n))
    approximate_prime_factor = 2
    for m in range(1, normal_order_n):
        prime_gaps_sum = 0.0
        prev_prime = approximate_prime_factor
        for x in range(int(l*float(n)/(float(math.log(n, 2)*normal_order_n)))):
            next_prime = prev_prime + \
                math.pow(prev_prime, 0.5)*math.log(prev_prime, 2)
            #print "next_prime: next_prime = ",next_prime
            prime_gaps_sum += math.pow(prev_prime, 0.5)*math.log(prev_prime, 2)
            prev_prime = next_prime
        approximate_prime_factor = int(
            approximate_prime_factor + prime_gaps_sum)
        tan_theta = float(n/math.pow(approximate_prime_factor, 2))
        if approximate_prime_factor > n:
            break
        print("####################################################################")
        print(("approximate ", m, "-th prime factor of ",
               n, ":", approximate_prime_factor))
        print(("tangent of ray shooting query angle :", tan_theta))
        print("####################################################################")


def zhang_ray_shooting_queries(n):
    # Shoots Ray Queries based on Yitang Zhang estimate for Gaps between infinitely many Twin Primes
    # of gap < 7 * 10^7 which is refinement of Goldston-Pintz-Yildirim Sieve
    k = 6.0
    l = 0.00001
    normal_order_n = int(k*math.log(math.log(n, 2), 2))
    print("=============================================================================================================")
    print(("Zhang Ray Shooting Queries (for large primes) - Approximate Factors of ", n, " are:"))
    print("=============================================================================================================")
    print(("normal_order_n(loglogN) = ", normal_order_n))
    approximate_prime_factor = 2
    for m in range(1, normal_order_n):
        prime_gaps_sum = 0.0
        prev_prime = approximate_prime_factor
        for x in range(int(l*float(n)/(float(math.log(n, 2)*normal_order_n)))):
            next_prime = prev_prime + 7*10000000
            #print "next_prime: next_prime = ",next_prime
            prime_gaps_sum += 7*10000000
            prev_prime = next_prime
        approximate_prime_factor = int(
            approximate_prime_factor + prime_gaps_sum)
        tan_theta = float(n/math.pow(approximate_prime_factor, 2))
        if approximate_prime_factor > n:
            break
        print("####################################################################")
        print(("approximate ", m, "-th prime factor of ",
               n, ":", approximate_prime_factor))
        print(("tangent of ray shooting query angle :", tan_theta))
        print("####################################################################")


def SearchTiles_and_Factorize(n, k):
    global globalmergedtiles
    global globalcoordinates
    global factors_accum
    global spcon

    spcon = SparkSession.builder.master("local[4]").appName(
        "Spark Factorization").getOrCreate().sparkContext

    if persisted_tiles == True:
        tileintervalsf = open(
            "/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.tileintervals", "r")

        tileintervalslist = tileintervalsf.read().split("\n")
        #print "tileintervalslist=",tileintervalslist
        tileintervalslist_accum = spcon.accumulator(
            tilesintervalslist, VectorAccumulatorParam())
        paralleltileintervals = spcon.parallelize(tileintervalslist)
        paralleltileintervals.foreach(tilesearch)
    else:
        factorsfile = open(
            "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.factors", "w")
        # hardy_ramanujan_ray_shooting_queries(n)
        # hardy_ramanujan_prime_number_theorem_ray_shooting_queries(n)
        # baker_harman_pintz_ray_shooting_queries(n)
        # cramer_ray_shooting_queries(n)
        # zhang_ray_shooting_queries(n)
        factors_accum = spcon.accumulator(
            factors_of_n, FactorsAccumulatorParam())
        # spcon.parallelize(spcon.range(1, n).collect()).foreach(
        #    tilesearch_nonpersistent)
        normal_order_n = (Decimal(math.log(n,2)) ** k)
        tiles_start = 1
        tiles_end = int(Decimal(n)/(Decimal(normal_order_n)*Decimal(normal_order_n)))
        for x in range(int(Decimal(normal_order_n) * Decimal(normal_order_n))):
            print("tiles_start:", tiles_start)
            print("tiles_end:", tiles_end)
            tiles = list(range(tiles_start, tiles_end))
            #print(("len(tiles):", len(tiles)))
            spcon.parallelize(tiles).foreach(
                tilesearch_nonpersistent)
            tiles_start = tiles_end
            tiles_end += int(Decimal(n)/(Decimal(normal_order_n) * Decimal(normal_order_n)))
        plt.show()
        print(("factors_accum.value = ", factors_accum.value))
        factors = []
        factordict = {}
        for f in factors_accum.value:
            factors.append(f)
        factordict[n] = list(set(factors))
        json.dump(factordict, factorsfile)
        return factors


if __name__ == "__main__":
    number_to_factorize = toint(sys.argv[1])
    print(("Spark Python version:", sys.version))
    print(("factors of ", number_to_factorize, "(", math.log(
        number_to_factorize, 2), " bits integer) are:"))
    HyperbolicRasterizationGraphicsEnabled=sys.argv[3]
    if HyperbolicRasterizationGraphicsEnabled=="True":
        hyperbolic_arc_rasterization(number_to_factorize)
    factors = SearchTiles_and_Factorize(number_to_factorize, int(sys.argv[2]))
    print(("factors of ", number_to_factorize, "(", math.log(
        number_to_factorize, 2), " bits integer) =", factors))
