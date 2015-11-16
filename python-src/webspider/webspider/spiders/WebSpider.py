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

from scrapy.spiders import Spider
from scrapy.selector import Selector
from webspider.items import WebSpiderItem

class WebSpider(Spider):
	name = "webspider"
	allowed_domains = "www.google.com"
	start_urls = ['https://www.google.com/search?hl=en&gl=in&tbm=nws&authuser=0&gl=in&authuser=0&tbs=sbd:1&tbm=nws&q=chennai+metropolitan+area+expansion']
	output=open("WebSpider.out","w")

	def parse(self,response):
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
		return items
			 
