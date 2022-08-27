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
import ImageGraph_Keras_Theano
#from ImageGraph_Keras_Theano import histogram_partition_distance_similarity 
import random
from GraphMining_GSpan import GSpan
from scipy.stats import wasserstein_distance 
from shapely.geometry import Polygon
from scipy import stats
from libpysal.weights import lat2W
from esda.moran import Moran
import ImageToBitMatrix
from osgeo import gdal
import rasterio
import rasterio.features
import rasterio.warp
from rasterio.windows import Window
import fiona.transform
import rasterio.sample
import math


os.environ['KERAS_BACKEND'] = 'theano'
#os.environ['KERAS_BACKEND'] = 'tensorflow'

def polya_urn_urban_growth_model(fourcoloredsegments,segmentedgis,iterations=1000):
    for newsegment in range(len(segmentedgis[7][0]) - 1):
        randomcolor=random.randint(1,4)
        randomcolorbin=fourcoloredsegments[randomcolor]
        #randomcolorbin.append(segmentedgis[7][0][newsegment])
        randomcolorbin.append("s"+str(newsegment))
    for n in range(iterations):
        randomcolor=random.randint(1,4)
        randomcolorbin=fourcoloredsegments[randomcolor]
        randombinelement=randomcolorbin[random.randint(0,len(randomcolorbin)-1)]
        randomcolorbin.append(randombinelement)
    return fourcoloredsegments

def urbansprawl_gini_coefficient(urbansprawldata):
    sumx=0.0
    sumxdiffy=0.0
    nans=0
    for x in urbansprawldata:
        if not math.isnan(x):
            sumx += float(x)
        else:
            nans += 1
    for x in urbansprawldata:
        for y in urbansprawldata:
            if not math.isnan(x) and not math.isnan(y):
                sumxdiffy += abs(float(x)-float(y))
    giniindex = sumxdiffy / (2*(len(urbansprawldata)-nans)*sumx)
    print("urbansprawl_gini_coefficient(): Gini Index of the dataset = ",giniindex)
    return giniindex

def urban_sprawl_from_raster(longx,latx,longy,laty,raster,dt):
    urbansprawlstatistics=[]
    for lon in np.arange(longx,longy,0.01):
        for lat in np.arange(latx,laty,0.01):
            values=data_from_raster_georeferencing(raster,longitude=lon,latitude=lat,sample=True,datatype=dt)
            urbansprawlstatistics.append(values[0])
    print("urban_sprawl_from_raster(): urbansprawlstatisitcs = ",urbansprawlstatistics)
    urbansprawl_gini_coefficient(urbansprawlstatistics)
    return urbansprawlstatistics

def data_from_raster_georeferencing(geotifffile,shapes=False,longitude=None,latitude=None,bandnum=1,datatype="Population",windowslice=100,sample=False):
    print("===================="+geotifffile+"=====================")
    longlatpolygons=[]
    raster = rasterio.open(geotifffile)
    if shapes==True:
        mask = raster.dataset_mask()
        for geom, val in rasterio.features.shapes(mask, transform=raster.transform):
             longlatpolygons.append(rasterio.warp.transform_geom(raster.crs, 'EPSG:4326', geom, precision=6))
        print("Longitude-Latitude Polygons in GeoTIFF raster:")
        print(longlatpolygons)
    print("Raster bounds:",raster.bounds)
    print("Raster height:",raster.height)
    print("Raster width:",raster.width)
    print("Raster top left - spatial value:",raster.xy(0,0))
    print("Raster bottom right - spatial value:",raster.xy(raster.height,raster.width))
    print("Raster transform:",raster.transform)
    print("Raster CRS:",raster.crs)
    print("Longitude:",longitude)
    print("Latitude:",latitude)
    if raster.crs == rasterio.crs.CRS.from_string("EPSG:4326"):
        xincrement=int(raster.width/windowslice)
        yincrement=int(raster.height/windowslice)
        window_id=0
        topx=0
        topy=0
        bottomx=xincrement
        bottomy=yincrement
        searchfound=None
        if sample==True:
            values = list(rasterio.sample.sample_gen(raster,[[longitude,latitude]]))
            print(datatype + " from raster for longitude-latitude:",values) 
            return values
        else:
            for x in range(windowslice):
                for y in range(windowslice):
                    print("Window id:",window_id)
                    print("Window dimensions:(",topx,",",topy,",",bottomx,",",bottomy,")")
                    banddata=raster.read(bandnum,window=Window(topx,topy,bottomx,bottomy))
                    window_id+=1
                    print("Raster data:",banddata)
                    if longitude is not None and latitude is not None:
                        if longitude > raster.bounds.left and longitude < raster.bounds.right and latitude > raster.bounds.bottom and latitude < raster.bounds.top:
                            try:
                                searchfound=banddata[row,col]
                                break
                            except:
                                print("Searched Longitude-Latitude not found...continuing")
                                pass
                        topy+=yincrement
                        bottomy+=yincrement
                    topy=0
                    bottomy=yincrement
                    topx+=xincrement
                    bottomx+=xincrement
            print(datatype + " from raster:",searchfound)
            return searchfound
    else:
        src_crs = "EPSG:4326"  #WGS84
        print("Source CRS:",src_crs)
        dst_crs = raster.crs.to_proj4() #mollweide
        print("Destination CRS:",dst_crs)
        lon,lat = fiona.transform.transform(src_crs,dst_crs,[longitude],[latitude])
        new_coords = [[x,y] for x,y in zip(lon,lat)]
        print("Transformed Coordinates:",new_coords)
        values = list(rasterio.sample.sample_gen(raster,new_coords))
        print(datatype + " from raster:",values) 
        return values

def translate_geotiff_to_jpeg(geotifffile,display=True,topx=0,topy=0,bottomx=1000,bottomy=1000,bandnum=1):
    #options = ['-ot Byte','-of JPEG','-b 1','-scale']
    geotifffiletoks=geotifffile.split(".")
    if display==True:
        print("Displaying image...")
        img = gdal.Open(geotifffile, gdal.GA_ReadOnly)
        band = img.GetRasterBand(bandnum)
        arr = band.ReadAsArray(topx,topy,bottomx,bottomy)
        plt.imshow(arr)
        print("Raster bands:",img.RasterCount)
        print("Raster Xsize:",img.RasterXSize)
        print("Raster Ysize:",img.RasterYSize)
        band.ComputeStatistics(0)
        statistics=band.GetStatistics(True,True)
        metadata=band.GetMetadata()
        print("Statistics:",statistics)
        print("MetaData:",metadata)
    jpegfilename=geotifffiletoks[0].split("/")
    #gdal.Translate("testlogs/RemoteSensingGIS/"+jpegfilename[2] + ".jpg",geotifffile,format='JPEG', width=1024, height=0, scaleParams=[[0, 255, 0, 65535]], outputType = gdal.GDT_UInt16)
    gdal.Translate("testlogs/RemoteSensingGIS/"+jpegfilename[2] + ".jpg",geotifffile,format='JPEG', width=1024, height=0, scaleParams=[[statistics[0],statistics[1]]], outputType = gdal.GDT_UInt16)

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

def urban_sprawl_dispersion(image):
    print(("image:",image))
    img=cv2.imread(image)
    print("img:",img)
    print("img.shape:",img.shape)
    w = lat2W(img.shape[0],img.shape[1])
    print("lat2W weights the Urban Sprawl dispersion:",w)
    img2Dmatrix=ImageToBitMatrix.image3D_to_2D(image)
    print("img2Dmatrix:",img2Dmatrix)
    MoransI = Moran(img2Dmatrix,w)
    print("Moran's I of the Urban Sprawl dispersion:",MoransI.I)
    print("Moran's p-norm of the Urab Sprawl dispersion:",MoransI.p_norm) 

def urban_sprawl_from_segments(image,segment,maximum_population_density=100000,sqkmtocontourarearatio=0,legend=None,sqkmareatopopulationratio=6.22,voronoi_delaunay=False,number_of_clusters=2,maxiterations=2):
    print(("Image:",image))
    img=cv2.imread(image)
    imagearea=img.shape[0]*img.shape[1]
    UrbanSprawlAreas=[]
    print(("Number of segments - Number of Urban areas:",len(segment[8][0])))
    urban_sprawl_dispersion(image)
    ImageGraph_Keras_Theano.contours_kmeans_clustering(image,segment,number_of_clusters=number_of_clusters,maxiterations=maxiterations)
    fig1 = plt.figure(dpi=100)
    cityid=0
    centroids=[]
    voronoifacets=segment[6]
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
    for n in range(len(segment[8][0]) - 1):
        #print(("Urban Area:",segment[8][0][n]))
        circumference = cv2.arcLength(segment[8][0][n],True)
        convexhull = cv2.convexHull(segment[8][0][n])
        #convexhull = ConvexHull(segment[8][0][n])
        contourarea = cv2.contourArea(segment[8][0][n])
        contourareas.append(contourarea)
        cv2.drawContours(img,segment[8][0][n],-1,(0,255,0),2)
        print("Contour boundary point:",segment[8][0][n][0])
        pop_dens=0
        try:
            contourcolor = img[segment[8][0][n][0][0][0],segment[8][0][n][0][0][1]]
            print("Contour color:",contourcolor)
            averageBGR = int((contourcolor[0] + contourcolor[1] + contourcolor[2])/3)
            if legend is None:
                population_density = (averageBGR/255) * maximum_population_density 
            else:
                prevcolor=0
                for color,populationrange in legend.items():
                    populationrangetoks=populationrange.split("-")
                    if averageBGR > prevcolor and averageBGR <= color:
                        population_density = int(populationrangetoks[1])
                    prevcolor=color
        except:
            population_density = maximum_population_density
        x,y,w,h = cv2.boundingRect(segment[8][0][n])
        print(("Convex Hull of Urban Area:" , convexhull))
        print(("Circumference of Urban Area:",circumference))
        (cx,cy),radius=cv2.minEnclosingCircle(segment[8][0][n])
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
        population_from_area=sqkmareatopopulationratio*urbansprawlsqkmarea*urbansprawlsqkmarea
        population_from_density=population_density*urbansprawlsqkmarea
        print(("Population of Urban Sprawl (from density):", population_from_density))
        print(("Population of Urban Sprawl (from area):",population_from_area))
        moments=cv2.moments(segment[8][0][n])
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
    if voronoi_delaunay:
        draw_voronoi_tessellation(img,centroids)
        draw_delaunay_triangulation(img,segment[7])
    print("Rankings of Urban Areas - sorted contour areas:")
    print(sorted(UrbanSprawlAreas))
    plt.show()
    imagetok1=image.split(".")
    imagetok2=imagetok1[0].split("/")
    cv2.imwrite("testlogs/"+imagetok2[1]+"-contourlabelled.jpg",img)
    cv2.waitKey()
    facegraph=segment[9] 
    print("Number of Vororoi Facets:",len(voronoifacetareas))
    print("Number of Contours:",len(contourareas))
    minsize=min(len(contourareas),len(voronoifacetareas))
    tau,pvalue = stats.kendalltau(sorted(contourareas[:minsize]),sorted(voronoifacetareas[:minsize]))
    print("(Correlation,PValue) between Contour areas and Voronoi polygon areas of Urban sprawls:",(tau,pvalue))
    print("Betweenness centrality of urban sprawl facegraph:",nx.betweenness_centrality(facegraph))
    print("Degree centrality of urban sprawl facegraph:",nx.degree_centrality(facegraph))
    print("Closeness centrality of urban sprawl facegraph:",nx.closeness_centrality(facegraph))
    print("PageRank of urban sprawl facegraph:",nx.pagerank(facegraph))
    facegraphminspanforest=nx.minimum_spanning_edges(facegraph,"boruvka")
    print("Minimum Spanning Forest Edges of Facegraph:",facegraphminspanforest)
    facegraphhits=nx.hits(facegraph)
    print("HITS Hub-Authorities values of Facegraph:", facegraphhits)
    print(facegraphhits)
    return (UrbanSprawlAreas)


if __name__ == "__main__":
    #seg1=image_segmentation("testlogs/NightLights_13nasa-india-2016.jpg")
    #seg2=image_segmentation("testlogs/NightLights_13nasa-india-2012.jpg")
    #seg3=image_segmentation("testlogs/NightLights_13nasa-india-2021.jpg")
    #seg4=ImageGraph_Keras_Theano.image_segmentation("testlogs/NASAVIIRSNightLightsChennaiMetropolitanArea_17November2021.jpg",voronoi_delaunay=True)
    #ImageGraph_Keras_Theano.histogram_partition_distance_similarity("testlogs/NightLights_13nasa-india-2016.jpg","testlogs/NightLights_13nasa-india-2012.jpg")
    #ImageGraph_Keras_Theano.histogram_partition_distance_similarity("testlogs/NightLights_13nasa-india-2016.jpg","testlogs/NightLights_13nasa-india-2021.jpg")
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2016.jpg",seg1)
    #urban_sprawl_from_segments("testlogs/NightLights_13nasa-india-2012.jpg",seg2)
    #urban_sprawl_from_segments("testlogs/NASAVIIRSNightLightsChennaiMetropolitanArea_17November2021.jpg",seg4,voronoi_delaunay=True)
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
    #seg9=image_segmentation("testlogs/HRSL_World_NightTimeStreets.jpg")
    #legend={235/3:"0-1",245/3:"1-50",255/3:"50-100",362/3:"100-250",372/3:"250-1000",382/3:"1000-2500",510/3:"2500-27057"}
    #legend={510/3:"0-1",382/3:"1-50",372/3:"50-100",362/3:"100-250",255/3:"250-1000",245/3:"1000-2500",235/3:"2500-27057"}
    #mapscale=147914382
    mapscale=266.0/854.0
    #urban_sprawl_from_segments("testlogs/HRSL_World_NightTimeStreets.jpg",seg9,-1,mapscale,legend)
    #seg10=image_segmentation("testlogs/SEDAC2030UrbanExpansionProbabilities.jpg")
    #urban_sprawl_from_segments("testlogs/SEDAC2030UrbanExpansionProbabilities.jpg",seg10,100000,sqkmtocontourarearatio=mapscale,legend=None)
    #fourcoloredsegments=defaultdict(list)
    #fourcoloredsegments=polya_urn_urban_growth_model(fourcoloredsegments,seg10)
    #print("Polya Urn Urban Growth Model for 4 colored urban sprawl segmentation:",fourcoloredsegments)
    #seg11=ImageGraph_Keras_Theano.image_segmentation("testlogs/ChennaiMetropolitanAreaTransitNetwork_GoogleMaps_20May2022.jpg")
    #urban_sprawl_from_segments("testlogs/ChennaiMetropolitanAreaTransitNetwork_GoogleMaps_20May2022.jpg",seg11,100000,sqkmtocontourarearatio=mapscale,legend=None,voronoi_delaunay=True)
    #seg12=ImageGraph_Keras_Theano.image_segmentation("testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg")
    #urban_sprawl_from_segments("testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg",seg12,voronoi_delaunay=True)
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_0_lon_70_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_0_lon_80_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_0_lon_90_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_70_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_90_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_20_lon_60_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_20_lon_70_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_20_lon_80_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_20_lon_90_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_30_lon_60_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_30_lon_70_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_30_lon_80_general-v1.5.tif")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/GHS_BUILT_S_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif")
    #data_from_raster_georeferencing("testlogs/RemoteSensingGIS/GHS_BUILT_S_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif",longitude=80.2707,latitude=13.0827,windowslice=15,datatype="BUILT-S")
    urban_sprawl_from_raster(80.1,13.0,80.3,13.2,"testlogs/RemoteSensingGIS/GHS_BUILT_S_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif",dt="BUILT-S")
    urban_sprawl_from_raster(80.1,13.0,80.3,13.2,"testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.5.tif",dt="Population")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_ST_DRAD.TIF")
    #data_from_raster_georeferencing("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_ST_DRAD.TIF",bandnum=1,datatype="Radiance")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_SR_B7.TIF")
    #data_from_raster_georeferencing("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_SR_B7.TIF",bandnum=1,datatype="Radiance")
