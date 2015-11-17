#-------------------------------------------------------------------------------------------------------------------------------------
#ASFER - AstroInfer - a classification,inference and predictive modelling software for mining patterns in Massive Data Sets, at present
#                       specialized for Astronomy DataSets
# 
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------------------------------------------------------------
#Copyright (C): 
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch): http://sourceforge.net/users/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------



########################################################################

#Geolocation Service JSON Request and Response for timezone Offset
#Copyright - https://gist.github.com/pamelafox/2288222/download#
#Simplified and modified for AstroInfer

#######################################################################


import sys
import urllib
import urllib2
import json
import logging


class GeonamesClient(object):
    BASE_URL = 'http://api.geonames.org/'

    def __init__(self, username):
        self.username = username

    def call(self, service, params=None):
        url = self.build_url(service, params)

        try:
            response = urllib2.urlopen(urllib2.Request(url))
            json_response = json.loads(response.read())
        except Exception:
		print "exception:"
        return json_response

    def build_url(self, service, params=None):
        url = '%s%s?username=%s' % (GeonamesClient.BASE_URL, service, self.username)
        if params:
            if isinstance(params, dict):
                params = dict((k, v) for k, v in params.items() if v is not None)
                params = urllib.urlencode(params)
            url = '%s&%s' % (url, params)
        return url
    
    # http://api.geonames.org/timezoneJSON?lat=47.01&lng=10.2&username=demo
    def find_timezone(self, params):
        return self.call('timezoneJSON', params)
###############################################################################

geonames_client = GeonamesClient('ka_shrinivaasan')
geonames_result = geonames_client.find_timezone({'lat': 0.773 , 'lng': 92.452})
print "timezoneGMToffset=", geonames_result['gmtOffset']
