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
        
    def sky_on_datetime(self,datetime,observedfrom="earth",observed="sun",position="latlon"):
        global planets
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
