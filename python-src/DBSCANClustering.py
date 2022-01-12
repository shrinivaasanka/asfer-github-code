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
from PIL import Image
import numpy as np
import pprint
import random
import ImageToBitMatrix
import cv2
from scipy.spatial.distance import directed_hausdorff
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.interpolate import splprep, splev
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from shapely.geometry import Polygon
from scipy.stats import wasserstein_distance
import dlib
import netrd
from networkx.algorithms import isomorphism
from collections import defaultdict

class DBSCAN(object):
    def __init__(self,imagefile,threshold=200,epsilon=2,minpoints=5):
        self.imagefile=imagefile
        self.img = cv2.imread(imagefile,0)
        #cv2.threshold(self.img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        print(self.img)
        self.threshold = threshold
        self.epsilon = epsilon
        self.minpoints = minpoints
        self.dbscandict = defaultdict(int)
        self.noise=-1
        self.undefined=0
        self.clusterlabel=1

    def find_neighbours(self,img,row,col,threshold,epsilon,minpoints,neuralnetwork=False,thresholdfunction="lambda x: x"):
        neighbours=[]
        if not neuralnetwork:
            for r in range(row-epsilon,row+epsilon):
                 for c in range(col-epsilon,col+epsilon):
                     if r > 0 and c > 0 and r < len(img)-1 and c < len(img[0])-1:
                          if img[r][c] < threshold:
                              neighbours.append((r, c))
            #print("neighbours of (",row,",",col,")",neighbours)
            return neighbours
        else:
            evaledthresholdfunction=eval(thresholdfunction)
            for r in range(row-epsilon,row+epsilon):
                 for c in range(col-epsilon,col+epsilon):
                     if r > 0 and c > 0 and r < len(img)-1 and c < len(img[0])-1:
                         evaledthreshold=evaledthresholdfunction(img[r][c])
                         #print("evaledthreshold:",evaledthreshold)
                         if evaledthreshold > threshold:
                             neighbours.append((r,c))
            #print("neighbours of (",row,",",col,")",neighbours)
            return neighbours

    def clustering(self):
        for row in range(len(self.img)-1):
            for col in range(len(self.img)-1):
                if self.dbscandict[(row,col)]!=self.undefined:
                    continue
                #neighbours = self.find_neighbours(self.img,row,col,self.threshold,self.epsilon,self.minpoints,neuralnetwork=True,thresholdfunction="lambda x: x")
                neighbours = self.find_neighbours(self.img,row,col,self.threshold,self.epsilon,self.minpoints)
                if len(neighbours) < self.minpoints:
                    self.dbscandict[(row,col)]=self.noise
                    continue
                self.clusterlabel += 1
                self.dbscandict[(row,col)]=self.clusterlabel
                seedpoints=neighbours
                if (row,col) in seedpoints:
                    seedpoints.remove((row,col))
                for s in seedpoints:
                    if self.dbscandict[s]==self.noise:
                        self.dbscandict[s]=self.clusterlabel
                    if self.dbscandict[s]!=self.undefined:
                        continue
                    self.dbscandict[s]=self.clusterlabel
                    #s_neighbours=self.find_neighbours(self.img,s[0],s[1],self.threshold,self.epsilon,self.minpoints,neuralnetwork=True,thresholdfunction="lambda x: x")
                    s_neighbours=self.find_neighbours(self.img,s[0],s[1],self.threshold,self.epsilon,self.minpoints)
                    if len(s_neighbours) >= self.minpoints:
                        seedpoints = seedpoints + s_neighbours
                    #seedpoints.remove(s)
        #print("DBSCAN cluster labelling of pixels:",self.dbscandict)

    def write_clustered_image(self,neuralnetwork=False,fraction=1):
        if not neuralnetwork:
            number_of_clusters=len(set(self.dbscandict.values()))
            print("number of DBSCAN density clusters:",number_of_clusters)
            print("size of image:",self.img.shape[0] * self.img.shape[1])
            print("size of dbscandict:",len(self.dbscandict.items()))
            dbscanimg = cv2.imread(self.imagefile)
            for k,v in self.dbscandict.items():
              cluster=self.dbscandict[k]
              dbscanimg[k[0],k[1]]=(cluster*2,cluster*3,cluster)
            imagefiletoks = self.imagefile.split(".")
            #cv2.imshow(imagefiletoks[0]+"_dbscanclustered.jpg",dbscanimg)
            cv2.imwrite(imagefiletoks[0]+"_dbscanclustered.jpg",dbscanimg)
            #cv2.waitKey()
        else:
            epsilon=int(min(self.img.shape[0],self.img.shape[1])*fraction)
            neighbours=self.find_neighbours(self.img,int(self.img.shape[0]/2),int(self.img.shape[1]/2),200,epsilon,200,neuralnetwork=True,thresholdfunction="lambda x: 2*x")
            dbscanimg = cv2.imread(self.imagefile)
            for pixel in neighbours:
                dbscanimg[pixel[0],pixel[1]]=(255,255,255)
            imagefiletoks = self.imagefile.split(".")
            #cv2.imshow(imagefiletoks[0]+"_neuralnetworkclustered.jpg",dbscanimg)
            cv2.imwrite(imagefiletoks[0]+"_neuralnetworkclustered.jpg",dbscanimg)
            #cv2.waitKey()

if __name__=="__main__":
    dbscan1=DBSCAN("image_pattern_mining/ImageNet/testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg")
    dbscan1.clustering()
    dbscan1.write_clustered_image(neuralnetwork=False)
    dbscan1.write_clustered_image(neuralnetwork=True)
    dbscan2=DBSCAN("image_pattern_mining/ImageNet/testlogs/HRSL_World_NightTimeStreets.jpg")
    dbscan2.write_clustered_image(neuralnetwork=True,fraction=0.25)

