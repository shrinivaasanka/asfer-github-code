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

import pysindy as ps
import numpy as np
import yfinance as yf

def SINDy_fit(t,x,y):
    print("================ SINDy non-linear dynamics governing equation discovery =========")
    print("t:",t)
    print("x:",x)
    print("y:",y)
    points=np.stack((x,y),axis=-1)
    model=ps.SINDy(feature_names=["x","y"])
    model.fit(points,t=t)
    model.print()

def stockquote_SINDy_model(ticker,period='5y',interval='1wk'):
    print("================= SINDy Stockquote Model =====================")
    print("Governing equation discovered for ticker:",ticker)
    pricehistory = yf.Ticker(ticker).history(period=period,interval=interval,actions=False)
    timeseries = np.asarray(list(pricehistory["Open"]))
    l=len(timeseries)
    t=np.arange(l)
    x=np.arange(l)
    y=timeseries
    SINDy_fit(t,x,y)

def precipitation_SINDy_model(rainfalltimeseries):
    print("================= SINDy Climate Model =====================")
    print("Governing equation discovered for precipitation timeseries:",rainfalltimeseries)
    l=len(rainfalltimeseries)
    t=np.arange(l)
    x=np.arange(l)
    y=rainfalltimeseries
    SINDy_fit(t,x,y)

if __name__=="__main__":
    t=np.linspace(0,1,100)
    x1=np.exp(-2 * t)
    y1=np.exp(t)
    SINDy_fit(t,x1,y1)
    stockquote_SINDy_model('MSFT')
    stockquote_SINDy_model('GOOG')
    stockquote_SINDy_model('AAPL')
    precipitation_SINDy_model([10,15,2,2,1,12,3,5,10])

