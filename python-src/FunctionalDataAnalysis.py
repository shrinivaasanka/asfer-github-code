# -------------------------------------------------------------------------------------------------------
# NEURONRAIN AI - ASFER - Software for Mining Large Datasets
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
# Krishna iResearch - https://www.krishna-iresearch.org/
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/ 
# --------------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib.axes import Axes as ax 
from skfda.misc.metrics import l2_distance
from skfda.ml.clustering import KMeans
from skfda.datasets import fetch_gait,fetch_aemet,fetch_handwriting
from skfda.exploratory.visualization.clustering import ClusterPlot
from skfda.representation.grid import FDataGrid

def cluster_functions(Xaxis=None,Yaxis=None,data=None,n_clust=2,n_ini=10):
    print("Data:",data)
    n_clusters = n_clust 
    n_init = n_ini 
    fda_kmeans = KMeans(
      n_clusters=n_clusters,
      n_init=n_init,
      metric=l2_distance,
      random_state=0,
    )
    fda_clusters = fda_kmeans.fit_predict(data)
    print("FDA clusters:",fda_clusters)
    #for cluster in range(n_clust):
    #    selection = (fda_clusters == cluster)
    #    print("selection:",selection)
    #    #ax.scatter(data[selection,0],data[selection,1])
    #    plt.plot(len(data[0]),len(data[0][0]),selection,'o')
    #fd = data.iloc[:, 0].array
    ClusterPlot(fda_kmeans, data).plot()
    plt.show()

if __name__=="__main__":
    print("-------------Meteorology Dataset FDA Clusters------------")
    X,_= fetch_aemet(return_X_y=True)
    cluster_functions(data=X)
    print("------------Gait Analysis Dataset FDA Clusters-----------")
    X,_= fetch_gait(return_X_y=True)
    cluster_functions(data=X)
    print("-----------Handwriting Dataset FDA Clusters--------------")
    X,_= fetch_handwriting(return_X_y=True)
    cluster_functions(data=X)
    randomfunction = [[1,2,3],[2,4,8],[5,6,7],[8,9,10]]
    gridpoints = [3,4,5]
    randomfunctiondata = FDataGrid(randomfunction,gridpoints)
    cluster_functions(data=randomfunctiondata)
