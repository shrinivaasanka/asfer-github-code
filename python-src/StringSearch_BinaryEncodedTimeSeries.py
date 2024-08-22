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

# This parses a stream time series datasource (e.g stock quote ticker) and encodes the fluctuations as binary string of 0s and 1s

from pprint import pprint
import random
import rpy2.robjects as robj
import atexit
import yfinance as yf

cnt = 0


def binary_encoded_fluctuations(ticker, period='2y', interval='1wk'):
    cnt = 0
    prev = 0.0
    binaryfluctuations=""
    time_series_data = []
    timeseries_binary = open("StringSearch_Pattern.txt", "w")
    pricehistory = yf.Ticker(ticker).history(
        period=period, interval=interval, actions=False)
    for o in list(pricehistory["Open"]):
        if o > prev:
            timeseries_binary.write("1")
            binaryfluctuations+="1"
        else:
            timeseries_binary.write("0")
            binaryfluctuations+="0"
        prev = o
        cnt += 1
    print(("Binary fluctuations:", binaryfluctuations))
    return binaryfluctuations
