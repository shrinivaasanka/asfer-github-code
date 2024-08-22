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

import yfinance as yf
import numpy as np
from MFDFA import MFDFA
import matplotlib.pyplot as plt
import librosa
from statsmodels.tsa.stattools import grangercausalitytests
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Source

def music_mfdfa_model(music,order=2,q=41,lagfrom=0.5,lagto=3,lagnum=100):
    print("--------------MFDFA model for Music ----------------------------")
    waveform, srate = librosa.load(music)
    timeseries = np.asarray(waveform)
    lag = np.unique(np.logspace(lagfrom,lagto,lagnum).astype(int))
    q_list = np.linspace(-10, 10, q)
    q_list = q_list[q_list != 0.0]
    lag, dfa = MFDFA(timeseries, lag=lag, q=q_list, order=order)
    print("mfdfa_model(): lag = ",lag)
    n = 0
    for curve in dfa:
        print("mfdfa_model(): curve ",n," = ",curve)
        plt.plot(dfa)
        n += 1
    toks=music.split("/")
    musicnametoks=toks[len(toks)-1].split(".")
    plt.savefig("testlogs/MultiFractals_Music_"+musicnametoks[0]+".jpg")

def precipitation_mfdfa_model(rainfallhistory,order=2):
    print("--------------MFDFA model for Precipitation ----------------------------")
    timeseries = np.asarray(rainfallhistory)
    lag = np.unique(np.logspace(0.5,3,100).astype(int))
    q_list = np.linspace(-10, 10, 41)
    q_list = q_list[q_list != 0.0]
    lag, dfa = MFDFA(timeseries, lag=lag, q=q_list, order=order)
    print("mfdfa_model(): lag = ",lag)
    n = 0
    for curve in dfa:
        print("mfdfa_model(): curve ",n," = ",curve)
        plt.plot(dfa)
        n += 1
    plt.savefig("testlogs/MultiFractals_Precipitation.jpg")

def stockquote_mfdfa_model(ticker,period='2y',interval='1wk',order=2,lagfrom=0.5,lagto=3,lagnum=100):
    print("--------------MFDFA model for ",ticker," ----------------------------")
    pricehistory = yf.Ticker(ticker).history(period=period,interval=interval,actions=False)
    timeseries = np.asarray(list(pricehistory["Open"]))
    lag = np.unique(np.logspace(lagfrom,lagto,lagnum).astype(int))
    q_list = np.linspace(-10, 10, 41)
    q_list = q_list[q_list != 0.0]
    lag, dfa = MFDFA(timeseries, lag=lag, q=q_list, order=order)
    print("mfdfa_model(): lag = ",lag)
    n = 0
    for curve in dfa:
        print("mfdfa_model(): curve ",n," = ",curve)
        plt.plot(dfa)
        n += 1
    plt.savefig("testlogs/MultiFractals_"+ticker+".jpg")

def granger_causality_GraphicalEventModel(dictoftimeseries,GEM_edge_probability_threshold=0.5,maxlag=3):
    print("granger_causality_GraphicalEventModel(): dictoftimeseries = ",dictoftimeseries)
    nxgem=nx.DiGraph()
    for t1k,t1v in dictoftimeseries.items():
        for t2k,t2v in dictoftimeseries.items():
            timeseries=[]
            if t1k != t2k:
                for t1,t2 in zip(t1v,t2v):
                     timeseries.append([t1,t2])
                print("granger_causality_GraphicalEventModel(): timeseries = ",timeseries)
                granger=grangercausalitytests(timeseries,maxlag)
                ssrftest=granger[1][0]["ssr_ftest"][1]
                ssr_chi2test=granger[1][0]["ssr_chi2test"][1]
                lrtest=granger[1][0]["lrtest"][1]
                paramsftest=granger[1][0]["params_ftest"][1]
                maxpvalue=max([ssrftest,ssr_chi2test,lrtest,paramsftest])
                print("granger_causality_GraphicalEventModel(): maxpvalue = ",maxpvalue)
                if maxpvalue > GEM_edge_probability_threshold:
                    nxgem.add_edge(t2k,t1k)
    print("granger_causality_GraphicalEventModel(): GEM nodes = ",nxgem.nodes())
    print("granger_causality_GraphicalEventModel(): GEM edges = ",nxgem.edges())
    write_dot(nxgem,"testlogs/GrangerCausality_EventTimeseriesGraphicalEventModel.dot")
    s=Source.from_file("testlogs/GrangerCausality_EventTimeseriesGraphicalEventModel.dot")
    s.render("testlogs/GrangerCausality_EventTimeseriesGraphicalEventModel.gv",format="jpg",view=True)

def stockquote_granger_causality(ticker1,ticker2,period='2y',interval='1wk',maxlag=3):
    print("===========================================================")
    print("Granger causality between ",ticker1," and ",ticker2)
    print("===========================================================")
    timeseries=[]
    pricehistory1 = yf.Ticker(ticker1).history(period=period,interval=interval,actions=False)
    timeseries1 = np.asarray(list(pricehistory1["Open"]))
    pricehistory2 = yf.Ticker(ticker2).history(period=period,interval=interval,actions=False)
    timeseries2 = np.asarray(list(pricehistory2["Open"]))
    for t1,t2 in zip(timeseries1,timeseries2):
        timeseries.append([t1,t2])
    granger=grangercausalitytests(timeseries,maxlag)
    print("Granger Causality of two timeseries: ",granger)
    return [(ticker1,timeseries1),(ticker2,timeseries2)]
