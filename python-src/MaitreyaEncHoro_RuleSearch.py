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
import sys
import getopt
import geonames
import math
from datetime import date, time, datetime, timedelta
from collections import defaultdict

useGeonames=True
max_iterations=100000000
min_year=0
min_month=0
min_days=0
min_hours=0
min_minutes=0
min_seconds=0
min_long=0
min_lat=0
max_year=0
max_month=0
max_days=0
max_hours=0
max_minutes=0
max_seconds=0
max_long=0
max_lat=0
opts, args = getopt.getopt(sys.argv[1:], "x", [ "min_year=", "min_month=", "min_days=", "min_hours=", "min_minutes=", "min_seconds=", "min_long=", "min_lat=", "max_year=", "max_month=", "max_days=", "max_hours=", "max_minutes=", "max_seconds=", "max_long=", "max_lat="])
print opts
print args
for opt, arg in opts:
	print opt
	print arg
	if opt == "--min_year":
			min_year = int(arg)
	if opt == "--min_month":
			min_month = int(arg)
	if opt == "--min_days":
			min_days = int(arg)
	if opt == "--min_hours":
			min_hours = int(arg)
	if opt == "--min_minutes":
			min_minutes = int(arg)
	if opt == "--min_seconds":
			min_seconds = int(arg)
	if opt == "--min_long":
			min_long = int(arg)
	if opt == "--min_lat":
			min_lat = int(arg)
	if opt == "--max_year":
			max_year = int(arg)
	if opt == "--max_month":
			max_month = int(arg)
	if opt == "--max_days":
			max_days = int(arg)
	if opt == "--max_hours":
			max_hours = int(arg)
	if opt == "--max_minutes":
			max_minutes = int(arg)
	if opt == "--max_seconds":
			max_seconds = int(arg)
	if opt == "--max_long":
			max_long = int(arg)
	if opt == "--max_lat":
			max_lat = int(arg)


class NextDateTimeTimezoneLonglat:
	def __iter__(self):
		global min_year
		global min_month
		global min_days
		global min_hours
		global min_minutes
		global min_seconds
		global min_long
		global min_lat
		global max_year
		global max_month
		global max_days
		global max_hours
		global max_minutes
		global max_seconds
		global max_long
		global max_lat
		print "__iter__:",min_long,max_long
		for long_deg in xrange(min_long, max_long,1):
			for long_min in xrange(0,9,1):
				for lat_deg in xrange(min_lat, max_lat,1):
					for lat_min in xrange(0,9,1):
						begin_datetime = datetime(min_year, min_month, min_days, min_hours, min_minutes, min_seconds)
						next_datetime = datetime(min_year, min_month, min_days, min_hours, min_minutes, min_seconds)
						end_datetime = datetime(max_year, max_month, max_days, max_hours, max_minutes, max_seconds)
						time_delta = timedelta(days=1)
						while next_datetime <= end_datetime:
							next_datetime = next_datetime + time_delta
							print "next_datetime: ", next_datetime
							date_time_timezone_longlat = " --date=\""+ str(next_datetime.year) + "-" + str(next_datetime.month) + "-" + str(next_datetime.day) + " " + str(next_datetime.hour) + ":" + str(next_datetime.minute) + ":" + str(next_datetime.second) + " " + self.geonames_time_zone(str(long_deg) +"."+ str(long_min) +" "+ str(lat_deg) +"."+ str(lat_min)) +"\"  --location=\" x "+ str(long_deg) +":"+ str(long_min) + ":" + str(0) + " "+ str(lat_deg) +":"+ str(lat_min) + ":" + str(0) +" \" --planet-list"
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
	rule_planets_list=[]
	for rule in rules_file:
		if rule.find("==============") == -1 and rule.find("Class Association") == -1:
			rule_planets=rule.strip().split(' ,')
			rule_planets_stripped=[]
			for r in rule_planets:
				rule_planets_stripped.append(r.strip())	
			rule_planets_list.append(rule_planets_stripped)
	next=NextDateTimeTimezoneLonglat()
	sign_planets_dict=defaultdict(list)

	for date_time_timezone_longlat in next:
		#Example commandline1: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient --date="1851-06-25 00:00:00 5.5" --location="x 94:48:0 28:0:0" --planet-list 
		#Example commandline2: /home/shrinivaasanka/Maitreya7_GitHub/martin-pe/maitreya7/releases/download/v7.1.1/maitreya-7.1.1/src/jyotish/maitreya_textclient  --date="2015-11-26 10:0:0 5.5"  --location=" x 80:0:0 13:0:0 " --planet-list 
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
				sign_planets_dict[row_tokens[3].strip()].append(row_tokens[0].strip())
		print "sign_planets_dict=",sign_planets_dict
		for rule_planets in rule_planets_list:
			for k,v in sign_planets_dict.iteritems():
				if (set(rule_planets[:-1]).issubset(set(v))):
					print "{",date_time_timezone_longlat,"} - There is a Class Association Rule match [",rule_planets[:-1],"] in sign ",k
				else:
					print "{",date_time_timezone_longlat,"} - There is no Class Association Rule match [",rule_planets[:-1],"] in sign ",k
			sign_planets_dict=defaultdict(list)
