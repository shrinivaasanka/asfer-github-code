#-------------------------------------------------------------------------------------------------------
#NEURONRAIN ASFER - Software for Mining Large Datasets
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------------
#K.Srinivasan
#NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
#Personal website(research): https://sites.google.com/site/kuja27/
#--------------------------------------------------------------------------------------------------------

import os
os.environ['KERAS_BACKEND']='theano' 
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.imagenet_utils import preprocess_input
from keras.applications import ResNet50 
from keras import backend
import cv2 
import numpy as np
from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlapGraph
import networkx as nx
from WordNetPath import path_between

def imagenet_imagegraph(imagefile):
	im1=image.load_img(imagefile,target_size=(224,224))
	im1array=image.img_to_array(im1)
	im1array=np.expand_dims(im1array,axis=0)
	im1array=preprocess_input(im1array)
	model=ResNet50(weights="imagenet")
	preds=model.predict(im1array)
	decodepreds=decode_predictions(preds)
	print "Predictions:",decodepreds
	image_to_text=""
	for pred in decodepreds[0]:
		image_to_text += " "
		image_to_text += pred[1]
	imagegraph=RecursiveGlossOverlapGraph(image_to_text)
	print "ImageGraph:",imagegraph
	return imagegraph

def imagenet_videograph(videofile, maxframes):
	vid = cv2.VideoCapture(videofile)
	videograph=[]
	cnt=0
	while True and cnt < maxframes:
		ret, frame = vid.read()
		cv2.imwrite("Frame_%d.jpg"%cnt,frame)
		videograph.append(imagenet_imagegraph("Frame_%d.jpg"%cnt))
		cnt += 1
	print "VideoGraph:", videograph
	return videograph

def videograph_eventnet_tensor_product(videograph):
	vg_en_tn_prdct=[]
	for v1 in videograph:
		vg_en_tn_prdct_row=[]
		for v2 in videograph:
			vg_en_tn_prdct_row.append(nx.tensor_product(v1[0].to_undirected(),v2[0].to_undirected()))
		vg_en_tn_prdct.append(vg_en_tn_prdct_row)
	print "Videograph EventNet Tensor Product Matrix:",vg_en_tn_prdct
	return vg_en_tn_prdct

def inverse_distance_intrinsic_merit(vg_en_tn_prdct):
	vg_en_tn_prdct_inverse_distance_video_weights=[]
	for row in vg_en_tn_prdct:
		for tensorproduct in row:
			tpedges=tensorproduct.edges()
			tpnodes=tensorproduct.nodes()
			print "Edges:",tpedges
			print "Nodes:",tpnodes
			vg_en_tn_prdct_inverse_distance_image_weights=[]
			for tpedge in tpedges:	
				path1=path_between(tpedge[0][0],tpedge[0][1])
				path2=path_between(tpedge[1][0],tpedge[1][1])
				distance1=len(path1)
				distance2=len(path2)
				if distance1 == 0:
					distance1 = 0.00001
				if distance2 == 0:
					distance2 = 0.00001
				vg_en_tn_prdct_inverse_distance_image_weights.append((1/float(distance1)) * (1/float(distance2)))
			vg_en_tn_prdct_inverse_distance_video_weights.append(vg_en_tn_prdct_inverse_distance_image_weights)
	print "Inverse Distance Merit of the Video:", vg_en_tn_prdct_inverse_distance_video_weights
	return vg_en_tn_prdct_inverse_distance_video_weights

if __name__=="__main__":
	#imagenet_imagegraph("../testlogs/PictureOf8_1.jpg")
	#imagenet_imagegraph("../testlogs/Chennai_Mahabalipuram_DSC00388.jpg")
	#imagenet_imagegraph("testlogs/WhiteTiger_1.jpg")
	imgnet_vg=imagenet_videograph("testlogs/ExampleVideo_1.mp4",2)
	vg_en_tn_prdct=videograph_eventnet_tensor_product(imgnet_vg)
	video_merit=inverse_distance_intrinsic_merit(vg_en_tn_prdct)
