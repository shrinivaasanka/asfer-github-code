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
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9789346927, 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch):
#http://sourceforge.net/users/ka_shrinivaasan
#https://www.ohloh.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------


import jellyfish
import sys

#JaroWinkler distance of 2 strings
distance_metric1="JaroWinkler"
#Jaro distance of 2 strings
distance_metric2="Jaro"
#MatchRating or Phonetic similarity of two strings
distance_metric3="MatchRating"
#Levenshtein distance of two strings
distance_metric4="Levenshtein"
#Hamming distance or edit distance of two strings
distance_metric5="Hamming"

def getSimilarity(str1,str2):
	distance={}
	if distance_metric1 == "JaroWinkler":
		distance[distance_metric1]=jellyfish.jaro_winkler(str1,str2)
	if distance_metric2 == "Jaro":
		distance[distance_metric2]=jellyfish.jaro_distance(str1,str2)
	if distance_metric3 == "MatchRating":
		distance[distance_metric3]=jellyfish.match_rating_comparison(str1,str2)
	if distance_metric4 == "Levenshtein":
		distance[distance_metric4]=jellyfish.levenshtein_distance(str1,str2)
	if distance_metric5 == "Hamming":
		distance[distance_metric5]=jellyfish.hamming_distance(str1,str2)
	return distance



str1 = sys.argv[1]
str2 = sys.argv[2]
print str1, str2
distance=getSimilarity(str1, str2)
print distance

