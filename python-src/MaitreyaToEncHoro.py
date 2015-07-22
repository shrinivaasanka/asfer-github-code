#ASFER - a ruleminer which gets rules specific to a query and executes them
#Copyright (C) 2009-2013  Ka.Shrinivaasan

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

#mail to: ka.shrinivaasan@gmail.com (Krishna iResearch)
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

useGeonames=True

def decimaldegreestodms(decdeg):
	min,sec=divmod(decdeg*3600,60)
	deg,min=divmod(min,60)
	return deg,min,sec
	
def writeToEncHorosAscRelative():
	enchoro=open("./asfer.enchoros.zodiacal","r")
	enchoroasc=open("./asfer.enchoros.ascrelative", "w")
	for line in enchoro:
		rotatedline=rotateAscRelative(line)
		if rotatedline != "\n":
			enchoroasc.write(rotatedline.rstrip(os.linesep))	
		enchoroasc.write("\n")	

def rotateAscRelative(line):
	linetoks=line.split("#")
	#print "=============================="
	#print "linetoks:",linetoks
	rotatedString=""
	ascBhava=0
	i=0
	while i < len(linetoks):
		ascIndex=linetoks[i].find('a')	
		if ascIndex != -1:
			ascBhava=i
			break
		i=i+1

	if ascBhava == 0:
		return line
	else:
		currBhava=ascBhava
		while True:
			rotatedString += linetoks[currBhava].rstrip(os.linesep)
			rotatedString += '#'
			currBhava = (currBhava + 1) % 12
			if currBhava == ascBhava:
				#print "rotatedString:",rotatedString
				return rotatedString[:-1]
				break
		

def writeToEncHoros(bhavaplanetsdict):
	enchoro=open("./asfer.enchoros.zodiacal","a")
	#if AscRelative:
		#for bhava, planets in bhavaplanetsdict:
	#	pass	
	#else:
	if not bhavaplanetsdict["Aries"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Aries"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Taurus"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Taurus"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Gemini"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Gemini"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Cancer"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Cancer"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Leo"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Leo"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Virgo"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Virgo"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Libra"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Libra"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Scorpio"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Scorpio"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Sagittarius"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Sagittarius"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Capricorn"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Capricorn"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Aquarius"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Aquarius"]:
		enchoro.write(planetindex[i])
	enchoro.write("#")

	if not bhavaplanetsdict["Pisces"]:
		enchoro.write("0")
	for i in bhavaplanetsdict["Pisces"]:
		enchoro.write(planetindex[i])
	#enchoro.write("#")
	enchoro.write("\n")
###################################################3
planetindex={}

planetindex["Sun"]="1"
planetindex["Moon"]="2"
planetindex["Mars"]="3"
planetindex["Mercury"]="4"
planetindex["Jupiter"]="5"
planetindex["Venus"]="6"
planetindex["Saturn"]="7"
planetindex["Rahu"]="8"
planetindex["Ketu"]="9"
planetindex["Ascendant"]="a"

bhavaplanetsdict={}
bhavaplanetsdict["Aries"]=[]
bhavaplanetsdict["Taurus"]=[]
bhavaplanetsdict["Gemini"]=[]
bhavaplanetsdict["Cancer"]=[]
bhavaplanetsdict["Leo"]=[]
bhavaplanetsdict["Virgo"]=[]
bhavaplanetsdict["Libra"]=[]
bhavaplanetsdict["Scorpio"]=[]
bhavaplanetsdict["Sagittarius"]=[]
bhavaplanetsdict["Capricorn"]=[]
bhavaplanetsdict["Aquarius"]=[]
bhavaplanetsdict["Pisces"]=[]

#eqfile=open("/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/cpp-src/earthquakesFrom1900with8plusmag.txt","r")
eqfile=open("./earthquakesFrom1900with8plusmag.txt","r")
for line in eqfile:
	tokens=line.split()
	print tokens
	timetokens=tokens[1].split(':')
	#placelonglat=tokens[len(tokens)-1] + " " + tokens[2] + " " + tokens[3]
	longdeg=decimaldegreestodms(float(tokens[3]))
	print "longitude degrees=",longdeg
	latdeg=decimaldegreestodms(float(tokens[2]))
	print "latitude degrees=",latdeg
	placelonglat="x " + str(int(longdeg[0])) +":"+str(int(longdeg[1]))+":"+str(int(longdeg[2])) + " " + str(int(latdeg[0])) +":"+str(int(latdeg[1]))+":"+str(int(latdeg[2]))

	#Geonames Geolocation free service lookup seems to have a limit on number of webservice lookups per hour 
	#preferentially switch with a boolean flag
	if useGeonames:
		#geonames_client = geonames.GeonamesClient('demo')
		geonames_client = geonames.GeonamesClient('ka_shrinivaasan')
		geonames_result = geonames_client.find_timezone({'lat': float(tokens[2]) , 'lng': float(tokens[3])})
		#timezone = geonames_result['timezoneId']
		#print geonames_result
		#print "timezone=",timezone
		#print "timezoneGMToffset=", geonames_result['gmtOffset']
		#if geonames_result['rawOffset'] is not None:
		#	geonames_timezone = str(geonames_result['rawOffset'])
		if geonames_result['gmtOffset'] is not None:
			geonames_timezone = str(geonames_result['gmtOffset'])
		else:
			genonames_timezone="0"
	else:
		geonames_timezone="5.5"

	if len(timetokens)==1 :
		#timezone and longitude/latitude hardcoded at present
		cmd="./maitreya_textclient --date=\""+tokens[0].replace("/","-",3)+" " + tokens[1]+ ":00:00 "+ geonames_timezone + "\" --location=\"" + placelonglat + "\" --planet-list 2>&1 > chartsummary"
	if len(timetokens)==2 :
		#timezone and longitude/latitude hardcoded at present
		cmd="./maitreya_textclient --date=\""+tokens[0].replace("/","-",3)+" " + tokens[1]+ ":00 "+ geonames_timezone + "\" --location=\""+ placelonglat + "\" --planet-list 2>&1 > chartsummary"
	else:
		#timezone and longitude/latitude hardcoded at present
		cmd="./maitreya_textclient --date=\""+tokens[0].replace("/","-",3)+" " + tokens[1]+ " "+ geonames_timezone + "\" --location=\""+ placelonglat + "\" --planet-list 2>&1 > chartsummary"
		
	print cmd
	os.system(cmd)
	chartsumfile=open("./chartsummary","r")
	chartsumfile.readline()
	chartsumfile.readline()
	for i in chartsumfile:
		chartsumtokens=i.split()
		#print chartsumtokens[0],", ", chartsumtokens[3]
		#print bhavaplanetsdict[chartsumtokens[3]] 
		if chartsumtokens:
			bhavaplanetsdict[chartsumtokens[3]].append(chartsumtokens[0])
		print "bhavaplanetsdict:",bhavaplanetsdict
	print bhavaplanetsdict
	writeToEncHoros(bhavaplanetsdict)
	writeToEncHorosAscRelative()
	bhavaplanetsdict={}
	bhavaplanetsdict["Aries"]=[]
	bhavaplanetsdict["Taurus"]=[]
	bhavaplanetsdict["Gemini"]=[]
	bhavaplanetsdict["Cancer"]=[]
	bhavaplanetsdict["Leo"]=[]
	bhavaplanetsdict["Virgo"]=[]
	bhavaplanetsdict["Libra"]=[]
	bhavaplanetsdict["Scorpio"]=[]
	bhavaplanetsdict["Sagittarius"]=[]
	bhavaplanetsdict["Capricorn"]=[]
	bhavaplanetsdict["Aquarius"]=[]
	bhavaplanetsdict["Pisces"]=[]
		

				

	
