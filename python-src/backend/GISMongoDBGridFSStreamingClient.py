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

import pymongo
import gridfs
from PIL import Image
import cv2
import numpy as np

class GISMongoDBGridFSStreamingClient(object):
    def __init__(self,host,port,database):
        self.mongodbclient = pymongo.MongoClient(host,port)
        self.mongodb = self.mongodbclient[database]
        self.mongofs = gridfs.GridFS(self.mongodb)
        print("MongoDB database:",self.mongodb.name)

    def streaming_download(self,imgname,imgid,shapeid):
        imgstr=self.mongofs.get(imgid)
        shapestr=self.mongofs.get(shapeid)
        img = np.frombuffer(imgstr.read(), dtype=np.uint8)
        img = np.reshape(img, eval(shapestr.read()))
        cv2.imwrite(imgname,img)
        cv2.waitKey()
        return img

    def streaming_upload(self,imgname):
        imgfile = cv2.imread(imgname)
        #imgfile = cv2.cvtColor(imgfile,cv2.COLOR_BGR2RGB)
        imageid = self.mongofs.put(imgfile.tostring())
        shapeid = self.mongofs.put(str(imgfile.shape),encoding='utf-8')
        return (imageid,shapeid,imgname)

if __name__=="__main__":
    mongodbclient=GISMongoDBGridFSStreamingClient("localhost",27017,"neuronraingis")
    img=mongodbclient.streaming_upload("../image_pattern_mining/ImageNet/testlogs/SEDAC_GPW4-11_PopulationEstimate2020_edited-contourlabelled.jpg")
    print("Uploaded image:",img)
    img=mongodbclient.streaming_download("./testlogs/GISMongoDBGridFSStreamingClient_ExampleImage.jpeg",img[0],img[1])
    print("Downloded image:",img)


