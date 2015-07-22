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

x_axs=[]
y_axs=[]
#Read input sequence (at present DJIA dataset)
#f=open("ChaosAttractorInputSequence.txt")
f=open("ChaosAttractorInputSequence_DJIA.txt")
f_str=f.read()
y_axs=f_str.split(",")
print y_axs 

k=0.0
while True:
	x_axs.append(k)
	if k > 19448.0:
		break
	k=k+1.0

print len(x_axs)
print len(y_axs)

#Local Polynomial Regression Fitting - LOESS - of above sequence using R loess() function in rpy2 and plot LOESS data to a PDF file
loessfn = robj.r['loess']
plotfn = robj.r['plot']

y_axs = y_axs[0:19448]
x_axs = x_axs[0:19448]

x = robj.FloatVector(x_axs)
y = robj.FloatVector(y_axs)
dataframe = robj.DataFrame({"x":x,"y":y})
loessdata = loessfn("y ~ x", data=dataframe)
print loessdata

pdffn = robj.r['pdf']
pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/asfer-code/python-src/DJIA_LOESS_rplot.pdf")
curvefn = robj.r['curve']

plotfn(loessdata)

