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
import shapely
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
from statistics import mean,median,stdev
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.style as mplstyle
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import osmnx
import DBSCANClustering
from descartes import PolygonPatch
from shapely.geometry import Point, LineString, Polygon
import geopandas as geo
import geemap
import ee
import seaborn
import pandas

mplstyle.use('fast')
shapely.speedups.disable()
os.environ['KERAS_BACKEND'] = 'theano'
#os.environ['KERAS_BACKEND'] = 'tensorflow'
citygeometry=[]

def learn_polya_urn_growth_weights(ncolorsegments_date1,ncolorsegments_date2):
    replicationweights=defaultdict(int)
    for date1color,date1bin in ncolorsegments_date1.items():
        date2bin=ncolorsegments_date2[date1color]
        if len(date1bin) > 0:
            replicationweights[date1color]=len(date2bin)/len(date1bin)
        else:
            replicationweights[date1color]=1
    print("learn_polya_urn_growth_weights() - contour growth weights between 2 dates (date1 to date2):",replicationweights)
    return replicationweights

def polya_urn_urban_growth_model(image,ncoloredsegments,segmentedgis,iterations=1000,replicationweights=None):
    img=cv2.imread(image)
    print("img shape:",img.shape)
    totalareabefore=0
    for newsegment in range(len(segmentedgis[8][0]) - 1):
        (cx,cy),radius=cv2.minEnclosingCircle(segmentedgis[8][0][newsegment])
        contourarea = cv2.contourArea(segmentedgis[8][0][newsegment])
        center=(int(cx),int(cy))
        #print("polya_urn_urban_growth_model() - contour center:",center)
        if center[0] < img.shape[0] and center[1] < img.shape[1]:
            contourcolor=img[center[0],center[1]]
            #print("polya_urn_urban_growth_model() - contour color:",contourcolor)
            randomcolorbin=ncoloredsegments[sum(contourcolor)]
            randomcolorbin.append(("s"+str(newsegment),contourarea))
    print("Urban sprawl segments before Polya Urn Growth for ",image,":")
    print("==============================================")
    totalsegmentsbefore=0
    for color,segments in ncoloredsegments.items():
        print("color ",color,":",len(segments))
        totalsegmentsbefore += len(segments)
        for segment in segments:
            totalareabefore += segment[1]
    print("Total number of segments before Polya Urn Urban Growth:",totalsegmentsbefore)
    print("Total number of segments after Polya Urn Urban Growth:",totalareabefore)
    colors=list(ncoloredsegments.keys())
    for n in range(iterations):
        randomcolor=random.randint(0,len(colors)-1)
        randomcolorbin=ncoloredsegments[colors[randomcolor]]
        if len(randomcolorbin) > 1:
            randombinelement=randomcolorbin[random.randint(0,len(randomcolorbin)-1)]
            if replicationweights != None:
                colorweight=replicationweights[colors[randomcolor]]
                print("color = ",colors[randomcolor],"; colorweight = ",colorweight)
                while colorweight >= 0:
                    randomcolorbin.append(randombinelement)
                    colorweight -= 1
            else:
                randomcolorbin.append(randombinelement)
    print("Urban sprawl segments after Polya Urn Growth for ",image,":")
    print("==============================================")
    totalsegmentsafter=0
    totalareaafter=0
    for color,segments in ncoloredsegments.items():
        print("color ",color,":",len(segments))
        totalsegmentsafter += len(segments)
        for segment in segments:
            totalareaafter += segment[1]
    print("Total number of segments after Polya Urn Urban Growth:",totalsegmentsafter)
    print("Total Urban sprawl area after Polya Urn Urban Growth:",totalareaafter)
    print("Percentage growth of urban sprawl simulated by Polya Urn Urban Growth Model (in terms of segments):",(totalsegmentsafter-totalsegmentsbefore)*100/totalsegmentsbefore)
    print("Percentage growth of urban sprawl simulated by Polya Urn Urban Growth Model (in terms of total area):",(totalareaafter-totalareabefore)*100/totalareabefore)
    return ncoloredsegments

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

def urban_sprawl_road_network_OSM(cityname=None,latx=0,laty=0,longx=0,longy=0,address=None,radius=1000,defaultcapacity=1,travel_speed=30,trip_times=[10,15,20,25,30]):
    if cityname is not None:
        roadgraph = osmnx.graph.graph_from_place(cityname)
    elif latx > 0 and laty > 0 and longx >0 and longy > 0:
        roadgraph = osmnx.graph.graph_from_bbox(latx,laty,longx,longy)
    elif address is not None:
        roadgraph = osmnx.graph.graph_from_address(address,dist=radius) 
    stats=osmnx.stats.basic_stats(roadgraph,area=math.pi*radius*radius)
    print("Basic statistics about road network graph:",stats)
    minweightedvertexcover=nx.algorithms.approximation.vertex_cover.min_weighted_vertex_cover(nx.Graph(roadgraph))
    print("Minimum weighted vertex cover of road network graph:",minweightedvertexcover)
    scc=nx.strongly_connected_components(nx.DiGraph(roadgraph))
    for c in scc:
        print("Strongly connected component of road network graph:",c)
    gdf_nodes,gdf_edges=osmnx.graph_to_gdfs(roadgraph,nodes=True,edges=True,node_geometry=True,fill_edge_geometry=True)
    x, y = gdf_nodes['geometry'].unary_union.centroid.xy
    center_node = osmnx.get_nearest_node(roadgraph, (y[0], x[0]))
    roadgraph = osmnx.project_graph(roadgraph)
    meters_per_minute = travel_speed * 1000 / 60
    for u, v, k, data in roadgraph.edges(data=True, keys=True):
        data['time'] = data['length'] / meters_per_minute
    isochrone_colors = osmnx.plot.get_colors(n=len(trip_times), cmap='plasma', start=0, return_hex=True)
    node_colors = {}
    for trip_time, color in zip(sorted(trip_times, reverse=True), isochrone_colors):
        subgraph = nx.ego_graph(roadgraph, center_node, radius=trip_time, distance='time')
        for node in subgraph.nodes():
            node_colors[node] = color
    nc = [node_colors[node] if node in node_colors else 'none' for node in roadgraph.nodes()]
    ns = [15 if node in node_colors else 0 for node in roadgraph.nodes()]
    fig, ax = osmnx.plot_graph(roadgraph, node_color=nc, node_size=ns, node_alpha=0.8, node_zorder=2, bgcolor='k', edge_linewidth=0.2, edge_color='#999999')
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(roadgraph, center_node, radius=trip_time, distance='time')
        node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
        bounding_poly = geo.GeoSeries(node_points).unary_union.convex_hull
        isochrone_polys.append(bounding_poly)
    fig, ax = osmnx.plot_graph(roadgraph, show=False, close=False, edge_color='#999999', edge_alpha=0.2, node_size=0, bgcolor='k')
    for polygon, fc in zip(isochrone_polys, isochrone_colors):
        patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
        ax.add_patch(patch)
    plt.show()
    print("--------- Locations (NetworkX) -----------")
    print(roadgraph.nodes()) 
    print("---------- Locations (GeoDataFrames) -------")
    print(gdf_nodes.to_json())
    print("--------- Roads (NetworkX) ---------------")
    print(roadgraph.edges())
    print("--------- Roads (GeoDataFrames) ---------")
    print(gdf_edges.to_json())
    print("Betweenness centrality of urban sprawl road network graph:",nx.betweenness_centrality(nx.Graph(roadgraph)))
    print("Cheeger Constant - Isoperimetric Number - Edge Expansion of urban sprawl road network graph minimum weight vertex cover:",nx.edge_expansion(roadgraph,minweightedvertexcover))
    print("Maxflow-Mincut of urban sprawl road network graph:")
    roadnetworkvertices=list(roadgraph.nodes())
    roadnetworkedges=list(roadgraph.edges())
    print("roadnetworkvertices:",roadnetworkvertices)
    print("roadnetworkedges:",roadnetworkedges)
    for e in roadnetworkedges:
        print("roadgraph[e[0]][e[1]]:",roadgraph[e[0]][e[1]])
        roadgraph[e[0]][e[1]][0]["capacity"] = defaultcapacity
    rand1=random.randint(0,len(roadnetworkvertices)-1)
    rand2=random.randint(0,len(roadnetworkvertices)-1)
    s=roadnetworkvertices[rand1]
    t=roadnetworkvertices[rand2]
    cut_value,partition = nx.minimum_cut(nx.Graph(roadgraph),s,t)
    reachable,nonreachable = partition
    cutset = set()
    for u,neighbours in ((n,roadgraph[n]) for n in reachable):
        cutset.update((u,v) for v in neighbours if v in nonreachable)
    print("sorted cutset:",sorted(cutset))
    osmnx.plot_graph(roadgraph,bgcolor="w",node_color="g",edge_color="r")
    return roadgraph

def GEE_city_average_radiance(viirsimagery):
    global citygeometry
    print("citygeometry:",citygeometry)
    return viirsimagery.reduceRegions(reducer=ee.Reducer.mean(),collection=citygeometry,scale=500)

def GEE_get_date(viirsimagery):
    return viirsimagery.set('date',viirsimagery.date().format())

def urban_sprawl_from_GEE(imagecollection,featurecollection,nightlightsparameter,cities):
    global citygeometry
    ee.Authenticate()
    ee.Initialize(project="urbansprawlviirsanalytics")
    viirs = ee.ImageCollection(imagecollection).select(nightlightsparameter)
    citygeometry = ee.FeatureCollection(featurecollection).filter(ee.Filter.inList('ADM1_NAME',cities))
    reduced_cities = viirs.map(GEE_city_average_radiance).flatten()
    reduced_dates = viirs.map(GEE_get_date)
    columns = ['ADM1_NAME','mean']
    cities_list = reduced_cities.reduceColumns(ee.Reducer.toList(len(columns)),columns).values().getInfo()
    dates_list = reduced_dates.reduceColumns(ee.Reducer.toList(1),["date"]).values().getInfo()
    print("cities_list:",cities_list)
    print("dates_list:",dates_list)
    citiespdf = pandas.DataFrame(numpy.array(cities_list).squeeze(),columns=columns)
    datespdf = pandas.DataFrame(numpy.array(dates_list).squeeze(),columns=["date"])
    for city in cities:
        citiespdf.loc[citiespdf["ADM1_NAME"]==city,"dates"] = numpy.array(dates_list).squeeze() 
    #joinedpdf=citiespdf.join(datespdf)
    citiespdf["dates"]=pandas.to_datetime(citiespdf["dates"])
    citiespdf["mean"]=citiespdf["mean"].astype(float)
    citiespdf.set_index("dates",inplace=True)
    print("-------- citiespdf ----------")
    print(citiespdf)
    fig,ax = plt.subplots(figsize=(15,7))
    for city in cities:
        radiance=citiespdf.loc[citiespdf["ADM1_NAME"]==city,:]
        print("------------radiance-----------")
        print(radiance)
        print(radiance.index)
        seaborn.lineplot(data=radiance,x=radiance.index,y="mean",label=city,ax=ax)
    ax.set_ylabel("average radiance",fontsize=1)
    ax.set_xlabel("date",fontsize=8)
    ax.legend(fontsize=8)
    ax.set_title("Mean radiance",fontsize=8)
    plt.show()
    return radiance

def urban_sprawl_from_raster(longx,latx,longy,laty,raster,dt):
    urbansprawlstatistics=[]
    rows=0
    for lon in np.arange(longx,longy,0.01):
        cols=0
        for lat in np.arange(latx,laty,0.01):
            values=data_from_raster_georeferencing(raster,longitude=lon,latitude=lat,sample=True,datatype=dt)
            urbansprawlstatistics.append(values[0])
            cols+=1
        rows+=1
    print("urban_sprawl_from_raster(): bounding box shape = ",(rows,cols))
    print("urban_sprawl_from_raster(): urbansprawlstatisitcs = ",urbansprawlstatistics)
    urbansprawl_gini_coefficient(urbansprawlstatistics)
    return (urbansprawlstatistics,(rows,cols))

def compare_raster_data(raster1data,raster2data):
    raster1hist=defaultdict(int)
    raster2hist=defaultdict(int)
    for r1 in raster1data:
        raster1hist[r1[0]] += 1
    for r2 in raster2data:
        raster2hist[r2[0]] += 1
    print("compare_raster_data(): raster1hist = ",raster1hist)
    print("compare_raster_data(): raster2hist = ",raster2hist)
    for k1,v1 in raster1hist.items():
        try:
            percentagedifference = ((v1-raster2hist[k1])/v1)*100
            print("Percentage change in ",k1,":",percentagedifference)
        except:
            print("Exception in raster histogram dictionary lookup")

def verhulste_ricker_population_growth_model(population_at_t1,intrinsic_growth_rate,carrying_capacity,metropolitan_agglomeration,fromyear,toyear):
    number_of_years=toyear-fromyear
    print("===================================================================")
    for y in range(1,number_of_years):
        projected_population_at_t2 = population_at_t1 * math.exp(intrinsic_growth_rate*(1 - population_at_t1/carrying_capacity))
        print("verhulste_ricker_population_growth_model(): projected " + metropolitan_agglomeration + " (year " + str(fromyear+y) + ") = ",projected_population_at_t2)
        population_at_t1 = projected_population_at_t2
    return projected_population_at_t2

def three_dimensional_urban_growth_model(rasterdata_2d,rasterdata_3d,longx,latx,longy,laty):
    raster2dhist=defaultdict(int)
    raster3dhist=defaultdict(int)
    heights=[]
    for rv,rs in zip(rasterdata_3d[0],rasterdata_2d[0]):
        height=rv[0]/rs[0]
        if math.isnan(height):
            height=0.0
        heights.append(height)
    avgbuildingheight=sum(heights)/len(heights)
    for r1 in rasterdata_2d[0]:
        raster2dhist[r1[0]] += 1
    for r2 in rasterdata_3d[0]:
        raster3dhist[r2[0]] += 1
    raster2dhist_sorted=sorted(raster2dhist.items(),key=operator.itemgetter(0),reverse=True)
    raster3dhist_sorted=sorted(raster3dhist.items(),key=operator.itemgetter(0),reverse=True)
    #print("three_dimensional_urban_growth_model(): raster2dhist = ",raster2dhist_sorted)
    #print("three_dimensional_urban_growth_model(): raster3dhist = ",raster3dhist_sorted)
    raster2dsurfaces=raster2dhist_sorted
    raster3dvolumes=raster3dhist_sorted
    maxbuildingheight=raster3dvolumes[0][0]/raster2dsurfaces[0][0]
    print("three_dimensional_urban_growth_model(): maximum building height = ",maxbuildingheight)
    print("three_dimensional_urban_growth_model(): heights = ",heights)
    print("three_dimensional_urban_growth_model(): mean(heights) = ",mean(heights))
    print("three_dimensional_urban_growth_model(): median(heights) = ",median(heights))
    print("three_dimensional_urban_growth_model(): stdev(heights) = ",stdev(heights))
    rows=rasterdata_3d[1][0]
    cols=rasterdata_3d[1][1]
    fig=plt.figure()
    ax = fig.gca(projection="3d")
    #rows, cols = np.meshgrid(rows, cols)
    X = np.arange(longx, longy, 0.01)
    Y = np.arange(latx, laty, 0.01)
    X, Y = np.meshgrid(X, Y)
    heights=np.asarray(heights).reshape(cols,rows)
    print("X.shape:",X.shape)
    print("Y.shape:",Y.shape)
    print("heights.shape:",heights.shape)
    surf = ax.plot_surface(X, Y, heights, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


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

def translate_geotiff_to_jpeg(geotifffile,display=True,topx=0,topy=0,bottomx=1000,bottomy=1000,bandnum=1,scaledown=50):
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
    gdal.Translate("testlogs/RemoteSensingGIS/"+jpegfilename[2] + ".jpg",geotifffile,format='JPEG', width=img.RasterXSize/scaledown, height=img.RasterYSize/scaledown, scaleParams=[[0, 255, 0, 65535]], outputType = gdal.GDT_UInt16)
    #gdal.Translate("testlogs/RemoteSensingGIS/"+jpegfilename[2] + ".jpg",geotifffile,format='JPEG', width=img.RasterXSize, height=img.RasterYSize, scaleParams=[[statistics[0],statistics[1]]], outputType = gdal.GDT_UInt16)

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
        #print(("centroid:", cent))
        subdiv.insert(tuple(cent))
    triangles = subdiv.getTriangleList()
    print(("image Delaunay triangles:", triangles))
    facets = subdiv.getVoronoiFacetList([])
    print(("image Voronoi Facets:", facets))
    for n in range(len(facets)):
        for f in facets[n]:
            fnp=np.array(f)
            #print("facet:",fnp)
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

def urban_sprawl_from_segments(image,segment,maximum_population_density=100000,sqkmtocontourarearatio=0,legend=None,sqkmareatopopulationratio=6.22,voronoi_delaunay=False,number_of_clusters=2,maxiterations=2,populationfromraster="None",scaleup=50):
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
        population_density=0
        if populationfromraster != "None":
            raster = rasterio.open(populationfromraster)
            (cx,cy),radius=cv2.minEnclosingCircle(segment[8][0][n])
            center=(int(cx),int(cy))
            longlat=raster.xy(center[0]*scaleup,center[1]*scaleup)
            print("urban_sprawl_from_segments(): raster xy longlat = ",longlat)
            values=data_from_raster_georeferencing(populationfromraster,shapes=False,longitude=longlat[0],latitude=longlat[1],bandnum=1,datatype="Population",sample=True)
            print("urban_sprawl_from_segments(): raster values = ",values)
            population_density = values[0]
        else:
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
    cv2.imwrite("testlogs/"+imagetok2[len(imagetok2)-1]+"-contourlabelled.jpg",img)
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

    #ncoloredsegments_2019=defaultdict(list)
    #seg12=ImageGraph_Keras_Theano.image_segmentation("testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg")
    #ncoloredsegments_2019=polya_urn_urban_growth_model("testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg",ncoloredsegments_2019,seg12)
    #urban_sprawl_from_segments("testlogs/GHSL_GIS_ChennaiMetropolitanArea.jpg",seg12,voronoi_delaunay=False,number_of_clusters=3,maxiterations=3)
    #print("Polya Urn Urban Growth Model for ",len(ncoloredsegments_2019.keys())," colored urban sprawl segmentation (Projection based on R2019A):",ncoloredsegments_2019)
    #print("===========================================================================================")
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
    #urban_sprawl_from_raster(80.1,13.0,80.3,13.2,"testlogs/RemoteSensingGIS/GHS_BUILT_S_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif",dt="BUILT-S")
    #urban_sprawl_from_raster(80.1,13.0,80.3,13.2,"testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.5.tif",dt="Population")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_ST_DRAD.TIF")
    #data_from_raster_georeferencing("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_ST_DRAD.TIF",bandnum=1,datatype="Radiance")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_SR_B7.TIF")
    #data_from_raster_georeferencing("testlogs/RemoteSensingGIS/LC08_L2SP_142051_20220729_20220806_02_T1_SR_B7.TIF",bandnum=1,datatype="Radiance")
    #translate_geotiff_to_jpeg("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.5.tif")
    #seg13=ImageGraph_Keras_Theano.image_segmentation("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.jpg")
    #urban_sprawl_from_segments("testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.jpg",seg13,maximum_population_density=100000,sqkmtocontourarearatio=mapscale,legend=None,sqkmareatopopulationratio=6.22,voronoi_delaunay=True,number_of_clusters=3,maxiterations=3,populationfromraster="testlogs/RemoteSensingGIS/FacebookMetaHRSL_IndiaPak_population_10_lon_80_general-v1.5.tif")

    #Chennai Metropolitan Area - GHSL R2022A BUILT-V overlay DBSCAN analysis
    #dbscan1=DBSCANClustering.DBSCAN("testlogs/ChennaiMetropolitanAreaExpansion21October2022_GHSLR2022A_BUILT-V-overlay.jpg")
    #dbscan1.clustering()
    #dbscan1.write_clustered_image(neuralnetwork=True)
    #seg14=ImageGraph_Keras_Theano.image_segmentation("testlogs/ChennaiMetropolitanAreaExpansion21October2022_GHSLR2022A_BUILT-V-overlay.jpg")
    #urban_sprawl_from_segments("testlogs/ChennaiMetropolitanAreaExpansion21October2022_GHSLR2022A_BUILT-V-overlay.jpg",seg14,maximum_population_density=11422,sqkmtocontourarearatio=mapscale,legend=None,sqkmareatopopulationratio=6.22,voronoi_delaunay=False,number_of_clusters=5,maxiterations=5)

    #Chennai Metropolitan Area Sprawl Bounding Box 1 - R2019A and R2022A comparison
    #r1data=urban_sprawl_from_raster(79.07,12.41,80.3,13.19,"testlogs/RemoteSensingGIS/GHS_SMOD_POP2015_GLOBE_R2019A_54009_1K_V2_0.tif",dt="Degree of Urbanization R2019A")
    #r2data=urban_sprawl_from_raster(79.07,12.41,80.3,13.19,"testlogs/RemoteSensingGIS/GHS_SMOD_P2030_GLOBE_R2022A_54009_1000_V1_0.tif",dt="Degree of Urbanization R2022A")
    #compare_raster_data(r1data,r2data)

    #Chennai Metropolitan Area Sprawl Bounding Box 2 - http://bboxfinder.com/#12.439259,79.271851,13.568572,80.351257 - R2019A and R2022A comparison
    #r1data=urban_sprawl_from_raster(79.271851,12.439259,80.351257,13.568572,"testlogs/RemoteSensingGIS/GHS_SMOD_POP2015_GLOBE_R2019A_54009_1K_V2_0.tif",dt="Degree of Urbanization R2019A")
    #r2data=urban_sprawl_from_raster(79.271851,12.439259,80.351257,13.568572,"testlogs/RemoteSensingGIS/GHS_SMOD_P2030_GLOBE_R2022A_54009_1000_V1_0_R8_C26.tif",dt="Degree of Urbanization R2022A")
    #compare_raster_data(r1data,r2data)

    #r2ddata=urban_sprawl_from_raster(79.271851,12.439259,80.351257,13.568572,"testlogs/RemoteSensingGIS/GHS_BUILT_S_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif",dt="BUILT_S R2022A")
    #r3ddata=urban_sprawl_from_raster(79.271851,12.439259,80.351257,13.568572,"testlogs/RemoteSensingGIS/GHS_BUILT_V_P2030LIN_GLOBE_R2022A_54009_100_V1_0_R8_C26.tif",dt="BUILT_V R2022A")
    #three_dimensional_urban_growth_model(r2ddata,r3ddata,79.271851,12.439259,80.351257,13.568572)
    
    #verhulste_ricker_population_growth_model(14730872,2.39/100.0,30000000,"Chennai Metropolitan Area Population",fromyear=2020,toyear=2050)
    #verhulste_ricker_population_growth_model(15195379,2.39/100.0,30000000,"Chennai Metropolitan Area Population",fromyear=2019,toyear=2050)

    #urban_sprawl_road_network_OSM(cityname="Kumbakonam")
    #urban_sprawl_road_network_OSM(latx=11.007927,laty=10.922989,longx=79.456730,longy=79.313908)
    #urban_sprawl_road_network_OSM(address="Uthiramerur, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Madurantakam, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Cheyyur, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Sholinghur, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Ranipet, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Cheyyar, Tamil Nadu, India",radius=6000)
    #urban_sprawl_road_network_OSM(address="Sricity, AP, India",radius=6000)

    #ncoloredsegments_2022=defaultdict(list)
    #seg14=ImageGraph_Keras_Theano.image_segmentation("testlogs/RemoteSensingGIS/ChennaiMetropolitanArea_GHSL_R2022A_GHS_SMOD_DegreeOfUrbanisation.jpg")
    #ncoloredsegments_2022=polya_urn_urban_growth_model("testlogs/RemoteSensingGIS/ChennaiMetropolitanArea_GHSL_R2022A_GHS_SMOD_DegreeOfUrbanisation.jpg",ncoloredsegments_2022,seg14)
    #urban_sprawl_from_segments("testlogs/RemoteSensingGIS/ChennaiMetropolitanArea_GHSL_R2022A_GHS_SMOD_DegreeOfUrbanisation.jpg",seg14,voronoi_delaunay=False,number_of_clusters=3,maxiterations=3)
    #print("Polya Urn Urban Growth Model for ",len(ncoloredsegments_2022.keys())," colored urban sprawl segmentation (Projection based on R2022A):",ncoloredsegments_2022)
    #print("===========================================================================================")
    #repweights=learn_polya_urn_growth_weights(ncoloredsegments_2019,ncoloredsegments_2022)
    #ncoloredsegments_2022=polya_urn_urban_growth_model("testlogs/RemoteSensingGIS/ChennaiMetropolitanArea_GHSL_R2022A_GHS_SMOD_DegreeOfUrbanisation.jpg",ncoloredsegments_2022,seg14,replicationweights=repweights)
    #print("Polya Urn Urban Growth Model for ",len(ncoloredsegments_2022.keys())," colored urban sprawl segmentation (Projection based on R2022A) - based on replacement matrix learnt from R2019A to R2022A:",ncoloredsegments_2022)
    urban_sprawl_from_GEE("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG","FAO/GAUL/2015/level1","avg_rad",['Berlin','Seoul','Sao Paulo'])
