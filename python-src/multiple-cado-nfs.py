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

#!/usr/bin/env python3.7
import os
import sys

if __name__=="__main__":
    frominteger=int(sys.argv[1])
    tointeger=int(sys.argv[2])
    for n in range(frominteger,tointeger):
        print("==========================")
        print("GNFS factorization of ",n)
        print("==========================")
        os.system("./cado-nfs.py --filelog INFO "+str(n)+" -t 4 ")
        os.system("cat ./multiple-cado-nfs-logs/multiple-cado-nfs.log >> ./multiple-cado-nfs.log")
        os.system("rm -rf multiple-cado-nfs-logs/*")

