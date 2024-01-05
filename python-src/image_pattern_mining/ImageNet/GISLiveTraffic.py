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

import requests
from bs4 import BeautifulSoup

def here_live_traffic(boundingbox=[12.439259,79.271851,13.568572,80.351257]):
    #page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id=NeuronRain_Live_Traffic&app_code=vS5i2op45RlaPW2GFKx8&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+','+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc')
    request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey=dLxfz-ex3bXiDfypspYxJnlhVUIsKrve_TL-tRlk86c&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    print(request)
    page = requests.get(request)
    bs = BeautifulSoup(page.text,"lxml")
    print(bs)

def tomtom_live_traffic(key,boundingbox=None,longlat=None):
    if boundingbox is not None:
        incidentrequest=f'https://api.tomtom.com/traffic/services/4/incidentDetails/s3/'+str(boundingbox[0])+'%2C'+str(boundingbox[1])+'%2C'+str(boundingbox[2])+'%2C'+str(boundingbox[3])+'/22/-1/json?key='+key+'&projection=EPSG4326&originalPosition=true'
        print("Traffic Incidents for bounding box:",incidentrequest)
        page = requests.get(incidentrequest)
        print(page.json())
    if longlat is not None:
        flowrequest=f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key='+key+'&point='+str(longlat[0])+','+str(longlat[1])
        print("Traffic flow for longitude-latitude:",flowrequest)
        page = requests.get(flowrequest)
        print(page.text)


if __name__=="__main__":
    #here_live_traffic()
    key='00cKrkjfS62WPuchRmUc6Q5RAJw80hO2'
    tomtom_live_traffic(key,boundingbox=[12.439259,79.271851,13.568572,80.351257])
    tomtom_live_traffic(key,longlat=[12.439259,79.271851])
