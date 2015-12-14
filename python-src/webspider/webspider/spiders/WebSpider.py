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

#Reference: https://simplypython.wordpress.com/2014/03/31/getting-google-search-results-with-scrapy/ and https://github.com/scrapy/dirbot/blob/master/dirbot/spiders/dmoz.py

import re
import os
import sys 

from injector import Module, provides, Injector, inject, singleton
from scrapy.spiders import Spider
from scrapy.selector import Selector
from webspider.items import WebSpiderItem
from bs4 import BeautifulSoup

class WebSpider(Spider):
	name = "webspider"
	crawling = "HTML"
	allowed_domains = "www.google.com"
	#start_urls = ['https://www.google.com/search?hl=en&gl=in&tbm=nws&authuser=0&q=theoretical+computer+science&oq=theoretical+computer+science&gs_l=news-cc.3..43j43i53.30043.38477.0.38618.28.9.0.19.19.2.775.3607.2j1j1j0j1j2j2.9.0...0.0...1ac.1.mtwb_lgjbI4']
	#start_urls = ['https://www.google.com/search?hl=en&gl=in&tbm=nws&authuser=0&q=Chennai&oq=Chennai&gs_l=news-cc.3...1525.3020.0.3307.7.6.0.0.0.0.0.0..0.0...0.0...1ac.1.#q=Chennai&hl=en&gl=in&authuser=0&tbm=nws&tbs=sbd:1','https://www.google.com/search?hl=en&gl=in&tbm=nws&authuser=0&gl=in&authuser=0&tbs=sbd:1&tbm=nws&q=chennai+metropolitan+area+expansion','https://www.google.co.in/search?q=Chennai+metropolitan+area+expansion&oq=Chennai+metropolitan+area+expansion&aqs=chrome..69i57.12903j0j8&sourceid=chrome&es_sm=93&ie=UTF-8']
	start_urls = ['http://tech.firstpost.com/news-analysis/apple-slashes-prices-of-bestseller-iphone-5s-now-available-for-rs-24999-in-india-291179.html']
	output=open("WebSpider-"+crawling+".out","w")

	def parse(self,response):
		if self.crawling=="Streaming":
			sys.path.insert(0,"/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/python-src/backend")
			import Abstract_DBBackend
			import MySQL_DBBackend
			import MySQL_Configuration
			import MongoDB_DBBackend
			import MongoDB_Configuration
			from pymongo.collection import Collection
			mysqldbobj=MySQL_DBBackend.MySQL_DBBackend()
			mysqlconfigobj=MySQL_Configuration.MySQL_Configuration()
			injector=Injector([mysqldbobj,mysqlconfigobj])
			handler=injector.get(Abstract_DBBackend.Abstract_DBBackend)
			#handler.execute_query("CREATE TABLE asfer_webspider(Description varchar(100))")
			select = Selector(response)
			links_list = select.xpath('//h3/a/@href').extract()
			links_list2 = [re.search('q=(.*)&sa',n).group(1) for n in links_list]
			desc_list=select.xpath('//h3/a/text()').extract()
			items=[]
			for desc in desc_list:
				item=WebSpiderItem()
				item['desc'] = desc
				items.append(item)
				self.output.write(desc)
				self.output.write("\n")
				handler.execute_query("INSERT INTO asfer_webspider(Description) VALUES(\""+desc+"\")","MySQL")
			handler.execute_query("SELECT * FROM asfer_webspider","MySQL")
			return items
		if self.crawling=="HTML":
			bsoup=BeautifulSoup(response.body)
			for script in bsoup(["script","style"]):
				script.extract()
			self.output.write(bsoup.get_text().encode("utf-8"))
