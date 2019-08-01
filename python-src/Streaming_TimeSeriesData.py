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

def autoregression_factored(timeseries,d):
	cnt=0
	autoreg=0.0
	weight=0.0
        lag=int(float(len(timeseries))/float(d) + 1)
	while cnt < len(timeseries)-lag:
		weight = (float(random.randint(1,100))) / 10000.0
		autoreg += weight * float(timeseries[cnt])
		cnt+=1
        print "lag:",lag
        print "timeseries:",timeseries
        print timeseries[len(timeseries)-lag]
        autoreg = autoreg * timeseries[len(timeseries)-lag]
	return autoreg

def ARMA(timeseries,q):
    projection_iteration=0
    time_series_data=timeseries
    while projection_iteration < 1000:
          arma=autoregression(time_series_data[:q]) + moving_averages(time_series_data[:q], 5)
          print("Iteration:",projection_iteration," - ARMA projection: ", arma)
          time_series_data.append(arma)
          projection_iteration +=1
    return time_series_data

def ARIMA(timeseries,q,d):
    projection_iteration=0
    time_series_data=timeseries
    while projection_iteration < 1000:
          arma=autoregression_factored(time_series_data[:q],d) + moving_averages(time_series_data[:q], 5)
          print("Iteration:",projection_iteration," - ARIMA projection: ", arma)
          time_series_data.append(arma)
          projection_iteration +=1
    return time_series_data
