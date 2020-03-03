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

# Python implementation for PAC Learning a Boolean Conjunction for five boolean variables
# Reference: http://www.cis.temple.edu/~giorgio/cis587/readings/pac.html

import json


def PACLearning(datasource, hypothesis):
    datasourcemappings = open(datasource, "r")
    dataset = json.load(datasourcemappings)

    i = 0
    number_of_variables = 0

    for d in range(len(dataset)):
        for k, v in list(dataset[d].items()):
            #print "key=",k,";value=",v
            if v == True:
                index = 0
                for i in k[len(k):0:-1]+k[0]:
                    if i == "1":
                        try:
                            #print "removing notx"+str(index+1)
                            hypothesis.pop("notx"+str(index+1))
                        except:
                            pass
                    else:
                        if i == "0":
                            try:
                                #print "removing x"+str(index+1)
                                hypothesis.pop("x"+str(index+1))
                            except:
                                pass
                    index = index+1

        hypolen = len(hypothesis)
        for i in range(hypolen):
            if "x"+str(i+1) in hypothesis and "notx"+str(i+1) in hypothesis:
                hypothesis.pop("x"+str(i+1))
                hypothesis.pop("notx"+str(i+1))

        print(("Boolean conjunction hypothesis approximating the dataset for bit position:", number_of_variables))
        print("=========================================================")
        hypostr = ""
        for k, v in list(hypothesis.items()):
            if (k in list(hypothesis.keys()) and "not"+k in list(hypothesis.keys())):
                pass
            else:
                hypostr = hypostr + k + " /\ "
        print((hypostr[:-3]))
        number_of_variables += 1


if __name__ == "__main__":
    #dataset={"10001":True, "11100":False, "11101":True, "10101":True, "00101":False, "11011":False, "11000":False, "00001":True, "10000":False, "00100":False,"00010":False}

    # First 5 primes in binary - f(00000) = 0010, f(00001) = 0011, f(00010) = 0101, f(00011) = 0111, f(00100) = 1011. For each prime bit 
    # position (0 or 1 mapped to False or True) a boolean conjunction is PAC learnt 
    # ------------------------------------------------------------------------------------------------------
    # Following Example mapping of first 5 primes defines f:n-th-prime <-> truth-value-of-i-th-bit-of-prime:
    # ------------------------------------------------------------------------------------------------------
    # dataset=[{"00000":False, "00001":False, "00010":False, "00011":False, "00100":True}, {"00000":False, "00001":False, "00010":True, "00011":True, "00100":True}, {"00000":True, "00001":True, "00010":False, "00011":True, "00100":True}, {"00000":False, "00001":True, "00010":True, "00011":True, "00100":True}]

    # First 10000 primes utm dataset
    hypothesis = {"x1": 1, "notx1": 1, "x2": 2, "notx2": 2, "x3": 3, "notx3": 3, "x4": 4, "notx4": 4, "x5": 5, "notx5": 5, "x6": 6, "notx6": 6, "x7": 7, "notx7": 7, "x8": 8, "notx8": 8, "x9": 9, "notx9": 9, "x10": 10, "notx10": 10, "x11": 11, "notx11": 11, "x12": 12, "notx12": 12, "x13": 13, "notx13": 13, "x14": 14, "notx14": 14, "x15": 15, "notx15": 15, "x16": 16, "notx16": 16}
    PACLearning("PACLearning_PrimeBitsMapping.txt", hypothesis)
