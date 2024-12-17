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
# K.Srinivasan
# NeuronRain Documentation and Licensing: http://neuronrain-documentation.readthedocs.io/en/latest/
# Personal website(research): https://acadpdrafts.readthedocs.io/en/latest/
#--------------------------------------------------------------------------------------------------------

from PIL import Image
import numpy
import cv2
import io
from cryptography.fernet import Fernet

def image_to_bitmatrix(image):
	bitmap=[]
	im = Image.open(image).convert("I")
	input_image_array=numpy.asarray(im).tolist()
	for r in input_image_array:
		rbit=list(map(tobit, r))
		bitmap.append(rbit)
	print("image_to_bitmatrix() for - ",image,":",bitmap)
	return bitmap

def image_to_bytes(image):
        im = Image.open(image)
        im_bytes = io.BytesIO()
        im.save(im_bytes,format=im.format)
        im_bytes=im_bytes.getvalue()
        print("image bytes:",im_bytes)
        return im_bytes

def fernet_encrypt_image(imagename,imagebytes):
        key = Fernet.generate_key()
        fer = Fernet(key)
        token = fer.encrypt(imagebytes)
        print("token:",token)
        encimage=open(imagename+"FernetEncryptedImage.fernet","w")
        encimage.write(str(token))
        return (fer,token)

def fernet_decrypt_image(imagename,fertoken):
        imagebytes=fertoken[0].decrypt(fertoken[1]) 
        image=Image.open(io.BytesIO(imagebytes))
        image.save(imagename+"FernetDecrypted."+image.format)
        print("image:",image)

def image3D_to_2D(image):
        img = cv2.imread(image)
        img2D = []
        (h,w) = img.shape[:2]
        for row in range(h):
            temp=[]
            for col in range(w):
                temp.append(sum(img[row,col].tolist()))
            img2D.append(temp)
        print("image3D_to_2D:",img2D)
        return img2D

def tobit(x):
	return x*0.001

if __name__=="__main__":
	#bm=image_to_bitmatrix("/home/shrinivaasanka/Krishna_iResearch_OpenSource/GitHub/asfer-github-code/python-src/testlogs/PictureOf1_1.jpg")
	#print("Bitmap:",bm)
        imagebytes1=image_to_bytes("/home/ksrinivasan/Krishna_iResearch_OpenSource_wc1/GitHub/asfer-github-code/python-src/image_pattern_mining/ImageNet/testlogs/CMIProfile_Screenshotfrom2013-04-08-190144.png")
        fertoken1=fernet_encrypt_image("CMIProfile_Screenshotfrom2013-04-08-190144.png",imagebytes1)
        fernet_decrypt_image("CMIProfile_Screenshotfrom2013-04-08-190144.png",fertoken1)
        imagebytes2=image_to_bytes("/home/ksrinivasan/Krishna_iResearch_OpenSource_wc1/GitHub/asfer-github-code/python-src/image_pattern_mining/ImageNet/testlogs/CMIProfile_Screenshotfrom2013-04-08-190231.png")
        fertoken2=fernet_encrypt_image("CMIProfile_Screenshotfrom2013-04-08-190231.png",imagebytes2)
        fernet_decrypt_image("CMIProfile_Screenshotfrom2013-04-08-190231.png",fertoken2)

