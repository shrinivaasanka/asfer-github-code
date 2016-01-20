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

#prints fundamental distance and median statistics for 2 datasets with R+rpy2 norm and median functions
#presently applied for Kullback-Leibler Divergence datasets
import rpy2.robjects as robj

class Norms_and_Basic_Statistics:
	def diff_elements(self,e):
		return abs(e[0]-e[1])

	def compute_norm_median_statistics(self):	
		f1=open("KLDivergence_Dataset2.txt")
		f2=open("KLDivergence_Dataset1.txt")
		dists0=map(float,f1.read().split())
		dists1=map(float,f2.read().split())
		plotfn = robj.r['plot']
		pdffn = robj.r['pdf']
	
		xydiff = map(self.diff_elements,zip(dists0,dists1))
		xydiffvec = robj.FloatVector(xydiff)
		xydiffmatrix = robj.r.matrix(xydiffvec,len(dists0))
		print xydiffmatrix
		rnorm = robj.r['norm']
		median = robj.r['median']
		sd = robj.r['sd']
		chisquared = robj.r['chisq.test']
		norm=rnorm(xydiffmatrix,"O")
		print "L1 norm"
		print norm
		norm=rnorm(xydiffmatrix,"I")
		print "Infinity norm"
		print norm
		norm=rnorm(xydiffmatrix,"F")
		print "Frobenius norm"
		print norm
		norm=rnorm(xydiffmatrix,"M")
		print "Maximum norm"
		print norm
		norm=rnorm(xydiffmatrix,"2")
		print "L2 norm"
		print norm
		print "Median of :",dists0
		medianx=median(robj.FloatVector(dists0))
		print medianx
		print "Median of :",dists1
		mediany=median(robj.FloatVector(dists1))
		print mediany
		print "Standard Deviation of :",dists0
		sdx=sd(robj.FloatVector(dists0))
		print sdx
		print "Standard Deviation of :",dists1
		sdy=sd(robj.FloatVector(dists1))
		print sdy
		chisq=chisquared(xydiffmatrix)
		print "Chi-Squared Test:"
		print chisq

if __name__=="__main__":
	nb=Norms_and_Basic_Statistics()
	nb.compute_norm_median_statistics()	
