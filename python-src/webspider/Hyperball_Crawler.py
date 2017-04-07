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

#An indexless crawler which tries to find a url matching a query string in a recursive crawl creating a hyperball of certain radius
#This is similar to Stanley Milgram, Kleinberg Lattice Small World Experiments and recent Hyperball algorithm for Facebook graph which
#concluded that Facebook has 3.74 degrees of freedom. Starts with a random url on world wide web. Success probability depends on average
#number of hops over large number of queries.

from bs4 import BeautifulSoup
from collections import deque
import requests

class Hyperball_Crawler(object):
	def __init__(self,pivot):
		self.pivot=pivot

	def crawl(self,query):
		deq=deque()
		central_url=self.pivot
		deq.append(central_url)
		hops=0

		while len(deq) > 0 and hops < 100:
			try:
				url=deq.popleft()
				print url[len(url)-3:]
				if url[len(url)-3:] != "pdf":
					print "url:",url
					r=requests.get(url)
					print "hops:",hops
					soup=BeautifulSoup(r.text)
					extracted_text=soup.get_text()
					if query in extracted_text:
						print "Query matches url:",url
					for link in soup.find_all('a'):
						deq.append(link.get('href'))	
				hops += 1	
			except:
				continue	

if __name__=="__main__":
	hypercrawler=Hyperball_Crawler("http://sites.google.com/site/kuja27/")
	query="Chennai"
	hypercrawler.crawl(query)
