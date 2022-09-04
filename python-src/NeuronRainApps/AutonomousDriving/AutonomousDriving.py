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
# Copyleft (Copyright+):
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# ------------------------------------------------------------------------------------------------------------------------------

import laspy
from scipy.spatial import cKDTree
import numpy as np

def read_lidar_stream(lasfile,clearance=100):
    las=laspy.read(lasfile)
    data=np.vstack((las.X,las.Y,las.Z)).transpose()
    kdtree=cKDTree(data)
    neighbours_distance,neighbours_indices=kdtree.query(data,clearance)
    print("neighbours_distance:",neighbours_distance)
    print("neighbours_indices:",neighbours_indices)
    ground=las.points[las.return_number == las.number_of_returns]
    obstacles=las.points[las.return_number != las.number_of_returns]
    print("Ground points:",ground.__dict__["array"])
    print("Obstacle points:",obstacles.__dict__["array"])
    minx = int(las.header.mins[0]*100)
    print("minx:",minx)
    miny = int(las.header.mins[1]*100)
    print("miny:",miny)
    maxx = int(las.header.maxs[0]*100)
    print("maxx:",maxx)
    maxy = int(las.header.maxs[1]*100)
    print("maxy:",maxy)
    #lattice = np.zeros((maxx-minx,maxy-miny))
    for point in obstacles.__dict__["array"]:
        x = (point[0] - minx)
        y = (point[1] - miny)
        #lattice[x][y] = 1
        print("Lattice(",x,",",y,"): marked as obstacle")

if __name__=="__main__":
    read_lidar_stream("simple.las") 
