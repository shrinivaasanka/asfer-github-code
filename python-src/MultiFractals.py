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

def stockquote_mfdfa_model(ticker,period='2y',interval='1wk',order=2):
    print("--------------MFDFA model for ",ticker," ----------------------------")
    pricehistory = yf.Ticker(ticker).history(period=period,interval=interval,actions=False)
    timeseries = np.asarray(list(pricehistory["Open"]))
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
    plt.savefig("testlogs/MultiFractals_"+ticker+".jpg")
