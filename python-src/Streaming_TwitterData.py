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
#Ph: 9789346927, 9003082186, 9791165980
#Krishna iResearch Open Source Products Profiles: 
#http://sourceforge.net/users/ka_shrinivaasan, https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#ZODIAC DATASOFT: https://github.com/shrinivaasanka/ZodiacDatasoft
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#Get Twitter Streaming Data - python-twitter - https://github.com/bear/python-twitter

import twitter
import pprint
import json

#OAuth Authentication 
#api=twitter.Api(consumer_key="VLxxxxxxxxxxxxxxF",consumer_secret="ZxxxxxxxxxxxxxxxxxB",access_token_key="1xxxxxxxxxxxxxxxxxxxxxI",access_token_secret="ixxxxxxxxxxxxxxxxxxxxxxxxxxxx")
api=twitter.Api(consumer_key="VLJl4Z0Wod88kE9nDTxF4sUxF",consumer_secret="Z3lzXjOLrTlOVmm5LXWHDf4MumeSG7Ln4TYSUIM00pdCuCzCTB",access_token_key="14233931-y4scOFQjzPICrCka5g79Tk9XGYWdn0433j49XkBzI",access_token_secret="i3poXTKyKotGQNlNk7sbqidraUb0qczEq2VHDREN35MsJ")


print api.VerifyCredentials()

#Search Tweets and print tweet data as stream
#while True:
print "###################################"
print "Refreshing search ..."
print "###################################"
#search=api.GetSearch("Chennai")

search=api.GetStreamFilter(track=["Chennai"])
#for i in api.GetFollowers():
for i in search:
	try:
		print "======================================"
		#print type(i)
		#print i.GetId()
		#print i.GetName()
		#pprint.pprint(i.GetCreatedAt())
		#pprint.pprint(i.GetGeo())
		#pprint.pprint(i.GetLocation())
		#jsontweet=json.loads(i)
		#pprint.pprint(jsontweet["status"]["text"])
		#pprint.pprint(i.GetText())
		#pprint.pprint(jsontweet)
		pprint.pprint(i["text"])
	except:
		pass
		
