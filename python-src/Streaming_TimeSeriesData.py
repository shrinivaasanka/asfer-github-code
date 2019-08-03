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
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

#Get historical stock quotes by looking up ticker symbol for date range - uses ystockquote pypi package
# and perform Time Series Analysis - AutoRegressiveMovingAverage - ARMA - on these streamed data
#X(t) = sigma_p_t-1(w1(i) * X(i)) + sigma_q_t-1(s(i) * w2(i)) where w1(i) and w2(i) are regression weights and s(i) are moving averages
#ARIMA is implemented as factorized polynomial defined in https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average

from pprint import pprint
import random
import rpy2.robjects as robj
import atexit
import math

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
	cnt=len(timeseries) - 1
	autoreg=0.0
	weight=0.0
	while cnt > 0:
		weight = (float(random.randint(1,100))) / 10000.0
		autoreg += weight * float(timeseries[cnt])
		cnt-=1
	return autoreg

def lag(timeseries,l):
    return timeseries[len(timeseries)-l]

def binomial_term(d,x):
    product = 1
    factorial = 1
    for y in range(1,x):
       product = product * (d - y) 
    for y in range(1,x):
       factorial = factorial * y
    return (product, factorial)

def lag_factor_binomial_expansion(d,timeseries):
    binomial_sum=0
    for x in range(1,d): 
        term=binomial_term(d,x)
        binomial_sum += math.pow(-1,x) * lag(timeseries,x) * float(term[0])/float(term[1])
    return float(binomial_sum)

def autoregression_factored(timeseries,p,d):
    cnt=p
    autoreg=0.0
    weight=0.0
    while cnt > 0:
	weight = (float(random.randint(1,100))) / 10000.0
        autoreg += weight * float(timeseries[cnt])
	cnt-=1
    autoreg = autoreg * lag_factor_binomial_expansion(d, timeseries)
    return autoreg

def ARMA(timeseries,pprime,q):
    time_series_data=timeseries
    arma=timeseries[len(timeseries)-1] - autoregression(time_series_data[pprime:]) - moving_averages(time_series_data[q:], 5)
    print("ARMA projection: ", arma)
    return time_series_data

def ARIMA(timeseries,p,d,q):
    time_series_data=timeseries
    arima=autoregression_factored(time_series_data,p,d) - moving_averages(time_series_data[q:], 5)
    print("ARIMA projection: ", abs(arima))
    return time_series_data
