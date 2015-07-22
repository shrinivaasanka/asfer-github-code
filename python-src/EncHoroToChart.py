#------------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#---------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

##################################
# * 0 - for unoccupied
# * 1 - Sun
# * 2 - Moon
# * 3 - Mars
# * 4 - Mercury
# * 5 - Jupiter
# * 6 - Venus
# * 7 - Saturn
# * 8 - Rahu
# * 9 - Ketu
# * a - ascendant
#################################

planet_names={0:"Unoccupied",1:"Sun",2:"Moon",3:"Mars",4:"Mercury",5:"Jupiter",6:"Venus",7:"Saturn",8:"Rahu",9:"Ketu"}

bhava_names=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

k=0

f=open("asfer.enchoros","r")

for line in f:
	print "##################################################################"
	print "Horoscope of encoding - [",line,"]"
	print "##################################################################" 
	bhavas=line.split("#")
	for planets in bhavas:
		#print "k=",k
		if k==12:
			break
		print bhava_names[k],":"
		for p in planets:
			if p != '\n':
				if p=="a":
					print "Ascendant /",
				else:
					print "/",planet_names[int(p)],"/",
		print "\n"
		k+=1
	k=0
