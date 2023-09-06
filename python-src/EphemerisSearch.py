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
import healpy as hp
from astroML.datasets import fetch_wmap_temperatures 
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from scipy.linalg import norm
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia
from astropy.coordinates import angular_separation


planetradecdict={}
planets=[]
ts=[]

def query_space(name,ra,dec,radius=0.0833333):
    query_cone = """SELECT
    TOP 10
    source_id,ra,dec,pmra,pmdec 
    FROM gaiadr2.gaia_source
    WHERE 1=CONTAINS(
      POINT(ra, dec),
      CIRCLE("""+str(ra)+""","""+str(dec)+""",+"""+str(radius)+"""))"""
    query=Gaia.launch_job(query_cone)
    results=query.get_results()
    print("---------------------",name,"------------------")
    print(results)
    return results

def locate_proper_motion_conjunction(queryresults1,queryresults2,duration=10000000,separation=0.01):
    year=0
    for q1 in queryresults1:
        for q2 in queryresults2:
            for y in range(1,duration):
                if q1["source_id"] != q2["source_id"]:
                    angdistance=angular_separation(q1["pmra"]*y,q1["pmdec"]*y,q2["pmra"]*y,q2["pmdec"]*y)
                    if angdistance < separation:
                        print("Angular separation between two bodies ",q1["source_id"]," and ",q2["source_id"]," in ",y," years:",angdistance)

def predict_EWE(datefrom,dateto,loc,bodypair,angularsepbounds):
    ephem=EphemerisSearch("de421.bsp")
    range_gravities={}
    solar_system_bodies={"Sun":10,"Moon":301,"Mars":499,"Mercury":199,"Jupiter":599,"Venus":299,"Saturn":699,"Uranus":799,"Neptune":899,"Pluto":999}
    date=Time(str(datefrom[0])+"-"+str(datefrom[1])+"-"+str(datefrom[2]) + " " + str(datefrom[3]) + ":" + str(datefrom[4]) + ":" + str(datefrom[5]))
    todate=Time(str(dateto[0])+"-"+str(dateto[1])+"-"+str(dateto[2]) + " " + str(datefrom[3]) + ":" + str(datefrom[4]) + ":" + str(datefrom[5]))
    bodies=bodypair.split("-")
    while date != todate: 
          obj1 = Horizons(id=solar_system_bodies[bodies[0]], location=loc, epochs=date.jd, id_type='id').vectors()
          obj2 = Horizons(id=solar_system_bodies[bodies[1]], location=loc, epochs=date.jd, id_type='id').vectors()
          skycoord1 = SkyCoord(x=obj1['x'], y=obj1['y'], z=obj1['z'], unit='au', frame="icrs", representation_type='cartesian')
          skycoord2 = SkyCoord(x=obj2['x'], y=obj2['y'], z=obj2['z'], unit='au', frame="icrs", representation_type='cartesian')
          separation = skycoord1.separation(skycoord2)
          print("Angular separation of " + bodypair + " on " + date.iso + ":",separation)
          if separation.is_within_bounds(angularsepbounds[0],angularsepbounds[1]):
              print("Angular separation of " + bodypair + " matches bounds for date:",date.iso)
          datetimetoks=date.iso.split(" ")
          datetoks=datetimetoks[0].split("-")
          timetoks=datetimetoks[1].split(":")
          print("datetoks:",datetoks)
          print("timetoks:",timetoks)
          gravities=ephem.extreme_weather_events_n_body_analytics([(datetoks[0],datetoks[1],datetoks[2],timetoks[0],timetoks[1],timetoks[2])],loc=loc)
          range_gravities[date]=gravities
          date += 1
    print("=========================================================================")
    print("predict_EWE(): N-Body gravitational acceleration on location " + loc + " for " + bodypair + " during date range ",datefrom," to ",dateto, ":")
    bodypairtoks=bodypair.split("-")
    body1_gravity_l2norms=[]
    body2_gravity_l2norms=[]
    for date,g in range_gravities.items():
        print("Gravity L2 Norm of ",bodypairtoks[0]," on ",date,":",norm(g[0][bodypairtoks[0]]))
        print("Gravity L2 Norm of ",bodypairtoks[1]," on ",date,":",norm(g[0][bodypairtoks[1]]))
        body1_gravity_l2norms.append(norm(g[0][bodypairtoks[0]]))
        body2_gravity_l2norms.append(norm(g[0][bodypairtoks[1]]))
    plt.plot(body1_gravity_l2norms,label=bodypair + "(" + bodypairtoks[0] + ")")
    plt.plot(body2_gravity_l2norms,label=bodypair + "(" + bodypairtoks[1] + ")")
    plt.legend()
    #plt.savefig("./testlogs/GISWeatherAnalytics.Gravity.jpg")
    plt.show()
    return (body1_gravity_l2norms,body2_gravity_l2norms)

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
    
    def extreme_weather_events_n_body_analytics(self,datesofEWEs=None,loc="@earth-moon",angularsep=False,maxiterations=200):
        Latlons=[]
        argdatesofEWEs=datesofEWEs
        if datesofEWEs == "Earthquakes":
            EWEdates=open("earthquakesFrom1900with8plusmag.pygen.txt")
            datesofEWEs=[]
            EWEdateslines=EWEdates.readlines()
            EWEdateslines.reverse()
            for d in EWEdateslines:
                 toks = d.split(" ")
                 datetoks = toks[0].split("/")
                 timetoks = toks[1].split(":")
                 if timetoks[0] == "":
                    timetoks[0]=0
                 if timetoks[1] == "":
                    timetoks[1]=0
                 ewedate = (int(datetoks[0]), int(datetoks[1]), int(datetoks[2]), int(timetoks[0]), int(timetoks[1]), 0)
                 datesofEWEs.append(ewedate)
        else: 
                if datesofEWEs == "Hurricanes": 
                    iteration=0
                    EWEdates=open("hurdat2_1851_2012-jun2013.pygen.txt")
                    EWEdateslines=EWEdates.readlines()
                    EWEdateslines.reverse()
                    datesofEWEs=[]
                    for d in EWEdateslines:
                        if iteration == maxiterations:
                            break
                        toks = d.split(" ")
                        toks = [x for x in toks if x != ""]
                        #print("toks:",toks)
                        datetoks = toks[0].split("/")
                        timetoks = toks[1].split(":")
                        longitude = float(toks[2])
                        latitude = float(toks[3])
                        latlon={'lon':longitude,'lat':latitude,'elevation':0.0}
                        Latlons.append(latlon)
                        if timetoks[0] == "":
                            timetoks[0]=0
                        if timetoks[1] == "":
                            timetoks[1]=0
                        ewedate = (int(datetoks[0]), int(datetoks[1]), int(datetoks[2]), int(timetoks[0]), int(timetoks[1]), 0)
                        datesofEWEs.append(ewedate)
                        iteration += 1
        print("extreme_weather_events_n_body_analytics(): datesofEWEs = ",datesofEWEs)
        gravities=[]
        angular_separation=defaultdict(list)
        if angularsep:
            for date in datesofEWEs:
                if date[0] >= 1899 and date[0] <= 2053:
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
        cnt=0
        for date in datesofEWEs:
            print("extreme_weather_events_n_body_analytics(): date:",date)
            print("datesofEWEs:",datesofEWEs)
            for i in solar_system_bodies.values():
                if argdatesofEWEs=="Hurricanes":
                    print("Latlons[cnt]:",Latlons[cnt])
                    obj = Horizons(id=i, location="@0", epochs=Time(str(date[0])+"-"+str(date[1])+"-"+str(date[2])).jd, id_type='id').vectors(refplane="earth")
                    #obj = Horizons(id=i, location=Latlons[cnt], epochs=Time(str(date[0])+"-"+str(date[1])+"-"+str(date[2])).jd, id_type='id').ephemerides()
                else:
                    obj = Horizons(id=i, location=loc, epochs=Time(str(date[0])+"-"+str(date[1])+"-"+str(date[2])).jd, id_type='id').vectors()
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
            gravitydict={}
            for g in range(len(gravity)):
                if len(Latlons) > 0:
                    print("extreme_weather_events_n_body_analytics(): gravity of ",solar_system[g]," at ",Latlons[cnt]," on ",date,":",gravity[g])
                else:
                    print("extreme_weather_events_n_body_analytics(): gravity of ",solar_system[g]," at ",loc," on ",date,":",gravity[g])
                gravitydict[solar_system[g]]=gravity[g]
            gravities.append(gravitydict)
            r_list = []
            v_list = []
            cnt+=1
        print("==============================================================")
        for g1 in gravities[0].values():
            for g2 in gravities[0].values():
                dh=directed_hausdorff([g1],[g2])
                print("extreme_weather_events_n_body_analytics(): Pairwise Directed hausdorff Distance of Gravitational Acceleration:",dh)
        return gravities
           

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

    def WMAP_CMB_analytics(self):
        wmapmasked=fetch_wmap_temperatures(masked=True)
        fig = plt.figure(1)
        hp.mollview(wmapmasked,min=-1,max=1, title="masked WMAP CMB",fig=1,unit=r'$Delta$T (mK)')
        powerspectrum = hp.anafast(wmapmasked.filled(), lmax=1024)
        scatter11 = np.arange(len(powerspectrum))
        plt.savefig("testlogs/WMAP_CMB_1.jpg")
        fig = plt.figure(3)
        ax = fig.add_subplot(111)
        ax.scatter(scatter11, scatter11 * (scatter11 + 1) * powerspectrum, s=4, c="black", lw=0, label='data')
        ax.set_xlabel(r'$\ell$')
        ax.set_ylabel(r'$\ell(\ell+1)C_\ell$')
        ax.set_title('Angular Power (not mask corrected)')
        ax.legend(loc='upper right')
        ax.grid()
        ax.set_xlim(0, 1100)
        plt.savefig("testlogs/WMAP_CMB_2.jpg")

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
    #print("======================HURRICANES=========================")
    #ephem.extreme_weather_events_n_body_analytics(datesofhurricanes,loc="@0")
    #print("======================EARTHQUAKES=========================")
    #ephem.extreme_weather_events_n_body_analytics(datesofearthquakes,loc="@0")

    #print("======================EARTHQUAKES=========================")
    #ephem.extreme_weather_events_n_body_analytics(datesofEWEs="Earthquakes")
    #print("======================HURRICANES=========================")
    #ephem.extreme_weather_events_n_body_analytics(datesofEWEs="Hurricanes",angularsep=True)
    #ephem.extreme_weather_events_n_body_analytics(datesofEWEs=datesofhurricanes,angularsep=True)

    #predict_EWE(datefrom=(2022,10,21,1,00,00),dateto=(2022,12,1,1,00,00),loc='@0',bodypair="Sun-Moon",angularsepbounds=('120d','180d'))
    #predict_EWE(datefrom=(2022,10,21,1,00,00),dateto=(2022,12,1,1,00,00),loc='@0',bodypair="Venus-Mercury",angularsepbounds=('0d','30d'))

    #ephem.hubble_deep_field_RGB_analytics("HubbleUltraDeepField_heic0611b")
    #ephem.hubble_deep_field_RGB_analytics(imagename="skimage_HXDF")
    #ephem.WMAP_CMB_analytics()
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
    q1=query_space("Hasta",12.15,17.32)
    q2=query_space("Uttaraphalguni",11.49,14.34)
    locate_proper_motion_conjunction(q1,q2,duration=8000)
