#-------------------------------------------------------------------------------------------------------
#ASFER - Software for Mining Large Datasets
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
#---------------------------------------------------------------------------------------------------------


from PIL import Image
import numpy

def image_to_bitmatrix(image):
	bitmap=[]
	im = Image.open(image).convert("I")
	input_image_array=numpy.asarray(im).tolist()
	for r in input_image_array:
		rbit=list(map(tobit, r))
		bitmap.append(rbit)
	print "image_to_bitmatrix() for - ",image,":",bitmap
	return bitmap

def tobit(x):
	return x*0.001

if __name__=="__main__":
	bm=image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg")
	print "Bitmap:",bm

