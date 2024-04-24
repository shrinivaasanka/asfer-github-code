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

import faulthandler
from time import gmtime, strftime, time_ns
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
#import numba
#from numba import jit
from joblib import Parallel,delayed

number_to_factorize = 0
persisted_tiles = False
HyperbolicRasterizationGraphicsEnabled = "True"

factors_accum = None
factors_of_n = []
spcon = None
maxfactors = 3

factorization_start = time_ns()
faulthandler.enable()


class VectorAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        return [0.0] * len(value)

    def addInPlace(self, val1, val2):
        for i in range(len(val1)):
            val1[i] += val2[i]
        return val1


class FactorsAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        # return [0.0] * len(value)
        return []

    def addInPlace(self, val1, val2):
        #print("val1 =",val1,"; val2 = ",val2)
        factors_of_n = val1
        if type(val2) == list:
            factors_of_n = val1 + val2
        else:
            factors_of_n.append(val2)
        # print("factors_of_n:",factors_of_n)
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

def tilesearch_nonpersistent(y, numfactors=maxfactors, padding=1, binarysearch="iterative",axisparallel="False"):
    global number_to_factorize
    n = number_to_factorize
    xtile_start = int(Decimal(n)/Decimal(y))-padding
    if xtile_start < 0:
        xtile_start = int(Decimal(n)/Decimal(y))
    xtile_end = int(Decimal(n)/Decimal(y+1))+padding
    #print("tilesearch_nonpersistent(): (",xtile_start,",",y,",",xtile_end,",",y,")")
    if binarysearch == "recursive":
        if axisparallel:
            binary_search_interval_nonpersistent( xtile_start, y, xtile_end, y, numfactors)
        else:
            binary_search_interval_nonpersistent( xtile_start, y, xtile_end, y+1, numfactors)
    elif binarysearch == "iterative":
        if axisparallel:
            iterative_binary_search_interval_nonpersistent( xtile_start, y, xtile_end, y, numfactors)
        else:
            iterative_binary_search_interval_nonpersistent( xtile_start, y, xtile_end, y+1, numfactors)

def hyperbolic_arc_rasterization(n):
    fig = plt.figure(dpi=100)
    for y in range(1, n):
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

def iterative_binary_search_interval_nonpersistent(xl,yl,xr,yr,numfactors=maxfactors):
    global factors_accum
    global factorization_start
    #print("iterative_binary_search_interval_nonpersistent(): binary seach of rasterized hyperbolic arc bow tilesegment xy = ",number_to_factorize," - segment(",xl,",",yl,",",xr,",",yr,")")
    xl_clone=Decimal(xl)
    yl_clone=Decimal(yl)
    xr_clone=Decimal(xr)
    yr_clone=Decimal(yr)
    while xl_clone <= xr_clone:
        midpoint = Decimal(int((xl_clone+xr_clone)/2))
        #print("Midpoint = ",midpoint)
        factorcandidate = Decimal(midpoint*yl_clone)
        if xl_clone==xr_clone:
             return
        #print("Factor candidate point : ",factorcandidate)
        if factorcandidate==number_to_factorize:
             print("at ", strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()), ") - Factor point located : [",midpoint,",",yl_clone,"]")
             factors_accum.add(factorcandidate.to_eng_string())
             factorization_present = time_ns()
             print("nanoseconds elapsed so far in finding all factors: ", factorization_present - factorization_start)
        if xl_clone*yl_clone==number_to_factorize:
             print("at ", strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()), ") - Factor point located : [",xl_clone,",",yl_clone,"]")
             factorization_present = time_ns()
             print("nanoseconds elapsed so far in finding all factors: ", factorization_present - factorization_start)
             factors_accum.add(xl_clone.to_eng_string())
             factors_accum.add(yl_clone.to_eng_string())
        if xr_clone*yr_clone==number_to_factorize:
             print("at ", strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()), ") - Factor point located : [",xr_clone,",",yr_clone,"]")
             factorization_present = time_ns()
             print("nanoseconds elapsed so far in finding all factors: ", factorization_present - factorization_start)
             factors_accum.add(xr_clone.to_eng_string())
             factors_accum.add(yr_clone.to_eng_string())
        if factorcandidate > number_to_factorize:
             #print("factorcandiate > num_fact")
             xr_clone = xl_clone + midpoint
        else:
             #print("factorcandiate < num_fact")
             xl_clone = xl_clone + midpoint

def binary_search_interval_nonpersistent(xl, yl, xr, yr, numfactors=maxfactors):
    global factors_accum
    global factorization_start
    sys.setrecursionlimit(30000)
    #intervalmidpoint = abs(int((Decimal(xr)-Decimal(xl))/Decimal(2)))
    if Decimal(xr) > Decimal(xl):
        intervalmidpoint = (int((Decimal(xr)-Decimal(xl))/Decimal(2)))
    else:
        intervalmidpoint = (int((Decimal(xl)-Decimal(xr))/Decimal(2)))
    #print("intervalmidpoint = ",intervalmidpoint)
    #print("factors_accum.aid:",factors_accum.aid)
    #print("factors_accum._value:",factors_accum._value)
    if intervalmidpoint == 0:
        if xl*yl == number_to_factorize:
            print(("Factors are: (", yl, ",", xl, ") (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            factors_accum.add(xl)
        elif xr*yr == number_to_factorize:
            print(("Factors are: (", yr, ",", xr, ") (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            factors_accum.add(xr)
        elif number_to_factorize/xl == xl:
            print(("Square root is: ", xl, " (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            factors_accum.add(xl)
        elif number_to_factorize/xr == xr:
            print(("Square root is: ", xr, " (at ", strftime(
                "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
            factors_accum.add(xr)
    if intervalmidpoint > 0 and len(factors_accum._value) < numfactors:
        factorcandidate = (xl+intervalmidpoint)*yl
        #print("factorcandidate = ",factorcandidate)
        if factorcandidate == number_to_factorize or xl*yl == number_to_factorize or xr*yr == number_to_factorize or xl*xl == number_to_factorize or xr*xr == number_to_factorize:
            print("=================================================")
            print("xl + intervalmidpoint = ", xl + intervalmidpoint)
            print("xl = ", xl)
            print("yl = ", yl)
            factorcriterion1 = ((xl + intervalmidpoint) *
                                yl == number_to_factorize)
            print("Factor point verification: (xl + intervalmidpoint)*yl == number_to_factorize = ", factorcriterion1)
            factorcriterion2 = (xl*yl == number_to_factorize)
            print(
                "Factor point verification: xl*yl == number_to_factorize = ", factorcriterion2)
            factorcriterion3 = (xr*yr == number_to_factorize)
            print(
                "Factor point verification: xr*yr == number_to_factorize = ", factorcriterion3)
            factorcriterion4 = (xr*xr == number_to_factorize)
            print(
                "Factor point verification: xr*xr == number_to_factorize = ", factorcriterion4)
            factorcriterion5 = (xl*xl == number_to_factorize)
            print(
                "Factor point verification: xl*xl == number_to_factorize = ", factorcriterion5)
            if factorcriterion1 == True:
                print(("Factors are: (", yl, ",", (xl+intervalmidpoint),
                      ") (at ", strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
                factors_accum.add(xl+intervalmidpoint)
                factors_accum.add(yl)
            if factorcriterion2 == True:
                print(("Factors are: (", yl, ",", xl, ") (at ", strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
                factors_accum.add(xl)
                factors_accum.add(yl)
            if factorcriterion3 == True:
                print(("Factors are: (", yr, ",", xr, ") (at ", strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
                factors_accum.add(xr)
                factors_accum.add(yr)
            if factorcriterion4 == True:
                print(("Square root is: (", xr, ") (at ", strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
                factors_accum.add(xr)
            if factorcriterion5 == True:
                print(("Square root is: (", xl, ") (at ", strftime(
                    "%a, %d %b %Y %H:%M:%S GMT", gmtime()), ")"))
                factors_accum.add(xl)
            factorization_present = time_ns()
            print("nanoseconds elapsed so far in finding all factors: ",
                  factorization_present - factorization_start)
            print("=================================================")
            print("factors_accum._value: ", factors_accum._value)
        else:
            if factorcandidate > number_to_factorize:
                binary_search_interval_nonpersistent(
                    xl, yl, xl+intervalmidpoint, yr)
            else:
                binary_search_interval_nonpersistent(
                    xl+intervalmidpoint, yl, xr, yr)


#@jit(parallel=True)
def tilesearch(tileintervalstr):
    global number_to_factorize
    if (len(tileintervalstr) > 1):
        tileinterval = eval(tileintervalstr)
        # print "tilesearch(): tileinterval=",tileinterval
        xleft = tileinterval[0]
        yleft = tileinterval[1]
        xright = tileinterval[2]
        yright = tileinterval[3]
        binary_search_interval(xleft, yleft, xright, yright)


#@jit(parallel=True)
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


# @jit(parallel=True)
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


# @jit(parallel=True)
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


# @jit(parallel=True)
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
            # print "next_prime: next_prime = ",next_prime
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


# @jit(parallel=True)
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
            # print "next_prime: next_prime = ",next_prime
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


# @jit(parallel=True)
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
            # print "next_prime: next_prime = ",next_prime
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

#@jit(nopython=True)
def parallel_tile_segments(tiles_per_PRAM,x):
    tiles_start = x*tiles_per_PRAM + 1 
    tiles_end = (x+1)*tiles_per_PRAM + 1
    tiles = list(range(tiles_start, tiles_end))
    print("tiles:", tiles)
    return tiles

#@jit(nopython=True)
def SearchTiles_and_Factorize(n, k, Parallel_for="False", StartFromSquareRoot="False"):
    global globalmergedtiles
    global globalcoordinates
    global factors_accum
    global spcon
    global factorization_start

    spcon = SparkSession.builder.master("local[4]").appName(
        "Spark Factorization").getOrCreate().sparkContext

    if persisted_tiles == True:
        tileintervalsf = open(
            "/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/cpp-src/miscellaneous/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.tileintervals", "r")

        tileintervalslist = tileintervalsf.read().split("\n")
        # print "tileintervalslist=",tileintervalslist
        tileintervalslist_accum = spcon.accumulator(
            tilesintervalslist, VectorAccumulatorParam())
        paralleltileintervals = spcon.parallelize(tileintervalslist)
        paralleltileintervals.foreach(tilesearch)
    else:
        if Parallel_for == "False":
            factorization_start = time_ns()
            print("factorization start (in nanoseconds):", factorization_start)
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
            normal_order_n = (Decimal(math.log(n, 2)) ** k)
            if StartFromSquareRoot=="True":
                tiles_start = int(Decimal(math.sqrt(n)))
            else:
                tiles_start = 1
            #tiles_end = int(Decimal(n)/(Decimal(normal_order_n)*Decimal(normal_order_n)))
            tiles_end = tiles_start + int(Decimal(n)/(Decimal(normal_order_n)))
            for x in range(int(Decimal(normal_order_n))):
                print("tiles_start:", tiles_start)
                print("tiles_end:", tiles_end)
                tiles = list(range(tiles_start, tiles_end))
                #print(("len(tiles):", len(tiles)))
                print("maxfactors:",maxfactors)
                print("1.factors_accum.value:",factors_accum.value)
                if len(factors_accum.value) >= maxfactors:
                    spcon.stop()
                    sys.exit("factors_accum.value > maxfactors, Factorization ends,Spark session is stopped and exiting")
                else:
                    spcon.parallelize(tiles).foreach(tilesearch_nonpersistent)
                tiles_start = tiles_end
                tiles_end += int(Decimal(n)/(Decimal(normal_order_n)))
            plt.show()
            print(("2.factors_accum.value = ", factors_accum.value))
            factors = []
            factordict = {}
            for f in factors_accum.value:
                factors.append(f)
            factordict[n] = list(set(factors))
            json.dump(factordict, factorsfile)
            return factors
        else:
            factorization_start = time_ns()
            print("factorization start (in nanoseconds):", factorization_start)
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
            polylog_n = (Decimal(math.log(n, 2)) ** k)
            tiles_per_PRAM = int(Decimal(n)/polylog_n)

            #((logN)^k sequential binary or interpolation searches of logN or loglogN time each on N/(logN)^k PRAMS-Multicores
            #for x in range(int(polylog_n)):
            #	 print("tiles_start:", tiles_start)
            #    print("tiles_end:", tiles_end)
            #    tiles = list(range(tiles_start, tiles_end))
            #    print(("len(tiles):", len(tiles)))
            #    spcon.parallelize(tiles).foreach(
            #        tilesearch_nonpersistent)
            #    tiles_start = tiles_end
            #    tiles_end += tiles_per_PRAM
            #    if len(factors_accum.value) > maxfactors:
            #        break
            #Earlier sequential for loop is parallelized by joblib to obtain a 2D array of set of tile segments followed by another nested parallelize() for each tile segment 1D array 
            tile_segments=Parallel(n_jobs=4)(delayed(parallel_tile_segments)(tiles_per_PRAM,x) for x in range(int(polylog_n)))
            print("tile_segments:",tile_segments)
            spcon.parallelize(tile_segments).flatMap(lambda x: x).foreach(tilesearch_nonpersistent)
            plt.show()
            print(("3.factors_accum.value = ", factors_accum.value))
            factors = []
            factordict = {}
            for f in factors_accum.value:
                factors.append(f)
            factordict[n] = list(set(factors))
            json.dump(factordict, factorsfile)
            return factors

def is_perfect_number_Euler_Sigma_Function(factors,number_to_factorize):
    intfactors=[int(x) for x in factors] 
    if 1 not in intfactors:
        intfactors.append(1)
    if number_to_factorize in intfactors:
        intfactors.remove(number_to_factorize)
    print("intfactors:",intfactors)
    if sum(intfactors)==number_to_factorize:
        print("Integer ",number_to_factorize," is Perfect") 
        return True
    else:
        print("Integer ",number_to_factorize," is not Perfect") 
        return False

if __name__ == "__main__":
    number_to_factorize = toint(sys.argv[1])
    print(("Spark Python version:", sys.version))
    print(("factors of ", number_to_factorize, "(", math.log(
        number_to_factorize, 2), " bits integer) are:"))
    HyperbolicRasterizationGraphicsEnabled = sys.argv[3]
    Parallel_for=sys.argv[4] 
    number_of_factors=sys.argv[5]
    StartFromSquareRoot=sys.argv[6]
    if number_of_factors=="all":
        maxfactors=sys.maxsize
    else:
        maxfactors=int(number_of_factors) 
    if HyperbolicRasterizationGraphicsEnabled == "True":
        hyperbolic_arc_rasterization(number_to_factorize)
    factors = SearchTiles_and_Factorize(number_to_factorize, int(sys.argv[2]), Parallel_for, StartFromSquareRoot)
    print(("factors of ", number_to_factorize, "(", math.log(
        number_to_factorize, 2), " bits integer) =", set(factors)))
    is_perfect_number_Euler_Sigma_Function(factors,number_to_factorize)
