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
#import cv2 
import numpy as np
from RecursiveGlossOverlap_Classifier import RecursiveGlossOverlapGraph

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

if __name__=="__main__":
	#imagenet_imagegraph("../testlogs/PictureOf8_1.jpg")
	#imagenet_imagegraph("../testlogs/Chennai_Mahabalipuram_DSC00388.jpg")
	imagenet_imagegraph("testlogs/WhiteTiger_1.jpg")
