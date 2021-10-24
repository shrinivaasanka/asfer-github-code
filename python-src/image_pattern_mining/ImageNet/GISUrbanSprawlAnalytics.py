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

import cv2
from keras.applications import ResNet50
import tensorly as tly
from tensorly.decomposition import non_negative_parafac
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import scipy.io
from scipy.spatial.distance import directed_hausdorff
from scipy.spatial import ConvexHull
import operator
from collections import defaultdict
from empath import Empath
from WordNetPath import path_between
import networkx as nx
from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlap_Classify
from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlapGraph
import numpy as np
from keras import backend
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing import image
from networkx.drawing.nx_pydot import write_dot
import os
from scipy.interpolate import splprep, splev
import numpy
from sympy.combinatorics.partitions import Partition
#os.environ['KERAS_BACKEND'] = 'theano'
os.environ['KERAS_BACKEND'] = 'tensorflow'
from ImageGraph_Keras_Theano import image_segmentation 

def urban_sprawl_from_segments(segment):
    UrbanSprawlAreas=[]
    print(("Number of segments - Number of Urban areas:",len(segment[7][0])))
    fig1 = plt.figure(dpi=100)
    for n in range(len(segment[7][0]) - 1):
        #print(("Urban Area:",segment[7][0][n]))
        circumference = cv2.arcLength(segment[7][0][n],True)
        convexhull = cv2.convexHull(segment[7][0][n])
        #print(("Convex Hull of Urban Area:" , convexhull))
        print(("Circumference of Urban Area:",circumference))
        radius = circumference/6.28
        area=3.14*radius*radius
        print(("Approximate area of Urban Sprawl:", area))
        UrbanSprawlAreas.append((area,convexhull,circumference))
        curve = convexhull 
        xaxis = []
        yaxis = []
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig1.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
    print(UrbanSprawlAreas)
    plt.show()
    return (UrbanSprawlAreas)


if __name__ == "__main__":
    seg=image_segmentation("testlogs/NightLights_13nasa-india-2016.jpg")
    urban_sprawl_from_segments(seg)
