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

import numpy as np
from scipy.spatial import Voronoi,voronoi_plot_2d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def scipy_voronoi_3d(points):
    voro = Voronoi(points)    
    polygons = []
    for index,region in enumerate(voro.regions): 
        poly = []
        for ridge in voro.ridge_vertices:
            if np.isin(ridge,region).all():
               poly.append(voro.vertices[ridge])
        polygons.append(poly)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    print("3D Voronoi polygons:",polygons)
    rng=np.random.default_rng()
    for poly in polygons:
        polygon = Poly3DCollection(poly, alpha=0.1, facecolors=rng.uniform(0,1,3),linewidths=0.5,edgecolors='black')
        ax.add_collection3d(polygon)
    ax.set_xlim([0,300])
    ax.set_ylim([0,300])
    ax.set_zlim([0,300])
    plt.show()

if __name__=="__main__":
    scipy_voronoi_3d([[0,1,0],[2,2,3],[10,10,250],[10,200,150],[230,110,50],[34,56,100],[53,223,100],[100,150,200],[110,180,230],[11,190,120],[35,123,43]])
