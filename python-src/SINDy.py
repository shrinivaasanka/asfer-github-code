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
import json
from scipy.integrate import solve_ivp
from pysindy.utils import lorenz
import matplotlib.pylab as plt
import math

def SINDy_fit_lorenz(t,x,y,order=2,degree=5,threshold=0.0001):
    print("================ SINDy non-linear dynamics governing equation discovery (Lorenz) =========")
    print("t:",t)
    print("x:",x)
    print("y:",y)
    integrator_keywords = {}
    integrator_keywords['rtol'] = 1e-12
    integrator_keywords['method'] = 'LSODA'
    integrator_keywords['atol'] = 1e-12
    t_span = (min(t), max(t))
    x0 = [-8, 8, 27]
    lorenzx = solve_ivp(lorenz, t_span, x0, t_eval=t, **integrator_keywords).y.T
    #print("lorenzx:",lorenzx)
    differentiation_method = ps.FiniteDifference(order=order)
    feature_library = ps.PolynomialLibrary(degree=degree)
    optimizer = ps.STLSQ(threshold=threshold)
    #model=ps.SINDy(differentiation_method=differentiation_method, feature_library=feature_library, optimizer=optimizer,feature_names=["x","y"])
    model=ps.SINDy()
    lorenzx_1=[math.sqrt(x*x+y*y+z*z) for x,y,z in lorenzx]
    print("lorenzx_1:",lorenzx_1)
    if len(t) > len(lorenzx_1):
        lorenzx_1 = np.append(lorenzx_1,np.zeros(len(lorenzx_1)-len(y)))
    else:
        lorenzx_1 = lorenzx_1[:len(lorenzx_1)]
    if len(t) > len(y):
        y = np.append(y,np.zeros(len(t)-len(y)))
    else:
        y = y[:len(t)]
    model.fit(np.asarray(lorenzx_1),t=t[1]-t[0])
    print("Lorenz model:",model)
    model.print()
    print("Lorenz model coefficients:",model.coefficients())
    print("Lorenz model equations:",model.equations())
    print("Lorenz model score:", model.score(y,t=t[1]-t[0]))
    #print("model score:", model.score(lorenzx,t=t[1]-t[0]))
    #print("len(lorenzx):",len(lorenzx))
    #print("len(y):",len(y))
    #y3d=[[yelem,telem,0] for yelem,telem in zip(y,t)]
    #print("y3d:",y3d)
    predictions=model.predict(y)
    print("Lorenz model predictions:", predictions)
    return predictions

def SINDy_fit(t,x,y,order=2,degree=5,threshold=0.0001):
    print("================ SINDy non-linear dynamics governing equation discovery =========")
    differentiation_method = ps.FiniteDifference(order=order)
    feature_library = ps.PolynomialLibrary(degree=degree)
    optimizer = ps.STLSQ(threshold=threshold)
    points=np.stack((x,y),axis=-1)
    model=ps.SINDy(differentiation_method=differentiation_method, feature_library=feature_library, optimizer=optimizer,feature_names=["x","y"])
    model.fit(points,t=t)
    model.print()
    print("model coefficients:",model.coefficients())
    print("model equations:",model.equations())
    predictions=model.predict(points)
    print("model predictions:", predictions)
    return predictions

def stockquote_SINDy_model(ticker,period='5y',interval='1wk',model='Plain'):
    print("================= SINDy Stockquote Model =====================")
    print("Governing equation discovered for ticker:",ticker)
    try:
        pricehistory = yf.Ticker(ticker).history(period=period,interval=interval,actions=False)
        timeseries = np.asarray(list(pricehistory["Open"]))
    except:
        print("Rate limit exception....")
        timeseries = np.random.rand(100) 
    l=len(timeseries)
    t=np.arange(l)
    x=np.arange(l)
    y=timeseries
    if model=="LorenzLogisticMap":
        t=np.arange(0,1.0,1.0/float(len(y)))
        predictions=SINDy_fit_lorenz(t,x,y)
    if model=="Plain":
        predictions=SINDy_fit(t,x,y)
    plt.plot(predictions)

def read_rainfall_dataset(rainfalltimeseriesjson,datasource='IMD',subdivision='Tamil Nadu'):
    if datasource == 'IMD':
        rftsjsonfile=open(rainfalltimeseriesjson)
        rftsjson=json.load(rftsjsonfile)
        rainfalltimeseries=[]
        for row in rftsjson["data"]:
            if row[0] == subdivision:
                for i in range(2,13):
                      if row[i] != 'NA':
                          rainfalltimeseries.append(float(row[i]))
        print("rainfall timeseries for state ", subdivision," :",rainfalltimeseries)
        return rainfalltimeseries

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
    t=np.arange(0,2,0.02)
    SINDy_fit_lorenz(t,x1,y1)
    stockquote_SINDy_model('MSFT',model='LorenzLogisticMap')
    stockquote_SINDy_model('GOOG',model='LorenzLogisticMap')
    stockquote_SINDy_model('AAPL',model='LorenzLogisticMap')
    stockquote_SINDy_model('AMZN',model='LorenzLogisticMap')
    stockquote_SINDy_model('META',model='LorenzLogisticMap')
    stockquote_SINDy_model('NVDA',model='LorenzLogisticMap')
    stockquote_SINDy_model('TSLA',model='LorenzLogisticMap')
    plt.show()
    rftimeseries=read_rainfall_dataset("RainfallTimeseries_Sub_Division_IMD_2017.json",subdivision="Tamil Nadu")
    print("length of timeseries:",len(rftimeseries))
    precipitation_SINDy_model(rftimeseries)
    rftimeseries=read_rainfall_dataset("RainfallTimeseries_Sub_Division_IMD_2017.json",subdivision="Coastal Andhra Pradesh")
    print("length of timeseries:",len(rftimeseries))
    precipitation_SINDy_model(rftimeseries)

