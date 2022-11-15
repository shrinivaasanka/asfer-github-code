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
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

import math
import sys
from complement import toint
import time
import matplotlib.pyplot as plt
import os
import json

if __name__=="__main__":
    mininteger=toint(sys.argv[1])
    integerrange=toint(sys.argv[2])
    actual_runtimes=[]
    theoretical_runtimes=[]
    depth=toint(sys.argv[3])
    constant=toint(sys.argv[4])
    exp=toint(sys.argv[5])
    for n in range(mininteger,mininteger+integerrange):
        print("================================================================================================")
        print("Factorization of ",n, " (",math.log(n,2)," bit integer) ")
        print("================================================================================================")
        starttime=time.time()
        number_to_factorize = n 
        HyperbolicRasterizationGraphicsEnabled = "False" 
        number_of_factors="1"
        #factors = DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.SearchTiles_and_Factorize(number_to_factorize, depth)
        os.system("/media/ksrinivasan/84f7d6fd-3d43-4215-8dcc-52b5fe1bffc6/home/ksrinivasan/spark-3.3.0-bin-hadoop3/bin/spark-submit DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py " + str(n) + " " + str(depth) + " " + HyperbolicRasterizationGraphicsEnabled  + " False " + str(number_of_factors) +" False")
        factorsjsonf=open("DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.factors")
        factors=json.loads(factorsjsonf.read())
        print(("factors of ", number_to_factorize, "(", math.log(number_to_factorize, 2), " bits integer) =", set(factors)))
        endtime=time.time()
        duration=endtime-starttime
        actual_runtimes.append(duration)
        print("Time - Factorization of ",n, " (",math.log(n,2)," bit integer) was done in time deltas:",duration)
        theoretical=constant*math.pow(math.log(n,2),exp)
        print("Time - Theoretical Factorization of ",n, " (",math.log(n,2)," bit integer) time :",theoretical)
        theoretical_runtimes.append(theoretical)
    plt.plot(range(integerrange),actual_runtimes)
    plt.plot(range(integerrange),theoretical_runtimes)
    plt.savefig("testlogs/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized_MultipleIntegers.jpg")
