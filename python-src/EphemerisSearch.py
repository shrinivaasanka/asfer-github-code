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

planetradecdict={}
planets=[]
ts=[]

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

    def planetarium_search(self,datetime1,datetime2,find_discrete=False,step_days=1):
        global planets
        global ts
        earth=planets["earth"]
        datetimeutc1=ts.utc(datetime1[0],datetime1[1],datetime1[2],datetime1[3],datetime1[4],datetime1[5])
        datetimeutc2=ts.utc(datetime2[0],datetime2[1],datetime2[2],datetime2[3],datetime2[4],datetime2[5])
        if find_discrete:
            degree_match.step_days = step_days 
            founddatetime,values = find_discrete(datetimeutc1,datetimeutc2,radec_match)
            print("planetarium_search(): found matching datetime = ",(founddatetime,values))
        else:
            try:
                datetime=datetimeutc1
                while datetime.tt_strftime() != datetimeutc2.tt_strftime():
                     print("=================================================================")
                     print("planetarium_search(): datetime to search for radec_match() = ",datetime.tt_strftime())
                     if radec_match(datetime):
                        print("planetarium_search(): found matching datetime = ",datetime.tt_strftime())
                        break
                     datetime += step_days 
            except Exception as ex:
                print("Exception:",ex)
        
    def sky_on_datetime(self,datetime,observedfrom="earth",observed="sun"):
        global planets
        t=ts.utc(datetime[0],datetime[1],datetime[2],datetime[3],datetime[4],datetime[5])
        planetobservedfrom=planets[observedfrom]
        planetobserved=planets[observed]
        astrometric=planetobservedfrom.at(t).observe(planetobserved)
        print("sky_on_datetime(): Right Ascension - Declination (Long-Lat) position of ",observed," from ",observedfrom," on ",datetime," (Year-Month-Day-Hour-Minute-Second):",astrometric.radec())
        return astrometric.radec()

if __name__=="__main__":
    ephem=EphemerisSearch("de421.bsp")
    ephem.sky_on_datetime((2022,7,7,1,15,30),"earth","mars")
    planetradecdict={}
    planetradecdict["sun"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","sun")
    planetradecdict["moon"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","moon")
    planetradecdict["mars"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","mars")
    planetradecdict["mercury"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","mercury")
    planetradecdict["jupiter barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","jupiter barycenter")
    planetradecdict["venus barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","venus barycenter")
    planetradecdict["saturn barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","saturn barycenter")
    planetradecdict["uranus barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","uranus barycenter")
    planetradecdict["neptune barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","neptune barycenter")
    planetradecdict["pluto barycenter"]=ephem.sky_on_datetime((2016,7,3,1,15,30),"earth","pluto barycenter")
    ephem.astronomical_event_to_search(planetradecdict)
    ephem.planetarium_search((2016,6,29,1,15,30),(2022,7,6,1,15,30))
    ephem.planetarium_search((-2016,6,29,1,15,30),(2022,7,6,1,15,30),step_days=100)
