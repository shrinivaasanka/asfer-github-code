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
#Copyright (C):
#Srinivasan Kannan (alias) Ka.Shrinivaasan (alias) Shrinivas Kannan
#Ph: 9791499106, 9003082186
#Krishna iResearch Open Source Products Profiles:
#http://sourceforge.net/users/ka_shrinivaasan,
#https://github.com/shrinivaasanka,
#https://www.openhub.net/accounts/ka_shrinivaasan
#Personal website(research): https://sites.google.com/site/kuja27/
#emails: ka.shrinivaasan@gmail.com, shrinivas.kannan@gmail.com,
#kashrinivaasan@live.com
#--------------------------------------------------------------------------------------------------------

#Singular Value Decomposition and Principal Component Analysis of data:
#Principal Component Analysis of matrix X is mapping X to component matrix Y by weighting with W:
#	Y = XW where X is n*m, W is m*m and Y is n*m matrix
#Singular Value Decomposition is a special case of Principal Component Analysis that decomposes X into product of 3 matrices:
#	X = L*U*transpose(R) where L is n*n, U is n*m and R is m*m matrix

import rpy2.robjects as robj

y_axs=[]
#Read input sequence (at present DJIA dataset)
f=open("ChaosAttractorInputSequence_DJIA.txt")
f_str=f.read()
y_axs=f_str.split(",")
print y_axs 

print len(y_axs)

x_axs=[]
k=0.0
while True:
        x_axs.append(k)
        if k > 100000.0:
                break
        k=k+1.0


plotfn = robj.r['plot']
pdffn = robj.r['pdf']

#Singular Value Decomposition and Principal Component Analysis of 2*100 matrix 
x = robj.FloatVector(x_axs[:1000])
y = robj.FloatVector(y_axs[:1000])
dataframe = robj.DataFrame({"x":x,"y":y})

pca_function = robj.r['princomp']
svd_function = robj.r['svd']
pca=pca_function(dataframe,True,True)
svd=svd_function(dataframe)
print "================================"
print "PCA - Principal Component Analysis"
print "================================"
print pca 
print "PCA 0:"
print pca[0] 
print "PCA 1:"
print pca[1] 
print "================================"
print "SVD - Singular Value Decomposition"
print "================================"
print svd
print "SVD 0:"
print svd[0]
print "SVD 1:"
print svd[1]
print "SVD 2:"
print svd[2]

pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/python-src/PrincipalComponentAnalysis.pdf")
plotfn(pca,type="l")
pdffn("/media/shrinivaasanka/0fc4d8a2-1c74-42b8-8099-9ef78d8c8ea2/home/kashrinivaasan/KrishnaiResearch_OpenSource/GitHub/asfer-github-code/python-src/SingularValueDecomposition.pdf")
plotfn(svd[1],type="l")
