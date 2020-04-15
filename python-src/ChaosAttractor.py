# ------------------------------------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://sites.google.com/site/kuja27/
# ---------------------------------------------------------------------------------------------------------

import rpy2.robjects as robj
import random

# non-linearity starts from k >= 3 and below 3 there are periods
input_seq = []
# correlation_flag="linear"
correlation_flag = "chaotic"


def plotGraph(x):
    no_of_hashes = x*100
    for i in range(int(no_of_hashes)):
        print("#", end=' ')
    print("\n")

# Chaotic PRG implementation - Verhulste's Logistic equation and Lehmer-Palmore Pseudorandom generator

def grow_cellular_automaton(n,lamda=0.8):
    xnext=list(n)
    for digit in range(3,len(n)-2):
        if n[digit-1] == '0' and n[digit+1] == '0':
            if lamda > 0.5:
                xnext[digit] = '0'
            else:
                xnext[digit] = '1'
        if n[digit-1] == '0' and n[digit+1] == '1':
            if lamda > 0.5:
                xnext[digit] = '1'
            else:
                xnext[digit] = '0'
        if n[digit-1] == '1' and n[digit+1] == '0':
            if lamda > 0.5:
                xnext[digit] = '1'
            else:
                xnext[digit] = '0'
        if n[digit-1] == '1' and n[digit+1] == '1':
            if lamda > 0.5:
                xnext[digit] = '0'
            else:
                xnext[digit] = '1'
    print("grow_cellular_automaton() - xnext:","".join(xnext))
    return "".join(xnext)

def ChaosPRG(algorithm="Logistic", seqlen=100, radix=10, initialcondition=0.7, prime=104729, seed=complex(1+0j)):
    x = initialcondition
    k = radix
    zed = 0+0j
    chaos_seq = []
    print("ChaosPRG() algorithm:", algorithm)
    while True:
        if algorithm == "CellularAutomaton":
            binx = x
            xnext = grow_cellular_automaton(binx,float(random.randint(0,100000))/100000.0) 
        if algorithm == "Mandelbrot":
            zed = zed * zed + seed 
        if algorithm == "Logistic":
            xnext = k*x*(1-x)
            print("x: ", x, ", xnext: ", xnext)
        if algorithm == "Lehmer-Palmore":
            xnext = (k * x) % prime
            print("x: ", x, ", xnext: ", xnext)
        # plotGraph(xnext)
        if algorithm == "Mandelbrot":
            chaos_seq.append(zed)
        if algorithm == "CellularAutomaton":
            chaos_seq.append(eval(x))
            x = xnext
        if algorithm == "Logistic" or algorithm == "Lehmer-Palmore":
            chaos_seq.append(float(x)*100000)
            x = xnext
        if len(chaos_seq) == seqlen:
            break
    print("chaos_seq:",chaos_seq)
    return chaos_seq


if __name__ == "__main__":
    # Read input sequence
    # f=open("ChaosAttractorInputSequence.txt")
    f = open("ChaosAttractorInputSequence_DJIA.txt")
    f_str = f.read()
    input_seq = f_str.split(",")
    # using rpy2.objects and compute R correlation coefficient
    if correlation_flag == "chaotic":
        chaosx1 = robj.FloatVector(
            ChaosPRG("Logistic", 19449, 3.8, 0.7, 104729))
        chaosx2 = robj.FloatVector(ChaosPRG("Lehmer-Palmore",19449,3.8,0.7,104729))
        chaosx4 = ChaosPRG("Mandelbrot",19449,3.8,0.7,104729,complex(0.3+0.3j))
        chaosx4 = robj.FloatVector([abs(x) for x in chaosx4])
        chaosx5 = robj.FloatVector(ChaosPRG("CellularAutomaton",19449,3.8,'0b00101001010101001',104729))
    if correlation_flag == "linear":
        chaosx3 = robj.FloatVector(range(19449))
    print("Chaotic PRG sequence - Logistic:", chaosx1)
    print("Chaotic PRG sequence - Lehmer-Palmore:", chaosx2)
    print("Chaotic PRG sequence - Mandelbrot:", chaosx4)
    print("Chaotic PRG sequence - CellularAutomaton:", chaosx5)
    inputstreamy = robj.FloatVector(input_seq[0:19449])
    corfn = robj.r['cor']
    ret1 = corfn(chaosx1, inputstreamy)
    ret2 = corfn(chaosx2, inputstreamy)
    ret3 = corfn(chaosx4, inputstreamy)
    ret4 = corfn(chaosx5, inputstreamy)
    print("correlation coefficient of pseudorandom (Logistic) and DJIA sequences is:", (ret1.r_repr(
    )))
    print("correlation coefficient of pseudorandom (Lehmer-Palmore) and DJIA sequences is:", (ret2.r_repr(
    )))
    print("correlation coefficient of pseudorandom (Mandelbrot) and DJIA sequences is:", (ret3.r_repr(
    )))
    print("correlation coefficient of pseudorandom (Cellular Automaton) and DJIA sequences is:", (ret4.r_repr(
    )))
