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

class CompressedSensing(object):
	def sketch(self,image_matrix):
		number_of_rows=len(image_matrix)
		number_of_columns=len(image_matrix[0])
		random_matrix=numpy.random.rand(number_of_columns,1)
		print "=============================="
		print "Random Matrix A:"
		print "=============================="
		print random_matrix
		print "=============================="
		print "Image Matrix X:"
		print "=============================="
		print image_matrix
		sketch=numpy.matmul(image_matrix,random_matrix)
		print "=============================="
		print "Sketch B=AX:"
		print "=============================="
		pprint.pprint(sketch)
		

if __name__=="__main__":
	input_image8 = ImageToBitMatrix.image_to_bitmatrix("./testlogs/PictureOf8_1.jpg")
	csensing=CompressedSensing()
	csensing.sketch(input_image8)
