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

from skyfield.api import load
from skyfield.searchlib import find_discrete
import os
import subprocess
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
from collections import defaultdict
import pprint
from astroquery.esa.hubble import ESAHubble
from PIL import Image
from astropy.io import fits
import numpy as np
from astroquery.jplhorizons import Horizons
import numpy as np
import scipy as sp
import time
import scipy.constants as cs
import matplotlib.pyplot as plt
from numba import jit
from numba import cuda
from mpl_toolkits.mplot3d import Axes3D
from astropy.time import Time
from skimage import data
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from skimage.morphology import convex_hull_image
from skimage import measure
from scipy.spatial.distance import directed_hausdorff


planetradecdict={}
planets=[]
ts=[]

def latlon_match(datetime):
    global planets
    print("===============================SKYFIELD========================================================")
    print("latlon_match(): datetime:",datetime.tt_strftime())
    print("latlon_match(): planetradecdict:",planetradecdict)
    earth=planets["earth"].at(datetime)
    sun=earth.observe(planets["sun"]).apparent().ecliptic_latlon()
    print("latlon_match(): sun:",sun)
    moon=earth.observe(planets["moon"]).apparent().ecliptic_latlon()
    print("latlon_match(): moon:",moon)
    mars=earth.observe(planets["mars"]).apparent().ecliptic_latlon()
    print("latlon_match(): mars:",mars)
    mercury=earth.observe(planets["mercury"]).apparent().ecliptic_latlon()
    print("latlon_match(): mercury:",mercury)
    jupiter=earth.observe(planets["jupiter barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): jupiter:",jupiter)
    venus=earth.observe(planets["venus barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): venus:",venus)
    saturn=earth.observe(planets["saturn barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): saturn:",saturn)
    uranus=earth.observe(planets["uranus barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): uranus:",uranus)
    neptune=earth.observe(planets["neptune barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): neptune:",neptune)
    pluto=earth.observe(planets["pluto barycenter"]).apparent().ecliptic_latlon()
    print("latlon_match(): pluto:",pluto)
    positions={"Sun":earth.observe(planets["sun"]),"Moon":earth.observe(planets["moon"]),"Mars":earth.observe(planets["mars"]),"Mercury":earth.observe(planets["mercury"]),"Jupiter":earth.observe(planets["jupiter barycenter"]),"Venus":earth.observe(planets["venus barycenter"]),"Saturn":earth.observe(planets["saturn barycenter"]),"Uranus":earth.observe(planets["uranus barycenter"]),"Neptune":earth.observe(planets["neptune barycenter"]),"Pluto":earth.observe(planets["pluto barycenter"])}
    for k1,v1 in positions.items():
        for k2,v2 in positions.items():
            if k1 != k2:
                print("Angular separation between ",k1," and ",k2,":",v1.separation_from(v2))
    print("===============================SKYFIELD========================================================")
    if str(sun) != str(planetradecdict["sun"]):
           return False
    if str(moon) != str(planetradecdict["moon"]):
           return False
    if str(mars) != str(planetradecdict["mars"]):
           return False
    if str(mercury) != str(planetradecdict["mercury"]):
           return False
    if str(jupiter) != str(planetradecdict["jupiter barycenter"]):
           return False
    if str(venus) != str(planetradecdict["venus barycenter"]):
           return False
    if str(saturn) != str(planetradecdict["saturn barycenter"]):
           return False
    if str(uranus) != str(planetradecdict["uranus barycenter"]):
           return False
    if str(neptune) != str(planetradecdict["neptune barycenter"]):
           return False
    if str(pluto) != str(planetradecdict["pluto barycenter"]):
           return False
    print("latlon_match(): FOUND MATCHING DATE AND TIME = ",datetime.tt_strftime())
    return True

def jplhorizons_ephemeris(body_id,location,epochs):
    horizons=Horizons(body_id,location,epochs)
    ephem=horizons.ephemerides()
    print("jplhorizons_ephemeris(): ephem for ",body_id," at ",location," for date(s) ",epochs)
    print("=================================")
    print(ephem)

def astropy_ephemeris(datetime):
    print("===============================ASTROPY=========================================================")
    print(datetime.tt_strftime())
    t=Time(datetime.tt_strftime()[:-3])
    loc = EarthLocation.of_site('greenwich')
    with solar_system_ephemeris.set('builtin'):
         earth = get_body('earth', t, loc)
         print("astropy - earth:",earth)
         sun = get_body('sun', t, loc)
         print("astropy - sun:",sun)
         moon = get_body('moon', t, loc)
         print("astropy - moon:",sun)
         mars = get_body('mars', t, loc)
         print("astropy - mars:",mars)
         mercury = get_body('mercury', t, loc)
         print("astropy - mercury:",mercury)
         jupiter = get_body('jupiter', t, loc)
         print("astropy - jupiter:",jupiter)
         venus = get_body('venus', t, loc)
         print("astropy - venus:",venus)
         saturn = get_body('saturn', t, loc)
         print("astropy - saturn:",saturn)
         uranus = get_body('uranus', t, loc)
         print("astropy - uranus:",uranus)
         neptune = get_body('neptune', t, loc)
         print("astropy - neptune:",neptune)
         earthmoon = get_body('earth-moon-barycenter',t,loc)
         print("astropy - earthmoon:",earthmoon)
    print("===============================ASTROPY=========================================================")

def radec_match(datetime):
    global planets
    print("radec_match(): datetime:",datetime.tt_strftime())
    print("radec_match(): planetradecdict:",planetradecdict)
    earth=planets["earth"].at(datetime)
    sun=earth.observe(planets["sun"]).radec()
    print("radec_match(): sun:",sun)
    moon=earth.observe(planets["moon"]).radec()
    print("radec_match(): moon:",moon)
    mars=earth.observe(planets["mars"]).radec()
    print("radec_match(): mars:",mars)
    mercury=earth.observe(planets["mercury"]).radec()
    print("radec_match(): mercury:",mercury)
    jupiter=earth.observe(planets["jupiter barycenter"]).radec()
    print("radec_match(): jupiter:",jupiter)
    venus=earth.observe(planets["venus barycenter"]).radec()
    print("radec_match(): venus:",venus)
    saturn=earth.observe(planets["saturn barycenter"]).radec()
    print("radec_match(): saturn:",saturn)
    uranus=earth.observe(planets["uranus barycenter"]).radec()
    print("radec_match(): uranus:",uranus)
    neptune=earth.observe(planets["neptune barycenter"]).radec()
    print("radec_match(): neptune:",neptune)
    pluto=earth.observe(planets["pluto barycenter"]).radec()
    print("radec_match(): pluto:",pluto)
    if str(sun) != str(planetradecdict["sun"]):
           return False
    if str(moon) != str(planetradecdict["moon"]):
           return False
    if str(mars) != str(planetradecdict["mars"]):
           return False
    if str(mercury) != str(planetradecdict["mercury"]):
           return False
    if str(jupiter) != str(planetradecdict["jupiter barycenter"]):
           return False
    if str(venus) != str(planetradecdict["venus barycenter"]):
           return False
    if str(saturn) != str(planetradecdict["saturn barycenter"]):
           return False
    if str(uranus) != str(planetradecdict["uranus barycenter"]):
           return False
    if str(neptune) != str(planetradecdict["neptune barycenter"]):
           return False
    if str(pluto) != str(planetradecdict["pluto barycenter"]):
           return False
    return True


class EphemerisSearch(object):
    def __init__(self,ephemeris):
        global planets
        global ts
        self.ephemeris = ephemeris
        ts = load.timescale()
        print("__init__():timescale now:",ts.now())
        planets = load(ephemeris)

    def astronomical_event_to_search(self,planetradecdict):
        planetradecdict = planetradecdict

    def planetarium_search(self,datetime1,datetime2,find_discrete=False,step_days=1,position="latlon"):
        global planets
        global ts
        earth=planets["earth"]
        datetimeutc1=ts.utc(datetime1[0],datetime1[1],datetime1[2],datetime1[3],datetime1[4],datetime1[5])
        datetimeutc2=ts.utc(datetime2[0],datetime2[1],datetime2[2],datetime2[3],datetime2[4],datetime2[5])
        if find_discrete:
            degree_match.step_days = step_days 
            founddatetime,values = find_discrete(datetimeutc1,datetimeutc2,radec_match)
            print("planetarium_search(): FOUND MATCHING DATE AND TIME = ",(founddatetime,values))
            print("=================================================================")
            print("Maitreya 8t Ephemeris for datetime:",datetime.tt_strftime())
            subprocess.call(["maitreya8t","--date=\""+ datetime.tt_strftime() + "\"", "--astronomical"],shell=False)
            print("=================================================================")
        else:
            try:
                datetime=datetimeutc1
                while datetime.tt_strftime() != datetimeutc2.tt_strftime():
                     print("=================================================================")
                     print("SkyField,AstroPy,Maitreya 8t Ephemeris are compared for datetime:",datetime.tt_strftime())
                     print("=================================================================")
                     if position=="latlon":
                        print("planetarium_search(): datetime to search for latlon_match() = ",datetime.tt_strftime())
                        if latlon_match(datetime):
                           print("planetarium_search(): FOUND MATCHING DATE AND TIME = ",datetime.tt_strftime())
                           break
                     if position=="radec_match":
                        print("planetarium_search(): datetime to search for radec_match() = ",datetime.tt_strftime())
                        if radec_match(datetime):
                           print("planetarium_search(): FOUND MATCHING DATE AND TIME = ",datetime.tt_strftime())
                           break
                     datetime += step_days 
                     astropy_ephemeris(datetime)
                     print("===============================MAITREYA8T==============================================")
                     subprocess.call(["maitreya8t","--date=\""+ datetime.tt_strftime() + "\"", "--astronomical"],shell=False)
                     print("===============================MAITREYA8T==============================================")
            except Exception as ex:
                print("Exception:",ex)
        
    def sky_on_datetime(self,datetime=None,observedfrom="earth",observed="sun",position="latlon",jplhorizons=False,jplhorizonsdata=None):
        global planets
        if jplhorizons:
            jplhorizons_ephemeris(jplhorizonsdata[0],jplhorizonsdata[1],jplhorizonsdata[2])
            return
        t=ts.utc(datetime[0],datetime[1],datetime[2],datetime[3],datetime[4],datetime[5])
        planetobservedfrom=planets[observedfrom]
        planetobserved=planets[observed]
        astrometric=planetobservedfrom.at(t).observe(planetobserved)
        if position=="radec": 
            print("sky_on_datetime(): Right Ascension - Declination position of ",observed," from ",observedfrom," on ",datetime," (Year-Month-Day-Hour-Minute-Second):",astrometric.radec())
            return astrometric.radec()
        if position=="latlon":
            print("SkyField - sky_on_datetime(): Long-Lat position of ",observed," from ",observedfrom," on ",datetime," (Year-Month-Day-Hour-Minute-Second):",astrometric.apparent().ecliptic_latlon())
            return astrometric.apparent().ecliptic_latlon()
    
    def extreme_weather_events_n_body_analytics(self,datesofEWEs):
        gravities=[]
        angular_separation=defaultdict(list)
        for date in datesofEWEs:
            date_t=ts.utc(date[0],date[1],date[2],date[3],date[4],date[5])
            earth=planets["earth"].at(date_t)
            positions={"Sun":earth.observe(planets["sun"]),"Moon":earth.observe(planets["moon"]),"Mars":earth.observe(planets["mars"]),"Mercury":earth.observe(planets["mercury"]),"Jupiter":earth.observe(planets["jupiter barycenter"]),"Venus":earth.observe(planets["venus barycenter"]),"Saturn":earth.observe(planets["saturn barycenter"]),"Uranus":earth.observe(planets["uranus barycenter"]),"Neptune":earth.observe(planets["neptune barycenter"]),"Pluto":earth.observe(planets["pluto barycenter"])}
            for k1,v1 in positions.items():
               for k2,v2 in positions.items():
                  if k1 != k2 and v1 != v2:
                     if k1+"-"+k2 not in positions.keys() and k2+"-"+k1 not in positions.keys():
                         #print("Angular separation between ",k1," and ",k2,":",v1.separation_from(v2))
                         angular_separation[k1+"-"+k2].append(v1.separation_from(v2))
        for k3,v3 in angular_separation.items():
            print("Angular separations for ",k3,":",v3)
        AU = 149597870700
        D = 24*60*60
        epsilon = 0.01
        #Get Starting Parameters for Sun-Pluto from Nasa Horizons
        r_list = []
        v_list = []
        m_list = [[1.989e30],[3.285e23],[4.867e24],[5.972e24],[6.39e23],[1.8989e27],[5.683e26],[8.681e25],[1.024e26],[1.309e22]] #Object masses for Sun-Pluto
        solar_system_bodies={"Sun":10,"Moon":301,"Mars":499,"Mercury":199,"Jupiter":599,"Venus":299,"Saturn":699,"Uranus":799,"Neptune":899,"Pluto":999}
        solar_system=["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Uranus","Neptune","Pluto"]
        for date in datesofEWEs:
            print("extreme_weather_events_n_body_analytics(): date:",date)
            for i in solar_system_bodies.values():
                obj = Horizons(id=i, location="@earth-moon", epochs=Time(str(date[0])+"-"+str(date[1])+"-"+str(date[2])).jd, id_type='id').vectors()
                print("extreme_weather_events_n_body_analytics(): Horizons Ephemeris query object for date (body :",i,") = ",obj)
                print("#################################################################")
                r_obj = [obj['x'][0], obj['y'][0], obj['z'][0]]
                v_obj = [obj['vx'][0], obj['vy'][0], obj['vz'][0]]
                r_list.append(r_obj)
                v_list.append(v_obj)
            r_i = np.array(r_list)*AU
            v_i = np.array(v_list)*AU/D
            m_i = np.array(m_list)
            gravity=self.n_body_gravitational_acceleration(r_i,m_i,epsilon)
            for g in range(len(gravity)):
                print("extreme_weather_events_n_body_analytics(): gravity of ",solar_system[g]," at Earth-Moon Barycenter on ",date,":",gravity[g])
            gravities.append(gravity)
            r_list = []
            v_list = []
            print("==============================================================")
            for g1 in gravities:
                for g2 in gravities:
                    dh=directed_hausdorff(g1,g2)
                    print("extreme_weather_events_n_body_analytics(): Pairwise Directed hausdorff Distance of Gravitational Acceleration:",dh)
           

    def n_body_gravitational_acceleration(self,r,m,epsilon):
        G = cs.gravitational_constant
        print("n_body_gravitational_acceleration():r=",r)
        print("n_body_gravitational_acceleration():m=",m)
        # positions r = [x,y,z] for all bodies in the N-Body System
        x = r[:,0:1]
        y = r[:,1:2]
        z = r[:,2:3]
        # matrices that store each pairwise body separation for each [x,y,z] direction: r_j - r_i
        dx = x.T - x
        dy = y.T - y
        dz = z.T - z
        #matrix 1/r^3 for the absolute value of all pairwise body separations together and
        #resulting acceleration components in each [x,y,z] direction
        inv_r3 = (dx**2 + dy**2 + dz**2 + epsilon**2)**(-1.5)
        print("n_body_gravitational_acceleration(): inv_r3.shape = ",len(inv_r3[0]))
        print("n_body_gravitational_acceleration(): m.shape = ",len(m))
        extension = len(inv_r3[0]) - len(m)
        print("n_body_gravitational_acceleration(): extension = ",extension)
        new_m = m
        for e in range(extension):
            new_m = np.append(new_m,[0.0000])
        print("n_body_gravitational_acceleration():inv_r3=",inv_r3)
        print("n_body_gravitational_acceleration(): m.shape after extension = ",len(new_m))
        ax = G * (dx * inv_r3) @ new_m
        ay = G * (dy * inv_r3) @ new_m
        az = G * (dz * inv_r3) @ new_m
        # pack together the three acceleration components
        a = np.hstack((ax,ay,az))
        return a

    def hubble_deep_field_RGB_analytics(self,imagename=None,postcard=False):
        if imagename=="skimage_HXDF":
            channels=["red","green","blue"]
            fig=plt.figure(imagename)
            image = data.hubble_deep_field()[0:500,0:500] 
            for i in range(0,3):
                fig.add_subplot(1,3,i+1)
                plt.imshow(image[:,:,i])
            plt.savefig("testlogs/"+imagename+"Channels.jpg")
            bins=np.arange(256)
            fig = plt.figure(imagename+"Histograms")
            for i in range(0,3):
                fig.add_subplot(1, 3, i+1)
                plt.hist(image[:,:,i].flatten(), bins, histtype = "stepfilled",
                    color="{0}".format(channels[i]))
                plt.ylim([0,18000])
                plt.title("{0}".format(channels[i]))
                plt.grid()
                plt.xlabel("Pixel value")
                plt.ylabel("Pixel count")
            plt.savefig("testlogs/"+imagename+"Histograms.jpg")
            return
        if postcard:
            esahubble = ESAHubble()
            esahubble.get_postcard(image, "RAW", 4096, "testlogs/"+image+".jpg")
        image = Image.open("testlogs/"+imagename+".jpg")
        xsize,ysize = image.size
        r, g, b = image.split()
        rdata = r.getdata()
        gdata = g.getdata()
        bdata = b.getdata()
        print("hubble_deep_field_RGB_analytics(): Red channel data = ",rdata)
        print("hubble_deep_field_RGB_analytics(): Green channel data = ",gdata)
        print("hubble_deep_field_RGB_analytics(): Blue channel data = ",bdata)
        npr = np.reshape(rdata,(ysize,xsize))
        npg = np.reshape(gdata,(ysize,xsize))
        npb = np.reshape(bdata,(ysize,xsize))
        blue_hist = np.histogram(npb.flatten())
        green_hist = np.histogram(npg.flatten())
        red_hist = np.histogram(npr.flatten())
        rgb=[npr,npg,npb]
        blue_white = float(blue_hist[0][len(blue_hist[0]) - 1]) / float(sum(blue_hist[0]))
        green_white = float(green_hist[0][len(green_hist[0]) - 1]) / float(sum(green_hist[0]))
        red_white = float(red_hist[0][len(red_hist[0]) - 1]) / float(sum(red_hist[0]))
        print(("Percentage of Blue Galaxies (Closer) :", blue_white))
        print(("Percentage of Green Galaxies (Closer) :", green_white))
        print(("Percentage of Red Galaxies (Farthest - Red Shift):", red_white))
        channels=["red","green","blue"]
        fig=plt.figure(imagename+"Histograms")
        bins=np.arange(256)
        for i in range(0,3):
            fig.add_subplot(1, 3, i+1)
            plt.hist(rgb[i].flatten(), bins, histtype = "stepfilled",
                    color="{0}".format(channels[i]))
            plt.ylim([0,18000])
            plt.title("{0}".format(channels[i]))
            plt.grid()
            plt.xlabel("Pixel value")
            plt.ylabel("Pixel count")
        plt.savefig("testlogs/"+imagename+"Histograms.jpg")
        red = fits.PrimaryHDU(data=npr)
        red.header["LATOBS"] = "111:11:11"
        red.header["LONGOBS"] = "50:50"
        red.writeto("testlogs/red_"+imagename+".fits")
        green = fits.PrimaryHDU(data=npg)
        green.header["LATOBS"] = "111:11:11"
        green.header["LONGOBS"] = "50:50"
        green.writeto("testlogs/green_"+imagename+".fits")
        blue = fits.PrimaryHDU(data=npb)
        blue.header["LATOBS"] = "111:11:11"
        blue.header["LONGOBS"] = "50:50"
        blue.writeto("testlogs/blue_"+imagename+".fits")
        os.remove("testlogs/red_"+imagename+".fits")
        os.remove("testlogs/green_"+imagename+".fits")
        os.remove("testlogs/blue_"+imagename+".fits")

if __name__=="__main__":
    ephem=EphemerisSearch("de421.bsp")
    #ephem.sky_on_datetime((2022,7,7,1,15,30),"earth","mars")
    #planetradecdict={}
    #planetradecdict["sun"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","sun")
    #planetradecdict["moon"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","moon")
    #planetradecdict["mars"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","mars")
    #planetradecdict["mercury"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","mercury")
    #planetradecdict["jupiter barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","jupiter barycenter")
    #planetradecdict["venus barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","venus barycenter")
    #planetradecdict["saturn barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","saturn barycenter")
    #planetradecdict["uranus barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","uranus barycenter")
    #planetradecdict["neptune barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","neptune barycenter")
    #planetradecdict["pluto barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","pluto barycenter")
    #ephem.astronomical_event_to_search(planetradecdict)
    #ephem.planetarium_search((2016,6,29,1,15,30),(2022,7,6,1,15,30))
    #ephem.planetarium_search((-2016,6,29,1,15,30),(2022,7,6,1,15,30),step_days=100)
    datesofhurricanes=[(2004,9,13,1,00,00),(2004,11,29,1,00,00),(2005,8,23,1,00,00),(2005,10,1,1,00,00),(2006,11,25,1,00,00),(2007,11,11,1,00,00),(2008,4,27,1,00,00),(2008,6,17,1,00,00),(2011,12,13,1,00,00),(2012,11,25,1,00,00),(2013,11,3,1,00,00),(2004,9,13,1,00,00),(2017,9,16,1,00,00),(2019,3,4,1,00,00)]
    datesofearthquakes=[(2011,3,11,5,46,23), (2008,5,12,6,27,59), (2004,12,26,00,58,52), (1999,9,20,17,47,16), (1994,1,17,12,30,54),(1995,1,16,20,46,51),(2009,4,6,1,32,42),(2010,2,27,6,34,13),(1989,10,18,00,4,14),(1992,6,28,11,57,35)]
    print("======================HURRICANES=========================")
    ephem.extreme_weather_events_n_body_analytics(datesofhurricanes)
    print("======================EARTHQUAKES=========================")
    ephem.extreme_weather_events_n_body_analytics(datesofearthquakes)
    ephem.hubble_deep_field_RGB_analytics("HubbleUltraDeepField_heic0611b")
    ephem.hubble_deep_field_RGB_analytics(imagename="skimage_HXDF")
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["10",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["301",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["499",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["199",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["599",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["299",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["699",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["799",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["899",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.sky_on_datetime(jplhorizons=True,jplhorizonsdata=["999",{'lon': 78.07, 'lat': 10.56, 'elevation': 0.093},{'start':'2022-07-01', 'stop':'2022-07-11', 'step':'1d'}])
    #ephem.hubble_deep_field_RGB_analytics("J6FL25S4Q",postcard=True)
