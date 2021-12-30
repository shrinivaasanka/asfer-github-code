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

############################################################################################################################
# Convolution Networks for Deep Learning:
# ----------------------------------------
#  Input bitmap (e.g JPEG image) ===> Hidden Layer Convolution Feature Map ===> Pooling Map (E.g Max Pooling)
#
# where Convolution is defined as a function that maps a sub-square of bits (receptive field) to a bit in Hidden Layer and sub-square is
# moved across the bitmap (stride or sliding window). Pooling layer condenses the convoluted hidden layer into a smaller map
# by choosing the maximum of bits in a sub-square of convolution.
#
#  bit(k,l) of convoluted layer = sigmoid_perceptron(bias + double-summation(activations-of-bits-in-subsquare*weight))
#
# Following implementation has only one layer in convolution and pooling. The weights and biases that minimize the cost
# function (or error from expected output) are learnt through backpropagation implementation .
# Convolution is deep in the sense that hidden structure in  input is learnt. Has some similarities to construction of a hologram.
# Reference: http://neuralnetworksanddeeplearning.com
############################################################################################################################

import math
from PIL import Image
import numpy as np
import pprint
import random
import DeepLearning_BackPropagation
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
from ImageGraph_Keras_Theano import histogram_partition_distance_similarity 
from GraphMining_GSpan import GSpan
import dlib
import netrd
from networkx.algorithms import isomorphism

TopologicalRecognition = True


def draw_delaunay_triangulation(img, triangles):
    delaunay_graph=nx.Graph()
    for triangle in triangles:
        point1 = (triangle[0], triangle[1])
        point2 = (triangle[2], triangle[3])
        point3 = (triangle[4], triangle[5])
        point1str = str(triangle[0]) + "#" + str(triangle[1])
        point2str = str(triangle[2]) + "#" + str(triangle[3])
        point3str = str(triangle[4]) + "#" + str(triangle[5])
        delaunay_graph.add_edge(point1str,point2str)
        delaunay_graph.add_edge(point2str,point3str)
        delaunay_graph.add_edge(point3str,point1str)
        cv2.line(img, point1, point2, (0, 255, 0), 1, cv2.LINE_8, 0)
        cv2.line(img, point2, point3, (0, 255, 0), 1, cv2.LINE_8, 0)
        cv2.line(img, point3, point1, (0, 255, 0), 1, cv2.LINE_8, 0)
    return delaunay_graph

def draw_voronoi_tessellation(img, centroids):
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
            fnp = np.array(f)
            print(("facet:", fnp))
            try:
                #cv2.fillConvexPoly(img,fnp,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),cv2.LINE_AA,0)
                cv2.polylines(img, np.int32([fnp]), True, (0, 0, 0), 1, cv2.LINE_AA, 0)
            except:
                continue

def face_recognition_image_segmentation_contours(imagefile1):
    img1 = cv2.imread(imagefile1, 0)
    ret, thresh1 = cv2.threshold(
        img1, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours1, hierarchy1 = cv2.findContours(
        thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("contours:",contours1)
    #contours1=cv2.findContours(thresh1,1,2)
    epsilon1 = 0.1*cv2.arcLength(contours1[0], True)
    # epsilon1=0.2
    approx1 = cv2.approxPolyDP(contours1[0], epsilon1, True)
    contour1polys = []
    fig1 = plt.figure(dpi=100)
    for cont in contours1:
        xaxis = []
        yaxis = []
        curve = cont
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig1.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
        points = np.stack((xaxis, yaxis), axis=-1)
        #print("points:",points.shape[0])
        try:
            if points.shape[0] > 3:
                contour1polys.append(splprep(points.T, k=points.shape[0]-1))
        except Exception as e:
            continue
    plt.show()
    print(("contour1polys:", contour1polys))
    return (contours1,contour1polys)


def face_recognition_image_segmentation(imagefile,fromlandmarks=True):
    contours = face_recognition_image_segmentation_contours(imagefile)
    img = cv2.imread(imagefile)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(
        dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg, connectivity=8)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStatsWithAlgorithm(
        sure_fg, connectivity=8, ltype=2, ccltype=cv2.CCL_GRANA)
    print(("image connected components - ret:", ret))
    print(("image connected components - labels:", labels))
    print(("image connected components - stats:", stats))
    print(("image connected components - centroids:", centroids))
    markers += 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 0, 0]
    print(("image connected components - markers:", markers))
    imagefiletoks1 = imagefile.split(".")
    imagefiletoks2 = imagefiletoks1[0].split("/")
    cv2.imwrite(
        "testlogs/" +
        imagefiletoks2[len(imagefiletoks2)-1] +
        "_segmented.jpg",
        img)
    imgdual = cv2.imread(imagefile)
    rect = (0, 0, imgdual.shape[1], imgdual.shape[0])
    print(("rect:", rect))
    subdiv = cv2.Subdiv2D(rect)
    print(("subdiv:", subdiv))
    contourcentroids=[]
    for n in range(len(contours[0])-1): 
        moments=cv2.moments(contours[0][n])
        if moments['m00'] != 0:
            centroidx = int(moments['m10']/moments['m00'])
            centroidy = int(moments['m01']/moments['m00'])
        else:
            (centroidx,centroidy),radius=cv2.minEnclosingCircle(contours[0][n])
        contourcentroids.append((int(centroidx),int(centroidy)))
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("/tmp/shape_predictor_68_face_landmarks.dat")
    rects = detector(gray,1)
    for rect in rects:
        shape = predictor(gray, rect)
        shape_np = np.zeros((68,2), dtype="int")
        for i in range(0,68):
            shape_np[i] = (shape.part(i).x,shape.part(i).y)
        shape = shape_np
    landmarkcentroids=[]
    if fromlandmarks:
        for landmark in shape:
            subdiv.insert(tuple(landmark))
            landmarkcentroids.append(landmark)
    else:
       for cent in contourcentroids:
           print(("centroid:", cent))
           subdiv.insert(tuple(cent))
    triangles = subdiv.getTriangleList()
    print(("image Delaunay triangles:", triangles))
    facets = subdiv.getVoronoiFacetList([])
    print(("image Voronoi Facets:", facets))
    facegraph = nx.Graph()
    prevpoint = ""
    for n in range(0,len(facets)-1):
        for facet in facets[n]:
            for point in facet:
                try:
                    print("point:",point)
                    firstvertex = True
                    if firstvertex:
                       prevpoint = str(point[0]) + "#" + str(point[1])
                       firstpoint = str(point[0]) + "#" + str(point[1])
                       firstvertex = False
                    point = str(point[0]) + "#" + str(point[1])
                    facegraph.add_edge(point, prevpoint)
                    prevpoint = point
                except:
                    pass 
            facegraph.add_edge(firstpoint, prevpoint)
    euler_characteristic=len(facegraph.nodes()) - len(facegraph.edges()) + len(facets)
    print(("Euler characteristic of the Voronoi facegraph:",euler_characteristic))
    voronoifacetareas=[]
    for n in range(len(facets)-1):
        for facet in facets[n]:
            polygon=[]
            for point in facet:
               polygon.append(tuple(point.tolist()))
            print(("Voronoi Facet polygon:",polygon))
            voronoifacet = Polygon(polygon)
            print(("Voronoi Facet Area:",voronoifacet.area))
            voronoifacetareas.append(voronoifacet.area)
    nx.draw_networkx(facegraph)
    if fromlandmarks:
        draw_voronoi_tessellation(img,landmarkcentroids)
        delaunaymesh=draw_delaunay_triangulation(img,triangles)
    else:
        draw_voronoi_tessellation(img,contourcentroids)
        delaunaymesh=draw_delaunay_triangulation(img,triangles)
    plt.show()
    imagetok=imagefile.split(".")
    write_dot(facegraph, imagetok[0] + "_FaceRecognition_Segmentation_FaceGraph.dot")
    cv2.imwrite(imagetok[0] + "-tessellated.jpg",img)
    cv2.waitKey()
    return (ret, markers, labels, stats, centroids, facets, triangles, contours, facegraph, sorted(voronoifacetareas), delaunaymesh)

def facegraph_similarity_metrics(image1name,image2name,image1,image2,isomorphism_iterations=25,ismagssymmetry=False,GED=False):
    print("====================================================")
    imageEMDsimilarity1=wasserstein_distance(image1[9],image2[9])
    print("EMD Similarity between Voronoi Facet Areas of the images - ",image1name," and ",image2name,":",imageEMDsimilarity1)
    epsilon1 = 0.1*cv2.arcLength(image1[7][0][0], True)
    approx1 = cv2.approxPolyDP(image1[7][0][0], epsilon1, True)
    epsilon2 = 0.1*cv2.arcLength(image2[7][0][0], True)
    approx2 = cv2.approxPolyDP(image2[7][0][0], epsilon2, True)
    imageContourDPsimilarity=directed_hausdorff(approx1[0], approx2[0])
    print(("Hausdorff Distance between DP polynomials approximating two facial image contours - ",image1name," and ",image2name,":", imageContourDPsimilarity))
    isVoronoiisomorphic = nx.is_isomorphic(image1[8],image2[8])
    print(("Voronoi FaceGraphs of two facial images are isomorphic - (True or False):",isVoronoiisomorphic))
    isDelaunayisomorphic = nx.is_isomorphic(image1[10],image2[10])
    print(("Delaunay Triangulation Mesh Graphs of two facial images are isomorphic - (True or False):",isDelaunayisomorphic))
    if isVoronoiisomorphic:
        print(("Voronoi FaceGraphs of two facial images are isomorphic - percentage similarity - ",image1name," and ",image2name,": 100.0"))
    if isDelaunayisomorphic:
        print(("Delaunay Triangulation Mesh Graphs of two facial images are isomorphic - percentage similarity - ",image1name," and ",image2name,": 100.0"))
    jaccard = netrd.distance.JaccardDistance()
    jaccarddistance = jaccard.dist(image1[8],image2[8])
    print(("Jaccard distance between Voronoi Facegraphs of two facial images - ",image1name," and ",image2name,":",jaccarddistance))
    jsd = netrd.distance.DegreeDivergence()
    jsddistance = jsd.dist(image1[8],image2[8])
    print(("Jensen-Shannon Degree Divergence distance between Voronoi Facegraphs of two facial images - ",image1name," and ",image2name,":",jsddistance))
    gm=isomorphism.GraphMatcher(image1[8],image2[8])
    isVoronoisubgraphisomorphic=gm.subgraph_is_isomorphic()
    print(("Voronoi FaceGraphs of two facial images are subgraph isomorphic - (True or False):",isVoronoisubgraphisomorphic))
    cnt=0
    for sgiso_vf2 in gm.subgraph_isomorphisms_iter():
        print("VF2 subgraph isomorphisms between two Voronoi facegraphs:",sgiso_vf2)
        print("VF2 subgraph isomorphisms between two Voronoi facegraphs - percentage similarity - ",image1name," and ",image2name,":",100.0*float(len(sgiso_vf2))/float(len(image1[8].nodes())))
        print("VF2 subgraph isomorphisms between two Voronoi facegraphs - percentage similarity - ",image2name," and ",image1name,":",100.0*float(len(sgiso_vf2))/float(len(image2[8].nodes())))
        cnt+=1
        if cnt > isomorphism_iterations:
            break
    if not ismagssymmetry:
        cnt=0
        ismags=isomorphism.ISMAGS(image1[8],image2[8])
        for sgiso_ismags_asymmetric in ismags.isomorphisms_iter(symmetry=False):
           print("ISMAGS subgraph isomorphism between two Voronoi facegraphs - without symmetry:",sgiso_ismags_asymmetric)
           print("ISMAGS subgraph isomorphism between two Voronoi facegraphs - without symmetry - percentage similarity - ",image1name," and ",image2name,":",100.0*float(len(sgiso_ismags_asymmetric))/float(len(image1[8].nodes())))
           print("ISMAGS subgraph isomorphism between two Voronoi facegraphs - without symmetry - percentage similarity - ",image2name," and ",image1name,":",100.0*float(len(sgiso_ismags_asymmetric))/float(len(image2[8].nodes())))
           cnt+=1
           if cnt > isomorphism_iterations:
              break
    else:
        cnt=0
        for sgiso_ISMAGS_symmetric in ismags.isomorphisms_iter(symmetry=True):
           print("ISMAGS subgraph isomorphisms between two Voronoi facegraphs - with symmetry:",sgiso_ismags_symmetric)
           print("ISMAGS subgraph isomorphism between two Voronoi facegraphs - with symmetry - percentage similarity - ",image1name," and ",image2name,":",100.0*float(len(sgiso_ismags_symmetric))/float(len(image1[8].nodes())))
           print("ISMAGS subgraph isomorphism between two Voronoi facegraphs - with symmetry - percentage similarity - ",image2name," and ",image1name,":",100.0*float(len(sgiso_ismags_symmetric))/float(len(image2[8].nodes())))
           cnt+=1
           if cnt > isomorphism_iterations:
              break
    if GED:
        minged=10000000000000000
        iteration=0
        for ged in nx.optimize_graph_edit_distance(image1[8],image2[8]):
          if ged < minged:
              minged=ged
              print("Optimized Graph edit distance - iteration ",iteration,":",minged)
              iteration+=1
        graphmining=GSpan([])
        graphmining.GraphEditDistance(image1[8],image2[8])

def handwriting_recognition(imagefile1, imagefile2):
    img1 = cv2.imread(imagefile1, 0)
    ret, thresh1 = cv2.threshold(
        img1, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours1, hierarchy1 = cv2.findContours(
        thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours1=cv2.findContours(thresh1,1,2)
    epsilon1 = 0.1*cv2.arcLength(contours1[0], True)
    # epsilon1=0.2
    approx1 = cv2.approxPolyDP(contours1[0], epsilon1, True)
    img2 = cv2.imread(imagefile2, 0)
    ret, thresh2 = cv2.threshold(
        img2, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours2, hierarchy2 = cv2.findContours(
        thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # contours2=cv2.findContours(thresh2,1,2)
    epsilon2 = 0.1*cv2.arcLength(contours2[0], True)
    # epsilon2=0.2
    approx2 = cv2.approxPolyDP(contours2[0], epsilon2, True)
    print(("Distance between DP polynomials approximating two handwriting contours:",
          directed_hausdorff(approx1[0], approx2[0])))
    #print "contours1:",contours1
    #print "contours1:",contours2
    pdf = PdfPages(
        "testlogs/DeepLearning_ConvolutionNetwork_BackPropagation.Raster.Homotopies.pdf")
    contour1polys = []
    contour2polys = []
    fig1 = plt.figure(dpi=100)
    for cont in contours1:
        xaxis = []
        yaxis = []
        curve = cont
        #print curve
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig1.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
        points = np.stack((xaxis, yaxis), axis=-1)
        #print "points:",points.shape[0]
        try:
            if points.shape[0] > 3:
                contour1polys.append(splprep(points.T, k=points.shape[0]-1))
        except Exception as e:
            continue
    plt.show()
    pdf.savefig(fig1)
    fig2 = plt.figure(dpi=100)
    for cont in contours2:
        xaxis = []
        yaxis = []
        curve = cont
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig2.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
        points = np.stack((xaxis, yaxis), axis=-1)
        #print "points:",points
        try:
            if points.shape[0] > 3:
                contour2polys.append(splprep(points.T, k=points.shape[0]-1))
        except Exception as e:
            continue
    plt.show()
    pdf.savefig(fig2)
    pdf.close()
    print(("contour1polys:", contour1polys))
    print(("contour2polys:", contour2polys))


class DeepLearningConvolution(object):
    def __init__(self, input_bitmap):
        self.sigmoidPerceptron = False
        self.input_bitmap = input_bitmap
        self.max_pooling_inference = []
        self.weight = [[[0.07, 0.07, 0.07, 0.07, 0.07],
                        [0.07, 0.07, 0.07, 0.07, 0.07],
                        [0.07, 0.07, 0.07, 0.07, 0.07],
                        [0.07, 0.07, 0.07, 0.07, 0.07],
                        [0.07, 0.07, 0.07, 0.07, 0.07],
                        [0.07, 0.07, 0.07, 0.07, 0.07]],
                       [[0.08, 0.08, 0.08, 0.08, 0.08],
                        [0.08, 0.08, 0.08, 0.08, 0.08],
                        [0.08, 0.08, 0.08, 0.08, 0.08],
                        [0.08, 0.08, 0.08, 0.08, 0.08],
                        [0.08, 0.08, 0.08, 0.08, 0.08],
                        [0.08, 0.08, 0.08, 0.08, 0.08]],
                       [[0.09, 0.09, 0.09, 0.09, 0.09],
                        [0.09, 0.09, 0.09, 0.09, 0.09],
                        [0.09, 0.09, 0.09, 0.09, 0.09],
                        [0.09, 0.09, 0.09, 0.09, 0.09],
                        [0.09, 0.09, 0.09, 0.09, 0.09],
                        [0.09, 0.09, 0.09, 0.09, 0.09]]]
        self.convolution_map = [[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]]
        self.max_pooling_map = [[[0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0]],
                                [[0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0]]]
        self.bias = 0.05

    def sigmoid(self, perceptron):
        # 1/(1+e^(-z))
        return float(1.0/(1.0+math.exp(-1.0*perceptron)))

    def receptive_field_window(self, i, j, stride, convolution_map_index):
        rfw = 0.0
        for p in range(stride):
            for q in range(stride):
                if i+p < len(self.input_bitmap[0]) and j+q < len(self.input_bitmap[0]):
                    # dynamic_weight=self.weight[convolution_map_index][p][q]*self.input_bitmap[i+p][j+q]*(p+q+1)/(p*q+1)
                    rfw = rfw + self.input_bitmap[i+p][j+q] * \
                        self.weight[convolution_map_index][p][q]
                    #rfw = rfw + self.input_bitmap[i+p][j+q]*dynamic_weight
        return rfw

    def convolution(self, stride):
        for convolution_map_index in range(3):
            for i in range(10):
                for j in range(10):
                    self.convolution_map[convolution_map_index][i][j] = self.bias + \
                        self.receptive_field_window(
                            i, j, stride, convolution_map_index)
            convolution_map_index += 1
        return self.convolution_map

    def max_pooling(self, pooling_slidewindow_width):
        for convolution_map_index in range(3):
            row = col = 0
            k = l = 0
            while row < len(self.convolution_map[convolution_map_index])-1:
                while col < len(self.convolution_map[convolution_map_index])-1:
                    maximum = self.find_maximum(self.convolution_map[convolution_map_index][row][col], self.convolution_map[convolution_map_index]
                                                [row+1][col], self.convolution_map[convolution_map_index][row][col+1], self.convolution_map[convolution_map_index][row+1][col+1])
                    self.max_pooling_map[convolution_map_index][k][l] = maximum
                    col = col+pooling_slidewindow_width
                    l = l+1
                col = 0
                l = 0
                row = row+pooling_slidewindow_width
                k = k+1
        return self.max_pooling_map

    def find_maximum(self, a, b, c, d):
        maximum = a
        if b > maximum:
            maximum = b
        if c > maximum:
            maximum = c
        if d > maximum:
            maximum = d
        return maximum

    # Connects all points in all max pooling layers into a single neural activation function and does
    # backpropagation iterations to recompute weights
    def infer_from_max_pooling(self, max_pooling_map, maxpool_map_width):
        weights = []
        for convmap in range(3):
            weights.append([])
        for convmap in range(3):
            for k in range(maxpool_map_width*maxpool_map_width*maxpool_map_width*maxpool_map_width*2):
                weights[convmap].append(0.01)
        inputlayer = []
        hiddenlayer = []
        expectedoutput = []
        # parameters - initial conditions - inputlayer,hiddenlayer,expectedoutputlayer,weights_array - for arbitrary number of variables
        self.max_pooling_inference = []
        for convmap in range(3):
            for p in range(maxpool_map_width):
                for q in range(maxpool_map_width):
                    inputlayer.append(max_pooling_map[convmap][p][q])
                    hiddenlayer.append(0.1)
                    expectedoutput.append(0.1*max_pooling_map[convmap][p][q])
            bpnn = DeepLearning_BackPropagation.BackPropagation(
                inputlayer, hiddenlayer, expectedoutput, weights[convmap])
            bpnn.compute_neural_network()
            # bpnn.print_layers()
            iter = 0
            while iter < 10:
                for m in range(len(inputlayer)):
                    for l in range(len(inputlayer)):
                        bpnn.backpropagation_pde_update_hidden_to_output(
                            m, len(weights)/2 + len(inputlayer)*m + l)

                for m in range(len(inputlayer)):
                    for l in range(len(inputlayer)):
                        bpnn.backpropagation_pde_update_input_to_hidden(
                            m, len(inputlayer)*m+l)

                #print "Recomputing Neural Network after backpropagation weight update"
                bpnn.compute_neural_network()
                #print "Error after Backpropagation- iteration :",iter
                #print bpnn.output_error(bpnn.output_layer,bpnn.expected_output_layer)
                #print "Layers in this iteration:"
                # bpnn.print_layers()
                #print "Weights updated in this iteration:"
                #print bpnn.weights
                iter = iter+1

            weighted_sum = 0.0
            for p in range(maxpool_map_width):
                for q in range(maxpool_map_width):
                    weighted_sum = weighted_sum + \
                        max_pooling_map[convmap][p][q] * \
                        (bpnn.weights[p*(maxpool_map_width)+q])
            if self.sigmoidPerceptron == True:
                self.max_pooling_inference.append(
                    self.sigmoid(weighted_sum+self.bias))
            else:
                self.max_pooling_inference.append((weighted_sum+self.bias))
            inputlayer = []
            hiddenlayer = []
            expectedoutput = []
        return self.max_pooling_inference


if __name__ == "__main__":
    # An example input picture bitmap with '0' inscribed as set of 1s
    input_bitmap11 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    input_bitmap12 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # An example input picture bitmap with '8' inscribed as set of 1s
    input_bitmap21 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    input_bitmap22 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # An example input picture bitmap with no patterns
    input_bitmap3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # An example input picture bitmap with pattern X inscribed with 1s
    input_bitmap41 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]

    input_bitmap42 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                      [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
                      [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                      [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]

    # An example input picture bitmap with pattern 1 inscribed with 1s
    input_bitmap51 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    input_bitmap52 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    print("#############################################")
    print("Topological Handwriting and Face Recognition")
    print("#############################################")
    if TopologicalRecognition == True:
        # handwriting_recognition("/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg","/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_2.jpg")
        # handwriting_recognition("/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg","/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf8_1.jpg")
        image1=face_recognition_image_segmentation("testlogs/IMG_20160610_071455.jpg")
        image2=face_recognition_image_segmentation("testlogs/IMG_20160610_071603.jpg")
        image3=face_recognition_image_segmentation("testlogs/KSrinivasan_2003.jpg")
        image4=face_recognition_image_segmentation("testlogs/IMG_20171112_180837.jpg")
        image5=face_recognition_image_segmentation("testlogs/ExamplePortrait1.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071455.jpg","testlogs/IMG_20160610_071603.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071603.jpg","testlogs/KSrinivasan_2003.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071455.jpg","testlogs/KSrinivasan_2003.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071455.jpg","testlogs/IMG_20171112_180837.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071603.jpg","testlogs/IMG_20171112_180837.jpg")
        histogram_partition_distance_similarity("testlogs/IMG_20160610_071455.jpg","testlogs/ExamplePortrait1.jpg")
        facegraph_similarity_metrics("testlogs/IMG_20160610_071455.jpg","testlogs/IMG_20160610_071603.jpg",image1,image2)
        facegraph_similarity_metrics("testlogs/IMG_20160610_071455.jpg","testlogs/KSrinivasan_2003.jpg",image1,image3)
        facegraph_similarity_metrics("testlogs/IMG_20160610_071603.jpg","testlogs/KSrinivasan_2003.jpg",image2,image3)
        facegraph_similarity_metrics("testlogs/IMG_20160610_071455.jpg","testlogs/IMG_20171112_180837.jpg",image1,image4)
        facegraph_similarity_metrics("testlogs/IMG_20160610_071603.jpg","testlogs/IMG_20171112_180837.jpg",image2,image4)
        facegraph_similarity_metrics("testlogs/IMG_20171112_180837.jpg","testlogs/ExamplePortrait1.jpg",image4,image5)
        exit()

    input_image1 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141138.jpg")
    input_image2 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141144.jpg")
    input_image3 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_141152.jpg")
    input_image4 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/IMG_20160712_131709.jpg")
    input_image5 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg")
    input_image6 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_2.jpg")
    input_image7 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf2_1.jpg")
    input_image8 = ImageToBitMatrix.image_to_bitmatrix(
        "/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf8_1.jpg")

    dlim1 = DeepLearningConvolution(input_image1)
    dlim2 = DeepLearningConvolution(input_image2)
    dlim3 = DeepLearningConvolution(input_image3)
    dlim4 = DeepLearningConvolution(input_image4)
    dlim5 = DeepLearningConvolution(input_image5)
    dlim6 = DeepLearningConvolution(input_image6)
    dlim7 = DeepLearningConvolution(input_image7)
    dlim8 = DeepLearningConvolution(input_image8)

    dlc11 = DeepLearningConvolution(input_bitmap11)
    dlc12 = DeepLearningConvolution(input_bitmap12)
    dlc21 = DeepLearningConvolution(input_bitmap21)
    dlc22 = DeepLearningConvolution(input_bitmap22)
    dlc3 = DeepLearningConvolution(input_bitmap3)
    dlc41 = DeepLearningConvolution(input_bitmap41)
    dlc42 = DeepLearningConvolution(input_bitmap42)
    dlc51 = DeepLearningConvolution(input_bitmap51)
    dlc52 = DeepLearningConvolution(input_bitmap52)

    convolution_stride = 5
    conv_dlim1 = dlim1.convolution(convolution_stride)
    conv_dlim2 = dlim2.convolution(convolution_stride)
    conv_dlim3 = dlim3.convolution(convolution_stride)
    conv_dlim4 = dlim4.convolution(convolution_stride)
    conv_dlim5 = dlim5.convolution(convolution_stride)
    conv_dlim6 = dlim6.convolution(convolution_stride)
    conv_dlim7 = dlim7.convolution(convolution_stride)
    conv_dlim8 = dlim8.convolution(convolution_stride)

    conv_map11 = dlc11.convolution(convolution_stride)
    conv_map12 = dlc12.convolution(convolution_stride)
    conv_map21 = dlc21.convolution(convolution_stride)
    conv_map22 = dlc22.convolution(convolution_stride)
    conv_map3 = dlc3.convolution(convolution_stride)
    conv_map41 = dlc41.convolution(convolution_stride)
    conv_map42 = dlc42.convolution(convolution_stride)
    conv_map51 = dlc51.convolution(convolution_stride)
    conv_map52 = dlc52.convolution(convolution_stride)

    pool_slidewindow_width = 2
    pool_dlim1 = dlim1.max_pooling(pool_slidewindow_width)
    pool_dlim2 = dlim2.max_pooling(pool_slidewindow_width)
    pool_dlim3 = dlim3.max_pooling(pool_slidewindow_width)
    pool_dlim4 = dlim4.max_pooling(pool_slidewindow_width)
    pool_dlim5 = dlim5.max_pooling(pool_slidewindow_width)
    pool_dlim6 = dlim6.max_pooling(pool_slidewindow_width)
    pool_dlim7 = dlim7.max_pooling(pool_slidewindow_width)
    pool_dlim8 = dlim8.max_pooling(pool_slidewindow_width)

    pool_map11 = dlc11.max_pooling(pool_slidewindow_width)
    pool_map12 = dlc12.max_pooling(pool_slidewindow_width)
    pool_map21 = dlc21.max_pooling(pool_slidewindow_width)
    pool_map22 = dlc22.max_pooling(pool_slidewindow_width)
    pool_map3 = dlc3.max_pooling(pool_slidewindow_width)
    pool_map41 = dlc41.max_pooling(pool_slidewindow_width)
    pool_map42 = dlc42.max_pooling(pool_slidewindow_width)
    pool_map51 = dlc51.max_pooling(pool_slidewindow_width)
    pool_map52 = dlc52.max_pooling(pool_slidewindow_width)

    print("##########################################")
    print("Set of Convolution Maps")
    print("##########################################")
    print(conv_dlim1)
    print(conv_dlim2)
    print(conv_dlim3)
    print(conv_dlim4)
    print(conv_dlim5)
    print(conv_dlim6)
    print(conv_dlim7)
    print(conv_dlim8)

    #print "Example 11:"
    # print "###########"
    # pprint.pprint(conv_map11)
    # print "###########"
    #print "Example 12:"
    # print "###########"
    # pprint.pprint(conv_map12)
    # print "###########"
    #print "Example 21:"
    # print "###########"
    # pprint.pprint(conv_map21)
    # print "###########"
    #print "Example 22:"
    # print "###########"
    # pprint.pprint(conv_map22)
    # print "###########"
    #print "Example 3:"
    # print "###########"
    # pprint.pprint(conv_map3)
    # print "###########"
    #print "Example 41:"
    # print "###########"
    # pprint.pprint(conv_map41)
    # print "###########"
    #print "Example 42:"
    # print "###########"
    # pprint.pprint(conv_map42)
    # print "###########"
    #print "Example 51:"
    # print "###########"
    # pprint.pprint(conv_map51)
    # print "###########"
    #print "Example 52:"
    # print "###########"
    # pprint.pprint(conv_map52)

    print("##########################################")
    print("Max Pooling Map")
    print("##########################################")
    print(pool_dlim1)
    print(pool_dlim2)
    print(pool_dlim3)
    print(pool_dlim4)
    print(pool_dlim5)
    print(pool_dlim6)
    print(pool_dlim7)
    print(pool_dlim8)

    #print "Example 11:"
    # print "###########"
    # pprint.pprint(pool_map11)
    # print "###########"
    #print "Example 12:"
    # print "###########"
    # pprint.pprint(pool_map12)
    # print "###########"
    #print "Example 21:"
    # print "###########"
    # pprint.pprint(pool_map21)
    # print "###########"
    #print "Example 22:"
    # print "###########"
    # pprint.pprint(pool_map22)
    # print "###########"
    #print "Example 3:"
    # print "###########"
    # pprint.pprint(pool_map3)
    # print "###########"
    #print "Example 41:"
    # print "###########"
    # pprint.pprint(pool_map41)
    # print "###########"
    #print "Example 42:"
    # print "###########"
    # pprint.pprint(pool_map42)
    # print "###########"
    #print "Example 51:"
    # print "###########"
    # pprint.pprint(pool_map51)
    # print "###########"
    #print "Example 52:"
    # print "###########"
    # pprint.pprint(pool_map52)

    maxpool_map_width = 5

    print("###########################################################################################")
    print("Final Layer of Inference from Max Pooling Layer - BackPropagation on Max Pooling Layer Neurons")
    print("###########################################################################################")
    dlim1infer = dlim1.infer_from_max_pooling(pool_dlim1, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim1infer))
    dlim2infer = dlim2.infer_from_max_pooling(pool_dlim2, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim2infer))
    dlim3infer = dlim3.infer_from_max_pooling(pool_dlim3, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim3infer))
    dlim4infer = dlim4.infer_from_max_pooling(pool_dlim4, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim4infer))
    dlim5infer = dlim5.infer_from_max_pooling(pool_dlim5, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim5infer))
    dlim6infer = dlim6.infer_from_max_pooling(pool_dlim6, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim6infer))
    dlim7infer = dlim7.infer_from_max_pooling(pool_dlim7, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim7infer))
    dlim8infer = dlim8.infer_from_max_pooling(pool_dlim8, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Image:", dlim8infer))

    #print "Example 11:"
    # print "###########"
    dlc11infer = dlc11.infer_from_max_pooling(pool_map11, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 11:", dlc11infer))
    # print "###########"
    #print "Example 12:"
    # print "###########"
    dlc12infer = dlc12.infer_from_max_pooling(pool_map12, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 12:", dlc12infer))
    # print "###########"
    #print "Example 21:"
    # print "###########"
    dlc21infer = dlc21.infer_from_max_pooling(pool_map21, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 21:", dlc21infer))
    # print "###########"
    #print "Example 22:"
    # print "###########"
    dlc22infer = dlc22.infer_from_max_pooling(pool_map22, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 22:", dlc22infer))
    # print "###########"
    #print "Example 3:"
    # print "###########"
    dlc3infer = dlc3.infer_from_max_pooling(pool_map3, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 3:", dlc3infer))
    # print "###########"
    #print "Example 41:"
    # print "###########"
    dlc41infer = dlc41.infer_from_max_pooling(pool_map41, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 41:", dlc41infer))
    # print "###########"
    #print "Example 42:"
    # print "###########"
    dlc42infer = dlc42.infer_from_max_pooling(pool_map42, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 42:", dlc42infer))
    # print "###########"
    #print "Example 51:"
    # print "###########"
    dlc51infer = dlc51.infer_from_max_pooling(pool_map51, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 51:", dlc51infer))
    # print "###########"
    #print "Example 52:"
    # print "###########"
    dlc52infer = dlc52.infer_from_max_pooling(pool_map52, maxpool_map_width)
    print(("Inference from Max Pooling Layer - Example 52:", dlc52infer))
