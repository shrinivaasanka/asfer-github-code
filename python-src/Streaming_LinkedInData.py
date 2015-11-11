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
#-----------------------------------------------------------------------------------------------------------------------------------


from linkedin import linkedin
import requests
import sys

if len(sys.argv) == 1:
	API_KEY = '75yiu77bfm2vd6'
	API_SECRET = '3HPATaZvp2cwnXRD'
	RETURN_URL = 'https://github.com/shrinivaasanka/asfer-github-code'
	#https://www.linkedin.com/uas/oauth2/authorization?scope=r_basicprofile%20rw_nus%20r_network%20r_contactinfo%20w_messages%20rw_groups%20r_emailaddress%20r_fullprofile&state=1ad259db36bd9094eae47982ea863d7d&redirect_uri=https%3A//github.com/shrinivaasanka/asfer-github-code&response_type=code&client_id=75yiu77bfm2vd6
	authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())

	print authentication.authorization_url
	print "==================="
	authurl_tokens=authentication.authorization_url.split("?") 
	authurl_tokens2=authurl_tokens[1].split("&")
	authurl_tokens2[0]="scope=r_basicprofile%20r_emailaddress"
	url_rewritten=authurl_tokens[0]+"?"
	url_rewritten=url_rewritten+authurl_tokens2[0]+"&"+authurl_tokens2[1]+"&"+authurl_tokens2[2]+"&"+authurl_tokens2[3]+"&"+authurl_tokens2[4]
	print url_rewritten

        authurl=raw_input("authurl:")	
	argv_tokens=authurl.split("?")
	authcode_toks=argv_tokens[1].split("=")
	authcode=authcode_toks[1].split("&")
	print authcode[0]

	authentication.authorization_code = authcode[0] 
	token=authentication.get_access_token()
	application = linkedin.LinkedInApplication(authentication)
	print application.get_profile()
	print application.get_connections()
