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
# -------------------------------------------------------------------------------------------------------
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
# --------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import json
from FlightRadar24 import FlightRadar24API
from pyflightdata import FlightData
import pprint
import pandas as pd
from datetime import datetime
import time
import dynetx as dx
import networkx as nx
import operator
import dynetx.algorithms as al

def flightradar24_live_air_traffic(zones=None,max_no_of_flights=10):
    fr_api = FlightRadar24API()
    airtrafficdyngraph = dx.DynDiGraph(edge_remove=True)
    #if radius == -1:
    #    flights = fr_api.get_flights()
    #else:
    #    bounds = fr_api.get_bounds_by_point(longitude, latitude, radius)
    #    print("bounds:",bounds)
    #    flights = fr_api.get_flights(bounds = bounds)
    #print("flights:",flights)
    #if airport_code is not None:
    #    airport = fr_api.get_airport(airport_code) 
    #    print("airport:",airport)

    if zones == None:
        zones = list(fr_api.get_zones().keys())
    print("zones:",zones)
    for zoneid in zones:
                try:
                     bounds = fr_api.get_bounds(fr_api.get_zones()[zoneid])
                     flights = fr_api.get_flights(
                     bounds = bounds
                     )
                except:
                     print("FlightRadarAPI exception")
                cnt=1
                for flight in flights[:max_no_of_flights]:
                    if len(flight.origin_airport_iata) > 1 and len(flight.destination_airport_iata):
                        try:
                            print(str(cnt)+".live flight in zone ",zoneid,"from ",fr_api.get_airport(flight.origin_airport_iata)," to ",fr_api.get_airport(flight.destination_airport_iata)," on ",datetime.utcnow(),"  at altitude ",flight.get_altitude()," and longitude-latitude ",(flight.longitude,flight.latitude))
                            airtrafficdyngraph.add_interaction(u=fr_api.get_airport(flight.origin_airport_iata),v=fr_api.get_airport(flight.destination_airport_iata),t=time.time_ns())
                            cnt+=1
                        except:
                           print("FlightRadarAPI exception")
    #timerespectingpaths=al.all_time_respecting_paths(airtrafficdyngraph)
    #print("Time respecting paths in air traffic dynamic graph:",timerespectingpaths)
    temporal_betweenness_centrality=nx.betweenness_centrality(airtrafficdyngraph)
    sorted_tbc = sorted(list(temporal_betweenness_centrality.items()), key=operator.itemgetter(1), reverse=True)
    print("Temporal Betweenness Centrality of Air Traffic Dynamic Graph:",sorted_tbc)
    for e in airtrafficdyngraph.stream_interactions():
            print("air traffic dynamic graph edge:",e)

def pyflightdata_live_air_traffic(airport_code="MAA"):
    flightdata=FlightData()
    fr_api = FlightRadar24API()
    pd.set_option("display.max_rows",None)
    pd.set_option("display.max_columns",None)
    stats=flightdata.get_airport_stats(airport_code)
    print("====================================================")
    print("Data for ",fr_api.get_airport(airport_code))
    print("====================================================")
    print("------------------------------------")
    print("airport stats :")
    print("------------------------------------")
    #pprint.pprint(stats)
    pprint.pprint(pd.json_normalize(stats))
    onground=flightdata.get_airport_onground(airport_code)
    print("------------------------------------")
    print("airport onground:")
    print("------------------------------------")
    #pprint.pprint(onground)
    pprint.pprint(pd.json_normalize(onground))
    arrivals=flightdata.get_airport_arrivals(airport_code)
    print("------------------------------------")
    print("airport arrivals:")
    print("------------------------------------")
    #pprint.pprint(arrivals)
    pprint.pprint(pd.json_normalize(arrivals))
    departures=flightdata.get_airport_departures(airport_code)
    print("------------------------------------")
    print("airport departures:")
    print("------------------------------------")
    #pprint.pprint(departures)
    pprint.pprint(pd.json_normalize(departures))

def here_live_traffic(key,bearertoken,boundingbox=[12.439259,79.271851,13.568572,80.351257]):
    #page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id=NeuronRain_Live_Traffic&app_code=vS5i2op45RlaPW2GFKx8&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+','+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc')
    #request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey=dLxfz-ex3bXiDfypspYxJnlhVUIsKrve_TL-tRlk86c&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey='+key+' -H \'Authorization: Bearer '+bearertoken+'\'&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    #request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey='+key+'&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    print(request)
    page = requests.get(request)
    bs = BeautifulSoup(page.text,"lxml")
    print(bs)

def tomtom_live_traffic(key,boundingbox=None,longlat=None,apiversion=4):
    if boundingbox is not None:
        #https://api.tomtom.com/traffic/services/5/incidentDetails?key={Your_Api_Key}&bbox=4.8854592519716675,52.36934334773164,4.897883244144765,52.37496348620152&fields={incidents{type,geometry{type,coordinates},properties{iconCategory}}}&language=en-GB&t=1111&timeValidityFilter=present
        if apiversion == 4:
            incidentrequest_v4=f'https://api.tomtom.com/traffic/services/4/incidentDetails/s3/'+str(boundingbox[0])+'%2C'+str(boundingbox[1])+'%2C'+str(boundingbox[2])+'%2C'+str(boundingbox[3])+'/22/-1/json?key='+key+'&projection=EPSG4326&originalPosition=true'
            print("Traffic Incidents for bounding box-version 4:",incidentrequest_v4)
            page = requests.get(incidentrequest_v4)
            jsonret=json.dumps(page.json(),indent=4)
            print(jsonret)
            return jsonret
        else:
            #incidentrequest_v5=f'https://api.tomtom.com/traffic/services/5/incidentDetails?key='+key+'&bbox='+str(boundingbox[1])+','+str(boundingbox[0])+','+str(boundingbox[3])+','+str(boundingbox[2])+'&fields={incidents{type,geometry{type,coordinates},properties{iconCategory}}}&language=en-GB&t=1111&timeValidityFilter=present'
            incidentrequest_v5=f'https://api.tomtom.com/traffic/services/5/incidentDetails?key='+key+'&bbox='+str(boundingbox[1])+','+str(boundingbox[0])+','+str(boundingbox[3])+','+str(boundingbox[2])
            print("Traffic Incidents for bounding box-version 5:",incidentrequest_v5)
            page = requests.get(incidentrequest_v5)
            jsonret=json.dumps(page.json(),indent=4)
            print(jsonret)
            return jsonret
    if longlat is not None:
        flowrequest=f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key='+key+'&point='+str(longlat[0])+','+str(longlat[1])
        print("Traffic flow for longitude-latitude:",flowrequest)
        page = requests.get(flowrequest)
        jsonret=json.dumps(page.json(),indent=4)
        print(jsonret)
        return jsonret

if __name__=="__main__":
    #here_live_traffic()
    tomtomkey='00cKrkjfS62WPuchRmUc6Q5RAJw80hO2'
    #herekey='dLxfz-ex3bXiDfypspYxJnlhVUIsKrve_TL-tRlk86c'
    #herekey='d3KvxwZzD66NN9TmEfCPNSjeo3othXi4yy-SYqcytFk'
    herekey='OVA-84BS3bge_Nhem9h7Mw'
    #herebearertoken='eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJ2UzVpMm9wNDVSbGFQVzJHRkt4OCIsImlhdCI6MTcwNDg4MDYwNywiZXhwIjoxNzA0OTY3MDA3LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLnpmd1BIOUhsMldzRGRwWDZZSERFMWcuQVlSOElLNUVfMy02eGVXeVdCVENsamhzc3NBaGZ0Mk5ac2RJdjd6bUlqVmFDOGhCc2pNNUhRdlVZUGJmSXI0ZXczQmxObGNfaEtiN0dzMzAzNFR3YUVHNGhIalBhNXU0eUZQM0F1ODAxeGpMeURERXdsLXFPQ2FpX1NUODVoQ1NCMUJpRUhNc0Y0N192V3hzUTUtb2ZlaHJUcmZtTnlZM1lMR08wYTBMZkZQeVlfZ2pOd2tGSHBiNHR4Nl82LVNaRWh0ZEFDUmR3ZXY0NUROX3E1TzRLMUljcGVMNG9aOERqT2phMDcxT2g5US4wNm9EWmhBV0c3V1F4R09MdEU4cTZNRE8tRFlCRXU5QmdHbXpyRGRTT0Jr.pe0ReOI69iv5zGvCsvBpiIAKW1JhUh7KpH2qAbh2VfN6QW5x7vuEbY9v6R4v92I4w_h6aeTY0a46V9I2psvfwj1wo-dvKlP6TfOksoYKqcUUrtjpzQUIeR2-eOTblMyeGbNQx9lRTfAznDQOFHf1S2vRXUznKszTcGkYzmyrrX8cXoXYsZmQJcsUE9E4MZ8O76H0vm5W0wJHyJuRvgoWsQf2U8nL_xeI6tHv1eLRjtOBzDrX9LC8moauhV-7UWuv22nFU2PgjbP-AvmE66XFHbf2jThtbEBSXv7TvMhCCaJgt3knePTZ371S-rYzbPRS5AI5ijjbW-JRABvlj9i2Hg'
    herebearertoken='eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJ2UzVpMm9wNDVSbGFQVzJHRkt4OCIsImlhdCI6MTcwNDg4NTQ4NywiZXhwIjoxNzA0OTcxODg3LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLm9Jejg3WU1vRmNIQlh3UXBfa21GdUEudVZUcTRaLWxxVVdUOVQtdjVPYm9WZVRqYmxESHRjcUVpRFN3TzZIY29fakdFOHNmWDRncnlzdTZ4bUdIek9BS1hNWWhVZVg2UG5yTTV3UWFRaU5CTXBmWFFqdE9JOUdkNXFSd0llSFI5My1lZ1RCc3hrY3dkZjRzdkdXV05JSTM4R3JZMS1NN0N2U1NyTklVc2FPaEk3WTJIcHZfdW9naVhPekhFdTJiaWhYOVMwTzdiSXVLZkxFVmRzdVFEaTdhOXRMbFh6M3FsM1VXekI1UHowMERvUE1QYWRKTmdzekFzbncweUU0aG9pNC5qU19ETVZDdjBqV0pQdzdLeDQxTS01MFpvaHVKdkp1UW1ZOUhxaGUyb2ZF.W7WZa_xW2araKc1vP3UpPjyVTNao-BfzdeZPl7gkx3SKbrMi_AUR3KhzcxqdmJnmgY8rJnUPo0s6W_MO6GmETwNFjMl8zPYNX6ILTNk_ncx6LeZHyxW9I2PVlBvMVrP1BncdbPe7g0rX7-D1coqs5xx4yQx9wBeu0KYVEirPLDz-lyRT9h8ro-g-q5o25-XgsY2ZAJyzKWGtMMuUQgQibWMfh3CrEmCuoXyInYXOx2qlJSZCPB5RvcTNqs9xcctFgDKQIS6dmGCpEdTv0uKcRGRT-jdHaEfUXZFeXaCJ0UYI0_0ra1Gu5LZTiMe89uGkle5TEtcNhFhjEQXtrtsJ0w'
    here_live_traffic(key=herekey,bearertoken=herebearertoken,boundingbox=[12.439259,79.271851,13.568572,80.351257])
    tomtom_live_traffic(tomtomkey,boundingbox=[12.439259,79.271851,13.568572,80.351257])
    tomtom_live_traffic(tomtomkey,boundingbox=[10.948860,79.348497,10.991413,79.421453],apiversion=4)
    tomtom_live_traffic(tomtomkey,boundingbox=[10.948860,79.348497,10.991413,79.421453],apiversion=5)
    tomtom_live_traffic(tomtomkey,longlat=[12.439259,79.271851])
    flightradar24_live_air_traffic()
    pyflightdata_live_air_traffic(airport_code="MAA")
