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
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/ 
# --------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#Python code from https://www.sciencedirect.com/science/article/pii/S0304397519304633 - figure 2 - Program 1 -
#[Yu.Matiyasevich] - The Riemann Hypothesis in computer science - additional statements included for WCET program analysis
#--------------------------------------------------------------------------------------------------------------

from math import gcd
import matplotlib.pyplot as plt
import sys
import hfd 
import ChaosAttractor
import numpy
import SINDy
import StringSearch_LongestRepeatedSubstring

h=m=p=0
d=f0=f3=n=q=1
lhs=[]
rhs=[]
lhsrhsratio=[]
matiyasevichlooprandomwalk=[]
sys.set_int_max_str_digits(150000)
maxiterations=3000
integerdivision=True
testconvergence=False
convergenceratio=0
sindylorenzpredictions=[]
prevlhsbyrhs=0
lhsbyrhs=0
prevrandomwalk=0
randomwalk=0
randomwalkbinarystring=""
step=0.1
while p**2*(m-f0) < f3:
    print("--------------------------")
    print("iteration:",n)
    print("--------------------------")
    if n > maxiterations:
        #plt.plot(lhs)
        #plt.plot(rhs)
        plt.plot(lhsrhsratio, label="LHS-RHS ratio")
        print("Stopping after ",maxiterations," iterations") 
        logisticseq=numpy.array(ChaosAttractor.ChaosPRG(algorithm="Logistic", seqlen=maxiterations, radix=3.5699340, initialcondition=0.000001, prime=104729, seed=complex(1+0j)))
        logisticseq=(logisticseq/100000)
        plt.plot(logisticseq.tolist(), label="ChaosPRG Logistic")
        plt.plot(sindylorenzpredictions/100, label="SINDy Lorenz Logistic predictions")
        plt.plot(matiyasevichlooprandomwalk,label="LHS-RHS ratio Jacob ladder random walk")
        plt.legend()
        plt.show()
        correlationcoeff=numpy.corrcoef(lhsrhsratio,logisticseq)
        print("Correlation coefficient between while loop LHS-RHS ratio and Logistic map:",correlationcoeff)
        print("Longest Common Substring - Suffix Array based - in LHSRHS ratio randomwalk string:",randomwalkbinarystring)
        lcsfile=open("StringSearch_Pattern.txt","w") 
        lcsfile.write(randomwalkbinarystring)
        lcsfile.close()
        suff_array = StringSearch_LongestRepeatedSubstring.SuffixArray()
        suff_array.construct_suffix_array()
        suff_array.longest_repeated_substring(suff_array.pattern)
        exit(1)
    #print("LHS:",p**2*(m-f0))
    lhs.append(p**2*(m-f0))
    #print("RHS:",f3)
    rhs.append(f3)
    lhsbyrhs=p**2*(m-f0)/f3
    print("LHS/RHS:",lhsbyrhs)
    lhsrhsratio.append(lhsbyrhs)
    if lhsbyrhs > prevlhsbyrhs:
        randomwalk=prevrandomwalk+step
        randomwalkbinarystring+="1"
    else:
        randomwalk=prevrandomwalk-step
        randomwalkbinarystring+="0"
    matiyasevichlooprandomwalk.append(randomwalk)
    prevlhsbyrhs=lhsbyrhs
    d = 2*n*d-4*(-1)**n*h
    n = n+1
    g = gcd(n,q)
    #print("g:",g)
    if integerdivision:
        q = n*(q // g)
    else:
        q = int(n*q/g)
    #print("q:",q)
    if g==1: p=p+1
    m=0; g=q
    while g>1:
        g=g//2; m=m+d
    h=f0
    f0=2*n*h
    f3=(2*n+3)*f3
    if len(lhsrhsratio) > 10:
        if testconvergence:
            convergenceratio=lhsrhsratio[len(lhsrhsratio)-1]/lhsrhsratio[len(lhsrhsratio)-2]
            print("D'Alembert series convergence test:",convergenceratio)
        fractaldimension=hfd.hfd(lhsrhsratio)
        print("Higuchi Fractal Dimension of the 1-dimensional timeseries:",fractaldimension)
        print("SINDy non-linear dynamics fit of LHS-RHS ratio series so far:")
        l=len(lhsrhsratio)
        #t=numpy.arange(l)
        x=numpy.arange(l)
        y=lhsrhsratio
        t=numpy.arange(0,1.0,1.0/float(len(y)))
        sindylorenzpredictions=SINDy.SINDy_fit_lorenz(t,x,numpy.asarray(y)/100)
print("Loop exits after ",n," iterations - Riemann Hypothesis is False")
print("after loop - LHS:",p**2*(m-f0))
print("after loop - RHS:",f3)
print("after loop - LHS/RHS:",p**2*(m-f0)/f3)
plt.plot(lhs)
plt.show()
plt.plot(rhs)
plt.show()

