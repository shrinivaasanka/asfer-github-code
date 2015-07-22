#------------------------------------------------------------------------------------------------------------
#ASFER - a ruleminer which gets rules specific to a query and executes them (component of iCloud Platform)
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
#
#---------------------------------------------------------------------------------------------------------
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Independent Open Source Developer, Researcher and Consultant
#Ph: 9789346927, 9003082186, 9791165980
#Open Source Products Profile(Krishna iResearch):
#http://sourceforge.net/users/ka_shrinivaasan
#https://www.ohloh.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com, kashrinivaasan@live.com
#---------------------------------------------------------------------------------------------------------

import rpy2.robjects as robj
import binascii

#Computational Music - Read input multimedia data and compute Discrete Fourier Transform using R fft() function from rpy2 
#DFT for each frequency f(j) = sigma_k_0_n-1(x(k)*e^(-2*pi*i*j*k)/n) for inputs x0,x1,...,x(n-1)
#f=open("DFT_multimedia_av_20150209_202206.webm","rb")
f=open("DFT_multimedia_HilbertRadioAddress.mp3.mpga","rb")
input_seq=[]
pos=0
fstr=f.read()
#while pos < len(fstr):
while pos < 1000:
	f.seek(pos,0)
	f.tell()
	b=f.read(1)
	input_seq.append((int(binascii.hexlify(b),16)))
	pos=pos+1
	print (int(binascii.hexlify(b),16))

#print input_seq
fftfn = robj.r['fft']
print input_seq[0]
fftdata=fftfn(robj.IntVector(input_seq),False)
#prints the frequencies or periodicities in input sequence as complex numbers
print "#######################################"
print "Frequencies"
print "#######################################"
print fftdata 
