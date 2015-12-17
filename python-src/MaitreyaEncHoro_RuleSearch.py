#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets
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
#--------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#*****************************************************************************/
# Copyright attribution for Maitreya text client referred in this file:
#
#  Maitreya, open source platform for Vedic and western astrology.
#  Release    7.0
#  Author     Martin Pettau
#  Copyright  2003-2012 by the author
#  http://www.saravali.de/
#****************************************************************************/

import os
import geonames
import math
from collections import defaultdict

useGeonames=True
max_iterations=100000000
min_year=2015
min_month=1
min_days=1
min_hours=0
min_minutes=0
min_seconds=0
min_long=0
min_lat=0
max_year=2016
max_month=2
max_days=2
max_hours=23
max_minutes=59
max_seconds=59
max_long=59
max_lat=59

class NextDateTimeTimezoneLonglat:
	def __iter__(self):
		for year in xrange(min_year, max_year,1):
			for month in xrange(min_month, max_month,1):
				for day in xrange(min_days, max_days,1):
					for hour in xrange(min_hours, max_hours,1):
						for minute in xrange(min_minutes, max_minutes,1):
							for second in xrange(min_seconds, max_seconds,1):
								for long_deg in xrange(min_long, max_long,1):
									for long_min in xrange(0,9,1):
										for lat_deg in xrange(min_lat, max_lat,1):
											for lat_min in xrange(0,9,1):
												date_time_timezone_longlat = " --date=\""+ str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second) + " " + self.geonames_time_zone(str(long_deg) +"."+ str(long_min) +" "+ str(lat_deg) +"."+ str(lat_min)) +"\"  --location=\" x "+ str(long_deg) +":"+ str(long_min) + ":" + str(0) + " "+ str(lat_deg) +":"+ str(lat_min) + ":" + str(0) +" \" --planet-list"
												yield date_time_timezone_longlat  


	def geonames_time_zone(self, latlong):
		print latlong
		latlong_tokens = latlong.split(" ")
		#Geonames Geolocation free service lookup seems to have a limit on number of webservice lookups per hour 
		#preferentially switch with a boolean flag
		if useGeonames:
			geonames_client = geonames.GeonamesClient('ka_shrinivaasan')
			geonames_result = geonames_client.find_timezone({'lat': latlong_tokens[1] , 'lng': latlong_tokens[0]})
			print geonames_result
			if geonames_result['gmtOffset'] is not None:
				geonames_timezone = str(geonames_result['gmtOffset'])
			else:
				geonames_timezone="0"
		else:
			geonames_timezone="5.5"
		return geonames_timezone


if __name__=="__main__":
	rules_file=open("./MinedClassAssociationRules.txt","r")
	next=NextDateTimeTimezoneLonglat()
	sign_planets_dict=defaultdict(list)
	for rule in rules_file:
		if rule.find("==============") == -1 and rule.find("Class Association") == -1:
			planets=rule.split(',')
			#Example commandline: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient --date="1851-06-25 00:00:00 5.5" --location="x 94:48:0 28:0:0" --planet-list 
			#/home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient  --date="0-0-0 0:0:0 0  --location=" x 0:0:0 0:1:0 " --planet-list 2>&1 > chartsummary.rulesearch

			for date_time_timezone_longlat in next:
				cmd="/home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient "+ date_time_timezone_longlat + " 2>&1 > chartsummary.rulesearch"
				print cmd
				os.system(cmd)
				print "============================================"
				chart=open("chartsummary.rulesearch","r")
				chart.readline()
				chart.readline()
				for row in chart:
					row_tokens=row.split()
					if row_tokens:
						sign_planets_dict[row_tokens[4]].append(row_tokens[0])
				print "sign_planets_dict=",sign_planets_dict
				message="{" + date_time_timezone_longlat + "} - There is no Class Association Rule match"
				for k,v in sign_planets_dict.iteritems():
					if set(v) == set(planets):
						message="{",date_time_timezone_longlat,"} - There is a Class Association Rule match [",k,"] in sign ",v
				print message
				sign_planets_dict=defaultdict(list)
