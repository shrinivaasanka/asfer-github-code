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

def here_live_traffic(key,bearertoken,boundingbox=[12.439259,79.271851,13.568572,80.351257]):
    #page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?app_id=NeuronRain_Live_Traffic&app_code=vS5i2op45RlaPW2GFKx8&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+','+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc')
    #request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey=dLxfz-ex3bXiDfypspYxJnlhVUIsKrve_TL-tRlk86c&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey='+key+' -H \'Authorization: Bearer '+bearertoken+'\'&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    #request='https://traffic.ls.hereapi.com/traffic/6.2/flow.xml?apiKey='+key+'&bbox='+str(boundingbox[0])+','+str(boundingbox[1])+';'+str(boundingbox[2])+','+str(boundingbox[3])+'&responseattributes=sh,fc'
    print(request)
    page = requests.get(request)
    bs = BeautifulSoup(page.text,"lxml")
    print(bs)

def tomtom_live_traffic(key,boundingbox=None,longlat=None):
    if boundingbox is not None:
        incidentrequest=f'https://api.tomtom.com/traffic/services/4/incidentDetails/s3/'+str(boundingbox[0])+'%2C'+str(boundingbox[1])+'%2C'+str(boundingbox[2])+'%2C'+str(boundingbox[3])+'/22/-1/json?key='+key+'&projection=EPSG4326&originalPosition=true'
        print("Traffic Incidents for bounding box:",incidentrequest)
        page = requests.get(incidentrequest)
        jsonret=json.dumps(page.json(),indent=4)
    if longlat is not None:
        flowrequest=f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key='+key+'&point='+str(longlat[0])+','+str(longlat[1])
        print("Traffic flow for longitude-latitude:",flowrequest)
        page = requests.get(flowrequest)
        jsonret=json.dumps(page.json(),indent=4)
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
    tomtom_live_traffic(tomtomkey,longlat=[12.439259,79.271851])
