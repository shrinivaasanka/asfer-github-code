#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets (subsystem of NeuronRain)
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

#RESTful and python tornado based Graphical User Interface entrypoint that reads from various html templates and passes on 
#incoming concurrent requests to NeuronRain subsystems - AsFer, VIRGO, KingCobra, USBmd and Acadpdrafts. Presently implements 
#simplest possible POST form without too much rendering (might require flask, twisted, jinja2 etc.,) for AsFer algorithms execution.
#This exposes a RESTful API for commandline clients like cURL. For example a cURL POST is done to NeuronRain as:
#cURL POST: curl -H "Content-Type: text/plain" -X POST -d '{"component":"AsFer","script":"<script_name>","arguments":"<args>"}' http://localhost:33333/neuronrain where REST url is <host:port>/neuronrain.
#Otherwise REST clients such as Advanced RESTful Client browser app can be used.
#With this NeuronRain is Software-As-A-Service (SaaS) Platform deployable on VIRGO linux kernel cloud, cloud OSes and containers like Docker. 
#More so, it is Platform-As-A-Service (PaaS) when run on a VIRGO cloud.
#Login page has entrypoint /neuronrain_auth and authentication is done by OAuth2 for non-root and plain cookie setting for root user. 

import tornado.ioloop
import tornado.web
import os
import sys
from pymongo.collection import Collection
from pymongo import MongoClient
import sys
import oauth2.tokengenerator
import oauth2.grant
import oauth2.store.mongodb
import oauth2.store.redisdb
import redis
from passlib.hash import sha256_crypt

class NeuronRain_REST_BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
	return self.get_secure_cookie("neuronrain_user")

class NeuronRain_REST_MainHandler(NeuronRain_REST_BaseHandler):
    @tornado.web.authenticated
    def get(self):
	self.render("templates/NeuronRain_Template_1.html")
	
class NeuronRain_REST_Algorithms_Handler(NeuronRain_REST_BaseHandler):
    def get(self):
	if self.current_user is not None:
		print "self.current_user:",self.current_user
		self.render("templates/NeuronRain_Template_1.html")
	else:
		self.redirect("/neuronrain_auth")

    @tornado.web.authenticated
    def post(self):
	sys.path.insert(0,"/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/python-src")
	self.set_header("Content-Type","text/html")
	component=self.get_argument('component','#AsFer')
	script=self.get_argument('script','#../WordNetSearchAndVisualizer.py')
	arguments=self.get_argument('arguments','#../WordNetSearchAndVisualizer-Data-Source.txt')
	print "component:",component
	print "script:",script
	print "arguments:",arguments
	self.write(component)
	self.write(" ")
	self.write(script)
	self.write(" ")
	self.write(arguments)
	os.system("python " + script + " " + arguments)

class NeuronRain_REST_Auth_Handler(NeuronRain_REST_BaseHandler):
	def get(self):
		self.render("templates/NeuronRain_Login_Template.html", errormessage="Invalid Login")
	
	def post(self):
                self.database_name = 'neuronrain_oauth'
                self.collection_name = 'neuronrain_users'
                self.client=MongoClient('localhost',27017)

		print "NeuronRain_REST_Auth_Handler.post()"
		username=self.get_argument('username','username')
		password=self.get_argument('password','password')
		encrypted_password=sha256_crypt.encrypt(password)

		self.set_secure_cookie("neuronrain_user",tornado.escape.json_encode(username))
		if username=="root" and password=="root":
			#self.redirect(self.get_argument('next'), r"/neuronrain")
			self.redirect(r"/neuronrain")
		else:
		 	try:
				self.database = self.client[self.database_name]
                		self.collection = self.database[self.collection_name]

				#Can be uncommented if there is a necessity to populate MongoDB:
				#---------------------------------------------------------------
                		#credentials1={
				#	  'identifier': 'neuronrain_user',
                       		#	   'secret': encrypted_password,
                       		#	   'redirect_uris': [],
                       		#	   'authorized_grants': [oauth2.grant.ClientCredentialsGrant.grant_type]
				#}
                		#document_id=self.collection.insert_one(credentials1).inserted_id
					
                		credentials=self.collection.find_one({"identifier":username})
				if sha256_crypt.verify(password, credentials["secret"]):
    					client_store = oauth2.store.mongodb.ClientStore(credentials)
    					token_store = oauth2.store.redisdb.TokenStore(rs=redis.Redis())
    					token_generator = oauth2.tokengenerator.Uuid4()
    					token_generator.expires_in[oauth2.grant.ClientCredentialsGrant.grant_type] = 3600
	
 					auth_controller = oauth2.Provider(
       						access_token_store=token_store,
       						auth_code_store=token_store,
       						client_store=client_store,
       						#site_adapter=None,
       						token_generator=token_generator
  					)
   					auth_controller.token_path = '/neuronrain'
					print "NeuronRain_REST_Auth_Handler.post(): before redirect"
					self.redirect(r"/neuronrain")
					print "NeuronRain_REST_Auth_Handler.post(): after redirect"
				else:
					raise Exception("Invalid Credentials")
			except:
				self.write("Exception Caught:")
				self.write(str(sys.exc_info()))
				

def make_app():
    return tornado.web.Application([(r"/",NeuronRain_REST_MainHandler),(r"/neuronrain", NeuronRain_REST_Algorithms_Handler),(r"/neuronrain_auth", NeuronRain_REST_Auth_Handler),], **settings)
    #return tornado.web.Application([(r"/",NeuronRain_REST_MainHandler),(r"/neuronrain_auth", NeuronRain_REST_Auth_Handler),], **settings)

if __name__ == "__main__":
    settings = { 
		"cookie_secret" : "ksjdksjwwiennknwiejiwjeionwnewijenkcnkn",
		"login_url" : "/neuronrain_auth"
	 }	
    app = make_app()
    app.listen(33333)
    tornado.ioloop.IOLoop.current().start()
