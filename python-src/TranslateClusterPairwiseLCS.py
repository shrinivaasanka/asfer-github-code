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

#Python find mysteriously doesnot work for variables and always returns -1. 
#Hence a very primitive substring find function has been implemented in asferfind(). 
#Knuth-Morris-Pratt can be implemented later if necessary

zodiacaldataset=True
ascrelativedataset=True

def asferfind(str1,str2):
        issubstring=False
	s1=0
	s2=0
	beg=-1
        while s1+len(str2) < len(str1):
		s2=0	
		print "##########################################"
                while s2 < len(str2):
                        if str1[s1+s2] == str2[s2]:
				print "asferfind(): str1[s1+s2]=",str1[s1+s2],"; str2[s2]=",str2[s2],";s2=",s2,";len(str2)=",len(str2),"; s1=",s1
				if s2 == len(str2)-2:
                                	issubstring=True
                                	beg=s1
					print "asferfind(): issubstring = True, beg=",beg
					break
			else:
				break
			s2=s2+1
		s1=s1+1
		if issubstring == True:
			break	
	if issubstring==True:
        	return beg
	else:
		return -1

def computebhava(str1,lcsbeg):
	prefix=str1[:lcsbeg]
	print "computebhava(): str1=",str1,",lcsbeg=",lcsbeg,",prefix=",prefix
	bhava=0
	for p in prefix:
		if p=="#":
			bhava=bhava+1
	return bhava
	
		
planet_names={'0':"Unoccupied",'1':"Sun",'2':"Moon",'3':"Mars",'4':"Mercury",'5':"Jupiter",'6':"Venus",'7':"Saturn",'8':"Rahu",'9':"Ketu"}

bhava_names=[]

if zodiacaldataset==True:
	bhava_names=["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
if ascrelativedataset==True:
	bhava_names=["Bhava1","Bhava2","Bhava3","Bhava4","Bhava5","Bhava6","Bhava7","Bhava8","Bhava9","Bhava10","Bhava11","Bhava12"]

k=0

f=open("asfer.ClusterPairwiseLCS.txt","r")

for line in f:
	print "##################################################################"
	print line
	print "##################################################################" 
	tokens=line.split(":")
	lcs=tokens[4]
	print "lcs=",lcs

	encstrtoks=tokens[3].split("[")
	if len(encstrtoks) > 1:
		encstr=encstrtoks[1].split("]")
		print "encstr=",encstr[0],"; lcs=",lcs

	#str1="sjdkjsdjksggggggggggggjkdjksjkdjkjskjdksjdjksdkjskj"
	#str2="ggggggg"
	#print str1.find(str2)

	#print encstr[0].find("0#0#")
	#lcsbeg=encstr[0].find(lcs)
	lcsbeg=asferfind(encstr[0],lcs)
	print "lcsbeg=", lcsbeg
	if lcsbeg != -1:
		lcsbhava=computebhava(encstr[0],lcsbeg)
		bhavas=lcs.split("#")
		print "====================================="
		print "Textually Translated Classified or Clustered LCS Pattern Rule:",
		i=0
		for b in bhavas:
			#print b
			for planet in b:
				if planet != "[" and planet != "]" and planet != "a" and planet != "\n":
					print planet_names[planet]," in ",bhava_names[lcsbhava+i],"|",
				else:
					if planet == "a":
						print "| Ascendant in ",bhava_names[lcsbhava+i],"|",
			i=i+1
		print 
		print "====================================="

