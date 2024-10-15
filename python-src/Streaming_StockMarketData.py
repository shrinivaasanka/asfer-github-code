# -------------------------------------------------------------------------------------------------------
# NEURONRAIN ASFER - Software for Mining Large Datasets
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

# Get historical stock quotes by looking up ticker symbol for date range - uses ystockquote pypi package
# and perform Time Series Analysis - AutoRegressiveMovingAverage - ARMA - on these streamed data
# X(t) = sigma_p_t-1(w1(i) * X(i)) + sigma_q_t-1(s(i) * w2(i)) where w1(i) and w2(i) are regression weights and s(i) are moving averages

#import ystockquote
from pprint import pprint
import random
import rpy2.robjects as robj
import atexit
from Streaming_TimeSeriesData import compute_mean, moving_averages, autoregression, ARMA, ARIMA, stockquote_Prophet_timeseries_forecast_model,bse_stockquote_and_stats
import numpy as np
from MultiFractals import stockquote_mfdfa_model
from MultiFractals import stockquote_granger_causality 
from MultiFractals import granger_causality_GraphicalEventModel

cnt = 0

if __name__ == "__main__":
    stockquote_Prophet_timeseries_forecast_model("AMZN")
    stockquote_Prophet_timeseries_forecast_model("MSFT")
    stockquote_Prophet_timeseries_forecast_model("GOOG")
    stockquote_Prophet_timeseries_forecast_model("TSLA")
    #bse_stockquote_and_stats()
    #cnt = 0
    #time_series_data = []
    #historic_data = [{'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}, {'Adj Close': 100}, {'Adj Close': 102}, {'Adj Close': 132}, {'Adj Close': 123}, {'Adj Close': 114}]
    #stockquote_mfdfa_model("TSLA")
    #stockquote_mfdfa_model("MSFT")
    #stockquote_mfdfa_model("AAPL")
    #ret1=stockquote_granger_causality("TSLA","AAPL",period='2y',interval='1wk',maxlag=3)
    #ret2=stockquote_granger_causality("TSLA","MSFT",period='2y',interval='1wk',maxlag=3)
    #ret3=stockquote_granger_causality("AMZN","MSFT",period='2y',interval='1wk',maxlag=3)
    #ret4=stockquote_granger_causality("GOOGL","MSFT",period='2y',interval='1wk',maxlag=3)
    #ret5=stockquote_granger_causality("IBM","MSFT",period='2y',interval='1wk',maxlag=3)
    #ret6=stockquote_granger_causality("GOOGL","MSFT",period='2y',interval='1wk',maxlag=3)
    #dictoftimeseries={}
    #dictoftimeseries[ret1[0][0]]=ret1[0][1]
    #dictoftimeseries[ret1[1][0]]=ret1[1][1]
    #dictoftimeseries[ret2[0][0]]=ret2[0][1]
    #dictoftimeseries[ret2[1][0]]=ret2[1][1]
    #dictoftimeseries[ret3[0][0]]=ret3[0][1]
    #dictoftimeseries[ret3[1][0]]=ret3[1][1]
    #dictoftimeseries[ret4[0][0]]=ret4[0][1]
    #dictoftimeseries[ret4[1][0]]=ret4[1][1]
    #dictoftimeseries[ret5[0][0]]=ret5[0][1]
    #dictoftimeseries[ret5[1][0]]=ret5[1][1]
    #dictoftimeseries[ret6[0][0]]=ret6[0][1]
    #dictoftimeseries[ret6[1][0]]=ret6[1][1]
    #granger_causality_GraphicalEventModel(dictoftimeseries)
    ## for k,v in ystockquote.get_historical_prices('GOOG', '2010-01-01', '2016-06-25').items():
    #for v in historic_data:
    #     #print v['High']
    #    time_series_data.append(float(v['Adj Close']))
    #    cnt += 1

    #projection_iterations = 0
    #while projection_iterations < 100:
    #    print("============================================================")
    #    # ARMA
    #    time_series_data_arma = ARMA(time_series_data, 2, 1)
    #    # ARIMA
    #    time_series_data_arima = ARIMA(time_series_data, 2, 2, 2)
    #    projection_iterations += 1
    #    print("============================================================")

    #y_axs = time_series_data_arima
    #x_axs = []
    # for i in xrange(len(time_series_data_arima)):
    #	x_axs.append(i)

    #x = robj.FloatVector(x_axs)
    #y = robj.FloatVector(y_axs)
    #dataframe = robj.DataFrame({"x":x,"y":y})
    #curvefn = robj.r['approxfun']
    #plotfn = robj.r['plot']
    #curvedata = curvefn(dataframe)
    # print(curvedata)

    #pdffn = robj.r['pdf']
    # pdffn("/media/ksrinivasan/Krishna_iResearch/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/DJIA_ARIMA_Time_Series.pdf")
    #plotfn(curvedata, 0, len(time_series_data_arima))
