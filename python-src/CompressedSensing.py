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
#Copyleft (Copyright+):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#-----------------------------------------------------------------------------------------------------------------------------------


import math
from PIL import Image
import numpy
import pprint
import random
import ImageToBitMatrix
import json
from scipy.sparse.linalg import lsmr
from scipy.linalg import pinv
from hyphen import Hyphenator
from TextCompression import VowellessText

class CompressedSensing(object):
	def __init__(self):
		self.image_matrix=[]	
		self.random_matrix=[]
		self.sketch_ratio=50

	def sketch(self,image_matrix):
		#A = (number_of_rows/self.sketch_ratio,number_of_rows)
		#x = (number_of_rows,number_of_columns)
		#Ax = B(sketch) = (number_of_rows/self.sketch_ratio,number_of_columns)	
		number_of_rows=len(image_matrix)
		number_of_columns=len(image_matrix[0])
		self.image_matrix=image_matrix
		self.random_matrix=numpy.random.rand(number_of_rows/self.sketch_ratio,number_of_rows)
		print "=============================="
		print "Random Matrix A:"
		print "=============================="
		print self.random_matrix
		print "=============================="
		print "Image Matrix X:"
		print "=============================="
		print image_matrix
		sketch=numpy.matmul(self.random_matrix,image_matrix)
		sketchf=open("CompressedSensing.sketch","w")
		print "=============================="
		print "Sketch B=AX:"
		print "=============================="
		pprint.pprint(sketch.tolist())
		json.dump(sketch.tolist(),sketchf)

	def approximate_inverse_of_random_matrix(self):
		#Approximate because a non-square matrix is inverted
		#Aapproxinv = (number_of_rows,number_of_rows/self.sketch_ratio)
		#Invokes Moore-Penrose Pseudoinverse function in numpy
		inverse=pinv(self.random_matrix)	
		print "approximate_inverse_of_random_matrix():"
		print inverse
		return inverse

	def decompress(self):
		#Ax = B(sketch) = (number_of_rows/self.sketch_ratio,number_of_columns)	
		#x = Aapproxinv.Ax = recovered approximate image = (number_of_rows,number_of_rows/self.sketch_ratio).(number_of_rows/self.sketch_ratio,number_of_columns)
		print "=============================="
		print "Decompression:"
		print "=============================="
		sketch=[]
		sketchf=open("CompressedSensing.sketch","r")
		sketch=json.load(sketchf)

		approximate_inv_random_matrix=self.approximate_inverse_of_random_matrix()
		print "================================"
		print "approximately inverted random matrix:"
		print "================================"
		print approximate_inv_random_matrix
		recoveredimage=numpy.matmul(approximate_inv_random_matrix,sketch)
		print "================================"
		print "Recovered Image:"
		print "================================"
		print recoveredimage

		print "============================================================="
		print "Error in decompression: Original Image - Decompressed Image:"
		print "============================================================="
		diff=numpy.subtract(self.image_matrix,recoveredimage)
		error=0.0
		for r in diff:
			for c in r:
				error += c 
		print "Percentage Error in decompression:",error/[len(diff)*len(diff[0])]
		print "Size of sketch:(",len(sketch),"*",len(sketch[0]),")"
		print "Size of Original Image:(",len(self.image_matrix),"*",len(self.image_matrix[0]),")"

        def syllable_boundary_text_compression(self,text):
                hyph_en=Hyphenator("en_US")
                syllables=hyph_en.syllables(unicode(text))
                syll_comp_text=[]
                vtext=VowellessText()
                for s in syllables:
                    syll_comp_text.append(vtext.removevowels(s))
                print "Vowelless Syllable Vector Compression for text - ",text,":",(syllables,"-".join(syll_comp_text))
                return (syllables,"-".join(syll_comp_text))

if __name__=="__main__":
	#input_image8 = ImageToBitMatrix.image_to_bitmatrix("./testlogs/PictureOf8_1.jpg")
	csensing=CompressedSensing()
	#csensing.sketch(input_image8)
	#csensing.decompress()
        sylltxt=csensing.syllable_boundary_text_compression("Beautiful")
