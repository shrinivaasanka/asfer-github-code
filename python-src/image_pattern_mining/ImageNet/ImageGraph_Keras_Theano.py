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
from empath import Empath
from collections import defaultdict
import operator

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
		cv2.imwrite(videofile+"Frame_%d.jpg"%cnt,frame)
		videograph.append(imagenet_imagegraph(videofile+"Frame_%d.jpg"%cnt))
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
		vg_en_tn_prdct_inverse_distance_image_row_weights=[]
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
			vg_en_tn_prdct_inverse_distance_image_row_weights.append(vg_en_tn_prdct_inverse_distance_image_weights)
		vg_en_tn_prdct_inverse_distance_video_weights.append(vg_en_tn_prdct_inverse_distance_image_row_weights)
	print "Inverse Distance Merit of the Video:", vg_en_tn_prdct_inverse_distance_video_weights
	return vg_en_tn_prdct_inverse_distance_video_weights

def large_scale_visual_sentiment(vg_en_tn_prdct):
	lexicon=Empath()
	vg_en_tn_prdct_sentiments=defaultdict(int)
	for row in vg_en_tn_prdct:
		for tensorproduct in row:
			tpedges=tensorproduct.edges()
			tpnodes=tensorproduct.nodes()
			print "Edges:",tpedges
			print "Nodes:",tpnodes
			for tpedge in tpedges:	
				sentiment00=lexicon.analyze((tpedge[0][0]).decode("utf-8"))
				for k,v in sentiment00.iteritems():
					vg_en_tn_prdct_sentiments[k] = vg_en_tn_prdct_sentiments[k] + v
				sentiment01=lexicon.analyze((tpedge[0][1]).decode("utf-8"))
				for k,v in sentiment01.iteritems():	
					vg_en_tn_prdct_sentiments[k] = vg_en_tn_prdct_sentiments[k] + v
				sentiment10=lexicon.analyze((tpedge[1][0]).decode("utf-8"))
				for k,v in sentiment10.iteritems():
					vg_en_tn_prdct_sentiments[k] = vg_en_tn_prdct_sentiments[k] + v
				sentiment11=lexicon.analyze((tpedge[1][1]).decode("utf-8"))
				for k,v in sentiment11.iteritems():
					vg_en_tn_prdct_sentiments[k] = vg_en_tn_prdct_sentiments[k] + v
	print "Sentiment Analysis of the Video:", sorted(vg_en_tn_prdct_sentiments.items(), key=operator.itemgetter(0), reverse=True)
	return vg_en_tn_prdct_sentiments

def core_topological_sort(vg_en_tn_prdct,threshold=1):
	invdistmerit=inverse_distance_intrinsic_merit(vg_en_tn_prdct)
	vg_en_tn_prdct_nxg=nx.DiGraph()
	rowframe=0
	columnframe=0
	for row in invdistmerit:
		for column in row:
			print "column:",column
			if max(column) > threshold: 
				vg_en_tn_prdct_nxg.add_edge(rowframe, columnframe)	
			columnframe = columnframe + 1
		rowframe = rowframe + 1
	vg_en_tn_prdct_nxg.remove_edges_from(nx.selfloop_edges(vg_en_tn_prdct_nxg))
	video_core=nx.k_core(vg_en_tn_prdct_nxg.to_undirected())
	topsorted_video_core=nx.topological_sort(video_core)	
	print "Topological Sorted Core Summary of the Video - Edges:",topsorted_video_core
	return topsorted_video_core

if __name__=="__main__":
	#imagenet_imagegraph("../testlogs/PictureOf8_1.jpg")
	#imagenet_imagegraph("../testlogs/Chennai_Mahabalipuram_DSC00388.jpg")
	#imagenet_imagegraph("testlogs/WhiteTiger_1.jpg")
	#imagenet_imagegraph("testlogs/ExampleImage_1.jpg")
	#imgnet_vg1=imagenet_videograph("testlogs/ExampleVideo_1.mp4",2)
	#imgnet_vg2=imagenet_videograph("testlogs/ExampleVideo_2.mp4",2)
	#vg_en_tn_prdct1=videograph_eventnet_tensor_product(imgnet_vg1)
	#video_merit=inverse_distance_intrinsic_merit(vg_en_tn_prdct1)
	#vg_en_tn_prdct2=videograph_eventnet_tensor_product(imgnet_vg2)
	#emotional_merit=large_scale_visual_sentiment(vg_en_tn_prdct2)
	#imgnet_vg3=imagenet_videograph("testlogs/ExampleVideo_3.mp4",2)
	#vg_en_tn_prdct3=videograph_eventnet_tensor_product(imgnet_vg3)
	#video_merit3=inverse_distance_intrinsic_merit(vg_en_tn_prdct3)
	#emotional_merit3=large_scale_visual_sentiment(vg_en_tn_prdct3)
	#topsortedcore=core_topological_sort(vg_en_tn_prdct3)
	imgnet_vg4=imagenet_videograph("testlogs/ExampleVideo_4.mp4",2)
	vg_en_tn_prdct4=videograph_eventnet_tensor_product(imgnet_vg4)
	topsortedcore=core_topological_sort(vg_en_tn_prdct4,1000)
