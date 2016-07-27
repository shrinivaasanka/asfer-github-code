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
#-----------------------------------------------------------------------------------------------------------------------------------

#This parses a stream time series datasource (e.g stock quote ticker) and encodes the fluctuations as binary string of 0s and 1s

import ystockquote
from pprint import pprint
import random
import rpy2.robjects as robj
import atexit

cnt=0

if __name__=="__main__":
	cnt = 0
	prev=0.0
	time_series_data=[]
	timeseries_binary=open("StringSearch_Pattern.txt","w")
	for k,v in ystockquote.get_historical_prices('MSFT', '2010-01-01', '2016-07-26').items():
		#print v['High']
		print v['Adj Close']
		time_series_data.append(float(v['Adj Close']))
		if float(v['Adj Close']) > prev:
			timeseries_binary.write("1")
		else:
			timeseries_binary.write("0")
		prev=float(v['Adj Close'])
		cnt += 1

