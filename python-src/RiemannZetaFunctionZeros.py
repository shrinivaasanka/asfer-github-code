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

#Fit a curve to the parsed dataset using approx() and approxfun() R functions

import math
import cmath
import rpy2.robjects as robj

x_axs=[]
y_axs=[]
#Read input sequence (zeros of Riemann Zeta Function - first 100000) 
f=open("RZF_zeros_100000.txt")
f_str=f.read()
y_axs=f_str.split("\n")
print y_axs 

k=0.0
while True:
	x_axs.append(k)
	if k > 100000.0:
		break
	k=k+1.0

print len(x_axs)
print len(y_axs)

plotfn = robj.r['plot']
pdffn = robj.r['pdf']

y_axs = y_axs[0:100000]
x_axs = x_axs[0:100000]

x = robj.FloatVector(x_axs)
y = robj.FloatVector(y_axs)
dataframe = robj.DataFrame({"x":x,"y":y})

curvefn = robj.r['curve']


print "====================Approx====================="
approxfn = robj.r['approx']
approxfunfn = robj.r['approxfun']

approxdata = approxfn(dataframe)
approxfundata = approxfunfn(dataframe)

print approxdata
pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/python-src/RZF_approx_rplot.pdf")
plotfn(approxdata)

pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/python-src/RZF_approxfun_rplot.pdf")
plotfn(approxfundata, 0, 100000)
#curvefn(approxfundata)

print "=============Real part of RZF zeros===========================" 
#Compute k = ln[sec(l*ln(P(xi)))] / lnP(xi) where zero s=k+il for primes P(x1),P(x2),... (2,3,5,7,11,...)
primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
i=0
n=0
while True:
	if n==14:
		break
	while True:
		if i == 14:
			break
		rzfzero=complex(0.5,y[n])
		secfn=complex(1.0,0)/cmath.cos(complex(y[i],0)*complex(cmath.log(primes[i]),0))
		#print secfn
		k = cmath.log(complex(secfn,0)) / cmath.log(complex(primes[i],0))
		#print "prime = ",primes[i],"; k=",k
		pxi_power_s=cmath.exp(rzfzero*cmath.log(y[i]))
		#print "====================================="
		#print "[prime^s has to be 1 for some prime and zero s]"
		#print "prime = ",primes[i]
		#print "RZF zero s =", rzfzero
		#print "pxi_power_s=",pxi_power_s
		i=i+1
	n=n+1

print "==========P(xi)=e^(n*pi/l)============"
for i in y:
	pxi=math.exp(750*math.pi/i)
	print pxi
