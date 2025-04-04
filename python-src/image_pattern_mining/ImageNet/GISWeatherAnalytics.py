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
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

import cv2
#from keras.applications import ResNet50
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
#from keras import backend
#from keras.applications.imagenet_utils import preprocess_input
#from keras.applications.imagenet_utils import decode_predictions
#from keras.preprocessing import image
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
from EphemerisSearch import predict_EWE 
from MultiFractals import precipitation_mfdfa_model
import itertools
import json
from sklearn.mixture import GaussianMixture
from scipy.signal import find_peaks
from sympy import partition
from sympy.combinatorics.partitions import IntegerPartition
from scipy.linalg import norm
import math
import xarray as xr
import matplotlib.pyplot as plt
import s3fs
from astropy.time import Time

def pressure_gradient(variablegravities=[],seasurfacelonglat=None,datefrom=None,dateto=None):
    date=Time(str(datefrom[0])+"-"+str(datefrom[1])+"-"+str(datefrom[2]) + " " + str(datefrom[3]) + ":" + str(datefrom[4]) + ":" + str(datefrom[5]))
    todate=Time(str(dateto[0])+"-"+str(dateto[1])+"-"+str(dateto[2]) + " " + str(datefrom[3]) + ":" + str(datefrom[4]) + ":" + str(datefrom[5]))
    pressuregradients=[]
    cnt=0
    while date != todate:
        s3 = s3fs.S3FileSystem(anon=True)
        store = s3fs.S3Map(root="s3://surftemp-sst/data/sst.zarr", s3=s3, create=False)
        sst_ds = xr.open_zarr(store)
        print("date:",date.value)
        print(dir(date))
        timetoks=date.value.split(" ")
        sst = sst_ds["analysed_sst"].sel(time=timetoks[0], lat=slice(seasurfacelonglat[1],seasurfacelonglat[1]+1),lon=slice(seasurfacelonglat[0],seasurfacelonglat[0]+1))
        print("sst:",sst)
        sstdict=sst.to_dict()
        print("sstdict keys:",sstdict.keys())
        print("sstdict values:",sstdict.values())
        for sstdata in sstdict["data"][0][0]: 
            pressuregradient = sstdata * variablegravities[cnt]
            print("pressure gradient on date " + str(date) + ":",pressuregradient)
            pressuregradients.append(pressuregradient)
        cnt += 1
        date += 1
    print("pressure gradients:",pressuregradients)

def barometric_pressure(sealevelpressure=29.92,mass=28.95,variablegravities=[],height=100,boltzmannconstant=1.380649,temperature=35):
    pressures=[]
    for gravity in variablegravities:
        pressureatheight = sealevelpressure*math.exp(-1 * (mass*gravity*height)/(boltzmannconstant*temperature))
        print("Sea Level Pressure:",sealevelpressure)
        print("Mass of air molecule:",mass)
        print("Variable N-Body model gravity:",gravity)
        print("Height from sea level:",height)
        print("Boltzmann constant:",boltzmannconstant)
        print("Temperature:",temperature)
        pressures.append(pressureatheight)
    return pressures

def invert_image(image):
    img=cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    invimg=cv2.bitwise_not(thresh)
    return invimg

def gaussian_ensemble_forecast_rainfall_timeseries(predEWEparams=None,days=5,forecast_seasonal_rainfall=20,historic_training_timeseries=None,maxiterations=100):
    maxgravitynorm=0
    ratelimiterror=True
    maxgravitypartition=[]
    iterations=0
    p = IntegerPartition([forecast_seasonal_rainfall])
    partition_number=partition(forecast_seasonal_rainfall)
    print(days," day Gaussian Ensemble Forecast:")
    print("-------------------------------------")
    for n in range(partition_number):
        candidate_partition=p.next_lex()
        print("gaussian_ensemble_forecast_rainfall_timeseries(): candidate rainfall timeseries forecast partition = ",candidate_partition)
        candidate_partition_dict=candidate_partition.as_dict()
        print("gaussian_ensemble_forecast_rainfall_timeseries(): length of candidate rainfall timeseries forecast partition = ",sum(candidate_partition_dict.values()))
        if sum(candidate_partition_dict.values()) == days:
             while ratelimiterror is True:
                try:
                     gmm_gravities=climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params=predEWEparams,precipitation_timeseries={"timeseries":historic_training_timeseries,"averageseasonalrainfall":forecast_seasonal_rainfall,'forecast_timeseries':candidate_partition_dict.values()})
                     ratelimiterror=False
                except Exception as e:
                     ratelimiterror=True
                     print("JPL Horizons Rate limit error....retrying:",e)
             print("gaussian_ensemble_forecast_rainfall_timeseries(): rainfall forecast timeseries ferrers:")
             print(candidate_partition.as_ferrers())
             for gmm_gravity in gmm_gravities:
                gmm_gravity_l2_norm1=norm(gmm_gravity[0])
                gmm_gravity_l2_norm2=norm(gmm_gravity[1])
                if gmm_gravity_l2_norm1 > maxgravitynorm:
                    maxgravitynorm=gmm_gravity_l2_norm1
                    maxgravitypartition=candidate_partition
                if gmm_gravity_l2_norm2 > maxgravitynorm:
                    maxgravitynorm=gmm_gravity_l2_norm2
                    maxgravitypartition=candidate_partition
        p = candidate_partition
        if iterations > maxiterations:
            break
        iterations += 1
    print("gaussian_ensemble_forecast_rainfall_timeseries(): Maximum probability rainfall timeseries = ",maxgravitypartition)

def climate_analytics(datasource,date="",time="",predict_EWE_params=None,precipitation_timeseries=None,computepressuregradient=False):
    if datasource == "precipitation_GaussianMixture":
        if precipitation_timeseries is not None:
            precipitation_timeseries_2D=list(zip(list(range(len(precipitation_timeseries["timeseries"]))),precipitation_timeseries["timeseries"]))
            precipitation_timeseries_forecast_2D=list(zip(list(range(len(precipitation_timeseries["forecast_timeseries"]))),precipitation_timeseries["forecast_timeseries"]))
            print("climate_analytics(): precipitation_timeseries_2D = ",precipitation_timeseries_2D)
        if predict_EWE_params is not None:
            print("climate_analytics(): N-Body conjunction to be searched pairwise:",predict_EWE_params['bodyconjunctions'])
            bodies=predict_EWE_params['bodyconjunctions'].split("-")
            bodypairs=itertools.combinations(bodies,2)
            bodypair_predict=[]
            for bp in bodypairs:
                gravityl2norms=predict_EWE(datefrom=predict_EWE_params['datefrom'],dateto=predict_EWE_params['dateto'],loc=predict_EWE_params['loc'],bodypair="-".join(bp),angularsepbounds=predict_EWE_params['angularsepbounds'],userdefinedlatlons=predict_EWE_params['longlat'])
                pressures0=barometric_pressure(variablegravities=gravityl2norms[0])
                pressures1=barometric_pressure(variablegravities=gravityl2norms[1])
                print("Barometric pressures for bodypair ",bp," in the daterange :",(pressures0,pressures1))
                plt.plot(pressures0,label="Barometric pressure - " + bp[0])
                plt.plot(pressures1,label="Barometric pressure - " + bp[1])
                plt.legend()
                plt.show()
                if computepressuregradient:
                    pressuregradient0=pressure_gradient(variablegravities=gravityl2norms[0],seasurfacelonglat=predict_EWE_params['seasurfacelonglat'],datefrom=predict_EWE_params["datefrom"],dateto=predict_EWE_params["dateto"])
                    pressuregradient1=pressure_gradient(variablegravities=gravityl2norms[1],seasurfacelonglat=predict_EWE_params['seasurfacelonglat'],datefrom=predict_EWE_params["datefrom"],dateto=predict_EWE_params["dateto"])
                #fig.savefig("testlogs/GISWeatherAnalytics.BarometricPressure."+str(predict_EWE_params['datefrom'][0])+"-"+str(predict_EWE_params['datefrom'][1]) + "-" + str(predict_EWE_params['datefrom'][2]) + "#"+str(predict_EWE_params['dateto'][0])+ "-" + str(predict_EWE_params['dateto'][1]) + "-" + str(predict_EWE_params['dateto'][2])+".jpg")
                modes_body1=find_peaks(gravityl2norms[0])
                modes_body2=find_peaks(gravityl2norms[1])
                no_of_modes_body1=len(modes_body1)
                no_of_modes_body2=len(modes_body2)
                modes_trainingdata=find_peaks(precipitation_timeseries['timeseries'])
                gmm_fit = GaussianMixture(n_components=len(modes_trainingdata),random_state=0).fit(precipitation_timeseries_2D)
                print("climate_analytics(): GMM mean fit from training timeseries:",gmm_fit.means_)
                gmm_predict_body1_fit = GaussianMixture(n_components=no_of_modes_body1,random_state=0,means_init=gmm_fit.means_).fit(precipitation_timeseries_2D)
                gmm_predict_body1_predict = gmm_predict_body1_fit.predict_proba(precipitation_timeseries_forecast_2D)
                gmm_predict_body2_fit = GaussianMixture(n_components=no_of_modes_body2,random_state=0,means_init=gmm_fit.means_).fit(precipitation_timeseries_2D)
                gmm_predict_body2_predict = gmm_predict_body2_fit.predict_proba(precipitation_timeseries_forecast_2D)
                print("climate_analytics(): number of N-Body gravity peaks (modes of predicted GMM for average seasonal rainfall ",precipitation_timeseries['averageseasonalrainfall'],") for bodypair ",bp," for daterange ",predict_EWE_params['datefrom'],"-",predict_EWE_params['dateto'],":",(no_of_modes_body1,no_of_modes_body2)) 
                print("climate_analytics(): GMM probabilities of user supplied Forecast rainfall timeseries for bodypair ",bp," for daterange ",predict_EWE_params['datefrom'],"-",predict_EWE_params['dateto'],":",gmm_predict_body1_predict) 
                print("climate_analytics(): GMM probabilities of user supplied Forecast rainfall timeseries for bodypair ",bp," for daterange ",predict_EWE_params['datefrom'],"-",predict_EWE_params['dateto'],":",gmm_predict_body2_predict) 
                bodypair_predict.append((gmm_predict_body1_predict,gmm_predict_body2_predict))
            return bodypair_predict
    if datasource == "precipitation_MFDFA":
        if precipitation_timeseries is not None:
            precipitation_mfdfa_model(precipitation_timeseries,order=2)
    if datasource == "n-body-analytics":
        ephem=EphemerisSearch("de421.bsp")
        if date != "" and time != "":
            ephem.extreme_weather_events_n_body_analytics(datesofEWEs=date,angularsep=True)
        if predict_EWE_params is not None:
            print("climate_analytics(): N-Body conjunction to be searched pairwise:",predict_EWE_params['bodyconjunctions'])
            bodies=predict_EWE_params['bodyconjunctions'].split("-")
            bodypairs=itertools.combinations(bodies,2)
            for bp in bodypairs:
                predict_EWE(datefrom=predict_EWE_params['datefrom'],dateto=predict_EWE_params['dateto'],loc=predict_EWE_params['loc'],bodypair="-".join(bp),angularsepbounds=predict_EWE_params['angularsepbounds'])
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

def sequence_mining_CAR_search(carjsonfile,pEWEparams,support=10.0,maxiterations=5):
    solar_system_bodies={"Sun":10,"Moon":301,"Mars":499,"Mercury":199,"Jupiter":599,"Venus":299,"Saturn":699,"Uranus":799,"Neptune":899,"Pluto":999}
    carf=open(carjsonfile)
    cars=json.load(carf)
    iterations=0
    for car,freq in cars.items():
        cartoks=car.split("-")
        cardiff=set.difference(set(cartoks),set(solar_system_bodies.keys()))
        if len(cartoks) > 1 and len(cardiff) == 0 and freq > support and iterations < maxiterations:
            print("CAR:",car)
            climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':pEWEparams["datefrom"],'dateto':pEWEparams["dateto"],'loc':pEWEparams['loc'],'bodyconjunctions':car,'angularsepbounds':pEWEparams['angularsepbounds']})
            iterations += 1

if __name__ == "__main__":
    #weather_forecast("Chennai")
    #weather_forecast(longitude=80.2707,latitude=13.0827)
    #climate_analytics("ecmwf-copernicus-era5",date="2021-11-29",time="12:00")
    #climate_analytics("ecmwf-mars",date="2021-11-29")
    #climate_analytics("high-low")
    #climate_analytics("noaa-hurricane")
    #datesofhurricanes=[(2004,9,13,1,00,00),(2004,11,29,1,00,00),(2005,8,23,1,00,00),(2005,10,1,1,00,00),(2006,11,25,1,00,00),(2007,11,11,1,00,00),(2008,4,27,1,00,00),(2008,6,17,1,00,00),(2011,12,13,1,00,00),(2012,11,25,1,00,00),(2013,11,3,1,00,00),(2004,9,13,1,00,00),(2017,9,16,1,00,00),(2019,3,4,1,00,00)]
    #North Atlantic Hurricanes - Harvey, Irma, Ian and Bay of Bengal Very Severe Cyclonic Storms - Amphan,Gaja,Varda,Thane,Ockhi
    #datesofstorms=[(2017,8,17,1,00,00),(2017,8,30,1,00,00),(2022,9,23,1,00,00),(2020,5,20,1,00,00),(2018,11,10,1,00,00),(2016,12,6,1,00,00),(2011,12,25,1,00,00),(2017,11,29,1,00,00)]
    #climate_analytics(datasource="n-body-analytics",date=datesofstorms)
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,10,21,17,30,00),'dateto':(2022,12,15,17,30,00),'loc':'@0','bodypair':"Venus-Mercury",'angularsepbounds':('0d','10d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,10,21,17,30,00),'dateto':(2022,12,15,17,30,00),'loc':'@0','bodypair':"Sun-Moon",'angularsepbounds':('120d','180d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,22,17,30,00),'dateto':(2022,12,31,17,30,00),'loc':'@0','bodypair':"Venus-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,22,17,30,00),'dateto':(2022,12,31,17,30,00),'loc':'@0','bodypair':"Mercury-Jupiter",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,22,17,30,00),'dateto':(2022,12,31,17,30,00),'loc':'@0','bodypair':"Jupiter-Venus",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,12,8,17,30,00),'dateto':(2022,12,27,17,30,00),'loc':'@0','bodypair':"Venus-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,12,8,17,30,00),'dateto':(2022,12,27,17,30,00),'loc':'@0','bodypair':"Mercury-Jupiter",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,12,8,17,30,00),'dateto':(2022,12,27,17,30,00),'loc':'@0','bodypair':"Jupiter-Venus",'angularsepbounds':('0d','30d')})

    #sequence_mining_CAR_search("../../MinedClassAssociationRules.json",pEWEparams={'datefrom':(2022,12,8,17,30,00),'dateto':(2022,12,27,17,30,00),'loc':'@0','angularsepbounds':('0d','30d')},maxiterations=5)
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,28,17,30,00),'dateto':(2022,12,8,17,30,00),'loc':'@0','bodyconjunctions':"Venus-Sun-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,28,17,30,00),'dateto':(2022,12,8,17,30,00),'loc':'@0','bodyconjunctions':"Venus-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,28,17,30,00),'dateto':(2022,12,8,17,30,00),'loc':'@0','bodyconjunctions':"Mercury-Jupiter",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,28,17,30,00),'dateto':(2022,12,8,17,30,00),'loc':'@0','bodyconjunctions':"Jupiter-Venus",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2022,11,28,17,30,00),'dateto':(2022,12,8,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Moon",'angularsepbounds':('0d','30d')})

    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2023,1,31,17,30,00),'dateto':(2023,2,10,17,30,00),'loc':'@0','bodyconjunctions':"Jupiter-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2023,1,31,17,30,00),'dateto':(2023,2,10,17,30,00),'loc':'@0','bodyconjunctions':"Venus-Sun-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2023,1,31,17,30,00),'dateto':(2023,2,10,17,30,00),'loc':'@0','bodyconjunctions':"Jupiter-Venus",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2023,1,31,17,30,00),'dateto':(2023,2,10,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Saturn-Mercury",'angularsepbounds':('0d','30d')})
    #climate_analytics(datasource="n-body-analytics",predict_EWE_params={'datefrom':(2023,9,5,17,30,00),'dateto':(2023,9,13,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mars-Mercury-Venus-Saturn",'angularsepbounds':('0d','180d')})

    nem_rainfall_timeseries=[2,1,3,1,4,2,1,8,21,10,6,4,8,16,9,14,8,6,10,16,5,2,1,1,1,1,3,4,2,4,14,18,10,10,5,8,2,4]
    #climate_analytics(datasource="precipitation_MFDFA",precipitation_timeseries=nem_rainfall_timeseries)
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2023,11,21,17,30,00),'dateto':(2024,1,8,17,30,00),'loc':'@0','bodyconjunctions':"Mercury-Jupiter",'angularsepbounds':('0d','60d')},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2023,11,21,17,30,00),'dateto':(2024,1,8,17,30,00),'loc':'@0','bodyconjunctions':"Mercury-Mars",'angularsepbounds':('0d','60d')},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,3,25,17,30,00),'dateto':(2024,4,30,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','60d')},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,5,5,17,30,00),'dateto':(2024,6,10,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d')},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,7,2,17,30,00),'dateto':(2024,8,10,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':[{'lon':78.7,'lat':10.56,'elevation':0.0}]},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})

    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,7,2,17,30,00),'dateto':(2024,8,10,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['568@399']},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,9,1,17,30,00),'dateto':(2024,10,31,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['223@399']},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2024,11,1,17,30,00),'dateto':(2024,12,31,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['223@399']},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2016,12,5,17,30,00),'dateto':(2016,12,7,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['223@399'],'seasurfacelonglat':(95,12)},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2011,12,24,17,30,00),'dateto':(2011,12,26,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['223@399'],'seasurfacelonglat':(95,12)},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]},computepressuregradient=True)
    climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2025,2,25,17,30,00),'dateto':(2025,4,30,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Mercury-Venus",'angularsepbounds':('0d','30d'),'longlat':['223@399'],'seasurfacelonglat':(95,12)},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]},computepressuregradient=False)
    #climate_analytics(datasource="precipitation_GaussianMixture",predict_EWE_params={'datefrom':(2023,11,21,17,30,00),'dateto':(2024,1,8,17,30,00),'loc':'@0','bodyconjunctions':"Sun-Moon",'angularsepbounds':('0d','60d')},precipitation_timeseries={"timeseries":nem_rainfall_timeseries,"averageseasonalrainfall":100,'forecast_timeseries':[10,2,12,25,30,1,2,3,4,10]})
    #gaussian_ensemble_forecast_rainfall_timeseries(predEWEparams={'datefrom':(2023,9,1,17,30,00),'dateto':(2023,12,1,17,30,00),'loc':'@0','bodyconjunctions':"Mercury-Jupiter",'angularsepbounds':('0d','30d')},days=5,forecast_seasonal_rainfall=10,historic_training_timeseries=nem_rainfall_timeseries)
    #gaussian_ensemble_forecast_rainfall_timeseries(predEWEparams={'datefrom':(2023,12,2,17,30,00),'dateto':(2024,1,8,17,30,00),'loc':'@0','bodyconjunctions':"Venus-Mercury-Sun-Jupiter",'angularsepbounds':('0d','30d')},days=5,forecast_seasonal_rainfall=35,historic_training_timeseries=nem_rainfall_timeseries)
    #gaussian_ensemble_forecast_rainfall_timeseries(predEWEparams={'datefrom':(2023,11,21,17,30,00),'dateto':(2024,1,8,17,30,00),'loc':'@0','bodyconjunctions':"Mars-Venus-Mercury-Sun-Jupiter",'angularsepbounds':('0d','60d')},days=5,forecast_seasonal_rainfall=35,historic_training_timeseries=nem_rainfall_timeseries)
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
