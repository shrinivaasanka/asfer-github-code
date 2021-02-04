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
# Copyleft (Copyright+):
# Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
# Ph: 9791499106, 9003082186
# Krishna iResearch Open Source Products Profiles:
# http://sourceforge.net/users/ka_shrinivaasan,
# https://github.com/shrinivaasanka,
# https://www.openhub.net/accounts/ka_shrinivaasan
# Personal website(research): https://sites.google.com/site/kuja27/
# emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
# kashrinivaasan@live.com
# -----------------------------------------------------------------------------------------------------------------------------------


import math
from PIL import Image
import numpy
import pprint
import random
import json
from scipy.sparse.linalg import lsmr
from scipy.linalg import pinv
from hyphen import Hyphenator
from TextCompression import VowellessText
from math import sqrt
from scipy.stats import wasserstein_distance
from scipy.spatial.distance import cdist
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics import adjusted_mutual_info_score
import numpy as np
from cv2 import *
import tensorflow as tf


class CompressedSensing(object):
    def __init__(self):
        self.image_matrix = []
        self.random_matrix = []
        self.sketch_ratio = 50

    def sketch(self, image_matrix):
        import ImageToBitMatrix
        #A = (number_of_rows/self.sketch_ratio,number_of_rows)
        #x = (number_of_rows,number_of_columns)
        # Ax = B(sketch) = (number_of_rows/self.sketch_ratio,number_of_columns)
        number_of_rows = len(image_matrix)
        number_of_columns = len(image_matrix[0])
        self.image_matrix = image_matrix
        self.random_matrix = numpy.random.rand(
            number_of_rows/self.sketch_ratio, number_of_rows)
        print("==============================")
        print("Random Matrix A:")
        print("==============================")
        print(self.random_matrix)
        print("==============================")
        print("Image Matrix X:")
        print("==============================")
        print(image_matrix)
        sketch = numpy.matmul(self.random_matrix, image_matrix)
        sketchf = open("CompressedSensing.sketch", "w")
        print("==============================")
        print("Sketch B=AX:")
        print("==============================")
        pprint.pprint(sketch.tolist())
        json.dump(sketch.tolist(), sketchf)

    def approximate_inverse_of_random_matrix(self):
        # Approximate because a non-square matrix is inverted
        #Aapproxinv = (number_of_rows,number_of_rows/self.sketch_ratio)
        # Invokes Moore-Penrose Pseudoinverse function in numpy
        inverse = pinv(self.random_matrix)
        print("approximate_inverse_of_random_matrix():")
        print(inverse)
        return inverse

    def decompress(self):
        # Ax = B(sketch) = (number_of_rows/self.sketch_ratio,number_of_columns)
        # x = Aapproxinv.Ax = recovered approximate image = (number_of_rows,number_of_rows/self.sketch_ratio).(number_of_rows/self.sketch_ratio,number_of_columns)
        print("==============================")
        print("Decompression:")
        print("==============================")
        sketch = []
        sketchf = open("CompressedSensing.sketch", "r")
        sketch = json.load(sketchf)

        approximate_inv_random_matrix = self.approximate_inverse_of_random_matrix()
        print("================================")
        print("approximately inverted random matrix:")
        print("================================")
        print(approximate_inv_random_matrix)
        recoveredimage = numpy.matmul(approximate_inv_random_matrix, sketch)
        print("================================")
        print("Recovered Image:")
        print("================================")
        print(recoveredimage)

        print("=============================================================")
        print("Error in decompression: Original Image - Decompressed Image:")
        print("=============================================================")
        diff = numpy.subtract(self.image_matrix, recoveredimage)
        error = 0.0
        for r in diff:
            for c in r:
                error += c
        print("Percentage Error in decompression:", error / \
            [len(diff)*len(diff[0])])
        print("Size of sketch:(", len(sketch), "*", len(sketch[0]), ")")
        print("Size of Original Image:(", len(
            self.image_matrix), "*", len(self.image_matrix[0]), ")")

    def syllable_boundary_text_compression(self, text, vectorspace_embedding=True):
        hyph_en = Hyphenator("en_US")
        texttoks = text.split(" ")
        syll_comp_text = []
        syllables = []
        alphabet_vectorspace_embedding = []
        for t in texttoks:
            syllables = syllables + hyph_en.syllables(str(t))
            alphabet_vectorspace_embedding.append(list(t))
        vtext = VowellessText()
        for s in syllables:
            syll_comp_text.append(vtext.removevowels(s))
        print("Vowelless Syllable Vector Compression for text - ", text, ":", (
            syllables, "-".join(syll_comp_text)))
        print("Alphabet vectorspace embedding of text:", alphabet_vectorspace_embedding)
        if vectorspace_embedding == True:
            return (syllables, alphabet_vectorspace_embedding,"-".join(syll_comp_text))
        else:
            return (syllables, "-".join(syll_comp_text))

    def tosig(self,array):
        lenarray=0
        for row in array:
            lenarray+=len(row)
        sig=np.empty((lenarray,3), dtype=np.float32)
        #print("sig:",sig)
        rowcnt=0
        colcnt=0
        cnt=0
        #print("array:",array)
        for a in array:
            #print("a:",a)
            for b in a:
                #print("b:",b)
                sig[cnt]=np.array([b,rowcnt,colcnt])
                colcnt+=1
                cnt+=1
            colcnt=0
            rowcnt+=1
        return sig

    def alphabet_vectorspace_embedding_distance(self, embedding1, embedding2, syllable_tensor_distance=False):
        if syllable_tensor_distance is True:
            distance=0
            ordembedding1=[]
            ordembedding2=[]
            for row in embedding1:
                ordrow=[]
                for col in row:
                    ordrow.append(ord(col))
                ordembedding1.append(ordrow)
            for row in embedding2:
                ordrow=[]
                for col in row:
                    ordrow.append(ord(col))
                ordembedding2.append(ordrow)
            print("embedding1:",embedding1)
            print("embedding2:",embedding2)
            print("ordembedding1:",ordembedding1)
            print("ordembedding2:",ordembedding2)
            ordembedding1sig=self.tosig(ordembedding1)
            ordembedding2sig=self.tosig(ordembedding2)
            distance_emd=cv2.EMD(ordembedding1sig,ordembedding2sig,cv2.DIST_L2)
            print("Earth Mover Distance between two String syllable tensors:",distance_emd)
            #print("Edit Distance between two Strings:",edit_distance("".join(embedding1),"".join(embedding2))
            #distance=cdist(ordembedding1np,ordembedding2np,'cityblock')
            #distance=wasserstein_distance(ordembedding1,ordembedding2)
            #distance_ami=adjusted_mutual_info_score(ordembedding1,ordembedding2)
            #distance_ari=adjusted_rand_score(ordembedding1np,ordembedding2np)
            #ordembedding1tf=tf.constant(ordembedding1)
            #ordembedding2tf=tf.constant(ordembedding2)
            #tensordistance=tf.norm(ordembedding1tf - ordembedding2tf)
            #print("String syllable tensor distance:",tensordistance)
            #ordembedding164=cv.fromarray(ordembedding1np)
            #ordembedding132=cv.CreateMat(ordembedding164.rows,ordembedding164.cols,cv.CV32_FC1)
            #cv.Convert(ordembedding164,ordembedding132)
            #ordembedding264=cv.fromarray(ordembedding2np)
            #ordembedding232=cv.CreateMat(ordembedding264.rows,ordembedding264.cols,cv.CV32_FC1)
            #cv.Convert(ordembedding264,ordembedding232)
            #distance_emd=cv.CalcEMD2(ordembedding132,ordembedding232,cv.CV_DIST_L2)
            return distance_emd
        else:
            len1=len(embedding1)
            len2=len(embedding2)
            leftjustified=embedding1
            if len1 > len2:
              leftjustified=embedding2
            else:
              leftjustified=embedding1
            for n in range(abs(len1-len2)):
              leftjustified.append('#')
            if len1 > len2:
              embedding2=leftjustified
            else:
              embedding1=leftjustified
            print("leftjustified:",leftjustified)
            print("embedding1:",embedding1)
            print("embedding2:",embedding2)
            distance=0
            for ordpair in zip(embedding1,embedding2):
              diff = abs(ord(ordpair[0]) - ord(ordpair[1]))
              distance += diff * diff
              distance = sqrt(distance)
              print("Alphabet Vectorspace Embedding Distance between ",embedding1," and ",embedding2,":",distance)
              print("Normalized Alphabet Vectorspace Embedding Distance between ",embedding1," and ",embedding2,":",distance/len(embedding1))
              return distance

if __name__ == "__main__":
    #input_image8 = ImageToBitMatrix.image_to_bitmatrix("./testlogs/PictureOf8_1.jpg")
    csensing = CompressedSensing()
    # csensing.sketch(input_image8)
    # csensing.decompress()
    sylltxt = csensing.syllable_boundary_text_compression(
        "This sentence is alphabet-syllable vector space embedded ")
