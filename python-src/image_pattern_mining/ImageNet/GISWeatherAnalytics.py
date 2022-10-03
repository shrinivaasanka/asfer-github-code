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
import Streaming_AbstractGenerator
import base64
import io
import imageio
from PIL import Image
import codecs
#import metview as mv
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import date
import climetlab
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.models import Sequential
from EphemerisSearch import EphemerisSearch

def invert_image(image):
    img=cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    invimg=cv2.bitwise_not(thresh)
    return invimg

def climate_analytics(datasource,date="",time=""):
    if datasource == "n-body-analytics":
        ephem=EphemerisSearch("de421.bsp")
        ephem.extreme_weather_events_n_body_analytics(datesofEWEs=date,angularsep=True)
    if datasource == "high-low":
        highlow = climetlab.load_dataset("high-low")
        for field, label in highlow.fields():
            climetlab.plot_map(field, width=256, title=highlow.title(label))
        (x_train, y_train, f_train), (x_test, y_test, f_test) = highlow.load_data(test_size=0.3, fields=True)
        model = Sequential()
        model.add(Input(shape=x_train[0].shape))
        model.add(Flatten())
        model.add(Dense(64, activation="sigmoid"))
        model.add(Dense(4, activation="softmax"))
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        print(model.summary())
        h = model.fit(x_train, y_train, epochs=100, verbose=0)
        model.evaluate(x_test, y_test)
        predicted = model.predict(x_test)
        for p, f in zip(predicted, f_test):
            climetlab.plot_map(f, width=256, title=highlow.title(p))
    if datasource == "ecmwf-mars":
        source=climetlab.load_source("mars", param=["2t", "msl"], levtype="sfc", area=[50, -50, 20, 50], grid=[1, 1], date=date)
        for s in source:
             climetlab.plot_map(s)
        return source
    if datasource == "noaa-hurricane":
        hurricanedata = climetlab.load_dataset("hurricane-database",bassin="atlantic")
        hurricanedf=hurricanedata.to_pandas()
        print("HURDAT2 Hurricane Pandas Dataframe:",hurricanedf)
        climetlab.plot_map(hurricanedf)
        return hurricanedf
    if datasource == "ecmwf-copernicus-era5":
        source = climetlab.load_source("cds", "reanalysis-era5-single-levels", variable=["2t", "msl"], product_type="reanalysis", area=[50, -50, 20, 50], date=date, time=time)
        for s in source:
            climetlab.plot_map(s)
        return source

def weather_forecast(location=None,longitude=None,latitude=None):
    owm = OWM('8d44d36bbc4d944fee0b5af20ea9be95')
    mgr = owm.weather_manager()

    if location is not None:
        observation = mgr.weather_at_place(location)
        w = observation.weather
        print(location + " - Detailed status:",w.detailed_status)         # 'clouds'
        print(location + " - Wind:",w.wind())                  # {'speed': 4.6, 'deg': 330}
        print(location + " - Humidity:",w.humidity)                # 87
        print(location + " - Temperature:",w.temperature('celsius'))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        print(location + " - Rain:",w.rain)                    # {}
        print(location + " - Heat index:",w.heat_index)              # None
        print(location + " - Clouds:",w.clouds)                  # 75
        print("===========================================")
    else:
        one_call = mgr.one_call(latitude, longitude)
        for n in range(7):
            print(str((latitude,longitude)) + " - Detailed status - Forecast - Day ",n,":",one_call.forecast_daily[n].detailed_status)
            print(str((latitude,longitude)) + " - Humidity - Forecast - Day ",n,":",one_call.forecast_daily[n].humidity)
            print(str((latitude,longitude)) + " - Precipitation probability - Forecast - Day ",n,":",one_call.forecast_daily[n].precipitation_probability)
            print(str((latitude,longitude)) + " - Rain - Forecast - Day ",n,":",one_call.forecast_daily[n].rain)
            print(str((latitude,longitude)) + " - Temperature - Forecast - Day ",n,":",one_call.forecast_daily[n].temp)
            print(str((latitude,longitude)) + " - Clouds - Forecast - Day ",n,":",one_call.forecast_daily[n].clouds)
            print("===========================================")

def weather_GIS_analytics(image,segment,phenomenon="Cloud"):
    print(("Image:",image))
    invimg=invert_image(image)
    img=cv2.imread(image)
    WeatherPhenomenonAreas=[]
    print((phenomenon + " Segment:",segment))
    print((phenomenon + " Contours:",len(segment[7][0])))
    fig1 = plt.figure(dpi=100)
    cityid=0
    for n in range(len(segment[7][0]) - 1):
        circumference = cv2.arcLength(segment[7][0][n],True)
        convexhull = cv2.convexHull(segment[7][0][n])
        contourarea = cv2.contourArea(segment[7][0][n])
        cv2.drawContours(img,segment[7][0][n],-1,(0,255,0),2)
        x,y,w,h = cv2.boundingRect(segment[7][0][n])
        print(("Circumference of " + phenomenon + ":",circumference))
        radius = circumference/6.28
        circulararea=3.14*radius*radius
        print(("Approximate circular area of " + phenomenon + ":", circulararea))
        print(("Contour Area of " + phenomenon + ":", contourarea))
        cv2.putText(img,str(cityid),(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        WeatherPhenomenonAreas.append((contourarea,cityid,circulararea,convexhull,circumference))
        curve = convexhull 
        xaxis = []
        yaxis = []
        for point in curve:
            xaxis.append(point[0][0])
            yaxis.append(point[0][1])
        ax = fig1.add_subplot(111)
        ax.plot(xaxis, yaxis, rasterized=True)
        cityid += 1
    plt.show()
    imagetok1=image.split(".")
    imagetok2=imagetok1[0].split("/")
    cv2.imwrite("testlogs/"+imagetok2[1]+"-contourlabelled.jpg",img)
    cv2.imwrite("testlogs/"+imagetok2[1]+"-inverted.jpg",invimg)
    cv2.waitKey()
    return (WeatherPhenomenonAreas)


if __name__ == "__main__":
    #weather_forecast("Chennai")
    #weather_forecast(longitude=80.2707,latitude=13.0827)
    #climate_analytics("ecmwf-copernicus-era5",date="2021-11-29",time="12:00")
    #climate_analytics("ecmwf-mars",date="2021-11-29")
    #climate_analytics("high-low")
    #climate_analytics("noaa-hurricane")
    #datesofhurricanes=[(2004,9,13,1,00,00),(2004,11,29,1,00,00),(2005,8,23,1,00,00),(2005,10,1,1,00,00),(2006,11,25,1,00,00),(2007,11,11,1,00,00),(2008,4,27,1,00,00),(2008,6,17,1,00,00),(2011,12,13,1,00,00),(2012,11,25,1,00,00),(2013,11,3,1,00,00),(2004,9,13,1,00,00),(2017,9,16,1,00,00),(2019,3,4,1,00,00)]
    #North Atlantic Hurricanes - Harvey, Irma, Ian and Bay of Bengal Very Severe Cyclonic Storms - Amphan,Gaja,Varda,Thane,Ockhi
    datesofstorms=[(2017,8,17,1,00,00),(2017,8,30,1,00,00),(2022,9,23,1,00,00),(2020,5,20,1,00,00),(2018,11,10,1,00,00),(2016,12,6,1,00,00),(2011,12,25,1,00,00),(2017,11,29,1,00,00)]
    climate_analytics(datasource="n-body-analytics",date=datesofstorms)
    #seg3=image_segmentation("testlogs/Windy_WeatherGIS_2021-11-11-13-07-51.jpg")
    #weather_GIS_analytics("testlogs/Windy_WeatherGIS_2021-11-11-13-07-51.jpg",seg3)
    #gisstream=Streaming_AbstractGenerator.StreamAbsGen("MongoDB","GISAndVisualStreaming","bucket1")
    #for imgmdb in gisstream: 
    #    #imgbase64 = codecs.encode(imgmdb.read(),"base64")
    #    #imgstr = imgbase64.decode("utf-8")
    #    imgdata = imgmdb.read()
    #    #print("GIS img bytes:",imgdata)
    #    pilimg = Image.open(io.BytesIO(imgdata))
    #    pilimg.save("testlogs/GISAndVisualStreamNoSQLStore.jpg")
    #    seg=image_segmentation("testlogs/GISAndVisualStreamNoSQLStore.jpg")
    #    weather_GIS_analytics("testlogs/GISAndVisualStreamNoSQLStore.jpg",seg)
