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

h=m=p=0
d=f0=f3=n=q=1
lhs=[]
rhs=[]
lhsrhsratio=[]
sys.set_int_max_str_digits(100000)
maxiterations=3000
integerdivision=False
while p**2*(m-f0) < f3:
    print("--------------------------")
    print("iteration:",n)
    print("--------------------------")
    if n > maxiterations:
        plt.plot(lhsrhsratio)
        plt.show()
        print("Stopping after ",maxiterations," iterations") 
        exit(1)
    print("LHS:",p**2*(m-f0))
    lhs.append(p**2*(m-f0))
    print("RHS:",f3)
    rhs.append(f3)
    print("LHS/RHS:",p**2*(m-f0)/f3)
    lhsrhsratio.append(p**2*(m-f0)/f3)
    d = 2*n*d-4*(-1)**n*h
    n = n+1
    g = gcd(n,q)
    print("g:",g)
    if integerdivision:
        q = n*(q // g)
    else:
        q = int(n*q/g)
    print("q:",q)
    if g==1: p=p+1
    m=0; g=q
    while g>1:
        g=g//2; m=m+d
    h=f0
    f0=2*n*h
    f3=(2*n+3)*f3
print("Loop exits after ",n," iterations - Riemann Hypothesis is False")
print("after loop - LHS:",p**2*(m-f0))
print("after loop - RHS:",f3)
print("after loop - LHS/RHS:",p**2*(m-f0)/f3)
plt.plot(lhs)
plt.show()
plt.plot(rhs)
plt.show()
