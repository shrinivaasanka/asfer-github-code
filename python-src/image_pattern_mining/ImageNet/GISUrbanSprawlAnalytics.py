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
from ImageGraph_Keras_Theano import histogram_partition_distance_similarity 
import random
from GraphMining_GSpan import GSpan
from scipy.stats import wasserstein_distance 
from shapely.geometry import Polygon
from scipy import stats

def draw_delaunay_triangulation(img,triangles):
    for triangle in triangles:
        point1 = (triangle[0], triangle[1])
        point2 = (triangle[2], triangle[3])
        point3 = (triangle[4], triangle[5])
        cv2.line(img, point1, point2, (0,255,0), 1, cv2.LINE_8,0)
        cv2.line(img, point2, point3, (0,255,0), 1, cv2.LINE_8,0)
        cv2.line(img, point3, point1, (0,255,0), 1, cv2.LINE_8,0)

def draw_voronoi_tessellation(img,centroids):
    rect = (0, 0, img.shape[1], img.shape[0])
    print(("rect:", rect))
    subdiv = cv2.Subdiv2D(rect)
    print(("subdiv:", subdiv))
    for cent in centroids:
        print(("centroid:", cent))
        subdiv.insert(tuple(cent))
    triangles = subdiv.getTriangleList()
    print(("image Delaunay triangles:", triangles))
    facets = subdiv.getVoronoiFacetList([])
    print(("image Voronoi Facets:", facets))
    for n in range(len(facets)):
        for f in facets[n]:
            fnp=np.array(f)
            print("facet:",fnp)
            try:
                #cv2.fillConvexPoly(img,fnp,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),cv2.LINE_AA,0)
                cv2.polylines(img,np.int32([fnp]),True,(0,0,0),1,cv2.LINE_AA,0)
            except:
                continue

def urban_sprawl_from_segments(image,segment,population_density=None,sqkmtocontourarearatio=0):
    print(("Image:",image))
    img=cv2.imread(image)
    imagearea=img.shape[0]*img.shape[1]
    UrbanSprawlAreas=[]
    print(("Number of segments - Number of Urban areas:",len(segment[7][0])))
    fig1 = plt.figure(dpi=100)
    cityid=0
    centroids=[]
    voronoifacets=segment[5]
    voronoifacetareas=[]
    contourareas=[]
    #print("voronoi facets:",voronoifacets)
    for n in range(len(voronoifacets)-1):
        for facet in voronoifacets[n]:
            polygon=[]
            for point in facet:
               #print("facet point:",point)
               polygon.append(tuple(point.tolist()))
            print(("Voronoi Facet (containing the urban sprawl) polygon:",polygon))
            voronoifacet = Polygon(polygon)
            print(("Voronoi Facet (containing the urban sprawl) Area:",voronoifacet.area))
            voronoifacetareas.append(voronoifacet.area)
    for n in range(len(segment[7][0]) - 1):
        #print(("Urban Area:",segment[7][0][n]))
        circumference = cv2.arcLength(segment[7][0][n],True)
        convexhull = cv2.convexHull(segment[7][0][n])
        #convexhull = ConvexHull(segment[7][0][n])
        contourarea = cv2.contourArea(segment[7][0][n])
        contourareas.append(contourarea)
        cv2.drawContours(img,segment[7][0][n],-1,(0,255,0),2)
        print("Contour boundary point:",segment[7][0][n][0])
        pop_dens=0
        try:
            contourcolor = img[segment[7][0][n][0][0][0],segment[7][0][n][0][0][1]]
            print("Contour color:",contourcolor)
            averageBGR = int((contourcolor[0] + contourcolor[1] + contourcolor[2])/3)
            pop_dens = (averageBGR/255) * 100000
        except:
            pop_dens = population_density
        if population_density == -1:
            population_density = pop_dens
        x,y,w,h = cv2.boundingRect(segment[7][0][n])
        print(("Convex Hull of Urban Area:" , convexhull))
        print(("Circumference of Urban Area:",circumference))
        (cx,cy),radius=cv2.minEnclosingCircle(segment[7][0][n])
        center=(int(cx),int(cy))
        centroids.append(center)
        radius=int(radius)
        cv2.circle(img,center,radius,(0,255,0),2)
        circulararea=3.14*radius*radius
        print(("Approximate circular area of Urban Sprawl:", circulararea))
        print(("Contour Area of Urban Sprawl:", contourarea))
        contourratio=float(contourarea)/float(imagearea)
        print(("Ratio of urban sprawl contour area to image area:",contourratio))
        urbansprawlsqkmarea=contourarea*sqkmtocontourarearatio
        print(("Square Kilometer Area of Urban Sprawl:", urbansprawlsqkmarea))
        population_from_area=6.22*urbansprawlsqkmarea*urbansprawlsqkmarea
        population_from_density=population_density*urbansprawlsqkmarea
        print(("Population of Urban Sprawl (from density):", population_from_density))
        print(("Population of Urban Sprawl (from area):",population_from_area))
        moments=cv2.moments(segment[7][0][n])
        if moments['m00'] != 0:
            centroidx = int(moments['m10']/moments['m00'])
            centroidy = int(moments['m01']/moments['m00'])
            print(('Centroid of the Urban Sprawl:',(centroidx,centroidy)))
        if contourratio > 0.0:
            cv2.putText(img,str(cityid),(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,0,0),1,cv2.LINE_AA)
            UrbanSprawlAreas.append((circulararea,contourarea,urbansprawlsqkmarea,contourratio,radius,circumference,cityid,convexhull,population_from_density,population_from_area))
        curve = convexhull 
        xaxis = []
        yaxis = []
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig1.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
        cityid += 1
    draw_voronoi_tessellation(img,centroids)
    draw_delaunay_triangulation(img,segment[6])
    print("Rankings of Urban Areas - sorted contour areas:")
    print(sorted(UrbanSprawlAreas))
    plt.show()
    imagetok1=image.split(".")
    imagetok2=imagetok1[0].split("/")
    cv2.imwrite("testlogs/"+imagetok2[1]+"-contourlabelled.jpg",img)
    cv2.waitKey()
    facegraph=segment[8] 
    print("Number of Vororoi Facets:",len(voronoifacetareas))
    print("Number of Contours:",len(contourareas))
    minsize=min(len(contourareas),len(voronoifacetareas))
    tau,pvalue = stats.kendalltau(sorted(contourareas[:minsize]),sorted(voronoifacetareas[:minsize]))
    print("(Correlation,PValue) between Contour areas and Voronoi polygon areas of Urban sprawls:",(tau,pvalue))
    print("Betweenness centrality of urban sprawl facegraph:",nx.betweenness_centrality(facegraph))
    print("Degree centrality of urban sprawl facegraph:",nx.degree_centrality(facegraph))
    print("Closeness centrality of urban sprawl facegraph:",nx.closeness_centrality(facegraph))
    print("PageRank of urban sprawl facegraph:",nx.pagerank(facegraph))
    return (UrbanSprawlAreas)


if __name__ == "__main__":
    #seg1=image_segmentation("testlogs/NightLights_13nasa-india-2016.jpg")
    #seg2=image_segmentation("testlogs/NightLights_13nasa-india-2012.jpg")
    #seg3=image_segmentation("testlogs/NightLights_13nasa-india-2021.jpg")
    #seg4=image_segmentation("testlogs/NASAVIIRSNightLightsChennaiMetropolitanArea_17November2021.jpg")
    #histogram_partition_distance_similarity("testlogs/NightLights_13nasa-india-2016.jpg","testlogs/NightLights_13nasa-india-2012.jpg")
    #histogram_partition_distance_similarity("testlogs/NightLights_13nasa-india-2016.jpg","testlogs/NightLights_13nasa-india-2021.jpg")
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2016.jpg",seg1)
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2012.jpg",seg2)
    #urban_sprawl_from_segments("testlogs/NASAVIIRSNightLightsChennaiMetropolitanArea_17November2021.jpg",seg4)
    #seg5=image_segmentation("testlogs/SEDAC_GPW4-11_PopulationEstimate2020_edited.jpeg")
    #urban_sprawl_from_segments("testlogs/SEDAC_GPW4-11_PopulationEstimate2020_edited.jpeg",seg5,5000,266.0/854.0)
    #seg6=image_segmentation("testlogs/SEDAC_GPW4-11_PopulationDensity2020_edited.jpeg")
    #urban_sprawl_from_segments("testlogs/SEDAC_GPW4-11_PopulationDensity2020_edited.jpeg",seg6,5000,266.0/854.0)
    #seg7=image_segmentation("testlogs/NightLights_13nasa-india-2012.jpg")
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2012.jpg",seg7,5000,266.0/854.0)
    #seg8=image_segmentation("testlogs/NightLights_13nasa-india-2016.jpg")
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2016.jpg",seg8,5000,266.0/854.0)
    #modularityseg7=nx.modularity_matrix(seg7[8])
    #modularityseg8=nx.modularity_matrix(seg8[8])
    #modularityseg7=modularityseg7.flatten().tolist()
    #modularityseg8=modularityseg8.flatten().tolist()
    #modemd=wasserstein_distance(modularityseg7[0],modularityseg8[0])
    #print("Increase in Community structure - Wasserstein EMD of modularity:",modemd)
    #minged=10000000000000000
    #iteration=0
    #for ged in nx.optimize_graph_edit_distance(seg7[8],seg8[8]):
    #    if ged < minged:
    #        minged=ged
    #        print("Optimized Graph edit distance - iteration ",iteration,":",minged)
    #        iteration+=1
    #graphmining=GSpan([])
    #graphmining.GraphEditDistance(seg7[8],seg8[8])
    seg9=image_segmentation("testlogs/HRSL_World_NightTimeStreets.jpg")
    urban_sprawl_from_segments("testlogs/HRSL_World_NightTimeStreets.jpg",seg9,-1,266.0/854.0)
