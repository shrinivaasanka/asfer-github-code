#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
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
#Copyleft (Copyright+):
#Srinivasan Kannan
#(also known as: Shrinivaasan Kannan, Shrinivas Kannan)
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

import requests
import pprint
from rest_client import similar_to_concepts

class ConceptNet5Client:
	def __init__(self):
		print "Init of ConceptNet Client"

	def query_association(self,concept1,concept2):
		conceptjson=requests.get("http://conceptnet5.media.mit.edu/c/en/"+concept1+"?filter=/c/en/"+concept2).json()
		return conceptjson

	def query_search(self,concept):
		conceptjson=requests.get("http://conceptnet5.media.mit.edu/search?end=/c/en/"+concept).json()
		return conceptjson

	def query_lookup(self,concept):
		conceptjson=requests.get("http://conceptnet5.media.mit.edu/c/en/"+concept).json()
		return conceptjson

if __name__=="__main__":
	conceptnet = ConceptNet5Client()
	print "========================================"
	print "Association"
	print "========================================"
	conceptjson=conceptnet.query_association("chennai","marina")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Search"
	print "========================================"
	conceptjson=conceptnet.query_search("chennai")
	pprint.pprint(conceptjson)
	print "========================================"
	print "Lookup"
	print "========================================"
	conceptjson=conceptnet.query_lookup("chennai")
	pprint.pprint(conceptjson)
