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
import subprocess

if __name__=="__main__":
    mininteger=toint(sys.argv[1])
    increment=toint(sys.argv[2])
    actual_runtimes=[]
    theoretical_runtimes=[]
    depth=toint(sys.argv[3])
    constant=toint(sys.argv[4])
    exp=toint(sys.argv[5])
    for n in range(mininteger,mininteger+increment):
        print("================================================================================================")
        print("Factorization of ",n, " (",math.log(n,2)," bit integer) ")
        print("================================================================================================")
        starttime=time.time()
        #subprocess.call(["/home/ksrinivasan/spark-3.0.1-bin-hadoop3.2/bin/spark-submit",
        #             "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py", str(n), str(depth), "False"], shell=False)
        subprocess.call(["/media/ksrinivasan/84f7d6fd-3d43-4215-8dcc-52b5fe1bffc6/home/ksrinivasan/spark-3.0.1-bin-hadoop3.2/bin/spark-submit",
                     "DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized.py", str(n), str(depth), "False"], shell=False)
        endtime=time.time()
        duration=endtime-starttime
        actual_runtimes.append(duration)
        print("Time - Factorization of ",n, " (",math.log(n,2)," bit integer) was done in time deltas:",duration)
        theoretical=constant*math.pow(math.log(n,2),exp)
        print("Time - Theoretical Factorization of ",n, " (",math.log(n,2)," bit integer) time :",theoretical)
        theoretical_runtimes.append(theoretical)
    plt.plot(range(increment),actual_runtimes)
    plt.plot(range(increment),theoretical_runtimes)
    plt.savefig("testlogs/DiscreteHyperbolicFactorizationUpperbound_TileSearch_Optimized_MultipleIntegers.jpg")
