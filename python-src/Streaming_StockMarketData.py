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

#Get historical stock quotes by looking up ticker symbol for date range - uses ystockquote pypi package
# and perform Time Series Analysis - AutoRegressiveMovingAverage - ARMA - on these streamed data
#X(t) = sigma_p_t-1(w1(i) * X(i)) + sigma_q_t-1(s(i) * w2(i)) where w1(i) and w2(i) are regression weights and s(i) are moving averages

import ystockquote
from pprint import pprint
import random
import rpy2.robjects as robj
import atexit

cnt=0

def compute_mean(timeseries):
	sum=0
	for i in timeseries:
		sum += i
	return float(sum/len(timeseries))

def moving_averages(timeseries, window):
	cnt=0
	mov_avg=0.0
	error_term=0.0
	mean=0.0
	while cnt+window < len(timeseries) :	
		error_term = (float(random.randint(1,100))) / 10000.0
		mean=compute_mean(timeseries[cnt:cnt+window])
		cnt+=1
		mov_avg += mean * error_term 
	return mov_avg

def autoregression(timeseries):
	cnt=0
	autoreg=0.0
	weight=0.0
	while cnt < len(timeseries):
		weight = (float(random.randint(1,100))) / 10000.0
		autoreg += weight * float(timeseries[cnt])
		cnt+=1
	return autoreg

if __name__=="__main__":
	cnt = 0
	time_series_data=[]
	for k,v in ystockquote.get_historical_prices('GOOG', '2010-01-01', '2016-06-25').items():
		#print v['High']
		print v['Adj Close']
		time_series_data.append(float(v['Adj Close']))
		cnt += 1

	#ARMA
	q=150
	projection_iteration=0
	while projection_iteration < 1000:
		arma=autoregression(time_series_data[:q]) + moving_averages(time_series_data[:q], 5)
		print "Iteration:",projection_iteration," - ARMA projection: ", arma
		time_series_data.append(arma)
		projection_iteration +=1

	y_axs = time_series_data
	x_axs = []
	for i in xrange(len(time_series_data)):
		x_axs.append(i)	 

	x = robj.FloatVector(x_axs)
	y = robj.FloatVector(y_axs)
	dataframe = robj.DataFrame({"x":x,"y":y})
	curvefn = robj.r['approxfun']
	plotfn = robj.r['plot']
	curvedata = curvefn(dataframe)
	print curvedata

	pdffn = robj.r['pdf']
	pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/python-src/DJIA_ARMA_Time_Series.pdf")
	plotfn(curvedata, 0, len(time_series_data))
